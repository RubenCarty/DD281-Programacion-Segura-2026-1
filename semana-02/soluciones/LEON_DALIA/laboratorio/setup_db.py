#!/usr/bin/env python3
import sqlite3
import bcrypt
import os

os.makedirs('../db', exist_ok=True)
conn = sqlite3.connect('../db/usuarios.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    usuario TEXT UNIQUE,
    hash_password TEXT,
    rol TEXT
)''')

usuarios = [
    ("juan.garcia", "MiPassword123!", "estudiante"),
    ("maria.lopez", "SecurePass456#", "estudiante"),
    ("admin", "AdminSuper012!", "administrador")
]

for u, p, r in usuarios:
    hash_pw = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, hash_password, rol) VALUES (?, ?, ?)", (u, hash_pw, r))
    print(f"✓ Usuario {u} creado")

conn.commit()
conn.close()
print("Base de datos creada en ../db/usuarios.db")
