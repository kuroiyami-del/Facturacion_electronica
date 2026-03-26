"""
factories/factura_factory.py - Patrón Factory para creación de facturas.

Patrón de Diseño: Factory Method
  - Encapsula la lógica de construcción de distintos tipos de facturas.
  - El cliente (FacturaService) no necesita saber cómo se construye cada tipo.

Tipos soportados:
  - FacturaEstandar: IVA 19%, sin descuentos ni retenciones.
  - FacturaConDescuento: Aplica descuento comercial antes de calcular IVA.
  - FacturaConRetencion: Descuenta retención en la fuente del total a pagar.
  - FacturaExportacion: Sin IVA (tarifa 0%) para exportaciones.
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import date

from app.models.factura import Factura, DetalleFactura, TipoFactura, EstadoFactura
from app.strategies.impuesto_strategy import (
    CalculadoraImpuestos,
    EstrategiaIVA19,
    EstrategiaIVA0,
    EstrategiaRetencionFuente,
    EstrategiaDescuentoComercial,
    obtener_estrategia_iva,
)


# ── Interfaz del Factory ──────────────────────────────────────────────────────

class FacturaCreator(ABC):
    """Clase base abstracta para todos los creadores de facturas."""

    @abstractmethod
    def crear_factura(
        self,
        empresa_id: int,
        cliente_id: int,
        usuario_id: int,
        numero_factura: str,
        detalles_data: list[dict],
        notas: str | None = None,
    ) -> Factura:
        """Crea y retorna una instancia de Factura configurada según el tipo."""
        ...

    def _construir_detalles(
        self, factura: Factura, detalles_data: list[dict]
    ) -> list[DetalleFactura]:
        """
        Genera las líneas de detalle y calcula los valores de cada una.
        Retorna los objetos DetalleFactura sin persistirlos aún.
        """
        detalles: list[DetalleFactura] = []
        for item in detalles_data:
            cantidad = Decimal(str(item["cantidad"]))
            precio_unitario = Decimal(str(item["precio_unitario"]))
            porcentaje_descuento = Decimal(str(item.get("porcentaje_descuento", "0")))
            porcentaje_iva = Decimal(str(item.get("porcentaje_iva", "19")))

            subtotal_bruto = (cantidad * precio_unitario).quantize(Decimal("0.01"))
            valor_descuento = (subtotal_bruto * porcentaje_descuento / 100).quantize(Decimal("0.01"))
            subtotal_neto = subtotal_bruto - valor_descuento
            valor_iva = (subtotal_neto * porcentaje_iva / 100).quantize(Decimal("0.01"))
            total_linea = subtotal_neto + valor_iva

            detalle = DetalleFactura(
                factura_id=factura.id,
                producto_id=item["producto_id"],
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                porcentaje_descuento=porcentaje_descuento,
                valor_descuento=valor_descuento,
                subtotal=subtotal_neto,
                porcentaje_iva=porcentaje_iva,
                valor_iva=valor_iva,
                total_linea=total_linea,
            )
            detalles.append(detalle)
        return detalles

    def _calcular_totales_factura(self, detalles: list[DetalleFactura]) -> dict[str, Decimal]:
        """Consolida los totales de todas las líneas de detalle."""
        subtotal = sum((d.subtotal for d in detalles), Decimal("0.00"))
        descuento_total = sum((d.valor_descuento for d in detalles), Decimal("0.00"))
        iva_total = sum((d.valor_iva for d in detalles), Decimal("0.00"))
        base_gravable = subtotal
        return {
            "subtotal": subtotal,
            "descuento_total": descuento_total,
            "base_gravable": base_gravable,
            "iva_total": iva_total,
        }


# ── Implementaciones concretas ────────────────────────────────────────────────

class FacturaEstandarCreator(FacturaCreator):
    """Crea una factura estándar con IVA 19% y sin retenciones ni descuentos globales."""

    def crear_factura(self, empresa_id, cliente_id, usuario_id,
                      numero_factura, detalles_data, notas=None) -> Factura:
        factura = Factura(
            empresa_id=empresa_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            numero_factura=numero_factura,
            tipo_factura=TipoFactura.ESTANDAR,
            estado=EstadoFactura.BORRADOR,
            fecha_emision=date.today(),
            notas=notas,
        )
        detalles = self._construir_detalles(factura, detalles_data)
        totales = self._calcular_totales_factura(detalles)

        factura.subtotal = totales["subtotal"]
        factura.descuento_total = totales["descuento_total"]
        factura.base_gravable = totales["base_gravable"]
        factura.iva_total = totales["iva_total"]
        factura.retencion_total = Decimal("0.00")
        factura.total = factura.base_gravable + factura.iva_total
        factura.detalles = detalles
        return factura


class FacturaConDescuentoCreator(FacturaCreator):
    """Crea una factura con descuento global sobre el subtotal total."""

    def __init__(self, porcentaje_descuento_global: Decimal) -> None:
        self._descuento = porcentaje_descuento_global

    def crear_factura(self, empresa_id, cliente_id, usuario_id,
                      numero_factura, detalles_data, notas=None) -> Factura:
        factura = Factura(
            empresa_id=empresa_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            numero_factura=numero_factura,
            tipo_factura=TipoFactura.CON_DESCUENTO,
            estado=EstadoFactura.BORRADOR,
            fecha_emision=date.today(),
            notas=notas,
        )
        detalles = self._construir_detalles(factura, detalles_data)
        totales = self._calcular_totales_factura(detalles)

        estrategia_descuento = EstrategiaDescuentoComercial(self._descuento)
        descuento_global = estrategia_descuento.calcular(totales["subtotal"])
        base_gravable = totales["subtotal"] - descuento_global
        iva_total = (base_gravable * Decimal("0.19")).quantize(Decimal("0.01"))

        factura.subtotal = totales["subtotal"]
        factura.descuento_total = totales["descuento_total"] + descuento_global
        factura.base_gravable = base_gravable
        factura.iva_total = iva_total
        factura.retencion_total = Decimal("0.00")
        factura.total = base_gravable + iva_total
        factura.detalles = detalles
        return factura


class FacturaConRetencionCreator(FacturaCreator):
    """Crea una factura con retención en la fuente (3.5%) descontada del total."""

    def crear_factura(self, empresa_id, cliente_id, usuario_id,
                      numero_factura, detalles_data, notas=None) -> Factura:
        factura = Factura(
            empresa_id=empresa_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            numero_factura=numero_factura,
            tipo_factura=TipoFactura.CON_RETENCION,
            estado=EstadoFactura.BORRADOR,
            fecha_emision=date.today(),
            notas=notas,
        )
        detalles = self._construir_detalles(factura, detalles_data)
        totales = self._calcular_totales_factura(detalles)

        calculadora = CalculadoraImpuestos()
        calculadora.agregar_estrategia(EstrategiaIVA19())
        calculadora.agregar_estrategia(EstrategiaRetencionFuente())
        resultado = calculadora.calcular_total_impuestos(totales["base_gravable"])

        factura.subtotal = totales["subtotal"]
        factura.descuento_total = totales["descuento_total"]
        factura.base_gravable = totales["base_gravable"]
        factura.iva_total = resultado.get("IVA 19%", Decimal("0.00"))
        factura.retencion_total = resultado.get("Retención en la Fuente 3.5%", Decimal("0.00"))
        factura.total = factura.base_gravable + factura.iva_total - factura.retencion_total
        factura.detalles = detalles
        return factura


class FacturaExportacionCreator(FacturaCreator):
    """Crea una factura de exportación: IVA 0% según normativa DIAN."""

    def crear_factura(self, empresa_id, cliente_id, usuario_id,
                      numero_factura, detalles_data, notas=None) -> Factura:
        # Forzar IVA 0 en todos los ítems
        for item in detalles_data:
            item["porcentaje_iva"] = "0"

        factura = Factura(
            empresa_id=empresa_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            numero_factura=numero_factura,
            tipo_factura=TipoFactura.EXPORTACION,
            estado=EstadoFactura.BORRADOR,
            fecha_emision=date.today(),
            notas=notas,
        )
        detalles = self._construir_detalles(factura, detalles_data)
        totales = self._calcular_totales_factura(detalles)

        factura.subtotal = totales["subtotal"]
        factura.descuento_total = totales["descuento_total"]
        factura.base_gravable = totales["base_gravable"]
        factura.iva_total = Decimal("0.00")
        factura.retencion_total = Decimal("0.00")
        factura.total = factura.base_gravable
        factura.detalles = detalles
        return factura


# ── Registro y selector de factories ─────────────────────────────────────────

FACTORIES: dict[str, type[FacturaCreator]] = {
    TipoFactura.ESTANDAR: FacturaEstandarCreator,
    TipoFactura.CON_DESCUENTO: FacturaConDescuentoCreator,
    TipoFactura.CON_RETENCION: FacturaConRetencionCreator,
    TipoFactura.EXPORTACION: FacturaExportacionCreator,
}


def obtener_factory(
    tipo_factura: str,
    porcentaje_descuento: Decimal | None = None,
) -> FacturaCreator:
    """
    Retorna la instancia del factory correspondiente al tipo de factura.
    Principio OCP: agregar nuevos tipos solo requiere registrar en FACTORIES.
    """
    if tipo_factura not in FACTORIES:
        raise ValueError(f"Tipo de factura no soportado: {tipo_factura}")

    if tipo_factura == TipoFactura.CON_DESCUENTO:
        descuento = porcentaje_descuento or Decimal("0")
        return FacturaConDescuentoCreator(descuento)

    return FACTORIES[tipo_factura]()