"""
Módulo utilitario principal - re-exporta funcionalidades especializadas.

Este módulo actúa como punto central para acceder a utilidades del sistema:
- Funciones de fecha (date_utils)
- Diálogos personalizados (dialog_windows)
- Exportación de datos (export_utils)
- Funciones administrativas (admin_utils)
"""

# Re-exportar todas las funciones de utilidad para retrocompatibilidad
from utils.date_utils import (
    valida_fecha,
    fecha_a_bd,
    bd_a_fecha,
    obtener_fecha_actual,
)
from views.dialog_windows import VentanaEstados, VentanaTags
from utils.exporta_utils import generar_json, generar_pdf
from utils.admin_utils import borrar_info, actualizar_clave_adm
from utils.constantes import FECHA_MIN

__all__ = [
    # Funciones de fecha
    "valida_fecha",
    "fecha_a_bd",
    "bd_a_fecha",
    "obtener_fecha_actual",
    # Clases de diálogo
    "VentanaEstados",
    "VentanaTags",
    # Funciones de exportación
    "generar_json",
    "generar_pdf",
    # Funciones administrativas
    "borrar_info",
    "actualizar_clave_adm",
    # Constantes
    "FECHA_MIN",
]
