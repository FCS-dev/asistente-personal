import tkinter as tk
from tkinter import simpledialog, messagebox


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
        tarea_descrip_label = tk.Label(master, text="Tarea").grid(
            row=0, column=0, sticky="e"
        )
        tarea_fecha_label = tk.Label(master, text="Fecha").grid(
            row=1, column=0, sticky="e"
        )
        tarea_prioridad_label = tk.Label(master, text="Prioridad").grid(
            row=2, column=0, sticky="e"
        )
        tarea_tags_label = tk.Label(master, text="Tags").grid(
            row=3, column=0, sticky="e"
        )

        # entrys tarea
        self.tarea_descrip_entry = tk.Entry(
            master,
            width=40,
        )
        self.tarea_fecha_entry = tk.Entry(master, width=10)
        self.tarea_prioridad_entry = tk.Entry(master, width=10)
        self.tarea_tags_entry = tk.Entry(master, width=40)

        self.tarea_descrip_entry.grid(row=0, column=1, sticky="w")
        self.tarea_fecha_entry.grid(row=1, column=1, sticky="w")
        self.tarea_prioridad_entry.grid(row=2, column=1, sticky="w")
        self.tarea_tags_entry.grid(row=3, column=1, sticky="w")

        # Rellenar si vienen datos iniciales (para editar)
        self.tarea_descrip_entry.insert(0, self.initial_data["descrip"])
        self.tarea_fecha_entry.insert(0, self.initial_data["fecha"])
        self.tarea_prioridad_entry.insert(0, self.initial_data["prioridad"])
        self.tarea_tags_entry.insert(0, self.initial_data["tag"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.tarea_descrip_entry

    def validate(self):
        # Validar campos no vacíos
        tarea = self.tarea_descrip_entry.get().strip()
        fecha = self.tarea_fecha_entry.get().strip()
        prioridad = self.tarea_prioridad_entry.get().strip()
        tags = self.tarea_tags_entry.get().strip()

        if not tarea or not fecha or not prioridad or not tags:
            messagebox.showwarning(
                "Campos vacíos", "Todos los campos son obligatorios."
            )
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "tarea": self.tarea_descrip_entry.get().strip(),
            "fecha": self.tarea_fecha_entry.get().strip(),
            "prioridad": self.tarea_prioridad_entry.get().strip(),
            "tags": self.tarea_tags_entry.get().strip(),
        }
