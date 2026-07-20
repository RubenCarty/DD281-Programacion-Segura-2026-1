#!/usr/bin/env python3
import os
import sqlite3
import time

import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "usuarios.db")


def crear_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(rounds=12)
    ).decode("utf-8")


def inicializar_bd():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    inicio = time.perf_counter()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                hash_password TEXT NOT NULL,
                rol TEXT DEFAULT 'estudiante',
                activo INTEGER DEFAULT 1,
                intentos_fallidos INTEGER DEFAULT 0,
                bloqueado_hasta TEXT DEFAULT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        usuarios = [
            ("juan.garcia", "MiPassword123!", "estudiante"),
            ("maria.lopez", "SecurePass456#", "estudiante"),
            ("prof.rodriguez", "DocPass789$", "docente"),
            ("admin", "AdminSuper012!", "administrador"),
        ]
        for usuario, password, rol in usuarios:
            try:
                cursor.execute(
                    "INSERT INTO usuarios (usuario, hash_password, rol) VALUES (?, ?, ?)",
                    (usuario, crear_hash(password), rol),
                )
                print(f"Usuario '{usuario}' creado")
            except sqlite3.IntegrityError:
                print(f"Usuario '{usuario}' ya existe")
    duracion = time.perf_counter() - inicio
    print(f"Base de datos: {DB_PATH}")
    print(f"Tiempo total: {duracion:.3f} segundos")


if __name__ == "__main__":
    inicializar_bd()
