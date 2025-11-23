import tkinter as tk
from tkinter import simpledialog, messagebox
import utiles as util


class VentanaEvento(simpledialog.Dialog):
    def __init__(self, parent, title="Eventos", initial_data=None):
        self.initial_data = initial_data or {
            "descrip": "",
            "fecini": "",
            "fecfin": "",
            "tag": "",
        }
        super().__init__(parent, title)

    def body(self, master):
        # labels evento
        evento_descrip_label = tk.Label(master, text="Nombre Evento").grid(
            row=0, column=0, sticky="e"
        )
        evento_fecha_inicio_label = tk.Label(master, text="Fecha inicio").grid(
            row=1, column=0, sticky="e"
        )
        evento_fecha_fin_label = tk.Label(master, text="Fecha Final").grid(
            row=2, column=0, sticky="e"
        )
        evento_tags_label = tk.Label(master, text="Tags").grid(
            row=3, column=0, sticky="e"
        )

        # entrys evento
        self.evento_descrip_entry = tk.Entry(
            master,
            width=40,
        )
        self.evento_fecha_inicio_entry = tk.Entry(master, width=10)
        self.evento_fecha_fin_entry = tk.Entry(master, width=10)
        self.evento_tags_entry = tk.Entry(master, width=40)

        self.evento_descrip_entry.grid(row=0, column=1, sticky="w")
        self.evento_fecha_inicio_entry.grid(row=1, column=1, sticky="w")
        self.evento_fecha_fin_entry.grid(row=2, column=1, sticky="w")
        self.evento_tags_entry.grid(row=3, column=1, sticky="w")

        # Rellenar si vienen datos iniciales (para editar)
        self.evento_descrip_entry.insert(0, self.initial_data["descrip"])
        self.evento_fecha_inicio_entry.insert(0, self.initial_data["fecini"])
        self.evento_fecha_fin_entry.insert(0, self.initial_data["fecfin"])
        self.evento_tags_entry.insert(0, self.initial_data["tag"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.evento_descrip_entry

    def validate(self):
        # Validar campos no vacíos
        fecfin = self.evento_fecha_fin_entry.get().strip()
        evento = self.evento_descrip_entry.get().strip()
        fecini = self.evento_fecha_inicio_entry.get().strip()
        if not fecfin:
            fecfin = self.evento_fecha_inicio_entry.get()
        tags = self.evento_tags_entry.get().strip()
        if (
            not evento
            or not util.valida_fecha(fecini)
            or not util.valida_fecha(fecfin)
            or not tags
        ):
            messagebox.showwarning(
                "Campos vacíos", "Todos los campos son obligatorios."
            )
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        fecfin = self.evento_fecha_fin_entry.get().strip()
        if not fecfin:
            fecfin = self.evento_fecha_inicio_entry.get().strip()
        self.result = {
            "evento": self.evento_descrip_entry.get().strip(),
            "fecini": util.fecha_a_bd(self.evento_fecha_inicio_entry.get().strip()),
            "fecfin": util.fecha_a_bd(fecfin),
            "tags": self.evento_tags_entry.get().strip(),
        }
