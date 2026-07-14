# PROGRAMACIÓN SEGURA — DD281
## Semana 7 | CSRF, Exposición de Datos Sensibles y Controles de Acceso

---

```
PROGRAMACIÓN SEGURA — DD281
Semana 7 | CSRF, Exposición de Datos Sensibles y Controles de Acceso

Nombre: _______________________  Código: __________  Fecha: __________
Tiempo: 90 minutos | Puntaje: 100 pts | Entrega: repositorio GitHub semana-07/guia/
Instrucciones: Justifique sus respuestas en C y D. En A marque solo una opción.
```

---

## SECCIÓN A — OPCIÓN MÚLTIPLE (20 puntos — 2 pts c/u)

*Marque solo una alternativa por pregunta.*

---

**Pregunta 1 (básica):**
¿Qué significa CSRF en seguridad web?

a) Cross-Server Request Forgery — falsificación de peticiones entre servidores

b) Cross-Site Request Forgery — un ataque que fuerza al navegador de una víctima autenticada a enviar peticiones no deseadas a un sitio web

c) Cross-Script Request Filtering — filtrado de peticiones que contienen scripts

d) Client-Side Resource Forgery — falsificación de recursos del lado del cliente

**Respuesta:** _____

---

**Pregunta 2 (básica):**
¿Por qué un ataque CSRF funciona aunque la víctima no haga clic en ningún botón?

a) Porque el atacante tiene acceso a las cookies de sesión de la víctima directamente

b) Porque el navegador envía automáticamente las cookies del dominio en cada petición HTTP, incluidas las originadas desde otros sitios

c) Porque CSRF explota vulnerabilidades en el servidor para ejecutar código arbitrario

d) Porque el ataque usa JavaScript para falsificar la identidad del usuario

**Respuesta:** _____

---

**Pregunta 3 (básica):**
¿Qué función de Python genera un token aleatorio criptográficamente seguro para usar como CSRF token?

a) `random.randint(0, 999999)`

b) `hashlib.md5(os.urandom(16)).hexdigest()`

c) `secrets.token_hex(32)`

d) `uuid.uuid1().hex`

**Respuesta:** _____

---

**Pregunta 4 (básica):**
¿Cuál de las siguientes funciones de hash es APROPIADA para almacenar contraseñas en una base de datos?

a) MD5

b) SHA-256 sin salt

c) bcrypt con factor de trabajo 12

d) SHA-1

**Respuesta:** _____

---

**Pregunta 5 (intermedia):**
Un desarrollador usa `app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'` en Flask. ¿Esto elimina completamente la necesidad de CSRF tokens?

a) Sí, porque SameSite=Strict impide que las cookies se envíen en peticiones cross-site, eliminando el vector de CSRF

b) No, porque SameSite no es compatible con todos los navegadores y versiones antiguas, por lo que CSRF tokens son necesarios como defensa adicional

c) No, porque SameSite=Strict solo protege las cookies de tipo HttpOnly, no las cookies de sesión

d) Sí, pero solo si se usa junto con SESSION_COOKIE_SECURE=True

**Respuesta:** _____

---

**Pregunta 6 (intermedia):**
¿Qué es el "principio de mínimo privilegio" en control de acceso?

a) Cifrar los datos con el algoritmo más ligero para minimizar el uso de CPU

b) Otorgar a cada usuario, proceso o sistema solo los permisos estrictamente necesarios para realizar su función, nada más

c) Limitar el número máximo de usuarios que pueden acceder a un sistema simultáneamente

d) Usar contraseñas cortas para minimizar el tiempo de verificación

**Respuesta:** _____

---

**Pregunta 7 (intermedia):**
En RBAC (Role-Based Access Control), ¿cuál es la ventaja principal sobre asignar permisos directamente a cada usuario?

a) RBAC es más rápido de implementar en cualquier framework

b) Los roles agrupan permisos de forma lógica, facilitando la gestión: cambiar el permiso del rol afecta a todos los usuarios con ese rol simultáneamente

c) RBAC elimina la necesidad de autenticación porque los roles son suficientes para identificar usuarios

d) RBAC es el único método compatible con OAuth 2.0 y JWT

**Respuesta:** _____

---

**Pregunta 8 (avanzada):**
Un atacante construye este HTML en su sitio web: `<img src="https://banco.com/eliminar-cuenta?confirm=true">`. ¿Qué tipo de CSRF es y qué condición debe cumplirse para que funcione?

a) CSRF en petición GET; requiere que banco.com permita modificar estado con peticiones GET y que la víctima tenga sesión activa en banco.com

b) CSRF en petición POST; requiere que la víctima esté conectada a la misma red que el atacante

c) XSS almacenado disfrazado de CSRF; requiere que banco.com tenga una vulnerabilidad XSS

d) CSRF de segundo orden; requiere que el atacante conozca el session ID de la víctima

**Respuesta:** _____

---

