"""
Utilidades para exportar datos a JSON y PDF.
Genera reportes para el usuario de la app
Métodos:
generar_json()
generar_pdf()
"""

import json
import logging
from pathlib import Path
from fpdf import FPDF
from utils.constantes import (
    PDF_MARGEN,
    PDF_TAMANIO_TITULO,
    PDF_TAMANIO_FUENTE,
    PDF_FUENTE,
)

# Configurar logging para errores
logger = logging.getLogger(__name__)


def generar_json(ruta, persistencia=None):
    """
    Exporta tareas, eventos y notas a archivo JSON.

    Args:
        ruta (str): Ruta del archivo JSON a crear
        persistencia: Instancia de Persistencia con datos. Si es None, crea una nueva.

    Returns:
        bool: True si se generó exitosamente, False en caso de error
    """
    if not ruta:
        return False

    try:
        # Si no se pasa persistencia, crear una instancia
        if persistencia is None:
            import repository.persistencia as bd

            persistencia = bd.Persistencia()

        data_file = Path(ruta)

        # Obtener datos de todas las entidades
        info_tareas = persistencia.trae_tareas()
        info_eventos = persistencia.trae_eventos()
        info_notas = persistencia.trae_notas()

        # Estructurar datos
        info_gnral = {
            "tareas": [
                {
                    "id": i[0],
                    "tarea_descrip": i[1],
                    "fecha": i[2],
                    "prioridad": i[3],
                    "estado": i[4],
                    "tags": i[5],
                }
                for i in info_tareas
            ],
            "eventos": [
                {
                    "id": i[0],
                    "evento_descrip": i[1],
                    "fecha_inicio": i[2],
                    "fecha_fin": i[3],
                    "tags": i[4],
                }
                for i in info_eventos
            ],
            "notas": [
                {
                    "id": i[0],
                    "nota_descrip": i[1],
                    "fecha_creacion": i[2],
                    "tags": i[3],
                }
                for i in info_notas
            ],
        }

        # Guardar archivo
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(info_gnral, f, ensure_ascii=False, indent=4)

        return True

    except IOError as e:
        logger.error(f"Error al escribir archivo JSON: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al generar JSON: {e}")
        return False


def generar_pdf(ruta, persistencia=None):
    """
    Exporta tareas, eventos y notas a archivo PDF.

    Args:
        ruta (str): Ruta del archivo PDF a crear
        persistencia: Instancia de Persistencia con datos. Si es None, crea una nueva.

    Returns:
        bool: True si se generó exitosamente, False en caso de error
    """
    if not ruta:
        return False

    try:
        # Si no se pasa persistencia, crear una instancia
        if persistencia is None:
            import repository.persistencia as bd

            persistencia = bd.Persistencia()

        pdf_file = Path(ruta)

        # Obtener datos
        info_tareas = persistencia.trae_tareas()
        info_eventos = persistencia.trae_eventos()
        info_notas = persistencia.trae_notas()

        # Crear PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=PDF_MARGEN)

        def agregar_titulo(texto):
            """Agrega un título formateado al PDF."""
            pdf.set_font(PDF_FUENTE, "B", PDF_TAMANIO_TITULO)
            pdf.cell(0, 12, texto, ln=True)
            y = pdf.get_y()
            pdf.line(10, y, 200, y)
            pdf.ln(3)
            pdf.set_font(PDF_FUENTE, size=PDF_TAMANIO_FUENTE)

        def agregar_item(labels, datos):
            """Agrega un item con múltiples campos al PDF."""
            pdf.set_font(PDF_FUENTE, size=PDF_TAMANIO_FUENTE)
            for label, valor in zip(labels, datos):
                if "descripción" in label.lower():
                    pdf.multi_cell(0, 6, f"{label}: {valor}")
                else:
                    pdf.cell(0, 6, f"{label}: {valor}", ln=True)
            pdf.ln(4)

        # Página de Tareas
        pdf.add_page()
        agregar_titulo("TAREAS REGISTRADAS")
        pdf.cell(0, 8, f"Total tareas: {len(info_tareas)}", ln=True)
        pdf.ln(3)

        if info_tareas:
            for i in info_tareas:
                agregar_item(
                    ["ID", "Descripción", "Fecha", "Prioridad", "Estado", "Tags"],
                    [i[0], i[1], i[2], i[3], i[4], i[5]],
                )
        else:
            pdf.cell(0, 10, "No hay tareas registradas.", ln=True)

        # Página de Eventos
        pdf.add_page()
        agregar_titulo("EVENTOS REGISTRADOS")
        pdf.cell(0, 8, f"Total eventos: {len(info_eventos)}", ln=True)
        pdf.ln(3)

        if info_eventos:
            for i in info_eventos:
                agregar_item(
                    ["ID", "Descripción", "Inicio", "Fin", "Tags"],
                    [i[0], i[1], i[2], i[3], i[4]],
                )
        else:
            pdf.cell(0, 10, "No hay eventos registrados.", ln=True)

        # Página de Notas
        pdf.add_page()
        agregar_titulo("NOTAS REGISTRADAS")
        pdf.cell(0, 8, f"Total notas: {len(info_notas)}", ln=True)
        pdf.ln(3)

        if info_notas:
            for i in info_notas:
                agregar_item(
                    ["ID", "Descripción", "Fecha creación", "Tags"],
                    [i[0], i[1], i[2], i[3]],
                )
        else:
            pdf.cell(0, 10, "No hay notas registradas.", ln=True)

        # Guardar PDF
        pdf.output(pdf_file)
        return True

    except IOError as e:
        logger.error(f"Error al escribir archivo PDF: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al generar PDF: {e}")
        return False
