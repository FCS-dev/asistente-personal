import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as msj
import utils.utiles as util
import repository.persistencia as bd

"""
Clase VentanaTarea()
UI principal de la actividad 'Tareas'
"""


class VentanaTarea(simpledialog.Dialog):
    def __init__(self, parent, title="Tareas", initial_data=None):
        self.initial_data = initial_data or {
            "descrip": "",
            "fecha": "",
            "prioridad": "",
            "tag": "",
        }
        super().__init__(parent, title)

    def body(self, master):
        # labels tarea
        tk.Label(master, text="Tarea").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Fecha").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="(dd/mm/yyyy)").grid(row=1, column=2, sticky="w")
        tk.Label(master, text="Prioridad").grid(row=2, column=0, sticky="e")
        # entrys tarea
        self.tarea_descrip_entry = tk.Entry(
            master,
            width=40,
        )

        self.tarea_fecha_entry = tk.Entry(master, width=10)
        # los tags ahora se seleccionan mediante un diálogo (VentanaTags)
        self.tarea_tags_entry = None

        self.tarea_descrip_entry.grid(row=0, column=1, columnspan=2, sticky="w")
        self.tarea_fecha_entry.grid(row=1, column=1, sticky="w")

        btn_tags = tk.Button(
            master, text="Definir Tags", command=self.mostrar_tags, width=20
        )
        btn_tags.grid(row=4, column=1, sticky="w")
        self.tags_preview_label = tk.Label(
            master,
            text="Seleccionados: " + (self.initial_data.get("tag") or "(ninguno)"),
            wraplength=300,
            justify="left",
        )
        self.tags_preview_label.grid(row=5, column=1, sticky="w")
        # atributo que guarda la cadena de tags seleccionados (coma-separada)
        self.tags_seleccionados = self.initial_data.get("tag") or ""

        # Prioridad: Radiobuttons
        valor_inicial = self.initial_data.get("prioridad")
        if valor_inicial not in ("Normal", "Alta"):
            valor_inicial = "Normal"

        self.prioridad_var = tk.StringVar(value=valor_inicial)

        rb_normal = tk.Radiobutton(
            master,
            text="Normal",
            variable=self.prioridad_var,
            value="Normal",
            command=self._actualizar_prioridad_entry,
            state="normal",
        )
        rb_normal.grid(row=2, column=1, sticky="w")
        rb_alta = tk.Radiobutton(
            master,
            text="Alta",
            variable=self.prioridad_var,
            value="Alta",
            command=self._actualizar_prioridad_entry,
            state="normal",
        )
        rb_alta.grid(row=3, column=1, sticky="w")

        # Entry interno para aplicar y validar
        self.tarea_prioridad_entry = tk.Entry(master, width=10)

        self._actualizar_prioridad_entry()

        # Rellenar si vienen datos iniciales (para editar)
        self.tarea_descrip_entry.insert(0, self.initial_data["descrip"])
        self.tarea_fecha_entry.insert(0, self.initial_data["fecha"])
        self.tarea_prioridad_entry.insert(0, self.initial_data["prioridad"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.tarea_descrip_entry

    def _actualizar_prioridad_entry(self):
        valor = self.prioridad_var.get()
        self.tarea_prioridad_entry.config(state="normal")
        self.tarea_prioridad_entry.delete(0, tk.END)
        self.tarea_prioridad_entry.insert(0, valor)
        self.tarea_prioridad_entry.config(state="readonly")

    def validate(self):
        tarea = self.tarea_descrip_entry.get().strip()
        fecha = self.tarea_fecha_entry.get().strip()
        prioridad = self.tarea_prioridad_entry.get().strip()
        if not tarea:
            msj.showwarning("Validación", "Debe ingresar una descripción para la tarea")
            return False
        if not util.valida_fecha(fecha):
            msj.showwarning(
                "Validación", "Debe ingresar una fecha válida (mínimo: 01/01/2020)"
            )
            return False
        if not prioridad:
            msj.showwarning("Validación", "Debe definir una prioridad para la tarea")
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "tarea": self.tarea_descrip_entry.get().strip(),
            "fecha": util.fecha_a_bd(self.tarea_fecha_entry.get().strip()),
            "prioridad": self.tarea_prioridad_entry.get().strip(),
            "tags": getattr(self, "tags_seleccionados", ""),
        }

    def mostrar_tags(self):
        datos = bd.Persistencia()
        filas = datos.todos_los_tags("Tareas")
        lista_tags = [f[0] for f in filas]
        inicial_tags = self.tags_seleccionados or self.initial_data.get("tag") or ""
        dialog = util.VentanaTags(
            parent=self.master, lista_tags=lista_tags, initial_tags=inicial_tags
        )
        if dialog.result is not None:
            self.tags_seleccionados = dialog.result
            texto = "Seleccionados: " + (
                self.tags_seleccionados if self.tags_seleccionados else "(ninguno)"
            )
            self.tags_preview_label.config(text=texto)
