"""
Utilidades administrativas y de seguridad.
Gestión de credenciales de administrador y operaciones sensibles.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import logging
from utils.constantes import (
    MSG_CONFIRMAR_BORRADO,
    MSG_VERIFICACION_ADMIN,
    MSG_CLAVE_ADMIN,
    MSG_CLAVE_ACTUAL,
    MSG_CLAVE_NUEVA,
    MSG_CLAVE_VACIA,
)

logger = logging.getLogger(__name__)


def _crear_ventana_temporal():
    """
    Crea una ventana Tk temporal para diálogos cuando no hay parent.

    Returns:
        tk.Tk: Ventana temporal oculta
    """
    root = tk.Tk()
    root.withdraw()
    return root


def _es_parent_valido(parent):
    """Verifica si parent es un widget Tkinter válido."""
    return parent is not None and hasattr(parent, "tk")


def borrar_info(parent=None, ejecutar_borrado=None):
    """
    Solicita confirmación y credenciales de admin para borrar toda la información.

    Args:
        parent: Widget padre para diálogos (opcional)
        ejecutar_borrado: Callable(usuario, clave) que realiza el borrado

    Returns:
        bool: True si se completó exitosamente, False en caso contrario
              o tupla (True, usuario, clave) si no se proporciona callback
    """
    created_root = None

    try:
        # Crear ventana temporal si parent es inválido
        if not _es_parent_valido(parent):
            created_root = _crear_ventana_temporal()
            parent = created_root

        # Confirmación inicial
        if not messagebox.askokcancel("Confirmación", MSG_CONFIRMAR_BORRADO):
            return False

        # Solicitar usuario
        usuario = simpledialog.askstring(
            "Verificación administrador",
            MSG_VERIFICACION_ADMIN,
            parent=parent,
        )
        if usuario is None:
            return False

        # Solicitar clave
        clave = simpledialog.askstring(
            "Verificación administrador",
            MSG_CLAVE_ADMIN,
            show="*",
            parent=parent,
        )
        if clave is None:
            return False

        # Ejecutar callback si se proporciona
        if ejecutar_borrado is not None and callable(ejecutar_borrado):
            try:
                resultado = ejecutar_borrado(usuario, clave)
                return bool(resultado)
            except Exception as e:
                logger.error(f"Error al ejecutar borrado: {e}")
                return False

        # Si no hay callback, retornar datos para procesamiento externo
        return (True, usuario, clave)

    finally:
        if created_root is not None:
            try:
                created_root.destroy()
            except Exception as e:
                logger.warning(f"Error al destruir ventana temporal: {e}")


def actualizar_clave_adm(parent=None, ejecutar_actualizacion=None):
    """
    Solicita credenciales de admin y nueva clave para actualizar.

    Args:
        parent: Widget padre para diálogos (opcional)
        ejecutar_actualizacion: Callable(usuario, clave_actual, clave_nueva)

    Returns:
        bool: True si se completó exitosamente, False en caso contrario
              o tupla (True, usuario, clave) si no se proporciona callback
    """
    created_root = None

    try:
        # Crear ventana temporal si parent es inválido
        if not _es_parent_valido(parent):
            created_root = _crear_ventana_temporal()
            parent = created_root

        # Solicitar usuario
        usuario = simpledialog.askstring(
            "Verificación administrador",
            MSG_VERIFICACION_ADMIN,
            parent=parent,
        )
        if usuario is None:
            return False

        # Solicitar clave actual
        clave = simpledialog.askstring(
            "Verificación administrador",
            MSG_CLAVE_ACTUAL,
            show="*",
            parent=parent,
        )
        if clave is None:
            return False

        # Solicitar clave nueva
        nva_clave = simpledialog.askstring(
            "Actualización clave",
            MSG_CLAVE_NUEVA,
            show="*",
            parent=parent,
        )
        if nva_clave is None:
            messagebox.showwarning("Aviso", MSG_CLAVE_VACIA)
            return False

        # Ejecutar callback si se proporciona
        if ejecutar_actualizacion is not None and callable(ejecutar_actualizacion):
            try:
                resultado = ejecutar_actualizacion(usuario, clave, nva_clave)
                return bool(resultado)
            except Exception as e:
                logger.error(f"Error al actualizar clave: {e}")
                return False

        # Si no hay callback, retornar datos para procesamiento externo
        return (True, usuario, clave)

    finally:
        if created_root is not None:
            try:
                created_root.destroy()
            except Exception as e:
                logger.warning(f"Error al destruir ventana temporal: {e}")
