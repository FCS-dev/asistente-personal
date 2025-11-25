"""
Utilidades para manejo de fechas.
Conversión y validación entre formatos de fecha (app <-> BD).
"""

import datetime as dt
from datetime import date
from utils.constantes import FECHA_MIN, FORMATO_FECHA_APP, FORMATO_FECHA_BD


def valida_fecha(fecha):
    """
    Valida si una fecha es válida.

    Args:
        fecha (str): Fecha en formato "DD/MM/YYYY" o "DD-MM-YYYY"

    Returns:
        bool: True si es válida y >= FECHA_MIN, False en caso contrario
    """
    if not fecha:
        return False
    try:
        fecha = fecha.replace("-", "/")  # Acepta ambos separadores
        fecha_obj = dt.datetime.strptime(fecha, FORMATO_FECHA_APP).date()
    except ValueError:
        return False

    if fecha_obj < FECHA_MIN:
        return False
    return True


def fecha_a_bd(fecha):
    """
    Convierte fecha del formato app al formato BD.

    Args:
        fecha (str): Fecha en formato "DD/MM/YYYY" o "DD-MM-YYYY"

    Returns:
        str: Fecha en formato "YYYY-MM-DD" o "" si hay error
    """
    if not fecha:
        return ""
    try:
        fecha = fecha.replace("-", "/")
        fecha_dt = dt.datetime.strptime(fecha, FORMATO_FECHA_APP)
        fecha_bd = fecha_dt.strftime(FORMATO_FECHA_BD)
    except ValueError:
        return ""
    return fecha_bd


def bd_a_fecha(fecha):
    """
    Convierte fecha del formato BD al formato app.

    Args:
        fecha (str): Fecha en formato "YYYY-MM-DD"

    Returns:
        str: Fecha en formato "DD/MM/YYYY" o "" si hay error
    """
    if not fecha:
        return ""
    try:
        fecha_dt = dt.datetime.strptime(fecha, FORMATO_FECHA_BD)
        return fecha_dt.strftime(FORMATO_FECHA_APP)
    except ValueError:
        return ""


def obtener_fecha_actual():
    """
    Obtiene la fecha actual.

    Returns:
        date: Fecha de hoy
    """
    return date.today()
