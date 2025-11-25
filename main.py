import tkinter as tk
import views.main_ui as ui
from controllers.controller_tareas import ControllerTareas
from controllers.controller_eventos import ControllerEventos
from controllers.controller_notas import ControllerNotas
import repository.persistencia as persist

# Programa principal
if __name__ == "__main__":
    root = tk.Tk()

    # Instancia para la gestion con BD
    bd = persist.Persistencia()
    bd.crea_tablas()  # Crea la BD y las tablas necesarias si no existen

    # Instancia para la gestion de la UI principal
    app_ui = ui.HandlerUI(root)

    # Instancias de controladores de cada tipo de actividad gestionada
    ctrl_tareas = ControllerTareas(bd, app_ui)
    ctrl_eventos = ControllerEventos(bd, app_ui)
    ctrl_notas = ControllerNotas(bd, app_ui)

    app_ui.set_controladores(ctrl_tareas, ctrl_eventos, ctrl_notas)
    app_ui.carga_tareas()
    app_ui.carga_eventos()
    app_ui.carga_notas()
    root.mainloop()
