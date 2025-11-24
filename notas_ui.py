import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as msj
import persistencia as bd
import utiles as util


class VentanaNota(simpledialog.Dialog):
    def __init__(self, parent, title="Notas", initial_data=None):
        self.initial_data = initial_data or {
            "descrip": "",
            "tag": "",
        }
        super().__init__(parent, title)

    def body(self, master):
        # labels nota
        tk.Label(master, text="Nota").grid(row=0, column=0, sticky="ne")
        tk.Label(master, text="Tags").grid(row=1, column=0, sticky="e")

        # entrys nota (tags mediante diálogo)
        self.nota_descrip_text = tk.Text(
            master, width=50, height=8, wrap="word", font=("Courier New", 10)
        )
        self.nota_tags_entry = None

        self.nota_descrip_text.grid(row=0, column=1, sticky="w")
        # botón para definir tags y label preview
        btn_tags = tk.Button(
            master, text="Definir Tags", command=self.mostrar_tags, width=20
        )
        btn_tags.grid(row=1, column=1, sticky="w")
        self.tags_preview_label = tk.Label(
            master,
            text="Seleccionados: " + (self.initial_data.get("tag") or "(ninguno)"),
            wraplength=300,
            justify="left",
        )
        self.tags_preview_label.grid(row=2, column=1, sticky="w")
        self.tags_seleccionados = self.initial_data.get("tag") or ""

        # Rellenar si vienen datos iniciales (para editar)
        # Para `Text` el índice inicial es "1.0"
        self.nota_descrip_text.insert("1.0", self.initial_data["descrip"])
        # self.nota_tags_entry no se usa; mantenemos tags en self.tags_seleccionados

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.nota_descrip_text

    def validate(self):
        nota = self.nota_descrip_text.get("1.0", "end-1c").strip()
        if not nota:
            msj.showwarning("Validación", "Debe ingresar un texto para la nota")
            return False
        return True

    def apply(self):
        # Guardar datos en resultado
        self.result = {
            "nota": self.nota_descrip_text.get("1.0", "end-1c").strip(),
            "tags": getattr(self, "tags_seleccionados", ""),
        }

    def mostrar_tags(self):
        datos = bd.Persistencia()
        filas = datos.todos_los_tags("Notas")
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
