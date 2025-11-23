import tkinter as tk
from tkinter import simpledialog, messagebox


class VentanaNota(simpledialog.Dialog):
    def __init__(self, parent, title="Notas", initial_data=None):
        self.initial_data = initial_data or {
            "descrip": "",
            "tag": "",
        }
        super().__init__(parent, title)

    def body(self, master):
        # labels nota
        nota_descrip_label = tk.Label(master, text="Nota").grid(
            row=0, column=0, sticky="e"
        )
        nota_tags_label = tk.Label(master, text="Tags").grid(
            row=1, column=0, sticky="e"
        )

        # entrys nota
        self.nota_descrip_entry = tk.Entry(
            master,
            width=40,
        )
        self.nota_tags_entry = tk.Entry(master, width=40)

        self.nota_descrip_entry.grid(row=0, column=1, sticky="w")
        self.nota_tags_entry.grid(row=1, column=1, sticky="w")

        # Rellenar si vienen datos iniciales (para editar)
        self.nota_descrip_entry.insert(0, self.initial_data["descrip"])
        self.nota_tags_entry.insert(0, self.initial_data["tag"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.nota_descrip_entry

    def validate(self):
        # Validar campos no vacíos
        nota = self.nota_descrip_entry.get().strip()
        tags = self.nota_tags_entry.get().strip()

        if not nota or not tags:
            messagebox.showwarning(
                "Campos vacíos", "Todos los campos son obligatorios."
            )
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "nota": self.nota_descrip_entry.get().strip(),
            "tags": self.nota_tags_entry.get().strip(),
        }