**Pregunta 9 (avanzada):**
¿Por qué bcrypt es más seguro que SHA-256 para almacenar contraseñas, aunque SHA-256 sea criptográficamente más fuerte?

a) Porque bcrypt usa un algoritmo de cifrado simétrico mientras que SHA-256 usa cifrado asimétrico

b) Porque bcrypt incluye un salt aleatorio automático y un factor de trabajo ajustable que hace cada hash deliberadamente lento, dificultando ataques de fuerza bruta masivos

c) Porque SHA-256 produce hashes de 256 bits que son más fáciles de adivinar que los 60 caracteres de bcrypt

d) Porque bcrypt está aprobado por NIST mientras que SHA-256 no tiene certificación para almacenamiento de contraseñas

**Respuesta:** _____

---

**Pregunta 10 (avanzada):**
Un endpoint devuelve `403 Forbidden` si el usuario no tiene el rol 'admin' pero `404 Not Found` si el recurso existe pero es del otro usuario. ¿Qué problema de seguridad existe?

a) Ninguno — usar los códigos HTTP correctos es una buena práctica

b) El código 403 revela que el recurso existe, mientras que 404 lo oculta — esta inconsistencia permite enumeración de recursos y revela la estructura del sistema

c) El error está en que debería devolver 401 en lugar de 403 para recursos de otros usuarios

d) Este patrón viola el estándar REST y puede causar errores en los clientes API

**Respuesta:** _____

---

## SECCIÓN B — COMPLETAR Y RELACIONAR (20 puntos)

### B1. Complete los espacios en blanco (10 pts — 2 pts c/u)

1. CSRF funciona porque los navegadores envían automáticamente las _________________ del dominio objetivo en cada petición HTTP, incluso si la petición se originó desde un sitio diferente.

2. El patrón de defensa CSRF más robusto consiste en incluir un _________________ único e impredecible en cada formulario, que el servidor verifica antes de procesar la petición.

3. Para almacenar contraseñas de forma segura, nunca se debe usar MD5 o SHA-1 porque son _________________ — en su lugar, se debe usar _________________, que incorpora un salt y un factor de trabajo ajustable.

4. El principio de _________________ establece que cada usuario, proceso o componente del sistema debe tener solo los permisos estrictamente necesarios para cumplir su función.

5. Los secretos de una aplicación (contraseñas de BD, API keys, secret keys) nunca deben estar _________________ en el código fuente; en su lugar deben almacenarse en _________________ de entorno o gestores de secretos.

---

### B2. Relacionar columnas (10 pts — 1.67 pts c/u)

| Columna A — Concepto | Respuesta | Columna B — Descripción / Defensa |
|---|---|---|
| 1. CSRF Token | → ___ | a) `bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))` |
| 2. SameSite=Strict | → ___ | b) `SELECT * FROM datos WHERE id=? AND usuario_id=?` |
| 3. bcrypt | → ___ | c) `<input type="hidden" name="csrf_token" value="{{ token }}>` |
| 4. Variables de entorno | → ___ | d) Cookie no se envía en ningún request cross-site |
| 5. Verificar propiedad (IDOR/RBAC) | → ___ | e) `SECRET_KEY = os.environ.get('SECRET_KEY')` |
| 6. RBAC Decorador | → ___ | f) `@requiere_rol('admin', 'gerente')` sobre la función |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN (30 puntos)

### C1. (10 puntos)

Analice el siguiente formulario HTML y el endpoint Flask:

```html
<!-- Formulario en pagoperu.com -->
<form action="/pago/realizar" method="POST">
  <input type="text" name="cuenta_destino">
  <input type="number" name="monto">
  <button type="submit">Pagar</button>
</form>
```

```python
@app.route('/pago/realizar', methods=['POST'])
def realizar_pago():
    if not session.get('user_id'):
        return redirect('/login')
    cuenta = request.form.get('cuenta_destino')
    monto = request.form.get('monto')
    # Procesa el pago directamente
    ejecutar_pago(session['user_id'], cuenta, monto)
    return jsonify({"ok": True})
```

**(a)** ¿Qué vulnerabilidad crítica contiene este código? ¿Cómo la clasificas según OWASP 2021?

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(b)** Construye el HTML completo que usaría un atacante para explotar esta vulnerabilidad desde su sitio evil.com. ¿Qué debe hacer la víctima (o qué no debe hacer) para que el ataque funcione?

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(c)** Reescribe el endpoint Flask de forma segura implementando la defensa principal.

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### C2. (10 puntos)

En la base de datos de una aplicación encontramos estas entradas de la tabla `usuarios`:

| id | username | password_stored | fecha_registro |
|----|----------|-----------------|----------------|
| 1 | admin | 5f4dcc3b5aa765d61d8327deb882cf99 | 2023-01-15 |
| 2 | carlos | e10adc3949ba59abbe56e057f20f883e | 2023-02-20 |

