"""
services/dian_service.py - Simulacro de integración con el servidor DIAN.

Genera CUFE (Código Único de Factura Electrónica) y simula la validación.
En producción este módulo reemplazaría las llamadas al web service real de la DIAN.
"""
import hashlib
import random
import string
import logging
from datetime import datetime
from decimal import Decimal

from app.config import get_settings

logger = logging.getLogger(__name__)


class DianService:
    """
    Servicio que simula la comunicación con el Portal de Facturación Electrónica de la DIAN.
    Implementa la generación del CUFE y el proceso de validación/autorización.
    """

    def __init__(self) -> None:
        self._settings = get_settings()

    def generar_cufe(
        self,
        numero_factura: str,
        fecha_factura: str,
        total: Decimal,
        nit_emisor: str,
        nit_receptor: str,
    ) -> str:
        """
        Genera el CUFE (Código Único de Factura Electrónica).
        
        Fórmula DIAN simplificada:
          CUFE = SHA-384(NumFac + FecFac + ValFac + NitOFE + NumAdq + ClTec)
        """
        clave_tecnica = self._settings.dian_api_key
        cadena = (
            f"{numero_factura}"
            f"{fecha_factura}"
            f"{total:.2f}"
            f"{nit_emisor}"
            f"{nit_receptor}"
            f"{clave_tecnica}"
        )
        cufe = hashlib.sha384(cadena.encode("utf-8")).hexdigest()
        logger.info("[DIAN] CUFE generado para factura %s: %s...", numero_factura, cufe[:16])
        return cufe

    def validar_factura(self, cufe: str, numero_factura: str) -> dict:
        """
        Simula la validación de una factura ante la DIAN.
        
        En el simulacro:
          - 95% de probabilidad de éxito.
          - 5% de probabilidad de rechazo (para probar el flujo de error).
        
        Retorna:
          {
            "aprobada": bool,
            "codigo_respuesta": str,
            "mensaje": str,
            "timestamp_dian": str,
          }
        """
        logger.info("[DIAN] Enviando factura %s para validación (CUFE: %s...)", numero_factura, cufe[:16])

        # Simulacro de latencia de la DIAN
        aprobada = random.random() < 0.95  # 95% de éxito

        if aprobada:
            return {
                "aprobada": True,
                "codigo_respuesta": "00",
                "mensaje": f"Factura {numero_factura} validada y autorizada por la DIAN.",
                "timestamp_dian": datetime.utcnow().isoformat(),
                "numero_autorizacion": self._generar_numero_autorizacion(),
            }
        else:
            return {
                "aprobada": False,
                "codigo_respuesta": "99",
                "mensaje": "Error de validación: firma digital no corresponde al NIT emisor.",
                "timestamp_dian": datetime.utcnow().isoformat(),
                "numero_autorizacion": None,
            }

    def _generar_numero_autorizacion(self) -> str:
        """Genera un número de autorización simulado de 18 dígitos."""
        return "".join(random.choices(string.digits, k=18))

    def generar_qr_data(self, cufe: str, numero_factura: str, total: Decimal) -> str:
        """
        Genera el contenido del código QR para la factura impresa.
        URL estándar de verificación DIAN.
        """
        return (
            f"https://catalogo-vpfe-hab.dian.gov.co/document/searchqr"
            f"?documentkey={cufe}"
        )