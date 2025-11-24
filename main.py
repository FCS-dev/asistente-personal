import tkinter as tk
import main_ui as ui
from controller_tareas import ControllerTareas
from controller_eventos import ControllerEventos
from controller_notas import ControllerNotas
import persistencia as persist

if __name__ == "__main__":
    root = tk.Tk()

    bd = persist.Persistencia()
    bd.crea_tablas()

    app_ui = ui.HandlerUI(root)

    ctrl_tareas = ControllerTareas(bd, app_ui)
    ctrl_eventos = ControllerEventos(bd, app_ui)
    ctrl_notas = ControllerNotas(bd, app_ui)

    app_ui.set_controladores(ctrl_tareas, ctrl_eventos, ctrl_notas)
    app_ui.carga_tareas()
    app_ui.carga_eventos()
    app_ui.carga_notas()
    root.mainloop()
