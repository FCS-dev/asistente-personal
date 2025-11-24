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
        # tipo: 'USER' (por defecto), 'ADMIN'
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL,
                    tipo TEXT NOT NULL DEFAULT 'USER',
                    fecha_creacion TEXT DEFAULT (DATE('now','localtime'))
                )""")
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        cantidad_usuarios = self.cursor.fetchone()[0]
        if cantidad_usuarios == 0:
            password = "abc123"
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.cursor.execute(
                "INSERT INTO usuarios (usuario,password_hash,tipo) VALUES (?,?,?)",
                ("Administrador", hashed, "ADMIN"),
            )
        # prioridad: 'Normal', 'Alta'
        # estado: 'Pendiente', 'En progreso', 'Completada', 'Archivada'
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarea_descrip TEXT NOT NULL,
                    fecha TEXT,          
                    prioridad TEXT DEFAULT 'Normal',      
                    estado TEXT DEFAULT 'Pendiente',         
                    tags TEXT   
                )""")
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nota_descrip TEXT NOT NULL,
                    fecha_creacion TEXT DEFAULT (DATE('now','localtime')),
                    tags TEXT
                )""")
        # fecha_fin: si no se especifica, debe ser la misma que fecha_inicio
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    evento_descrip TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL,    
                    fecha_fin TEXT,                
                    tags TEXT
                )""")
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    tag_descrip TEXT NOT NULL
                )""")
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM tags")
        # Solo se crearan los tags si la bd fue recreada
        if self.cursor.fetchone()[0] == 0:
            tags_tareas = [
                "Personal",
                "Trabajo",
                "Salud",
                "Finanzas",
                "Hogar",
                "Estudios",
                "Urgente",
                "Ideas",
                "Proyectos",
            ]
            tags_eventos = [
                "Reunión",
                "Cumpleaños",
                "Cita médica",
                "Viaje",
                "Plazo administrativo",
                "Recordatorio",
            ]
            tags_notas = [
                "Idea",
                "Apunte",
                "Información general",
                "Investigación",
                "Enlace/Referencia",
            ]
            for i in tags_tareas:
                self.cursor.execute(
                    f"INSERT INTO tags (tipo,tag_descrip) VALUES ('Tareas','{i}')"
                )
            for i in tags_eventos:
                self.cursor.execute(
                    f"INSERT INTO tags (tipo,tag_descrip) VALUES ('Eventos','{i}')"
                )
            for i in tags_notas:
                self.cursor.execute(
                    f"INSERT INTO tags (tipo,tag_descrip) VALUES ('Notas','{i}')"
                )
            self.conn.commit()

    # Tareas
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

    def cambiar_estado_tarea(self, id_tarea, nuevo_estado):
        self.cursor.execute(
            "UPDATE tareas SET estado=? WHERE id=?",
            (
                nuevo_estado,
                id_tarea,
            ),
        )
        self.conn.commit()

    def eliminar_tarea(self, id):
        self.cursor.execute("DELETE FROM tareas WHERE id=?", (id,))
        self.conn.commit()

    # Notas
    def trae_notas(self):
        self.cursor.execute("SELECT * FROM notas ORDER BY fecha_creacion DESC")
        notas = self.cursor.fetchall()
        return notas

    def trae_una_nota(self, id):
        self.cursor.execute("SELECT * FROM notas WHERE id=?", (id,))
        nota = self.cursor.fetchone()
        return nota

    def guardar_nueva_nota(self, nota, tags):
        self.cursor.execute(
            "INSERT INTO notas (nota_descrip,tags) VALUES (?, ?)",
            (
                nota,
                tags,
            ),
        )
        self.conn.commit()

    def guardar_nota(self, id_nota, descrip, tags):
        self.cursor.execute(
            "UPDATE notas SET nota_descrip=?, tags=? WHERE id=?",
            (
                descrip,
                tags,
                id_nota,
            ),
        )
        self.conn.commit()

    def eliminar_nota(self, id):
        self.cursor.execute("DELETE FROM notas WHERE id=?", (id,))
        self.conn.commit()

    # Eventos
    def trae_eventos(self):
        self.cursor.execute("SELECT * FROM eventos ORDER BY fecha_fin DESC")
        eventos = self.cursor.fetchall()
        return eventos

    def trae_un_evento(self, id):
        self.cursor.execute("SELECT * FROM eventos WHERE id=?", (id,))
        evento = self.cursor.fetchone()
        return evento

    def guardar_nuevo_evento(self, evento, fecini, fecfin, tags):
        if not fecfin:
            fecfin = fecini
        self.cursor.execute(
            "INSERT INTO eventos (evento_descrip, fecha_inicio, fecha_fin, tags) VALUES (?, ?, ?, ?)",
            (
                evento,
                fecini,
                fecfin,
                tags,
            ),
        )
        self.conn.commit()

    def guardar_evento(self, id_evento, descrip, fecini, fecfin, tags):
        if not fecfin:
            fecfin = fecini
        self.cursor.execute(
            "UPDATE eventos SET evento_descrip=?, fecha_inicio=?, fecha_fin=?, tags=? WHERE id=?",
            (
                descrip,
                fecini,
                fecfin,
                tags,
                id_evento,
            ),
        )
        self.conn.commit()

    def eliminar_evento(self, id):
        self.cursor.execute("DELETE FROM eventos WHERE id=?", (id,))
        self.conn.commit()

    # Tags
    def todos_los_tags(self, tipo):
        self.cursor.execute("SELECT tag_descrip FROM tags WHERE tipo=?", (tipo,))
        return self.cursor.fetchall()

    def eliminar_data(self, adm, clave):
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND tipo='ADMIN'",
            (adm,),
        )
        linea_adm = self.cursor.fetchone()
        if not linea_adm:
            return False
        password = linea_adm[2]
        if not bcrypt.checkpw(clave.encode("utf-8"), password):
            return False
        try:
            self.cursor.execute("DELETE FROM tareas")
            self.cursor.execute("DELETE FROM notas")
            self.cursor.execute("DELETE FROM eventos")
            self.conn.commit()
        except Exception as e:
            return False
        return True

    def cambiar_clave(self, adm, clave, nva_clave):
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND tipo='ADMIN'",
            (adm,),
        )
        linea_adm = self.cursor.fetchone()
        if not linea_adm:
            return False
        id_user = linea_adm[0]
        password = linea_adm[2]
        if not bcrypt.checkpw(clave.encode("utf-8"), password):
            # print(f"Administrador: {adm}")
            # print(f"Clave ANTERIOR: {clave}")
            # print(f"Clave NUEVA: {nva_clave}")
            return False
        try:
            hashed = bcrypt.hashpw(nva_clave.encode(), bcrypt.gensalt())
            self.cursor.execute(
                "UPDATE usuarios SET password_hash=? WHERE id=?",
                (hashed, id_user),
            )
            self.conn.commit()
        except Exception as e:
            return False
        return True

    # Cerrando la conexion
    def cerrar_conexion(self):
        self.conn.close()
