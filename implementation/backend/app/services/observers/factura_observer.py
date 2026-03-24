"""
services/observers/factura_observer.py - Patrón Observer para eventos de factura.

Patrón de Diseño: Observer
  - El sujeto (FacturaEventBus) notifica a todos los observadores registrados
    cuando se produce un evento (ej. factura emitida, validada, anulada).
  - Los observadores reaccionan de forma desacoplada: email, inventario, auditoría.

Principio SOLID:
  - OCP: Se agregan nuevos observadores sin modificar el EventBus.
  - DIP: El EventBus depende de la abstracción FacturaObserver, no de implementaciones.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ── Tipos de eventos ──────────────────────────────────────────────────────────

class EventoFactura(str, Enum):
    EMITIDA = "EMITIDA"
    VALIDADA_DIAN = "VALIDADA_DIAN"
    RECHAZADA_DIAN = "RECHAZADA_DIAN"
    ANULADA = "ANULADA"
    PAGADA = "PAGADA"


@dataclass
class DatosEventoFactura:
    """Payload inmutable que acompaña a cada evento de factura."""
    evento: EventoFactura
    factura_id: int
    numero_factura: str
    cliente_id: int
    cliente_nombre: str
    cliente_email: str | None
    total: Decimal
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


# ── Interfaz del observador ───────────────────────────────────────────────────

class FacturaObserver(ABC):
    """Interfaz base que deben implementar todos los observadores de facturas."""

    @abstractmethod
    def actualizar(self, datos: DatosEventoFactura) -> None:
        """Recibe y procesa un evento de factura."""
        ...


# ── Implementaciones de observadores ─────────────────────────────────────────

class ObservadorNotificacionEmail(FacturaObserver):
    """
    Observador: envía notificación por email al cliente cuando se emite la factura.
    En producción integraría con SendGrid / Amazon SES.
    """

    def actualizar(self, datos: DatosEventoFactura) -> None:
        if datos.evento == EventoFactura.EMITIDA and datos.cliente_email:
            logger.info(
                "[EMAIL] Enviando factura %s a %s (total: $%s)",
                datos.numero_factura,
                datos.cliente_email,
                datos.total,
            )
            # TODO: integrar cliente real de email
            # email_client.send(to=datos.cliente_email, subject=f"Factura {datos.numero_factura}", ...)


class ObservadorActualizacionInventario(FacturaObserver):
    """
    Observador: actualiza el inventario de productos cuando se emite una factura.
    El ajuste real de stock se delega al ProductoRepository.
    """

    def actualizar(self, datos: DatosEventoFactura) -> None:
        if datos.evento == EventoFactura.EMITIDA:
            logger.info(
                "[INVENTARIO] Ajustando stock por factura %s",
                datos.numero_factura,
            )
            # La lógica real de actualización de stock se invoca desde FacturaService


class ObservadorAuditoria(FacturaObserver):
    """
    Observador: registra en el log de auditoría todos los eventos de facturas.
    Cubre el requisito de trazabilidad para la DIAN.
    """

    def actualizar(self, datos: DatosEventoFactura) -> None:
        logger.info(
            "[AUDITORIA] Evento=%s | Factura=%s | Cliente=%s | Total=%s | ts=%s",
            datos.evento.value,
            datos.numero_factura,
            datos.cliente_nombre,
            datos.total,
            datos.timestamp.isoformat(),
        )


class ObservadorDIAN(FacturaObserver):
    """
    Observador: inicia el proceso de validación con la DIAN al emitir la factura.
    Actúa como punto de entrada al simulacro de integración DIAN.
    """

    def actualizar(self, datos: DatosEventoFactura) -> None:
        if datos.evento == EventoFactura.EMITIDA:
            logger.info(
                "[DIAN] Encolando factura %s para validación DIAN",
                datos.numero_factura,
            )
            # En producción: encolaría en Celery / RQ para envío asíncrono


# ── EventBus (Sujeto) ─────────────────────────────────────────────────────────

class FacturaEventBus:
    """
    Sujeto del patrón Observer. Gestiona el registro de observadores
    y la difusión de eventos de facturas a todos los suscriptores.
    """

    def __init__(self) -> None:
        self._observadores: list[FacturaObserver] = []

    def suscribir(self, observador: FacturaObserver) -> None:
        """Registra un nuevo observador en el bus de eventos."""
        if observador not in self._observadores:
            self._observadores.append(observador)
            logger.debug("[EventBus] Observador registrado: %s", type(observador).__name__)

    def desuscribir(self, observador: FacturaObserver) -> None:
        """Elimina un observador del bus de eventos."""
        self._observadores.remove(observador)

    def publicar(self, datos: DatosEventoFactura) -> None:
        """Notifica a todos los observadores suscritos del evento ocurrido."""
        logger.info(
            "[EventBus] Publicando evento %s para factura %s (%d observadores)",
            datos.evento.value,
            datos.numero_factura,
            len(self._observadores),
        )
        for observador in self._observadores:
            try:
                observador.actualizar(datos)
            except Exception as exc:
                logger.error(
                    "[EventBus] Error en observador %s: %s",
                    type(observador).__name__,
                    exc,
                )


def crear_event_bus_por_defecto() -> FacturaEventBus:
    """
    Fábrica que crea y configura el EventBus con los observadores estándar.
    Llamada una sola vez durante el arranque de la aplicación.
    """
    bus = FacturaEventBus()
    bus.suscribir(ObservadorAuditoria())
    bus.suscribir(ObservadorNotificacionEmail())
    bus.suscribir(ObservadorActualizacionInventario())
    bus.suscribir(ObservadorDIAN())
    return bus