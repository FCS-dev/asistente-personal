import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as msj
import utils.utiles as util
import repository.persistencia as bd

"""
Clase VentanaEvento()
UI principal de la actividad 'Evento'
"""


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
        tk.Label(master, text="Nombre Evento").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Fecha inicio").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="Fecha Final").grid(row=2, column=0, sticky="e")
        tk.Label(master, text="Tags").grid(row=3, column=0, sticky="e")

        # entrys evento (tags ahora mediante diálogo)
        self.evento_descrip_entry = tk.Entry(
            master,
            width=40,
        )
        self.evento_fecha_inicio_entry = tk.Entry(master, width=10)
        self.evento_fecha_fin_entry = tk.Entry(master, width=10)
        self.evento_tags_entry = None

        self.evento_descrip_entry.grid(row=0, column=1, sticky="w")
        self.evento_fecha_inicio_entry.grid(row=1, column=1, sticky="w")
        self.evento_fecha_fin_entry.grid(row=2, column=1, sticky="w")
        # boton para definir tags y label preview
        btn_tags = tk.Button(
            master, text="Definir Tags", command=self.mostrar_tags, width=20
        )
        btn_tags.grid(row=3, column=1, sticky="w")
        self.tags_preview_label = tk.Label(
            master,
            text="Seleccionados: " + (self.initial_data.get("tag") or "(ninguno)"),
            wraplength=300,
            justify="left",
        )
        self.tags_preview_label.grid(row=4, column=1, sticky="w")
        self.tags_seleccionados = self.initial_data.get("tag") or ""

        # Rellenar si vienen datos iniciales (para editar)
        self.evento_descrip_entry.insert(0, self.initial_data["descrip"])
        self.evento_fecha_inicio_entry.insert(0, self.initial_data["fecini"])
        self.evento_fecha_fin_entry.insert(0, self.initial_data["fecfin"])

        # El campo de nombre recibe el foco al abrir el diálogo
        return self.evento_descrip_entry

    def validate(self):
        fecfin = self.evento_fecha_fin_entry.get().strip()
        evento = self.evento_descrip_entry.get().strip()
        fecini = self.evento_fecha_inicio_entry.get().strip()
        if not fecfin:
            fecfin = self.evento_fecha_inicio_entry.get()
        if not evento:
            msj.showwarning("Validación", "Debe ingresar una descripción para la tarea")
            return False
        if not util.valida_fecha(fecini) or not util.valida_fecha(fecfin):
            msj.showwarning(
                "Validación",
                "Debe ingresar fechas de inicio y final válidas (mínimo: 01/01/2020)",
            )
            return False
        if util.fecha_a_bd(fecini) > util.fecha_a_bd(fecfin):
            msj.showwarning(
                "Validación",
                "La fecha de final debe ser posterior o igual a la fecha de inicio del evento",
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
            "tags": getattr(self, "tags_seleccionados", ""),
        }

    def mostrar_tags(self):
        datos = bd.Persistencia()
        filas = datos.todos_los_tags("Eventos")
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
