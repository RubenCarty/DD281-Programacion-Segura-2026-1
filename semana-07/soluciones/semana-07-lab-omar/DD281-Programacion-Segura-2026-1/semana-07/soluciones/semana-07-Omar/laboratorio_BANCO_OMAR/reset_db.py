import os
import sqlite3
import hashlib
import bcrypt

def reset():
    files = ["banco_vulnerable.db", "banco_segura.db"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            print(f"     Eliminado: {f}")
        else:
            print(f"  —  No existía: {f}")

    print("\n  Reiniciando app_vulnerable (banco_vulnerable.db)...")
    conn = sqlite3.connect("banco_vulnerable.db")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id            INTEGER PRIMARY KEY,
            username      TEXT    UNIQUE,
            password_hash TEXT,
            rol           TEXT,
            saldo         REAL
        );
        CREATE TABLE IF NOT EXISTS transferencias (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            origen    TEXT,
            destino   TEXT,
            monto     REAL,
            fecha     DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        INSERT OR IGNORE INTO usuarios VALUES
          (1,'admin',   '21232f297a57a5a743894a0e4a801fc3','admin',  999999.0),
          (2,'carlos',  '827ccb0eea8a706c4c34a16891f84e7b','cliente',  5000.0),
          (3,'atacante','202cb962ac59075b964b07152d234b70','cliente',     0.0);
    """)
    conn.commit()
    conn.close()
    print("     banco_vulnerable.db reiniciado")

    print("\n  Reiniciando app_segura (banco_segura.db) con bcrypt...")
    users = [
        (1, 'admin',    'admin',   'admin',   999999.0),
        (2, 'carlos',   '12345',   'cliente',   5000.0),
        (3, 'atacante', '123',     'cliente',      0.0),
    ]
    conn2 = sqlite3.connect("banco_segura.db")
    conn2.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id            INTEGER PRIMARY KEY,
            username      TEXT    UNIQUE,
            password_hash TEXT,
            rol           TEXT,
            saldo         REAL
        );
    """)
    
    for uid, username, pwd, rol, saldo in users:
        h = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(rounds=12))
        conn2.execute(
            "INSERT OR IGNORE INTO usuarios (id, username, password_hash, rol, saldo) VALUES (?,?,?,?,?)",
            (uid, username, h.decode(), rol, saldo)
        )
    conn2.commit()
    conn2.close()
    print("     banco_segura.db reiniciado")

if __name__ == '__main__':
    print("\n     RESET DEMO — BancoNacional.pe Lab S7\n")
    reset()