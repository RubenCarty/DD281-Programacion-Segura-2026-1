import sqlite3
import hashlib

conn=sqlite3.connect("banco.db")

c=conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY,
username TEXT,
password_hash TEXT,
saldo REAL,
email TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS cuentas(
usuario_id INTEGER,
numero TEXT,
saldo REAL
)
""")

c.execute("DELETE FROM usuarios")
c.execute("DELETE FROM cuentas")

password=hashlib.md5("123456".encode()).hexdigest()

c.execute("""
INSERT INTO usuarios
VALUES
(1,'juan',?,5000,'juan@gmail.com')
""",(password,))

c.execute("""
INSERT INTO cuentas
VALUES
(1,'999888777',5000)
""")

conn.commit()

conn.close()

print("Base creada correctamente")