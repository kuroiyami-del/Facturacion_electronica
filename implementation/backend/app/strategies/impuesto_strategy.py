"""
strategies/impuesto_strategy.py - Patrón Strategy para cálculo de impuestos.

Patrón de Diseño: Strategy
  - Define una familia de algoritmos de cálculo (IVA, Retención, Descuento).
  - Permite intercambiar el algoritmo en tiempo de ejecución sin modificar el cliente.

Principio SOLID:
  - OCP: Se pueden agregar nuevas estrategias sin modificar el código existente.
  - SRP: Cada estrategia tiene una única responsabilidad de cálculo.
"""
from abc import ABC, abstractmethod
from decimal import Decimal


class ImpuestoStrategy(ABC):
    """Interfaz base para todas las estrategias de cálculo de impuestos."""

    @abstractmethod
    def calcular(self, subtotal: Decimal) -> Decimal:
        """Calcula y retorna el valor del impuesto o descuento aplicado."""
        ...

    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre descriptivo de la estrategia."""
        ...


class EstrategiaIVA0(ImpuestoStrategy):
    """IVA al 0% — Bienes y servicios exentos con tarifa cero."""

    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")

    def nombre(self) -> str:
        return "IVA 0%"


class EstrategiaIVA5(ImpuestoStrategy):
    """IVA al 5% — Aplica a ciertos bienes como vivienda y medicina prepagada."""

    TASA = Decimal("0.05")

    def calcular(self, subtotal: Decimal) -> Decimal:
        return (subtotal * self.TASA).quantize(Decimal("0.01"))

    def nombre(self) -> str:
        return "IVA 5%"


class EstrategiaIVA19(ImpuestoStrategy):
    """IVA al 19% — Tarifa general en Colombia."""

    TASA = Decimal("0.19")

    def calcular(self, subtotal: Decimal) -> Decimal:
        return (subtotal * self.TASA).quantize(Decimal("0.01"))

    def nombre(self) -> str:
        return "IVA 19%"


class EstrategiaRetencionFuente(ImpuestoStrategy):
    """
    Retención en la fuente al 3.5% (tarifa base para servicios en Colombia).
    Se resta del total a pagar.
    """

    TASA = Decimal("0.035")

    def calcular(self, subtotal: Decimal) -> Decimal:
        return (subtotal * self.TASA).quantize(Decimal("0.01"))

    def nombre(self) -> str:
        return "Retención en la Fuente 3.5%"


class EstrategiaDescuentoComercial(ImpuestoStrategy):
    """
    Descuento comercial configurable (expresado en porcentaje 0–100).
    Reduce la base gravable antes de calcular el IVA.
    """

    def __init__(self, porcentaje_descuento: Decimal) -> None:
        if not (Decimal("0") <= porcentaje_descuento <= Decimal("100")):
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        self._porcentaje = porcentaje_descuento / Decimal("100")

    def calcular(self, subtotal: Decimal) -> Decimal:
        return (subtotal * self._porcentaje).quantize(Decimal("0.01"))

    def nombre(self) -> str:
        return f"Descuento {self._porcentaje * 100:.1f}%"


class EstrategiaExento(ImpuestoStrategy):
    """Productos/servicios excluidos del IVA — No aplica ningún impuesto."""

    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")

    def nombre(self) -> str:
        return "Exento de IVA"


class CalculadoraImpuestos:
    """
    Contexto del patrón Strategy.
    Orquesta múltiples estrategias para calcular el total de impuestos de una línea.
    """

    def __init__(self) -> None:
        self._estrategias: list[ImpuestoStrategy] = []

    def agregar_estrategia(self, estrategia: ImpuestoStrategy) -> "CalculadoraImpuestos":
        """Agrega una estrategia de cálculo. Retorna self para encadenamiento fluido."""
        self._estrategias.append(estrategia)
        return self

    def calcular_total_impuestos(self, subtotal: Decimal) -> dict[str, Decimal]:
        """
        Aplica todas las estrategias y retorna un diccionario con el detalle
        y el total consolidado de impuestos.
        """
        resultados: dict[str, Decimal] = {}
        for estrategia in self._estrategias:
            resultados[estrategia.nombre()] = estrategia.calcular(subtotal)
        resultados["total_impuestos"] = sum(resultados.values(), Decimal("0.00"))
        return resultados


# ── Fábrica de estrategias (mapeo desde tipo de impuesto del modelo) ──────────

MAPA_ESTRATEGIAS: dict[str, type[ImpuestoStrategy]] = {
    "IVA_0": EstrategiaIVA0,
    "IVA_5": EstrategiaIVA5,
    "IVA_19": EstrategiaIVA19,
    "EXENTO": EstrategiaExento,
    "EXCLUIDO": EstrategiaExento,
}


def obtener_estrategia_iva(tipo_impuesto: str) -> ImpuestoStrategy:
    """Retorna la estrategia de IVA correspondiente al tipo del producto."""
    clase = MAPA_ESTRATEGIAS.get(tipo_impuesto, EstrategiaIVA19)
    return clase()