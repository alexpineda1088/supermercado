# db.py — helpers para SQLite
import sqlite3
from sqlite3 import Connection
from typing import List, Dict

# Ruta de la base de datos (Flask recomienda carpeta instance)
DB_PATH = 'instance/inventario.db'

# Schema inicial
SCHEMA = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
);
"""

# =========================
# Conexión y creación de tabla
# =========================
def get_connection() -> Connection:
    """Devuelve conexión SQLite con row_factory dict-like"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos y crea tabla si no existe"""
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()


# =========================
# Operaciones CRUD
# =========================
def obtener_todos() -> List[Dict]:
    """Devuelve todos los productos como lista de diccionarios"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, cantidad, precio FROM productos ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def obtener_por_id(id_producto: int) -> Dict:
    """Devuelve un producto por ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE id=?", (id_producto,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def insertar_producto(d: Dict):
    """Inserta un producto en la base de datos"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
        (d['id'], d['nombre'], d['cantidad'], d['precio'])
    )
    conn.commit()
    conn.close()

def actualizar_producto_db(d: Dict):
    """Actualiza un producto existente"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
        (d['nombre'], d['cantidad'], d['precio'], d['id'])
    )
    conn.commit()
    conn.close()

def eliminar_producto_db(id_producto: int):
    """Elimina un producto por ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id=?", (id_producto,))
    conn.commit()
    conn.close()
