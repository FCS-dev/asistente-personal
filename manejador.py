import sqlite3, os, bcrypt
import tkinter as tk
from tkinter import messagebox as msj
import tareas as task
import notas as note
import eventos as event


class Principal:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB = os.path.join(BASE_DIR, "passistant.db")

        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()
        self.create_tables()

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
        btn_nuevo_tarea.pack(pady=5)
        btn_nuevo_nota.pack(pady=5)
        btn_nuevo_evento.pack(pady=5)

        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        btn_cualquiera = tk.Button(
            left_frame, text="xxx", command=self.nueva_tarea, width=20
        )
        btn_cualquiera.pack(pady=5)
        # # Frame derecho con Listbox para mostrar contactos
        # right_frame = tk.Frame(root)
        # right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # self.listbox = tk.Listbox(right_frame, width=50, height=20)
        # self.listbox.pack(fill=tk.BOTH, expand=True)

        # # --- Menú ---
        # menu_bar = Menu(root)
        # file_menu = Menu(menu_bar, tearoff=0)
        # file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        # file_menu.add_separator()
        # file_menu.add_command(label="Salir", command=self.on_closing)
        # menu_bar.add_cascade(label="Archivo", menu=file_menu)
        # root.config(menu=menu_bar)

        # Cargar contactos de la base de datos
        # self.load_contacts()

        # Control de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
                prioridad TEXT,      
                estado TEXT DEFAULT 'pendiente',         
                tags TEXT   
            )""")
        # fecha TEXT,          -- YYYY-MM-DD
        # prioridad TEXT,      -- 'baja', 'media', 'alta'
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

    # -------------------------------
    # Cargar contactos desde DB
    # -------------------------------
    # def load_contacts(self):
    # self.cursor.execute("SELECT * FROM contactos")
    # self.contacts = (
    #     self.cursor.fetchall()
    # )  # lista de tuplas (id, nombre, email, telefono)
    # self.update_listbox()  # actualizar la interfaz

    # -------------------------------
    # CRUD: Añadir contacto
    # -------------------------------
    # def add_contact(self):
    # dialog = ContactDialog(self.root)  # abrir diálogo
    # if dialog.result:  # si el usuario pulsa aceptar
    #     self.cursor.execute(
    #         "INSERT INTO contactos (nombre, email, telefono) VALUES (?, ?, ?)",
    #         (dialog.result["name"], dialog.result["email"], dialog.result["phone"]),
    #     )
    #     self.conn.commit()  # guardar cambios
    #     self.load_contacts()  # actualizar interfaz

    # -------------------------------
    # CRUD: Editar contacto
    # -------------------------------
    # def edit_contact(self):
    # selection = self.listbox.curselection()
    # if not selection:
    #     messagebox.showwarning("Advertencia", "Selecciona un contacto para editar.")
    #     return

    # index = selection[0]
    # contact_id, nombre, email, telefono = self.contacts[index]

    # # abrir diálogo
    # dialog = ContactDialog(
    #     self.root,
    #     title="Editar Contacto",
    #     initial_data={"name": nombre, "email": email, "phone": telefono},
    # )

    # if dialog.result:
    #     self.cursor.execute(
    #         """
    #         UPDATE contactos SET nombre=?, email=?, telefono=? WHERE id=?
    #     """,
    #         (
    #             dialog.result["name"],
    #             dialog.result["email"],
    #             dialog.result["phone"],
    #             contact_id,
    #         ),
    #     )
    #     self.conn.commit()
    #     self.load_contacts()

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

    # -------------------------------
    # INTERFAZ: actualizar Listbox
    # -------------------------------

    # Mostrar contactos en el Listbox
    # def update_listbox(self):
    # self.listbox.delete(0, tk.END)
    # for row in self.contacts:
    #     _id, nombre, email, telefono = row
    #     text = f"Nombre: {nombre} | Email: {email} | Teléfono: {telefono}"
    #     self.listbox.insert(tk.END, text)

    # -------------------------------
    # EXPORTAR CONTACTOS A PDF
    # -------------------------------
    # def export_to_pdf(self):
    #     if not self.contacts:
    #         messagebox.showwarning("Sin datos", "No hay contactos para exportar.")
    #         return

    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)

    #     # Desempaquetamos tuplas directamente
    #     for _, nombre, email, telefono in self.contacts:
    #         text = f"Nombre: {nombre} | Email: {email} | Teléfono: {telefono}"
    #         pdf.multi_cell(0, 8, text)  # multi_cell permite saltos de línea automáticos

    #     pdf_file = "contacts.pdf"
    #     try:
    #         pdf.output(pdf_file)  # guardamos PDF
    #         messagebox.showinfo(
    #             "PDF Exportado", f"Los contactos se han exportado como {pdf_file}"
    #         )
    #     except Exception as e:
    #         messagebox.showerror(
    #             "Error al exportar PDF", f"No se pudo guardar el PDF:\n{e}"
    #         )

    # -------------------------------
    # CERRAR APLICACIÓN
    # -------------------------------
    def on_closing(self):
        self.conn.close()  # cerramos conexión a la base de datos
        self.root.destroy()  # cerramos ventana
