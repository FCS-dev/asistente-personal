import views.tareas_ui as task
from tkinter import messagebox as msj
import utils.utiles as util

"""
'Tareas'
Clase encargada de gestionar los user_events corespondientes.
Métodos:
traer_tareas() -> Trae las 'tareas' de la BD
nueva_tarea() -> Controla el flujo para el registro de nuevas 'tareas'
cambiar_estado_tarea() -> Controla el flujo para modificar el estado de las 'tareas'
eliminar_tarea() -> Controla el flujo para la eliminación de 'tareas'
editar_tarea() -> Controla el flujo para la edición de 'tareas'
"""


class ControllerTareas:
    def __init__(self, bd, ui):
        self.bd = bd
        self.ui = ui

    def traer_tareas(self):
        return self.bd.trae_tareas()

    def nueva_tarea(self):
        dialog = task.VentanaTarea(self.ui.root)
        if dialog.result:
            tarea = dialog.result["tarea"]
            fecha = dialog.result["fecha"]
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            self.bd.guarda_nueva_tarea(tarea, fecha, prioridad, tags)
            self.ui.carga_tareas()

    def cambiar_estado_tarea(self):
        selection = self.ui.listbox_tareas.curselection()
        try:
            if selection[0] not in self.ui.id_map_t:
                msj.showerror("Error", "No seleccionaste una tarea válida")
                return  # fila de título u otra no válida
            id_real = self.ui.id_map_t.get(selection[0])  # ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una tarea válida")
            return
        fila = self.bd.trae_una_tarea(id_real)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la tarea a modificar")
            return
        dialog = util.VentanaEstados(
            self.ui.root,
            title="Cambiar Estado",
            initial_data={
                "tipo": "tarea",
                "id": fila[0],
                "tarea": fila[1],
                "fecha": util.bd_a_fecha(fila[2]),
                "prioridad": fila[3],
                "estado": fila[4],
                "tag": fila[5],
            },
        )
        if dialog.result:
            estado = dialog.result["estado"]
            id = id_real
            self.bd.cambiar_estado_tarea(id, estado)
            self.ui.carga_tareas()

    def eliminar_tarea(self):
        selection = self.ui.listbox_tareas.curselection()
        try:
            if selection[0] not in self.ui.id_map_t:
                msj.showerror("Error", "No seleccionaste una tarea válida")
                return  # fila de título u otra no válida
            id_real = self.ui.id_map_t.get(selection[0])  # ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una tarea válida")
            return
        if msj.askokcancel(
            "Confirmación", "¿Seguro de eliminar la tarea seleccionada?"
        ):
            self.bd.eliminar_tarea(id_real)
            self.ui.carga_tareas()

    def editar_tarea(self, id_tarea):
        fila = self.bd.trae_una_tarea(id_tarea)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la tarea a modificar")
            return
        dialog = task.VentanaTarea(
            self.ui.root,
            title="Editar Tarea",
            initial_data={
                "id": fila[0],
                "descrip": fila[1],
                "fecha": util.bd_a_fecha(fila[2]),
                "prioridad": fila[3],
                "estado": fila[4],
                "tag": fila[5],
            },
        )
        if dialog.result:
            tarea = dialog.result["tarea"]
            fecha = dialog.result["fecha"]
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            id = id_tarea
            self.bd.guardar_tarea(id, tarea, fecha, prioridad, tags)
            self.ui.carga_tareas()
