import datetime as dt
from datetime import date

import tkinter as tk
from tkinter import simpledialog

FECHA_MIN = dt.date(2020, 1, 1)


def valida_fecha(fecha):
    if not fecha:
        return False
    try:
        fecha = fecha.replace("-", "/")  # '-' o '/' será igual de válido
        fecha_obj = dt.datetime.strptime(fecha, "%d/%m/%Y").date()
    except ValueError:
        return False
    if fecha_obj < FECHA_MIN:  ### Para que no sea menor a la fecha establecida
        return False
    return True


def fecha_a_bd(fecha):
    if not fecha:
        return ""
    try:
        fecha = fecha.replace("-", "/")  # '-' o '/' será igual de válido
        fecha_dt = dt.datetime.strptime(fecha, "%d/%m/%Y")
        fecha_bd = fecha_dt.strftime("%Y-%m-%d")  # formato para BD
    except ValueError:
        return ""
    return fecha_bd


def bd_a_fecha(fecha):
    if not fecha:
        return ""
    try:
        fecha_dt = dt.datetime.strptime(fecha, "%Y-%m-%d")  # formato BD
        return fecha_dt.strftime("%d/%m/%Y")  # formato app
    except ValueError:
        return ""


def obtener_fecha_actual():
    fecha_actual = date.today()
    return fecha_actual


class VentanaEstados(simpledialog.Dialog):
    def __init__(self, parent, title="Cambiar Estado", initial_data={}):
        self.initial_data = (
            initial_data  # debe venir el ID y sobre quien va el cambios de estado
        )
        super().__init__(parent, title)

    def body(self, master):
        if self.initial_data["tipo"] == "tarea":
            id = self.initial_data["id"]
            tarea = self.initial_data["tarea"]
            fecha = self.initial_data["fecha"]
            prioridad = self.initial_data["prioridad"]
            estado = self.initial_data["estado"]
            tags = self.initial_data["tag"]

            # labels tarea
            tk.Label(master, text="Tarea").grid(row=0, column=0, sticky="e")
            tk.Label(master, text=tarea).grid(row=0, column=1, sticky="w")
            tk.Label(master, text="Fecha").grid(row=1, column=0, sticky="e")
            tk.Label(master, text=fecha).grid(row=1, column=1, sticky="w")
            tk.Label(master, text="Prioridad").grid(row=2, column=0, sticky="e")
            tk.Label(master, text=prioridad).grid(row=2, column=1, sticky="w")
            tk.Label(master, text="Tags").grid(row=3, column=0, sticky="e")
            tk.Label(master, text=tags).grid(row=3, column=1, sticky="w")
            tk.Label(master, text="Estado").grid(row=4, column=0, sticky="e")

            valor_inicial = estado

            self.estado_var = tk.StringVar(value=valor_inicial)

            # Estado: 'Pendiente', 'En progreso', 'Completada','Archivada'
            # Radiobutton Pendiente
            rb_pendiente = tk.Radiobutton(
                master,
                text="Pendiente",
                variable=self.estado_var,
                value="Pendiente",
                command=self._actualizar_estado_entry,
                state="normal",
            )
            rb_pendiente.grid(row=4, column=1, sticky="w")
            # Radiobutton En progreso
            rb_progreso = tk.Radiobutton(
                master,
                text="En progreso",
                variable=self.estado_var,
                value="En progreso",
                command=self._actualizar_estado_entry,
                state="normal",
            )
            rb_progreso.grid(row=5, column=1, sticky="w")
            # Radiobutton Completada
            rb_completada = tk.Radiobutton(
                master,
                text="Completada",
                variable=self.estado_var,
                value="Completada",
                command=self._actualizar_estado_entry,
                state="normal",
            )
            rb_completada.grid(row=6, column=1, sticky="w")
            # Radiobutton Archivada
            rb_archivada = tk.Radiobutton(
                master,
                text="Archivada",
                variable=self.estado_var,
                value="Archivada",
                command=self._actualizar_estado_entry,
                state="normal",
            )
            rb_archivada.grid(row=7, column=1, sticky="w")

            # Entry interno para aplicar y validar
            self.tarea_estado_entry = tk.Entry(master, width=11)
            self._actualizar_estado_entry()

            # El campo de nombre recibe el foco al abrir el diálogo
            return self.tarea_estado_entry

    def _actualizar_estado_entry(self):
        valor = self.estado_var.get()
        self.tarea_estado_entry.config(state="normal")
        self.tarea_estado_entry.delete(0, tk.END)
        self.tarea_estado_entry.insert(0, valor)
        self.tarea_estado_entry.config(state="readonly")

    # def validate(self):
    #     return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "estado": self.tarea_estado_entry.get().strip(),
        }


"""
Ventana para seleccionar tags mediante checkboxes.
- lista_tags: lista de strings (opcional). Si no se pasa, se intentará cargar desde
    la base de datos usando `bd.todos_los_tags(tipo)`.
- initial_tags: cadena con tags separados por comas (ej: 'Trabajo,Importante')
- bd: instancia de Persistencia (opcional). Necesaria si no se provee lista_tags.
- tipo: 'Tareas'|'Eventos'|'Notas' (opcional). Necesario si bd se usa para cargar tags.
"""


