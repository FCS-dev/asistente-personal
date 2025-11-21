import tkinter as tk
from tkinter import messagebox as msj
import persistencia as persist
import tareas as task
import notas as note
import eventos as event
import utiles as util


class Handler:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")
        self.bd = persist.Persistencia()
        self.bd.crea_tablas()

        # Frame izq c/Listbox para mostrar pdtes
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.listbox_tareas = tk.Listbox(
            left_frame, width=100, height=10, font=("Courier New", 10)
        )
        self.listbox_tareas.pack(fill=tk.BOTH, expand=True)

        # buttons
        btn_nuevo_tarea = tk.Button(
            root, text="Nueva Tarea", command=self.nueva_tarea, width=20
        )
        btn_nuevo_nota = tk.Button(
            root, text="Nueva Nota", command=self.nueva_nota, width=20
        )
        btn_nuevo_evento = tk.Button(
            root, text="Nuevo Evento", command=self.nuevo_evento, width=20
        )
        btn_nuevo_tarea.pack(pady=10, padx=10)
        btn_nuevo_nota.pack(pady=10, padx=10)
        btn_nuevo_evento.pack(pady=10, padx=10)

        # # --- Menú ---
        # menu_bar = Menu(root)
        # file_menu = Menu(menu_bar, tearoff=0)
        # file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        # file_menu.add_separator()
        # file_menu.add_command(label="Salir", command=self.on_closing)
        # menu_bar.add_cascade(label="Archivo", menu=file_menu)
        # root.config(menu=menu_bar)

        # Cargar contactos de la base de datos
        self.carga_tareas_pendientes()
        self.listbox_tareas.bind("<Double-Button-1>", self.doble_click)

        # Control de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def doble_click(self, event):
        lb = event.widget
        try:
            index = lb.curselection()[0]
            if index not in self.id_map:
                return  # fila de título u otra no válida
            id_real = self.id_map.get(index)  # recuperamos el ID interno
            self.editar_tarea(id_real)
        except IndexError:
            pass

    def nueva_tarea(self):
        dialog = task.VentanaTarea(self.root)
        if dialog.result:
            tarea = dialog.result["tarea"]
            fecha = dialog.result["fecha"]
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            self.bd.guarda_nueva_tarea(tarea, fecha, prioridad, tags)
            self.carga_tareas_pendientes()

    def nueva_nota(self):
        dialog = note.VentanaTarea(self.root)
        if dialog.result:
            nota = dialog.result["nota"]
            tags = dialog.result["tags"]
            self.bd.guardar_nueva_nota(nota, tags)

    def nuevo_evento(self):
        dialog = event.VentanaTarea(self.root)
        if dialog.result:
            evento = dialog.result["evento"]
            fecini = dialog.result["fecini"]
            fecfin = dialog.result["fecfin"]
            tags = dialog.result["tags"]
            self.bd.guardar_nuevo_evento(evento, fecini, fecfin, tags)

    def carga_tareas_pendientes(self):
        self.tareas = self.bd.trae_tareas()
        self.actualiza_listbox_tareas()

    def editar_tarea(self, id_tarea):
        fila = self.bd.trae_una_tarea(id_tarea)
        if not fila:
            msj.showerror("Error", "NO se encontro el ID de la tarea a modificar")
            return
        dialog = task.VentanaTarea(
            self.root,
            title="Editar Tarea",
            initial_data={
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
            # print(fecha)
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            id = id_tarea
            self.bd.guardar_tarea(id, tarea, fecha, prioridad, tags)
            self.carga_tareas_pendientes()

    def actualiza_listbox_tareas(self):
        self.listbox_tareas.delete(0, tk.END)
        self.id_map = {}
        if self.tareas:
            self.listbox_tareas.insert(tk.END, "TAREAS")
            offset = 1  # las tareas empiezan desde índice 1
        for i, row in enumerate(self.tareas):
            _id, tarea_descrip, fecha, prioridad, estado, tags = row
            text = f"{tarea_descrip[:35]:<35} | {util.bd_a_fecha(fecha)} | {prioridad:>6} | {estado:<11} | {tags[:20]:>15}"
            self.listbox_tareas.insert(tk.END, text)
            self.id_map[i + offset] = _id  # guardamos el ID

    def on_closing(self):
        self.bd.cerrar_conexion()
        self.root.destroy()
