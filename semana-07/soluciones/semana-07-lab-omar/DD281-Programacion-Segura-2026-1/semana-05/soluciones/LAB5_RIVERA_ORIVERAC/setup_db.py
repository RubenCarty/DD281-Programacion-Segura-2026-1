#!/usr/bin/env python3
"""
setup_db.py — Inicializa la base de datos de demostración
IMPORTANTE: Esta base de datos contiene datos FICTICIOS solo para el laboratorio
"""
import sqlite3
import os

DB_PATH = "tienda.db"

def crear_base_datos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'cliente',
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER,
            monto REAL,
            tarjeta TEXT,
            estado TEXT DEFAULT 'pendiente'
        )
    """)

    usuarios = [
        (1, 'admin',    'AdminPass123', 'admin',   'admin@tienda.com'),
        (2, 'juan',     'juan2024',     'cliente',  'juan@email.com'),
        (3, 'maria',    'maria123',     'cliente',  'maria@email.com'),
        (4, 'vendedor', 'vend456',      'vendedor', 'ventas@tienda.com'),
    ]

    productos = [
        (1, 'Laptop HP 15',    2499.00, 'electronica', 15),
        (2, 'Mouse Logitech',    89.00, 'electronica', 50),
        (3, 'Cuaderno A4',       12.50, 'utiles',      200),
        (4, 'Memoria USB 64GB', 45.00,  'electronica', 30),
        (5, 'Mochila Escolar',  85.00,  'accesorios',  40),
    ]

    pedidos = [
        (1, 2, 2499.00, '****1234', 'completado'),
        (2, 3, 89.00,   '****5678', 'pendiente'),
        (3, 2, 130.00,  '****9012', 'completado'),
    ]

    cursor.executemany("INSERT OR IGNORE INTO usuarios VALUES (?,?,?,?,?)", usuarios)
    cursor.executemany("INSERT OR IGNORE INTO productos VALUES (?,?,?,?,?)", productos)
    cursor.executemany("INSERT OR IGNORE INTO pedidos VALUES (?,?,?,?,?)", pedidos)

    conn.commit()
    conn.close()
    print(f"Base de datos creada: {DB_PATH}")
    print(f"  Usuarios: {len(usuarios)} | Productos: {len(productos)} | Pedidos: {len(pedidos)}")

if __name__ == "__main__":
    crear_base_datos()
