import os
import bcrypt
import sqlite3


class Persistencia:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB = os.path.join(BASE_DIR, "passistant.db")
        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()

    def crea_tablas(self):
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
                    estado TEXT DEFAULT 'Pendiente',         
                    tags TEXT   
                )""")
        # fecha TEXT,          -- YYYY-MM-DD
        # prioridad TEXT,      -- 'Normal' y 'Alta'
        # estado TEXT,         -- 'Pendiente', 'En progreso', 'Completada','Archivada'
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

    def trae_tareas(self):
        self.cursor.execute("SELECT * FROM tareas ORDER BY fecha DESC")
        tareas = self.cursor.fetchall()
        return tareas

    def trae_una_tarea(self, id):
        self.cursor.execute("SELECT * FROM tareas WHERE id=?", (id,))
        tarea = self.cursor.fetchone()
        return tarea

    def guarda_nueva_tarea(self, tarea, fecha, prioridad, tags):
        self.cursor.execute(
            "INSERT INTO tareas (tarea_descrip,fecha, prioridad,tags) VALUES (?, ?, ?,?)",
            (tarea, fecha, prioridad, tags),
        )
        self.conn.commit()

    def guardar_tarea(self, id_tarea, tarea, fecha, prioridad, tags):
        self.cursor.execute(
            "UPDATE tareas SET tarea_descrip=?,fecha=?, prioridad=?, tags=? WHERE id=?",
            (
                tarea,
                fecha,
                prioridad,
                tags,
                id_tarea,
            ),
        )
        self.conn.commit()

    def guardar_nueva_nota(self, nota, tags):
        self.cursor.execute(
            "INSERT INTO notas (nota_descrip,tags) VALUES (?, ?)",
            (
                nota,
                tags,
            ),
        )
        self.conn.commit()

    def guardar_nuevo_evento(self, evento, fecini, fecfin, tags):
        self.cursor.execute(
            "INSERT INTO eventos (evento_descrip,fecha_inicio,fecha_fin,tags) VALUES (?, ?, ?, ?)",
            (
                evento,
                fecini,
                fecfin,
                tags,
            ),
        )
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()
