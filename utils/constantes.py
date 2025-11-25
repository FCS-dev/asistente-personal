"""
Constantes globales del asistente personal.
Centralizadas para facilitar mantenimiento y evitar valores mágicos.
"""

from datetime import date

# Fechas
FECHA_MIN = date(2020, 1, 1)
FORMATO_FECHA_APP = "%d/%m/%Y"  # Formato mostrado al usuario
FORMATO_FECHA_BD = "%Y-%m-%d"  # Formato almacenado en BD

# Estados de Tareas
ESTADO_PENDIENTE = "Pendiente"
ESTADO_PROGRESO = "En progreso"
ESTADO_COMPLETADA = "Completada"
ESTADO_ARCHIVADA = "Archivada"

ESTADOS_VALIDOS = [
    ESTADO_PENDIENTE,
    ESTADO_PROGRESO,
    ESTADO_COMPLETADA,
    ESTADO_ARCHIVADA,
]

# Tipos de Actividades
TIPO_TAREA = "tarea"
TIPO_EVENTO = "evento"
TIPO_NOTA = "nota"

TIPOS_VALIDOS = [TIPO_TAREA, TIPO_EVENTO, TIPO_NOTA]

# Configuración para PDF
PDF_MARGEN = 15
PDF_TAMANIO_TITULO = 16
PDF_TAMANIO_FUENTE = 10
PDF_FUENTE = "Arial"

# Mensajes
MSG_CONFIRMAR_BORRADO = (
    "¿Esta seguro de borrar toda la información registrada en la BD?"
)
MSG_VERIFICACION_ADMIN = "Usuario administrador:"
MSG_CLAVE_ADMIN = "Clave de administrador:"
MSG_CLAVE_ACTUAL = "Clave ACTUAL:"
MSG_CLAVE_NUEVA = "Clave NUEVA:"
MSG_CLAVE_VACIA = "La clave del administrador no puede estar vacía"