class VentanaTags(simpledialog.Dialog):
    def __init__(
        self,
        parent,
        lista_tags=None,
        initial_tags=None,
        bd=None,
        tipo=None,
        title="Seleccionar Tags",
    ):
        # Cargar lista de tags desde BD si no fue provista
        if lista_tags is None:
            if bd is not None and tipo is not None:
                filas = bd.todos_los_tags(tipo)
                # bd.todos_los_tags devuelve lista de tuplas [(tag,), ...]
                lista_tags = [f[0] for f in filas]
            else:
                lista_tags = []

        self.lista_tags = lista_tags
        # inicializar conjunto de tags existentes (limpiando espacios)
        if initial_tags:
            if isinstance(initial_tags, (list, tuple, set)):
                self.initial_tags = set([t.strip() for t in initial_tags])
            else:
                self.initial_tags = set(
                    [t.strip() for t in initial_tags.split(",") if t.strip()]
                )
        else:
            self.initial_tags = set()

        self.vars = []  # almacenará tuplas (tag, IntVar)

        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Selecciona los Tags:").grid(row=0, column=0, sticky="w")
        checkbox_frame = tk.Frame(master)
        checkbox_frame.grid(row=1, column=0, sticky="w")
        # Armando checkboxes dinámicos...
        for tag in self.lista_tags:
            var = tk.IntVar()
            if tag in self.initial_tags:
                var.set(1)
            chk = tk.Checkbutton(
                checkbox_frame,
                text=tag,
                variable=var,
            )
            chk.pack(anchor="w")
            self.vars.append((tag, var))
        return None

    def apply(self):
        # Guardar solo los tags marcados como cadena separada por comas
        seleccionados = [tag for tag, var in self.vars if var.get() == 1]
        self.result = ",".join(seleccionados) if seleccionados else ""


def generar_json():
    from pathlib import Path
    import persistencia as bd
    import json

    data_file = Path("data_passistant.json")
    persist = bd.Persistencia()
    info_tareas = persist.trae_tareas()
    info_eventos = persist.trae_eventos()
    info_notas = persist.trae_notas()

    info_gnral = {
        "tareas": [],
        "eventos": [],
        "notas": [],
    }
    for i in info_tareas:
        fila = {
            "id": i[0],
            "tarea_descrip": i[1],
            "fecha": i[2],
            "prioridad": i[3],
            "estado": i[4],
            "tags": i[5],
        }
        info_gnral["tareas"].append(fila)
    for i in info_eventos:
        fila = {
            "id": i[0],
            "evento_descrip": i[1],
            "fecha_inicio": i[2],
            "fecha_fin": i[3],
            "tags": i[4],
        }
        info_gnral["eventos"].append(fila)
    for i in info_notas:
        fila = {"id": i[0], "nota_descrip": i[1], "fecha_creacion": i[2], "tags": i[3]}
        info_gnral["notas"].append(fila)
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(info_gnral, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return False
    return True


def generar_pdf():
    from pathlib import Path
    import persistencia as bd
    from fpdf import FPDF

    pdf_file = Path("data_passistant.pdf")
    persist = bd.Persistencia()

    info_tareas = persist.trae_tareas()
    info_eventos = persist.trae_eventos()
    info_notas = persist.trae_notas()

    # Crear PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # ----- TAREAS -----
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "TAREAS", ln=True)
    pdf.set_font("Arial", size=12)

    if info_tareas:
        for i in info_tareas:
            pdf.multi_cell(
                0,
                8,
                f"ID: {i[0]}\n"
                f"Descripción: {i[1]}\n"
                f"Fecha: {i[2]}\n"
                f"Prioridad: {i[3]}\n"
                f"Estado: {i[4]}\n"
                f"Tags: {i[5]}\n"
                "---------------------------",
            )
    else:
        pdf.cell(0, 10, "No hay tareas registradas.", ln=True)

    # ----- EVENTOS -----
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EVENTOS", ln=True)
    pdf.set_font("Arial", size=12)

    if info_eventos:
        for i in info_eventos:
            pdf.multi_cell(
                0,
                8,
                f"ID: {i[0]}\n"
                f"Descripción: {i[1]}\n"
                f"Inicio: {i[2]}\n"
                f"Fin: {i[3]}\n"
                f"Tags: {i[4]}\n"
                "---------------------------",
            )
    else:
        pdf.cell(0, 10, "No hay eventos registrados.", ln=True)

    # ----- NOTAS -----
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "NOTAS", ln=True)
    pdf.set_font("Arial", size=12)

    if info_notas:
        for i in info_notas:
            pdf.multi_cell(
                0,
                8,
                f"ID: {i[0]}\n"
                f"Descripción: {i[1]}\n"
                f"Fecha creación: {i[2]}\n"
                f"Tags: {i[3]}\n"
                "---------------------------",
            )
    else:
        pdf.cell(0, 10, "No hay notas registradas.", ln=True)

    try:
        pdf.output(pdf_file)
    except Exception:
        return False

    return True
