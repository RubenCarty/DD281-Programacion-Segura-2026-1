#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# setup_db.py — Inicializa la base de datos SQLite con usuarios de prueba
# ══════════════════════════════════════════════════════════════════
import sqlite3
import bcrypt
import os

DB_PATH = "db/usuarios.db"

def crear_hash(password: str) -> str:
    """Crea hash bcrypt con factor de coste 12."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute("""
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
    """)
    
    # Usuarios de prueba
    usuarios_test = [
        ("juan.garcia",   "MiPassword123!",  "estudiante"),
        ("maria.lopez",   "SecurePass456#",  "estudiante"),
        ("prof.rodriguez","DocPass789$",     "docente"),
        ("admin",         "AdminSuper012!",  "administrador"),
    ]
    
    print("Creando usuarios de prueba con bcrypt (factor 12)...")
    print("Esto puede tomar unos segundos por el factor de coste...\n")
    
    for usuario, password, rol in usuarios_test:
        hash_pw = crear_hash(password)
        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, hash_password, rol) VALUES (?, ?, ?)",
                (usuario, hash_pw, rol)
            )
            print(f"  ✓ Usuario '{usuario}' creado")
            print(f"    Hash: {hash_pw[:30]}...")
        except sqlite3.IntegrityError:
            print(f"  ⚠ Usuario '{usuario}' ya existe — omitido")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Base de datos inicializada en: {DB_PATH}")
    print(f"  Tamaño: {os.path.getsize(DB_PATH)} bytes")

if __name__ == "__main__":
    inicializar_bd()