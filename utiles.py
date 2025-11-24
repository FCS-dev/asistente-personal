import datetime as dt
from datetime import date

import tkinter as tk
from tkinter import simpledialog, messagebox

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


def generar_json(ruta):
    from pathlib import Path
    import persistencia as bd
    import json

    if not ruta:
        return False
    data_file = Path(ruta)
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
    except Exception:
        return False
    # except Exception as e:
    #     return False
    return True


def generar_pdf(ruta):
    from pathlib import Path
    import persistencia as bd
    from fpdf import FPDF

    if not ruta:
        return False
    pdf_file = Path(ruta)
    persist = bd.Persistencia()
    info_tareas = persist.trae_tareas()
    info_eventos = persist.trae_eventos()
    info_notas = persist.trae_notas()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    def agregar_titulo(texto):
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 12, texto, ln=True)
        y = pdf.get_y()  # posición vertical actual
        pdf.line(10, y, 200, y)  # x1, y1, x2, y2 (márgenes estándar)
        pdf.ln(3)
        pdf.set_font("Arial", size=10)

    def agregar_item(labels, datos):
        pdf.set_font("Arial", size=10)
        for label, valor in zip(labels, datos):
            if label.lower().startswith("descripción"):
                pdf.multi_cell(0, 6, f"{label}: {valor}")
            else:
                pdf.cell(0, 6, f"{label}: {valor}", ln=True)
        pdf.ln(4)

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
    try:
        pdf.output(pdf_file)
    except Exception:
        return False
    return True


def borrar_info(parent=None, ejecutar_borrado=None):
    created_root = None
    # Si parent no es un widget tkinter válido, crear uno temporal
    if parent is None or not hasattr(parent, "tk"):
        created_root = tk.Tk()
        created_root.withdraw()
    try:
        if not messagebox.askokcancel(
            "Confirmación",
            "¿Esta seguro de borrar toda la información registrada en la BD?",
        ):
            return False
        # Usuario administrador
        usuario = simpledialog.askstring(
            "Verificación administrador",
            "Usuario administrador:",
            parent=parent,
        )
        if usuario is None:
            return False

        # Clave enmascarada
        clave = simpledialog.askstring(
            "Verificación administrador",
            "Clave de administrador:",
            show="*",
            parent=parent,
        )
        if clave is None:
            return False

        if ejecutar_borrado is not None and callable(ejecutar_borrado):
            try:
                resultado = ejecutar_borrado(usuario, clave)
            except Exception as e:
                return False
            if resultado:
                return True
            else:
                return False
        return (True, usuario, clave)
    finally:
        try:
            created_root.destroy()
        except Exception:
            pass


def actualizar_clave_adm(parent=None, ejecutar_actualizacion=None):
    created_root = None
    # Si parent no es un widget tkinter válido, crear uno temporal
    if parent is None or not hasattr(parent, "tk"):
        created_root = tk.Tk()
        created_root.withdraw()
    try:
        # Usuario administrador
        usuario = simpledialog.askstring(
            "Verificación administrador",
            "Usuario administrador:",
            parent=parent,
        )
        if usuario is None:
            return False
        # Clave enmascarada
        clave = simpledialog.askstring(
            "Verificación administrador",
            "Clave ACTUAL:",
            show="*",
            parent=parent,
        )
        if clave is None:
            return False
        nva_clave = simpledialog.askstring(
            "Actualización clave",
            "Clave NUEVA:",
            show="*",
            parent=parent,
        )
        if nva_clave is None:
            messagebox.showwarning(
                "Aviso", "La clave del administrador no puede estar vacía"
            )
            return False
        if ejecutar_actualizacion is not None and callable(ejecutar_actualizacion):
            try:
                resultado = ejecutar_actualizacion(usuario, clave, nva_clave)
            except Exception as e:
                return False
            if resultado:
                return True
            else:
                return False
        return (True, usuario, clave)
    finally:
        try:
            created_root.destroy()
        except Exception:
            pass
