"""
services/factura_service.py - Orquestador principal del módulo de facturación.

Este servicio conecta Factory, Strategy, Observer y Repository en un único flujo
de negocio: crear → calcular → persistir → notificar → validar DIAN.
"""
from decimal import Decimal
from datetime import date
import logging

from sqlalchemy.orm import Session

from app.models.factura import Factura, EstadoFactura, TipoFactura
from app.models.empresa import Empresa
from app.repositories.factura_repository import FacturaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.factories.factura_factory import obtener_factory
from app.services.dian_service import DianService
from app.services.observers.factura_observer import (
    FacturaEventBus,
    DatosEventoFactura,
    EventoFactura,
    crear_event_bus_por_defecto,
)

logger = logging.getLogger(__name__)

# EventBus global de la aplicación (instancia única)
_event_bus: FacturaEventBus | None = None


def obtener_event_bus() -> FacturaEventBus:
    """Retorna el EventBus global, creándolo si aún no existe."""
    global _event_bus
    if _event_bus is None:
        _event_bus = crear_event_bus_por_defecto()
    return _event_bus


class FacturaService:
    """
    Servicio de dominio para la gestión completa del ciclo de vida de facturas.
    
    Orquesta:
      - Factory   → construcción del objeto Factura según su tipo.
      - Repository → persistencia en la base de datos.
      - Strategy  → cálculo de impuestos (delegado al Factory).
      - Observer  → notificaciones a otros módulos tras emitir/anular.
      - DianService → validación electrónica.
    """

    def __init__(self, db: Session) -> None:
        self._db = db
        self._factura_repo = FacturaRepository(db)
        self._cliente_repo = ClienteRepository(db)
        self._dian_service = DianService()
        self._event_bus = obtener_event_bus()

    # ── Creación ──────────────────────────────────────────────────────────────

    def crear_factura(
        self,
        empresa: Empresa,
        cliente_id: int,
        usuario_id: int,
        detalles_data: list[dict],
        tipo_factura: str = TipoFactura.ESTANDAR,
        porcentaje_descuento: Decimal | None = None,
        notas: str | None = None,
    ) -> Factura:
        """
        Crea una nueva factura en estado BORRADOR.
        
        Flujo:
          1. Genera el número de consecutivo.
          2. Selecciona el factory según el tipo.
          3. Construye el objeto con detalles y totales calculados.
          4. Persiste en la base de datos.
        """
        numero_factura = self._generar_numero_factura(empresa)
        factory = obtener_factory(tipo_factura, porcentaje_descuento)
        factura = factory.crear_factura(
            empresa_id=empresa.id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            numero_factura=numero_factura,
            detalles_data=detalles_data,
            notas=notas,
        )

        # Persistir factura y sus detalles
        self._db.add(factura)
        self._db.commit()
        self._db.refresh(factura)
        logger.info("[FacturaService] Factura %s creada en borrador.", factura.numero_factura)
        return factura

    # ── Emisión ───────────────────────────────────────────────────────────────

    def emitir_factura(self, factura_id: int) -> Factura:
        """
        Cambia el estado de BORRADOR a EMITIDA y notifica a los observadores.
        La notificación dispara: email, inventario, auditoría y envío a DIAN.
        """
        factura = self._factura_repo.get_con_detalles(factura_id)
        if factura is None:
            raise ValueError(f"Factura con id={factura_id} no encontrada.")
        if factura.estado != EstadoFactura.BORRADOR:
            raise ValueError(
                f"Solo se pueden emitir facturas en BORRADOR. Estado actual: {factura.estado}"
            )

        factura.estado = EstadoFactura.EMITIDA
        self._db.commit()
        self._db.refresh(factura)

        # Notificar a todos los observadores
        self._publicar_evento(EventoFactura.EMITIDA, factura)

        # Iniciar validación DIAN automáticamente
        return self.validar_con_dian(factura.id)

    # ── Validación DIAN ───────────────────────────────────────────────────────

    def validar_con_dian(self, factura_id: int) -> Factura:
        """
        Genera el CUFE y envía la factura al simulacro DIAN para validación.
        Actualiza el estado a VALIDADA_DIAN o RECHAZADA según la respuesta.
        """
        factura = self._factura_repo.get_con_detalles(factura_id)
        if factura is None:
            raise ValueError(f"Factura {factura_id} no encontrada.")

        nit_receptor = factura.cliente.numero_documento if factura.cliente else "000000000"
        cufe = self._dian_service.generar_cufe(
            numero_factura=factura.numero_factura,
            fecha_factura=factura.fecha_emision.isoformat(),
            total=factura.total,
            nit_emisor=factura.empresa.nit,
            nit_receptor=nit_receptor,
        )

        respuesta = self._dian_service.validar_factura(cufe, factura.numero_factura)
        factura.cufe = cufe
        factura.qr_code = self._dian_service.generar_qr_data(cufe, factura.numero_factura, factura.total)
        factura.validada_dian = respuesta["aprobada"]
        factura.respuesta_dian = respuesta["mensaje"]
        factura.estado = (
            EstadoFactura.VALIDADA_DIAN if respuesta["aprobada"] else EstadoFactura.RECHAZADA
        )

        self._db.commit()
        self._db.refresh(factura)

        evento = EventoFactura.VALIDADA_DIAN if respuesta["aprobada"] else EventoFactura.RECHAZADA_DIAN
        self._publicar_evento(evento, factura)
        return factura

    # ── Anulación ─────────────────────────────────────────────────────────────

    def anular_factura(self, factura_id: int, motivo: str) -> Factura:
        """Anula una factura y notifica a los observadores."""
        factura = self._factura_repo.get_by_id(factura_id)
        if factura is None:
            raise ValueError(f"Factura {factura_id} no encontrada.")
        if factura.estado == EstadoFactura.ANULADA:
            raise ValueError("La factura ya se encuentra anulada.")

        factura.estado = EstadoFactura.ANULADA
        factura.notas = f"{factura.notas or ''} | ANULADA: {motivo}"
        self._db.commit()
        self._db.refresh(factura)

        self._publicar_evento(EventoFactura.ANULADA, factura)
        return factura

    # ── Consultas ─────────────────────────────────────────────────────────────

    def obtener_historial(
        self, fecha_inicio: date | None = None, fecha_fin: date | None = None
    ) -> list[Factura]:
        """Retorna el historial de facturas, opcionalmente filtrado por rango de fechas."""
        if fecha_inicio and fecha_fin:
            return self._factura_repo.get_por_rango_fechas(fecha_inicio, fecha_fin)
        return self._factura_repo.get_all(limit=500)

    def resumen_ventas(self, fecha_inicio: date, fecha_fin: date) -> dict:
        """Genera un resumen de ventas para el período indicado."""
        facturas = self._factura_repo.get_por_rango_fechas(fecha_inicio, fecha_fin)
        total = self._factura_repo.total_ventas_periodo(fecha_inicio, fecha_fin)
        return {
            "total_facturas": len(facturas),
            "total_ventas": total,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
        }

    # ── Privados ──────────────────────────────────────────────────────────────

    def _generar_numero_factura(self, empresa: Empresa) -> str:
        """Genera el número de factura con prefijo y consecutivo automático."""
        ultimo = self._factura_repo.get_ultimo_consecutivo(empresa.id, empresa.prefijo_factura)
        siguiente = ultimo + 1
        return f"{empresa.prefijo_factura}{siguiente:08d}"

    def _publicar_evento(self, evento: EventoFactura, factura: Factura) -> None:
        """Construye el payload del evento y lo publica en el EventBus."""
        cliente = factura.cliente
        datos = DatosEventoFactura(
            evento=evento,
            factura_id=factura.id,
            numero_factura=factura.numero_factura,
            cliente_id=factura.cliente_id,
            cliente_nombre=cliente.nombre if cliente else "Desconocido",
            cliente_email=cliente.email if cliente else None,
            total=factura.total,
        )
        self._event_bus.publicar(datos)