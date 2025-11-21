import sqlite3, os, bcrypt
import tkinter as tk
from tkinter import messagebox as msj
import tareas as task
import notas as note
import eventos as event


class Handler:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")
        ########
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB = os.path.join(BASE_DIR, "passistant.db")

        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()
        self.create_tables()
        ########
        # Frame izq c/Listbox para mostrar pdtes
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.listbox_tareas = tk.Listbox(
            left_frame, width=80, height=10, font=("Courier New", 10)
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

    ########
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                tipo TEXT NOT NULL DEFAULT 'USER',
                fecha_creacion TEXT DEFAULT (DATE('now','localtime'))
            )""")
        # 'tipo' por defecto 'USER'.
        #  Valores posibles: 'USER', 'ADMIN'
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        cantidad_usuarios = self.cursor.fetchone()[0]
        if cantidad_usuarios == 0:
            password = "abc123"
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.cursor.execute(
                "INSERT INTO usuarios (usuario,password_hash,tipo) VALUES (?,?,?)",
                ("Administrador", hashed, "ADMIN"),
            )
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea_descrip TEXT NOT NULL,
                fecha TEXT,          
                prioridad TEXT DEFAULT 'Normal',      
                estado TEXT DEFAULT 'pendiente',         
                tags TEXT   
            )""")
        # fecha TEXT,          -- YYYY-MM-DD
        # prioridad TEXT,      -- 'Normal' y 'Alta'
        # estado TEXT,         -- 'pendiente', 'en_progreso', 'completada'
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nota_descrip TEXT NOT NULL,
                fecha_creacion TEXT DEFAULT (DATE('now','localtime')),
                tags TEXT
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento_descrip TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,    
                fecha_fin TEXT,                
                tags TEXT
            )""")
        # fecha_inicio TEXT NOT NULL,     -- YYYY-MM-DD
        # fecha_fin TEXT,                 -- si no hay, usar misma fecha_inicio
        self.conn.commit()

    ######
    #### xCAMBIAR contenido: persistencia.guardar_nueva_tarea(!!!!
    def nueva_tarea(self):
        dialog = task.VentanaTarea(self.root)
        if dialog.result:  # si el usuario pulsa aceptar
            self.cursor.execute(
                "INSERT INTO tareas (tarea_descrip,fecha, prioridad,tags) VALUES (?, ?, ?,?)",
                (
                    dialog.result["tarea"],
                    dialog.result["fecha"],
                    dialog.result["prioridad"],
                    dialog.result["tags"],
                ),
            )
            self.conn.commit()
            self.carga_tareas_pendientes()  # actualizar interfaz

    #### xCAMBIAR contenido: persistencia.guardar_nueva_nota(!!!!
    def nueva_nota(self):
        dialog = note.VentanaTarea(self.root)
        if dialog.result:
            self.cursor.execute(
                "INSERT INTO notas (nota_descrip,tags) VALUES (?, ?)",
                (
                    dialog.result["nota"],
                    dialog.result["tags"],
                ),
            )
            self.conn.commit()

    #### xCAMBIAR contenido: persistencia.guardar_nuevo_evento(!!!!
    def nuevo_evento(self):
        dialog = event.VentanaTarea(self.root)
        if dialog.result:
            self.cursor.execute(
                "INSERT INTO eventos (evento_descrip,fecha_inicio,fecha_fin,tags) VALUES (?, ?, ?, ?)",
                (
                    dialog.result["evento"],
                    dialog.result["fecini"],
                    dialog.result["fecfin"],
                    dialog.result["tags"],
                ),
            )
            self.conn.commit()

    #### xCAMBIAR contenido: persistencia.trae_tareas(!!!!
    def carga_tareas_pendientes(self):
        self.cursor.execute("SELECT * FROM tareas ORDER BY fecha DESC")
        self.tareas = self.cursor.fetchall()
        self.actualiza_listbox_tareas()  # actualizar la interfaz

    #### xCAMBIAR contenido: persistencia.guardar_tarea(... generar traer_1_tarea!!!!
    def editar_tarea(self, id_tarea):
        self.cursor.execute("SELECT * FROM tareas WHERE id=?", (id_tarea,))
        fila = self.cursor.fetchone()
        if not fila:
            msj.showerror("Error", "NO se encontro el ID de la tarea a modificar")
            return
        dialog = task.VentanaTarea(
            self.root,
            title="Editar Tarea",
            initial_data={
                "descrip": fila[1],
                "fecha": fila[2],
                "prioridad": fila[3],
                "tag": fila[4],
            },
        )
        if dialog.result:
            self.cursor.execute(
                "UPDATE tareas SET tarea_descrip=?,fecha=?, prioridad=?, tags=? WHERE id=?",
                (
                    dialog.result["tarea"],
                    dialog.result["fecha"],
                    dialog.result["prioridad"],
                    dialog.result["tags"],
                    id_tarea,
                ),
            )
            self.conn.commit()
            self.carga_tareas_pendientes()

    # -------------------------------
    # CRUD: Borrar contacto
    # -------------------------------
    # def delete_contact(self):
    #     selection = self.listbox.curselection()
    #     if not selection:
    #         messagebox.showwarning("Advertencia", "Selecciona un contacto para borrar.")
    #         return

    #     index = selection[0]
    #     contact_id = self.contacts[index][0]  # obtenemos id del contacto

    #     self.cursor.execute("DELETE FROM contactos WHERE id=?", (contact_id,))
    #     self.conn.commit()
    #     self.load_contacts()

    def actualiza_listbox_tareas(self):
        self.listbox_tareas.delete(0, tk.END)
        self.id_map = {}
        if self.tareas:
            self.listbox_tareas.insert(tk.END, "TAREAS")
            offset = 1  # las tareas empiezan desde índice 1
        for i, row in enumerate(self.tareas):
            _id, tarea_descrip, fecha, prioridad, estado, tags = row
            text = f"{tarea_descrip[:35]:<35} | {fecha} | {prioridad} | {estado:<11} | {tags}"
            self.listbox_tareas.insert(tk.END, text)
            self.id_map[i + offset] = _id  # guardamos el ID

    def on_closing(self):
        self.conn.close()  # cerramos conexión a la base de datos
        self.root.destroy()  # cerramos ventana
