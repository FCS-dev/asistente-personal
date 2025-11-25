import views.eventos_ui as event
from tkinter import messagebox as msj
import utils.utiles as util

"""
'Eventos'
Clase encargada de gestionar los user_events corespondientes.
Métodos:
traer_eventos() -> Trae los 'eventos' de la BD
nuevo_evento() -> Controla el flujo para el registro de nuevos 'eventos'
eliminar_evento() -> Controla el flujo para la eliminación de 'eventos'
editar_evento() -> Controla el flujo para la edición de 'eventos'
"""


class ControllerEventos:
    def __init__(self, bd, ui):
        self.bd = bd
        self.ui = ui

    def traer_eventos(self):
        return self.bd.trae_eventos()

    def nuevo_evento(self):
        dialog = event.VentanaEvento(self.ui.root)
        if dialog.result:
            evento = dialog.result["evento"]
            fecini = dialog.result["fecini"]
            fecfin = dialog.result["fecfin"]
            tags = dialog.result["tags"]
            self.bd.guardar_nuevo_evento(evento, fecini, fecfin, tags)
            self.ui.carga_eventos()

    def eliminar_evento(self):
        selection = self.ui.listbox_eventos.curselection()
        try:
            if selection[0] not in self.ui.id_map_e:
                msj.showerror("Error", "No seleccionaste un evento válido")
                return  # fila de título u otra no válida
            id_real = self.ui.id_map_e.get(selection[0])  # ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste un evento válido")
            return
        if msj.askokcancel(
            "Confirmación", "¿Seguro de eliminar el evento seleccionado?"
        ):
            self.bd.eliminar_evento(id_real)
            self.ui.carga_eventos()

    def editar_evento(self, id_evento):
        fila = self.bd.trae_un_evento(id_evento)
        if not fila:
            msj.showerror("Error", "No se encontro el ID del evento a modificar")
            return
        dialog = event.VentanaEvento(
            self.ui.root,
            title="Editar Evento",
            initial_data={
                "id": fila[0],
                "descrip": fila[1],
                "fecini": util.bd_a_fecha(fila[2]),
                "fecfin": util.bd_a_fecha(fila[3]),
                "tag": fila[4],
            },
        )
        if dialog.result:
            descrip = dialog.result["evento"]
            fecini = dialog.result["fecini"]
            fecfin = dialog.result["fecfin"]
            tags = dialog.result["tags"]
            id = id_evento
            self.bd.guardar_evento(id, descrip, fecini, fecfin, tags)
            self.ui.carga_eventos()
