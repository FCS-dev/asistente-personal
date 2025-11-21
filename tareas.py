import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as msj
import utiles as util


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
        tk.Label(master, text="Tags").grid(row=4, column=0, sticky="e")

        # entrys tarea
        self.tarea_descrip_entry = tk.Entry(
            master,
            width=40,
        )
        self.tarea_fecha_entry = tk.Entry(master, width=10)
        self.tarea_tags_entry = tk.Entry(master, width=40)

        self.tarea_descrip_entry.grid(row=0, column=1, columnspan=2, sticky="w")
        self.tarea_fecha_entry.grid(row=1, column=1, sticky="w")
        self.tarea_tags_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        # -----------------------------
        # Prioridad: Radiobuttons
        # -----------------------------
        valor_inicial = self.initial_data.get("prioridad")
        if valor_inicial not in ("Normal", "Alta"):
            valor_inicial = "Normal"

        self.prioridad_var = tk.StringVar(value=valor_inicial)

        # Radiobutton Normal
        rb_normal = tk.Radiobutton(
            master,
            text="Normal",
            variable=self.prioridad_var,
            value="Normal",
            command=self._actualizar_prioridad_entry,
            state="normal",
        )
        rb_normal.grid(row=2, column=1, sticky="w")

        # Radiobutton Alta
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
        self.tarea_tags_entry.insert(0, self.initial_data["tag"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.tarea_descrip_entry

    def _actualizar_prioridad_entry(self):
        valor = self.prioridad_var.get()
        self.tarea_prioridad_entry.config(state="normal")
        self.tarea_prioridad_entry.delete(0, tk.END)
        self.tarea_prioridad_entry.insert(0, valor)
        self.tarea_prioridad_entry.config(state="readonly")

    def validate(self):
        # Validar campos no vacíos
        tarea = self.tarea_descrip_entry.get().strip()
        fecha = self.tarea_fecha_entry.get().strip()
        prioridad = self.tarea_prioridad_entry.get().strip()
        tags = self.tarea_tags_entry.get().strip()
        if not tarea or not util.valida_fecha(fecha) or not prioridad or not tags:
            msj.showwarning("Verificar información", "Debe introducir datos válidos.")
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "tarea": self.tarea_descrip_entry.get().strip(),
            "fecha": util.fecha_a_bd(self.tarea_fecha_entry.get().strip()),
            "prioridad": self.tarea_prioridad_entry.get().strip(),
            "tags": self.tarea_tags_entry.get().strip(),
        }
