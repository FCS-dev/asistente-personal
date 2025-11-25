import views.notas_ui as note
from tkinter import messagebox as msj

"""
'Notas'
Clase encargada de gestionar los user_events corespondientes.
Métodos:
traer_notas() -> Trae las 'notas' de la BD
nueva_nota() -> Controla el flujo para el registro de nuevas 'notas'
eliminar_nota() -> Controla el flujo para la eliminación de 'notas'
editar_nota() -> Controla el flujo para la edición de 'notas'
"""


class ControllerNotas:
    def __init__(self, bd, ui):
        self.bd = bd
        self.ui = ui

    def traer_notas(self):
        return self.bd.trae_notas()

    def nueva_nota(self):
        dialog = note.VentanaNota(self.ui.root)
        if dialog.result:
            nota = dialog.result["nota"]
            tags = dialog.result["tags"]
            self.bd.guardar_nueva_nota(nota, tags)
            self.ui.carga_notas()

    def eliminar_nota(self):
        selection = self.ui.listbox_notas.curselection()
        try:
            if selection[0] not in self.ui.id_map_n:
                msj.showerror("Error", "No seleccionaste una nota válida")
                return  # fila de título u otra no válida
            id_real = self.ui.id_map_n.get(selection[0])  # ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una nota válida")
            return
        if msj.askokcancel("Confirmación", "¿Seguro de eliminar la nota seleccionada?"):
            self.bd.eliminar_nota(id_real)
            self.ui.carga_notas()

    def editar_nota(self, id_nota):
        fila = self.bd.trae_una_nota(id_nota)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la nota a modificar")
            return
        dialog = note.VentanaNota(
            self.ui.root,
            title="Editar Nota",
            initial_data={
                "id": fila[0],
                "descrip": fila[1],
                "tag": fila[3],
            },
        )
        if dialog.result:
            nota_descrip = dialog.result["nota"]
            tags = dialog.result["tags"]
            id = id_nota
            self.bd.guardar_nota(id, nota_descrip, tags)
            self.ui.carga_notas()