**(a)** ¿Qué algoritmo se usó para almacenar las contraseñas? ¿Cómo lo identificas? (3 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(b)** ¿Cuáles son las contraseñas reales de admin y carlos? *Pista: son contraseñas comunes.* (3 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(c)** Escribe el código Python correcto para registrar un nuevo usuario con bcrypt y para verificar su contraseña al hacer login. (4 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### C3. Mini caso (10 puntos)

Un desarrollador de startup deja accidentalmente en GitHub público su archivo `config.py`:

```python
# config.py — subido a GitHub por error
DATABASE_URL = "postgresql://superadmin:Startup2024!@db.miempresa.com:5432/produccion"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET_KEY = "TU_STRIPE_LIVE_KEY_AQUI"
SENDGRID_API_KEY = "SG.xxxxxx.yyyyyy"
ADMIN_PASSWORD = "MiPassword123"
```

**(a)** ¿Qué tipo de vulnerabilidad representa esto según OWASP 2021? ¿Cuál es el riesgo específico de cada credencial expuesta? (5 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(b)** La startup elimina el archivo de GitHub 3 horas después. ¿El riesgo desaparece? ¿Qué deben hacer inmediatamente? (5 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

## SECCIÓN D — AVANZADO Y DE CASO (30 puntos)

**Caso profesional:** FinTech360 es una startup de pagos digitales con 500,000 usuarios en Perú. Durante una auditoría de seguridad contratada, el equipo descubre el siguiente código en producción:

```python
# app.py de FinTech360 (fragmentos del sistema de pagos)
import hashlib, sqlite3, os
from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = "fintech2024secret"

DB_PASS = "Admin@Fintech!2024"  # Contraseña de producción
DB_URL = f"postgresql://admin:{DB_PASS}@prod.fintech360.pe:5432/pagos"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = hashlib.md5(request.form.get('password').encode()).hexdigest()
    conn = sqlite3.connect('fintech.db')
    user = conn.execute(
        f"SELECT * FROM usuarios WHERE user='{username}' AND pass='{password}'"
    ).fetchone()
    conn.close()
    if user:
        session['uid'] = user[0]
        session['tipo'] = user[2]  # 'cliente' o 'admin'
        return jsonify({"ok": True})
    return jsonify({"error": "Inválido"}), 401

@app.route('/pago', methods=['POST'])
def realizar_pago():
    if not session.get('uid'):
        return jsonify({"error": "No auth"}), 401
    # Sin verificación CSRF
    cuenta = request.form.get('cuenta')
    monto = float(request.form.get('monto'))
    conn = sqlite3.connect('fintech.db')
    conn.execute(f"UPDATE wallets SET balance=balance-{monto} WHERE uid={session['uid']}")
    conn.execute(f"UPDATE wallets SET balance=balance+{monto} WHERE cuenta='{cuenta}'")
    conn.commit()
    return jsonify({"transferido": monto})

@app.route('/admin/reportes')
def reportes_admin():
    # Sin verificación de rol
    conn = sqlite3.connect('fintech.db')
    data = conn.execute("SELECT * FROM transacciones").fetchall()
    conn.close()
    return jsonify(data)
```

---

### D1. Auditoría completa (10 puntos)

Completa la siguiente tabla de hallazgos de seguridad para FinTech360. Identifica al menos 7 vulnerabilidades:

| # | Línea/Función | Vulnerabilidad | OWASP 2021 | Severidad | Impacto concreto |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |

*Espacio para análisis adicional:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### D2. Diseño de solución (10 puntos)

Como consultor de seguridad, propón una arquitectura de seguridad para FinTech360 que corrija las vulnerabilidades críticas. Debes:

1. Describir los controles de seguridad que implementarías para cada categoría: autenticación, CSRF, datos en tránsito y en reposo, control de acceso.
2. Escribir el código corregido completo para la función `realizar_pago()` con protección CSRF y consultas parametrizadas.
3. Diseñar el decorador `@requiere_rol('admin')` que verificaría el tipo de usuario en `reportes_admin()`.

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### D3. Pensamiento crítico (10 puntos)

FinTech360 está sujeta a regulación de la SBS (Superintendencia de Banca, Seguros y AFP) del Perú y a la Ley 29733 (Protección de Datos Personales).

1. ¿Cuáles de las vulnerabilidades encontradas podrían resultar en sanciones regulatorias de la SBS? Argumente por qué.
2. La ANPD (Autoridad Nacional de Protección de Datos Personales) puede imponer multas de hasta 100 UIT (~S/. 495,000). ¿Qué vulnerabilidades específicas de FinTech360 expondrían datos personales y activarían esta regulación?
3. Más allá de las multas, ¿qué impacto reputacional y operacional podría sufrir FinTech360 si estas vulnerabilidades fueran explotadas y publicadas?

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

*Fin de la guía — Semana 7 | Universidad Autónoma del Perú | Programación Segura DD281*
