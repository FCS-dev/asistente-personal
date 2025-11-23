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
        # Frames: Tareas, Eventos, Notas
        tarea_frame = tk.Frame(root)
        evento_frame = tk.Frame(root)
        nota_frame = tk.Frame(root)
        tarea_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        evento_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        nota_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)

        self.listbox_tareas = tk.Listbox(
            tarea_frame, width=100, height=10, font=("Courier New", 10)
        )
        self.listbox_tareas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.listbox_eventos = tk.Listbox(
            evento_frame, width=100, height=10, font=("Courier New", 10)
        )
        self.listbox_eventos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.listbox_notas = tk.Listbox(
            nota_frame, width=100, height=10, font=("Courier New", 10)
        )
        self.listbox_notas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        botones_frame_tarea = tk.Frame(tarea_frame)
        botones_frame_tarea.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        botones_frame_evento = tk.Frame(evento_frame)
        botones_frame_evento.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        botones_frame_nota = tk.Frame(nota_frame)
        botones_frame_nota.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        ####
        # buttons
        btn_nuevo_tarea = tk.Button(
            botones_frame_tarea, text="Nueva Tarea", command=self.nueva_tarea, width=20
        )
        btn_cambiar_estado_tarea = tk.Button(
            botones_frame_tarea,
            text="Cambiar Estado",
            command=self.cambiar_estado_tarea,
            width=20,
        )
        btn_eliminar_tarea = tk.Button(
            botones_frame_tarea,
            text="Eliminar Tarea",
            command=self.eliminar_tarea,
            width=20,
        )
        btn_nuevo_evento = tk.Button(
            botones_frame_evento,
            text="Nuevo Evento",
            command=self.nuevo_evento,
            width=20,
        )
        btn_eliminar_evento = tk.Button(
            botones_frame_evento,
            text="Eliminar Evento",
            command=self.eliminar_evento,
            width=20,
        )
        btn_nuevo_nota = tk.Button(
            botones_frame_nota, text="Nueva Nota", command=self.nueva_nota, width=20
        )
        btn_eliminar_nota = tk.Button(
            botones_frame_nota,
            text="Eliminar Nota",
            command=self.eliminar_nota,
            width=20,
        )
        btn_nuevo_tarea.pack(pady=10, padx=10)
        btn_cambiar_estado_tarea.pack(pady=10, padx=10)
        btn_eliminar_tarea.pack(pady=10, padx=10)
        btn_nuevo_evento.pack(pady=10, padx=10)
        btn_eliminar_evento.pack(pady=10, padx=10)
        btn_nuevo_nota.pack(pady=10, padx=10)
        btn_eliminar_nota.pack(pady=10, padx=10)

        tarea_frame.grid_columnconfigure(0, weight=1)
        tarea_frame.grid_rowconfigure(0, weight=1)
        evento_frame.grid_columnconfigure(0, weight=1)
        evento_frame.grid_rowconfigure(0, weight=1)
        nota_frame.grid_columnconfigure(0, weight=1)
        nota_frame.grid_rowconfigure(0, weight=1)

        # carga de tareas
        self.carga_tareas()
        self.carga_eventos()
        self.carga_notas()
        # declarando evento dobleclick
        self.listbox_tareas.bind("<Double-Button-1>", self.doble_click_tarea)
        self.listbox_eventos.bind("<Double-Button-1>", self.doble_click_evento)
        self.listbox_notas.bind("<Double-Button-1>", self.doble_click_nota)
        # Control de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def doble_click_tarea(self, event):
        lb = event.widget
        try:
            index = lb.curselection()[0]
            if index not in self.id_map_t:
                msj.showerror("Error", "No seleccionaste una tarea válida")
                return  # fila de título u otra no válida
            id_real = self.id_map_t.get(index)  # recuperamos el ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una tarea válida")
            return
        self.editar_tarea(id_real)

    def carga_tareas(self):
        self.tareas = self.bd.trae_tareas()
        self.actualiza_listbox_tareas()

    def nueva_tarea(self):
        dialog = task.VentanaTarea(self.root)
        if dialog.result:
            tarea = dialog.result["tarea"]
            fecha = dialog.result["fecha"]
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            self.bd.guarda_nueva_tarea(tarea, fecha, prioridad, tags)
            self.carga_tareas()

    def cambiar_estado_tarea(self):
        selection = self.listbox_tareas.curselection()
        try:
            if selection[0] not in self.id_map_t:
                msj.showerror("Error", "No seleccionaste una tarea válida")
                return  # fila de título u otra no válida
            id_real = self.id_map_t.get(selection[0])  # recuperamos el ID interno
            # self.editar_tarea(id_real)
        except IndexError:
            msj.showerror("Error", "No seleccionaste una tarea válida")
            return
        fila = self.bd.trae_una_tarea(id_real)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la tarea a modificar")
            return
        dialog = util.VentanaEstados(
            self.root,
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
            self.carga_tareas()

    def eliminar_tarea(self):
        selection = self.listbox_tareas.curselection()
        try:
            if selection[0] not in self.id_map_t:
                msj.showerror("Error", "No seleccionaste una tarea válida")
                return  # fila de título u otra no válida
            id_real = self.id_map_t.get(selection[0])  # recuperamos el ID interno
            # self.editar_tarea(id_real)
        except IndexError:
            msj.showerror("Error", "No seleccionaste una tarea válida")
            return
        if msj.askokcancel(
            "Confirmación", "¿Seguro de eliminar la tarea seleccionada?"
        ):
            self.bd.eliminar_tarea(id_real)
            self.carga_tareas()

    def editar_tarea(self, id_tarea):
        fila = self.bd.trae_una_tarea(id_tarea)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la tarea a modificar")
            return
        dialog = task.VentanaTarea(
            self.root,
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
            # print(fecha)
            prioridad = dialog.result["prioridad"]
            tags = dialog.result["tags"]
            id = id_tarea
            self.bd.guardar_tarea(id, tarea, fecha, prioridad, tags)
            self.carga_tareas()

    def actualiza_listbox_tareas(self):
        self.listbox_tareas.delete(0, tk.END)
        self.id_map_t = {}
        if self.tareas:
            self.listbox_tareas.insert(tk.END, "TAREAS")
            self.listbox_tareas.itemconfig(0, bg="#e0e0e0")
            offset = 1  # las tareas empiezan desde índice 1
        else:
            offset = 0
        for i, row in enumerate(self.tareas):
            _id, tarea_descrip, fecha, prioridad, estado, tags = row
            if estado == "Pendiente":
                simbolo = "•"  # bullet
            elif estado == "En progreso":
                simbolo = "→"  # flecha
            elif estado == "Completada":
                simbolo = "✔"  # check
            elif estado == "Archivada":
                simbolo = "[A]"  # archivado
            else:
                simbolo = "-"  # símbolo genérico
            text = f"{simbolo:>3} {tarea_descrip[:35]:<35} | {util.bd_a_fecha(fecha)} | {prioridad:<6} | {estado:<11} | {tags[:20]:>15}"
            index = self.listbox_tareas.size()  # índice actual antes de insertar
            self.listbox_tareas.insert(tk.END, text)
            # Estableciendo colores por prioridad
            if prioridad == "Alta":
                self.listbox_tareas.itemconfig(index, bg="#ffdddd")  # rosa pastel
            else:
                self.listbox_tareas.itemconfig(index, bg="#ffffff")  # blanco
            self.id_map_t[i + offset] = _id  # guardamos el ID

    def doble_click_evento(self, event):
        lb = event.widget
        try:
            index = lb.curselection()[0]
            if index not in self.id_map_e:
                msj.showerror("Error", "No seleccionaste un evento válido")
                return  # fila de título u otra no válida
            id_real = self.id_map_e.get(index)  # recuperamos el ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una evento válido")
            return
        self.editar_evento(id_real)

    def carga_eventos(self):
        self.eventos = self.bd.trae_eventos()
        self.actualiza_listbox_eventos()

    def nuevo_evento(self):
        dialog = event.VentanaEvento(self.root)
        if dialog.result:
            evento = dialog.result["evento"]
            fecini = dialog.result["fecini"]
            fecfin = dialog.result["fecfin"]
            tags = dialog.result["tags"]
            self.bd.guardar_nuevo_evento(evento, fecini, fecfin, tags)
            self.carga_eventos()

    def eliminar_evento(self):
        selection = self.listbox_eventos.curselection()
        try:
            if selection[0] not in self.id_map_e:
                msj.showerror("Error", "No seleccionaste un evento válido")
                return  # fila de título u otra no válida
            id_real = self.id_map_e.get(selection[0])  # recuperamos el ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste un evento válido")
            return
        if msj.askokcancel(
            "Confirmación", "¿Seguro de eliminar el evento seleccionado?"
        ):
            self.bd.eliminar_evento(id_real)
            self.carga_eventos()

    def editar_evento(self, id_evento):
        fila = self.bd.trae_un_evento(id_evento)
        if not fila:
            msj.showerror("Error", "No se encontro el ID del evento a modificar")
            return
        dialog = event.VentanaEvento(
            self.root,
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
            self.carga_eventos()

    def actualiza_listbox_eventos(self):
        import datetime as dt
        # from datetime import date

        self.listbox_eventos.delete(0, tk.END)
        self.id_map_e = {}
        if self.eventos:
            self.listbox_eventos.insert(tk.END, "EVENTOS")
            self.listbox_eventos.itemconfig(0, bg="#e0e0e0")
            offset = 1  # los evetos empiezan desde índice 1
        else:
            offset = 0
        for i, row in enumerate(self.eventos):
            _id, evento_descrip, fecha_inicio, fecha_fin, tags = row
            text = f"{evento_descrip[:50]:<50} | {util.bd_a_fecha(fecha_inicio)} | {util.bd_a_fecha(fecha_fin)} | {tags[:20]:>15}"
            index = self.listbox_eventos.size()  # índice actual antes de insertar
            self.listbox_eventos.insert(tk.END, text)
            fecha_actual = util.obtener_fecha_actual()
            f1 = dt.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()  # fecha_ini
            f2 = dt.datetime.strptime(fecha_fin, "%Y-%m-%d").date()  # fecha_fin
            if f2 < fecha_actual:  # Evento ya expiró
                color = "#ffdddd"  # rosa
            elif f1 <= fecha_actual <= f2:  # Evento esta en proceso
                color = "#ffffff"  # blanco
            else:  # Evento futuro
                color = "#cff6f6"  # celeste
            self.listbox_eventos.itemconfig(index, bg=color)
            self.id_map_e[i + offset] = _id  # guardamos el ID

    def doble_click_nota(self, event):
        lb = event.widget
        try:
            index = lb.curselection()[0]
            if index not in self.id_map_n:
                msj.showerror("Error", "No seleccionaste una nota válida")
                return  # fila de título u otra no válida
            id_real = self.id_map_n.get(index)  # recuperamos el ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una nota válida")
            return
        self.editar_nota(id_real)

    def carga_notas(self):
        self.notas = self.bd.trae_notas()
        self.actualiza_listbox_notas()

    def nueva_nota(self):
        dialog = note.VentanaNota(self.root)
        if dialog.result:
            nota = dialog.result["nota"]
            tags = dialog.result["tags"]
            self.bd.guardar_nueva_nota(nota, tags)
            self.carga_notas()

    def eliminar_nota(self):
        selection = self.listbox_notas.curselection()
        try:
            if selection[0] not in self.id_map_n:
                msj.showerror("Error", "No seleccionaste una nota válida")
                return  # fila de título u otra no válida
            id_real = self.id_map_n.get(selection[0])  # recuperamos el ID interno
        except IndexError:
            msj.showerror("Error", "No seleccionaste una nota válida")
            return
        if msj.askokcancel("Confirmación", "¿Seguro de eliminar la nota seleccionada?"):
            self.bd.eliminar_nota(id_real)
            self.carga_notas()

    def editar_nota(self, id_nota):
        fila = self.bd.trae_una_nota(id_nota)
        if not fila:
            msj.showerror("Error", "No se encontro el ID de la nota a modificar")
            return
        dialog = note.VentanaNota(
            self.root,
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
            self.carga_notas()

    def actualiza_listbox_notas(self):
        self.listbox_notas.delete(0, tk.END)
        self.id_map_n = {}
        if self.notas:
            self.listbox_notas.insert(tk.END, "NOTAS")
            self.listbox_notas.itemconfig(0, bg="#e0e0e0")
            offset = 1  # las notas empiezan desde índice 1
        else:
            offset = 0
        for i, row in enumerate(self.notas):
            _id, nota_descrip, fecha_creacion, tags = row
            text = f"{nota_descrip[:60]:<60} | {util.bd_a_fecha(fecha_creacion)} | {tags[:20]:>15}"
            self.listbox_notas.insert(tk.END, text)
            # Estableciendo colores por prioridad
            self.id_map_n[i + offset] = _id  # guardamos el ID

    def on_closing(self):
        self.bd.cerrar_conexion()
        self.root.destroy()
