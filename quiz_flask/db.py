import sqlite3
from datetime import datetime

DB_FILE = 'quiz.db'  # Nombre del archivo de la DB (se creará automáticamente)

def init_db():
    """Inicializa la base de datos si no existe."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios (id único, nombre único)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Crear tabla de sesiones (id, user_id referencia, porcentaje, fecha)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            porcentaje REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_or_create_user(nombre):
    """Obtiene el ID del usuario si existe, o lo crea."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE nombre = ?', (nombre,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return result[0]
    else:
        cursor.execute('INSERT INTO usuarios (nombre) VALUES (?)', (nombre,))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

def save_sesion(user_id, porcentaje):
    """Guarda una sesión con el porcentaje y fecha actual."""
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sesiones (user_id, porcentaje, fecha) VALUES (?, ?, ?)', (user_id, porcentaje, fecha))
    conn.commit()
    conn.close()

def get_progreso_usuario(user_id):
    """Obtiene el progreso: lista de (fecha, porcentaje) ordenado por fecha."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT fecha, porcentaje FROM sesiones WHERE user_id = ? ORDER BY fecha ASC', (user_id,))
    progreso = cursor.fetchall()
    conn.close()
    return progreso
