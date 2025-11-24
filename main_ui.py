import tkinter as tk
from tkinter import messagebox as msj
from tkinter import filedialog

import persistencia as persist
import utiles as util


class HandlerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-Asistente Personal - P.F. Python 2025 (Franco Calderón)")
        self.bd = persist.Persistencia()

        # Menú
        menu_bar = tk.Menu(root)
        user_menu = tk.Menu(menu_bar, tearoff=0)
        user_menu.add_command(label="Exportar a PDF", command=self.exportar_pdf_user)
        user_menu.add_command(label="Exportar JSON", command=self.exportar_json_user)
        user_menu.add_command(
            label="Generar Gráficos", command=self.generar_graficos_user
        )
        ##user_menu.add_separator()
        adm_menu = tk.Menu(menu_bar, tearoff=0)
        adm_menu.add_command(label="Borrar info BD", command=self.borrar_info_bd_adm)
        adm_menu.add_command(label="Cambiar contraseña", command=self.cambiar_clave_adm)

        menu_bar.add_cascade(label="Usuario", menu=user_menu)
        menu_bar.add_cascade(label="Administrador", menu=adm_menu)
        menu_bar.add_command(label="Salir", command=self.on_closing)
        root.config(menu=menu_bar)

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
            botones_frame_tarea,
            text="Nueva Tarea",
            command=lambda: self.ctrl_t.nueva_tarea(),
            width=20,
        )
        btn_cambiar_estado_tarea = tk.Button(
            botones_frame_tarea,
            text="Cambiar Estado",
            command=lambda: self.ctrl_t.cambiar_estado_tarea(),
            width=20,
        )
        btn_eliminar_tarea = tk.Button(
            botones_frame_tarea,
            text="Eliminar Tarea",
            command=lambda: self.ctrl_t.eliminar_tarea(),
            width=20,
        )
        btn_nuevo_evento = tk.Button(
            botones_frame_evento,
            text="Nuevo Evento",
            command=lambda: self.ctrl_e.nuevo_evento(),
            width=20,
        )
        btn_eliminar_evento = tk.Button(
            botones_frame_evento,
            text="Eliminar Evento",
            command=lambda: self.ctrl_e.eliminar_evento(),
            width=20,
        )
        btn_nuevo_nota = tk.Button(
            botones_frame_nota,
            text="Nueva Nota",
            command=lambda: self.ctrl_n.nueva_nota(),
            width=20,
        )
        btn_eliminar_nota = tk.Button(
            botones_frame_nota,
            text="Eliminar Nota",
            command=lambda: self.ctrl_n.eliminar_nota(),
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

        # declarando evento dobleclick
        self.listbox_tareas.bind("<Double-Button-1>", self.doble_click_tarea)
        self.listbox_eventos.bind("<Double-Button-1>", self.doble_click_evento)
        self.listbox_notas.bind("<Double-Button-1>", self.doble_click_nota)
        # Control de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_controladores(self, ctrl_t, ctrl_e, ctrl_n):
        self.ctrl_t = ctrl_t
        self.ctrl_e = ctrl_e
        self.ctrl_n = ctrl_n

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
        self.ctrl_t.editar_tarea(id_real)

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
        self.ctrl_e.editar_evento(id_real)

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
        self.ctrl_n.editar_nota(id_real)

    def carga_tareas(self):
        self.tareas = self.ctrl_t.traer_tareas()
        self.actualiza_listbox_tareas()

    def carga_eventos(self):
        self.eventos = self.ctrl_e.traer_eventos()
        self.actualiza_listbox_eventos()

    def carga_notas(self):
        self.notas = self.ctrl_n.traer_notas()
        self.actualiza_listbox_notas()

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

    def actualiza_listbox_eventos(self):
        import datetime as dt

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

    def exportar_pdf_user(self):
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("Archivo PDF", "*.pdf")]
        )
        if not ruta_archivo:
            return
        if util.generar_pdf(ruta_archivo):
            msj.showinfo("Confirmación", "El archivo .PDF fue generado correctamente")
        else:
            msj.showwarning(
                "Aviso",
                "El archivo .PDF no pudo ser generado. Contacte con el Administrador del sistema",
            )

    def exportar_json_user(self):
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("Archivo de texto", "*.json")]
        )
        if not ruta_archivo:
            return
        if util.generar_json(ruta_archivo):
            msj.showinfo("Confirmación", "El archivo .JSON fue generado correctamente")
        else:
            msj.showwarning(
                "Aviso",
                "El archivo .JSON no pudo ser generado. Contacte con el Administrador del sistema",
            )

    def generar_graficos_user(self):
        pass

    def cambiar_clave_adm(self):
        if util.actualizar_clave_adm(self.root, self.bd.cambiar_clave):
            msj.showinfo("Aviso", "Se actualizó la clave del administrador con éxito")
        else:
            msj.showwarning(
                "Aviso",
                "No se pudo actualizar la clave del administrador, datos inválidos",
            )

    def borrar_info_bd_adm(self):
        if util.borrar_info(self.root, self.bd.eliminar_data):
            msj.showinfo(
                "Aviso", "Se ha eliminado toda la información registrada de la BD"
            )
        else:
            msj.showwarning(
                "Aviso",
                "No se pudo eliminar la información de la BD, Contacte con el admnistrador",
            )
        self.carga_tareas()
        self.carga_eventos()
        self.carga_notas()

    def on_closing(self):
        self.bd.cerrar_conexion()
        self.root.destroy()
