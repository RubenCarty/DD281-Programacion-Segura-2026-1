# SESIÓN DE CLASE — SEMANA 7
## Programación Segura DD281 | Universidad Autónoma del Perú

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) |
| **Semana** | 7 |
| **Tema** | CSRF, Exposición de Datos Sensibles y Controles de Acceso |
| **Logro** | Implementa controles de seguridad avanzados para prevenir falsificación de peticiones y exposición de datos sensibles |
| **Valor** | Excelencia en la protección de la integridad de las transacciones |
| **Duración** | 3 horas 20 minutos |
| **Trabajo colaborativo** | Simulación de Ataque y Defensa CSRF |

---

## TABLA DE CONTENIDOS
1. [Cronograma](#cronograma)
2. [Inicio](#inicio)
3. [Utilidad](#utilidad)
4. [Transformación](#transformacion)
5. [Receso](#receso)
6. [Práctica](#practica)
7. [Cierre](#cierre)
8. [Guion Verbal](#guion-verbal)
9. [Casos Reales](#casos-reales)
10. [Evaluación Formativa](#evaluacion-formativa)
11. [Referencias APA 7](#referencias)
12. [Recursos Reales](#recursos)

---

## CRONOGRAMA {#cronograma}

| Bloque | Actividad | Duración | Responsable |
|---|---|---|---|
| Bloque 1 | INICIO (Rompe-hielo, Logro, Revisión S6, Diagnóstico) | 20 min | Docente |
| Bloque 1 | UTILIDAD | 10 min | Docente |
| Bloque 1 | RECESO | 20 min | — |
| Bloque 2 | TRANSFORMACIÓN (T1-T5) | 70 min | Docente + Estudiantes |
| Bloque 3 | PRÁCTICA (Grupal + Individual) | 40 min | Estudiantes |
| Bloque 3 | CIERRE | 10 min | Docente |
| **TOTAL** | | **170 min** | |

---

# 1. INICIO (20 min) {#inicio}

## a) ROMPE-HIELO (5 min): "El banco hackeado sin saberlo"

**Instrucción para el docente:** Muestra este escenario en pantalla o léelo en voz alta:

> *"María está en casa revisando las noticias en su laptop. Tiene abierta en otra pestaña su cuenta bancaria en banco.pe. Sin saberlo, abre un correo de marketing con una imagen rota. Al cargar la página, su navegador ejecuta silenciosamente una transferencia de S/. 2,000 a una cuenta desconocida. María no tocó nada en el banco."*

**Pregunta al grupo (mostrar en pantalla):**

> **¿Cómo fue posible una transferencia bancaria sin que María hiciera nada en la página del banco?**

Dejar 2 minutos de discusión en parejas. Luego pedir 2-3 respuestas. No dar la respuesta todavía — esto genera la tensión cognitiva que motiva la clase.

**Respuesta que se construirá durante la sesión:** El navegador de María envió automáticamente sus cookies de sesión del banco cuando la página maliciosa le hizo enviar un formulario oculto. Eso es exactamente CSRF.

---

## b) LOGRO DE APRENDIZAJE (3 min)

**Guion verbal textual:**

*"Buenos días/tardes. Hoy vamos a aprender tres cosas que todo programador que trabaja en aplicaciones web DEBE dominar. Primero: CSRF — un ataque que hace que el navegador de tus usuarios ejecute acciones en tu aplicación sin que ellos lo sepan. Segundo: cómo proteger datos sensibles, especialmente contraseñas — porque si tienes MD5 en tu base de datos hoy, cualquier atacante que acceda a ella tiene todas las contraseñas en segundos. Tercero: control de acceso basado en roles — porque no todos los usuarios deben ver todo. Al terminar esta sesión, van a poder implementar estas tres protecciones en código real. Empecemos."*

---

## c) REVISIÓN SESIÓN ANTERIOR (7 min)

*El docente hace las siguientes preguntas para recuperar los aprendizajes de la Semana 6 (XSS, Sesiones, IDOR).*

**Pregunta 1:** "¿Qué es XSS y cuál es la diferencia entre XSS reflejado y almacenado?"

**Respuesta esperada detallada:** XSS (Cross-Site Scripting) es la inyección de código JavaScript en páginas web que otros usuarios visualizan. XSS reflejado: el payload viene en el request (ej: en un parámetro de URL) y se refleja en la respuesta — requiere que la víctima haga clic en un link crafteado. XSS almacenado: el payload se guarda en la base de datos y se ejecuta para TODOS los usuarios que visiten la página afectada — más peligroso porque no requiere que la víctima haga clic en nada específico.

**Si un estudiante responde mal:** "Casi. La clave está en dónde vive el payload: en XSS reflejado viene y va en el mismo request; en XSS almacenado queda guardado en el servidor y afecta a múltiples víctimas futuras. La diferencia práctica es que el almacenado puede comprometer miles de cuentas con un solo payload."

**Pregunta 2:** "Nombren tres atributos de seguridad que debe tener una cookie de sesión y qué ataque previene cada uno."

**Respuesta esperada detallada:** (1) `HttpOnly`: impide que JavaScript lea la cookie — previene robo de cookies mediante XSS. (2) `Secure`: la cookie solo se transmite en HTTPS — previene sniffing en redes inseguras. (3) `SameSite=Strict`: la cookie no se envía en requests cross-site — previene CSRF (aunque esto lo veremos hoy en detalle).

**Si un estudiante responde mal:** "Bien encaminado. Recuerden: HttpOnly = JavaScript no puede tocarla; Secure = solo viaja por HTTPS; SameSite = no sale del sitio de origen. Hoy vamos a profundizar en SameSite porque tiene relación directa con el tema de hoy."

**Pregunta 3:** "¿Qué es IDOR y cómo se corrige en una API REST?"

**Respuesta esperada detallada:** IDOR (Insecure Direct Object Reference) es una vulnerabilidad de control de acceso donde un usuario puede acceder a recursos de otros usuarios cambiando un identificador en la URL o el request. Se corrige verificando en el servidor que el recurso solicitado pertenece al usuario autenticado en sesión, usando `AND usuario_id = ?` en la consulta SQL, y devolviendo el mismo error 404 tanto para "no existe" como para "no autorizado" (para evitar enumeración).

---

## d) DIAGNÓSTICO INICIAL (5 min)

**Pregunta 1:** "¿Han escuchado el término CSRF antes? ¿Qué creen que significa?"

**Respuesta esperada:** Cross-Site Request Forgery. La mayoría no lo habrá escuchado — esto es normal. El objetivo es activar la curiosidad.

**Pregunta 2:** "Si un usuario tiene contraseña 'password123' y la aplicación usa MD5, ¿cuánto tiempo creen que tardaría un atacante en obtenerla si tuviera acceso a la base de datos?"

**Respuesta esperada:** Instantáneo o menos de 1 segundo. MD5 de 'password123' está en todas las tablas rainbow. Muchos estudiantes sobreestiman la seguridad del hash MD5.

**Pregunta 3:** "¿Qué significa que un usuario tenga rol 'admin' en una aplicación? ¿Por qué es importante que un 'cliente' no pueda hacer lo que hace un 'admin'?"

**Respuesta esperada:** Un admin tiene permisos para gestionar usuarios, ver datos de todos, hacer configuraciones del sistema. Un cliente solo debe poder gestionar sus propios datos. La separación previene escalada de privilegios y protege la integridad del sistema.

---

# 2. UTILIDAD (10 min) {#utilidad}

## ¿Por qué importa este tema hoy?

**Dato 1 — Costo real del CSRF:**
Según el reporte de IBM "Cost of Data Breach 2023", el costo promedio de una brecha de seguridad es **$4.45 millones USD**. Los ataques de control de acceso deficiente (donde se clasifica CSRF) son responsables del 11% de todos los brechas documentadas.

**Dato 2 — Contraseñas expuestas:**
En el breach de Equifax 2017 (147 millones de registros), se encontraron contraseñas de administración en texto plano en portales internos. El costo total de la multa y reparaciones superó los **$575 millones USD**. RockYou (2009): 32 millones de contraseñas en texto plano, expuestas en 1 hora.

**Dato 3 — CSRF en finanzas:**
ING Direct (2008) fue víctima de CSRF que permitió realizar transferencias bancarias desde cuentas de clientes autenticados. El banco debió reembolsar las pérdidas de los afectados y reforzar toda su infraestructura.

**Aplicación actual:**
Hoy, toda empresa que desarrolla aplicaciones web debe implementar:
- Protección CSRF en todos los formularios y APIs que modifiquen estado
- bcrypt o Argon2 para almacenamiento de contraseñas (nunca MD5/SHA1)
- RBAC para separar permisos por rol de usuario

**Pregunta retadora de apertura:**

> **"Si una aplicación ya tiene `SESSION_COOKIE_SAMESITE='Strict'`, ¿necesita además implementar CSRF tokens?"**

**Respuesta esperada:** SameSite=Strict es muy efectivo para navegadores modernos, pero no todos los navegadores lo implementan de forma idéntica, y las versiones antiguas no lo soportan. Además, existen vectores de ataque específicos (como DNS rebinding o subdominios comprometidos) donde SameSite no protege completamente. La defensa en capas (SameSite + CSRF token) es la práctica correcta según OWASP. Nunca depender de una sola línea de defensa.

---

# 3. TRANSFORMACIÓN (70 min) {#transformacion}

## T1. ¿Qué es CSRF y cómo funciona? (20 min)

### Explicación conceptual

CSRF (Cross-Site Request Forgery) es un ataque que engaña al navegador de un usuario autenticado para que envíe peticiones HTTP no deseadas a una aplicación donde tiene sesión activa. El atacante no roba las credenciales — usa las cookies de sesión existentes que el navegador envía automáticamente.

**Diagrama ASCII del ataque:**
```
FLUJO DEL ATAQUE CSRF
═══════════════════════════════════════════════════════════
                    ┌─────────────────┐
                    │   banco.com     │
                    │ (sitio legítimo)│
                    └────────┬────────┘
                             │ 1. María inicia sesión
                             │ 2. banco.com setea cookie: session=ABC123
                             │
                    ┌────────▼────────┐
                    │  Navegador      │
                    │  de María       │◄──── 3. María visita evil.com
                    └────────┬────────┘
                             │
              ┌──────────────▼──────────────┐
              │  evil.com envía formulario   │
              │  oculto apuntando a banco.com│
              │  + onload="form.submit()"    │
              └──────────────┬──────────────┘
                             │ 4. Navegador envía POST a banco.com
                             │    CON cookie session=ABC123 automáticamente
                             ▼
                    ┌─────────────────┐
                    │   banco.com     │
                    │ "Petición válida│◄── 5. El banco ejecuta la
                    │  de María"      │       transferencia
                    └─────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Cuenta del     │
                    │  Atacante       │◄── 6. El dinero llega
                    └─────────────────┘
═══════════════════════════════════════════════════════════
```

**Código del ataque (HTML en evil.com):**
```html
<!DOCTYPE html>
<html>
<!-- Esta página está en evil.com -->
<body onload="document.forms[0].submit()">
  <!-- El formulario apunta al banco legítimo -->
  <form action="https://banco.com/transferir" method="POST" style="display:none">
    <input type="hidden" name="destino" value="cuenta-atacante-999">
    <input type="hidden" name="monto" value="5000">
    <!-- NO hay CSRF token — el atacante no puede conocerlo -->
  </form>
  <p>Cargando tu descuento especial...</p>
</body>
</html>
```

**Código vulnerable en Flask:**
```python
@app.route('/transferir', methods=['POST'])
def transferir():
    if not session.get('user_id'):  # Solo verifica autenticación
        return redirect('/login')
    
    destino = request.form.get('destino')
    monto = request.form.get('monto')
    
    # ❌ VULNERABLE: no verifica que la petición vino del mismo sitio
    conn = sqlite3.connect('banco.db')
    conn.execute(
        "UPDATE cuentas SET saldo = saldo - ? WHERE usuario_id = ?",
        (monto, session['user_id'])
    )
    conn.execute(
        "UPDATE cuentas SET saldo = saldo + ? WHERE numero = ?",
        (monto, destino)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Transferencia exitosa"})
```

**PREGUNTA AL GRUPO 1:** "Si el banco usa HTTPS, ¿el ataque CSRF sigue funcionando? ¿Por qué?"

**RESPUESTA ESPERADA DETALLADA:** Sí, CSRF funciona aunque el sitio use HTTPS. HTTPS cifra la comunicación entre el navegador y el servidor, pero no impide que el navegador envíe automáticamente las cookies del dominio al hacer una petición cross-site. El cifrado protege el contenido en tránsito (nadie puede interceptarlo), pero el problema del CSRF no es la confidencialidad de los datos — es que el servidor no puede distinguir si la petición fue iniciada por el usuario o por el sitio del atacante. HTTPS resuelve un problema diferente (sniffing/man-in-the-middle); CSRF tokens resuelven el problema de la origen de la petición.

### MINI ACTIVIDAD T1 (4 min)
El docente muestra este fragmento y pregunta: "¿Puede este `<img>` ejecutar un CSRF? ¿Bajo qué condición?"
```html
<img src="https://banco.com/eliminar-cuenta?confirm=true">
```
**Respuesta:** Sí, si el endpoint `/eliminar-cuenta` acepta la acción via GET. Este es el anti-patrón más grave en REST: modificar estado con GET. La imagen se carga automáticamente, el navegador hace un GET a banco.com con las cookies, y si el servidor ejecuta la eliminación, el ataque funciona. Lección: NUNCA modificar estado con peticiones GET.

---

## T2. Defensas contra CSRF (15 min)

### Defensa 1 — CSRF Token (Synchronizer Token Pattern)

El servidor genera un token aleatorio único por sesión, lo incluye en el formulario HTML como campo oculto, y verifica que el token enviado en el POST coincide con el guardado en la sesión. El atacante no puede conocer el valor del token porque está en la sesión del servidor.

```python
import secrets

@app.route('/transferir-form')
def mostrar_form():
    # ✅ Generar token único e impredecible por sesión
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return render_template('transferir.html', csrf_token=session['csrf_token'])

@app.route('/transferir', methods=['POST'])
def transferir_seguro():
    if not session.get('user_id'):
        return redirect('/login')
    
    # ✅ Verificar CSRF token
    token_recibido = request.form.get('csrf_token', '')
    token_esperado = session.get('csrf_token', '')
    
    # Comparación segura contra timing attacks
    if not secrets.compare_digest(token_recibido, token_esperado):
        return jsonify({"error": "Petición inválida"}), 403
    
    # Regenerar token después de cada uso
    session['csrf_token'] = secrets.token_hex(32)
    
    # Procesar transferencia...
    destino = request.form.get('destino')
    monto = float(request.form.get('monto'))
    # ... resto del código
    return jsonify({"ok": True})
```

Template HTML con token:
```html
<!-- transferir.html -->
<form method="POST" action="/transferir">
  <!-- ✅ El atacante no puede conocer este valor — está en la sesión del servidor -->
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input type="text" name="destino" placeholder="Número de cuenta">
  <input type="number" name="monto" placeholder="Monto">
  <button type="submit">Transferir</button>
</form>
```

### Defensa 2 — SameSite Cookie

```python
# En Flask
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
# Strict: la cookie NO se envía en NINGÚN request que provenga de otro sitio
# Lax: la cookie se envía en navegación de nivel superior (GET seguro) pero no en POST cross-site
# None: la cookie siempre se envía (requiere Secure=True; peligroso)
```

### Defensa 3 — Flask-WTF (automatización)

```python
# pip install flask-wtf
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
csrf = CSRFProtect(app)  # ✅ Protege TODOS los formularios POST automáticamente

# En el template solo agregar:
# {{ form.hidden_tag() }}  o  {{ csrf_token() }}
# Flask-WTF genera, incluye y valida el token automáticamente
```

### Defensa 4 — Validar Origin/Referer header

```python
from urllib.parse import urlparse

DOMINIOS_PERMITIDOS = {'miaplicacion.com', 'www.miaplicacion.com'}

@app.before_request
def verificar_origin():
    if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
        origin = request.headers.get('Origin') or request.headers.get('Referer', '')
        if origin:
            parsed = urlparse(origin)
            if parsed.netloc not in DOMINIOS_PERMITIDOS:
                return jsonify({"error": "Origen no permitido"}), 403
```

**PREGUNTA AL GRUPO 2:** "Si el atacante también puede poner un CSRF token en su formulario malicioso, ¿el mecanismo falla?"

**RESPUESTA ESPERADA DETALLADA:** No falla. El atacante puede incluir cualquier string como CSRF token en su formulario, pero el servidor verifica que ese token coincida con el que está almacenado en la SESIÓN DEL SERVIDOR del usuario víctima. El atacante no puede acceder a la sesión del servidor porque esa información nunca se envía al navegador del atacante — solo se envía al navegador de la víctima (y mediante la cookie de sesión, no directamente accesible por JS en otro dominio gracias a Same-Origin Policy). Si el atacante pone un token aleatorio, no coincidirá con el de la sesión → petición rechazada. Si pone el token correcto, eso significaría que accedió a la sesión del usuario víctima, lo cual es un ataque diferente (XSS o session hijacking).

---

## T3. Exposición de Datos Sensibles — Contraseñas (15 min)

### El problema de MD5 y SHA1 para contraseñas

```python
import hashlib

# ❌ MD5 — NUNCA para contraseñas
password = "password123"
hash_md5 = hashlib.md5(password.encode()).hexdigest()
print(hash_md5)  # 482c811da5d5b4bc6d497ffa98491e38
# Este hash está en CrackStation.net — crackeado en 0ms

# ❌ SHA-256 sin salt — también incorrecto
hash_sha256 = hashlib.sha256(password.encode()).hexdigest()
print(hash_sha256)  # ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
# También está en tablas rainbow para passwords comunes
```

**¿Por qué MD5 es inseguro para contraseñas?**

| Característica | MD5/SHA-256 | bcrypt/Argon2 |
|---|---|---|
| Velocidad | ~10,000,000,000/seg en GPU | ~20-100/seg intencionalmente |
| Salt automático | No (debe hacerse manualmente) | Sí (embebido en el hash) |
| Factor de trabajo ajustable | No | Sí (rounds/cost) |
| Diseñado para contraseñas | No (diseñado para integridad) | Sí |
| Tiempo para crackear "password123" | Instantáneo (en tablas rainbow) | ~Miles de años con GPU moderna |

**bcrypt — implementación correcta:**
```python
import bcrypt

# AL REGISTRAR USUARIO — generar hash con salt
def registrar_usuario(username: str, password: str):
    # Convertir password a bytes
    password_bytes = password.encode('utf-8')
    
    # gensalt genera un salt aleatorio de 22 chars
    # rounds=12 significa 2^12 = 4096 iteraciones (~250ms intencionalmente)
    salt = bcrypt.gensalt(rounds=12)
    
    # El hash resultante incluye: algoritmo + salt + hash (todo en uno)
    # Ejemplo: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
    password_hash = bcrypt.hashpw(password_bytes, salt)
    
    # Guardar en BD como bytes o decodificado como string
    conn = sqlite3.connect('app.db')
    conn.execute(
        "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
        (username, password_hash.decode('utf-8'))
    )
    conn.commit()
    conn.close()

# AL VERIFICAR LOGIN
def verificar_login(username: str, password_ingresado: str) -> bool:
    conn = sqlite3.connect('app.db')
    user = conn.execute(
        "SELECT password_hash FROM usuarios WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    
    if not user:
        # ✅ Siempre hacer el checkpw incluso si el usuario no existe
        # (previene timing attacks que revelan si el usuario existe)
        bcrypt.checkpw(b'dummy', bcrypt.hashpw(b'dummy', bcrypt.gensalt()))
        return False
    
    # checkpw extrae el salt del hash almacenado automáticamente
    return bcrypt.checkpw(
        password_ingresado.encode('utf-8'),
        user[0].encode('utf-8')
    )
```

**PREGUNTA AL GRUPO 3:** "Si bcrypt es intencionalmente lento (250ms por hash), ¿afecta la experiencia del usuario en el login?"

**RESPUESTA ESPERADA DETALLADA:** 250ms por login es imperceptible para el usuario humano (el umbral de percepción es ~100-200ms). Sin embargo, para un atacante con una GPU que intenta 10 mil millones de MD5/segundo, pasar a 4 operaciones/segundo (bcrypt rounds=12 en un servidor típico) convierte un ataque de fuerza bruta que tomaría segundos en uno que tomaría miles de años. El sacrificio de rendimiento es mínimo para usuarios legítimos pero devastador para atacantes. Si el sitio tiene millones de usuarios haciendo login simultáneamente, se ajustan los rounds o se usa Argon2id con configuración apropiada — el tradeoff siempre a favor de la seguridad.

---

## T4. Exposición de Datos Sensibles — Secretos y Configuración (10 min)

### El problema de los secretos hardcodeados

**Escenario real:** En 2023, un desarrollador de startup subió accidentalmente a un repositorio GitHub público su archivo `config.py` con credenciales de producción. Bots automatizados detectaron las credenciales en menos de 3 minutos. La empresa sufrió acceso no autorizado a su base de datos con 50,000 clientes.

```python
# ❌ NUNCA hardcodear secretos en el código
DATABASE_URL = "postgresql://admin:MiPassword2024@prod.empresa.com/clientes"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_KEY = "TU_STRIPE_LIVE_KEY_AQUI"
app.secret_key = "mi_aplicacion_2024"

# ✅ Usar variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()  # Lee el archivo .env (solo en desarrollo local)

DATABASE_URL = os.environ.get('DATABASE_URL')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY_ID')
STRIPE_KEY = os.environ.get('STRIPE_SECRET_KEY')

# Para Flask secret_key — generar aleatoriamente si no existe
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

**Archivo `.env` (en desarrollo local — NUNCA subir a git):**
```bash
DATABASE_URL=postgresql://admin:MiPassword2024@localhost:5432/app_dev
AWS_SECRET_KEY_ID=tu_clave_aws_aqui
STRIPE_SECRET_KEY=TU_STRIPE_TEST_KEY_AQUI
SECRET_KEY=genera_con_python_-c_"import_secrets;print(secrets.token_hex(32))"
```

**Archivo `.gitignore` (crítico):**
```
# SECRETOS — nunca en git
.env
.env.local
.env.production
*.key
credentials.json
config/secrets.yml
secrets/
```

**PREGUNTA AL GRUPO 4:** "Un desarrollador borra el archivo `.env` de GitHub 2 horas después de subirlo accidentalmente. ¿El problema está resuelto?"

**RESPUESTA ESPERADA DETALLADA:** No. Los secretos expuestos siguen siendo un riesgo activo por varias razones: (1) GitHub mantiene historial de commits — el archivo puede recuperarse con `git log` incluso si se eliminó. (2) Servicios como GitGuardian, TruffleHog y los propios bots de seguridad de GitHub escanean repositorios públicos en tiempo real — el secreto puede haber sido detectado y almacenado en minutos. (3) Wayback Machine y otros archivadores web pueden haber indexado el contenido. (4) Bots maliciosos que monitorean GitHub constantemente pueden haberlo capturado. La acción correcta es: revocar INMEDIATAMENTE todas las credenciales expuestas (cambiar contraseñas, regenerar API keys) y revisar logs de acceso en todos los servicios afectados para verificar si hubo uso no autorizado.

---

## T5. Controles de Acceso — RBAC (10 min)

### Role-Based Access Control

RBAC organiza los permisos en roles en lugar de asignarlos directamente a usuarios. Un usuario tiene un rol; el rol tiene permisos. Cambiar el permiso del rol afecta a todos los usuarios con ese rol simultáneamente.

**Implementación en Flask con decoradores:**
```python
from functools import wraps
from flask import session, jsonify

def requiere_login(f):
    """Verifica que el usuario esté autenticado"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def requiere_rol(*roles_permitidos):
    """Verifica que el usuario tenga uno de los roles especificados"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('user_id'):
                return jsonify({"error": "No autenticado"}), 401
            
            rol_actual = session.get('rol')
            if rol_actual not in roles_permitidos:
                # 403 Forbidden — sabe que existe pero no tiene permiso
                return jsonify({"error": "Acceso denegado — permisos insuficientes"}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

# Uso en rutas:
@app.route('/panel-admin')
@requiere_rol('admin')  # Solo admin
def panel_admin():
    return jsonify({"datos": "sensibles del sistema"})

@app.route('/reportes')
@requiere_rol('admin', 'gerente')  # Admin o gerente
def ver_reportes():
    return jsonify({"reporte": "ventas"})

@app.route('/mis-pedidos')
@requiere_login  # Cualquier usuario autenticado
def mis_pedidos():
    # Solo devuelve los pedidos del usuario en sesión
    pedidos = db.execute(
        "SELECT * FROM pedidos WHERE usuario_id = ?",
        (session['user_id'],)
    ).fetchall()
    return jsonify([dict(p) for p in pedidos])
```

**Tabla de roles típicos en e-commerce:**
| Rol | Puede | No puede |
|---|---|---|
| cliente | Ver/editar su perfil, ver sus pedidos | Ver pedidos de otros, gestionar usuarios |
| vendedor | Ver todos los pedidos, actualizar estado | Eliminar usuarios, ver datos financieros |
| gerente | Ver reportes, gestionar vendedores | Eliminar datos, cambiar config del sistema |
| admin | Todo | (sin restricciones) |

**PREGUNTA AL GRUPO 5:** "¿Por qué es un error dar rol 'admin' a todos los desarrolladores en producción, aunque sea más conveniente para ellos?"

**RESPUESTA ESPERADA DETALLADA:** El principio de mínimo privilegio establece que cada entidad debe tener solo los permisos estrictamente necesarios para su función. Dar acceso admin a todos los desarrolladores en producción viola este principio por varias razones: (1) Superficie de ataque aumentada — si la cuenta de un desarrollador es comprometida (phishing, contraseña débil), el atacante obtiene acceso admin completo. (2) Error humano — un desarrollador con acceso de escritura puede borrar accidentalmente tablas en producción. (3) Auditoría imposible — si todos son admin, es imposible rastrear quién hizo qué cambio. La práctica correcta: acceso de solo lectura para monitoreo, acceso de escritura específico solo para las tablas que gestionan, acceso admin solo mediante herramientas auditadas y con autorización explícita.

**MINI ACTIVIDAD T5 (3 min):** El docente muestra este endpoint sin decorador:
```python
@app.route('/eliminar-usuario/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    conn = sqlite3.connect('app.db')
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    return jsonify({"eliminado": user_id})
```
Pregunta: "¿Qué decorador(es) agregarías y por qué?"
Respuesta: `@requiere_rol('admin')` — la eliminación de usuarios es la operación más destructiva y debe restringirse solo a admins. También se podría agregar un log de auditoría que registre quién eliminó qué usuario y cuándo.

---

**PREGUNTA INTEGRADORA (Grupo 6):** "Tenemos una aplicación con CSRF, contraseñas MD5 y sin RBAC. Si solo pudieran arreglar UN problema hoy, ¿cuál priorizarían y por qué?"

**RESPUESTA ESPERADA DETALLADA:** No hay una sola respuesta correcta — se evalúa el razonamiento técnico. Argumento para CSRF: en una aplicación financiera, el CSRF permite vaciar cuentas de usuarios activos en este momento — impacto inmediato y directo. Argumento para MD5: si la BD es comprometida (por SQLi u otro vector), todas las contraseñas quedan expuestas instantáneamente — afecta a TODOS los usuarios históricos. Argumento para RBAC: sin control de roles, cualquier usuario autenticado puede acceder a funcionalidades de admin — escalada de privilegios inmediata. El docente debe valorar la coherencia del argumento y que mencionen el impacto en usuarios reales.

---

# 4. RECESO (20 min) {#receso}

---

# 5. PRÁCTICA (40 min) {#practica}

## a) CASO PRÁCTICO GRUPAL (25 min)

**ESCENARIO: "BancoNacional.pe — Auditoría de Seguridad Urgente"**

El CTO de BancoNacional.pe los ha contratado como consultores de seguridad de emergencia. Han encontrado este código en el sistema de pagos en producción. Tienen 20 minutos para el análisis y 5 para la presentación.

```python
from flask import Flask, request, session, jsonify, redirect
import sqlite3, hashlib, os
import logging

app = Flask(__name__)
app.secret_key = "banco2024"
# Sin SESSION_COOKIE_SAMESITE
# Sin SESSION_COOKIE_HTTPONLY

# Credenciales de producción hardcodeadas
DB_PASS = "BancoAdmin2024"
DB_URL = f"postgresql://admin:{DB_PASS}@prod-db.banco.pe:5432/clientes"

logging.basicConfig(level=logging.DEBUG)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Hash MD5 de la contraseña
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    conn = sqlite3.connect('banco.db')
    # Consulta concatenada
    user = conn.execute(
        f"SELECT * FROM usuarios WHERE username='{username}' AND password_hash='{password_hash}'"
    ).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['rol'] = 'cliente'  # Siempre 'cliente' sin importar el rol real
        logging.debug(f"Login exitoso: user={username}, password={password}")
        return jsonify({"mensaje": "Login exitoso"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/transferir', methods=['POST'])
def transferir():
    if not session.get('user_id'):
        return redirect('/login')
    
    destino = request.form.get('destino')
    monto = request.form.get('monto')
    
    # Sin CSRF token, sin validación de monto
    conn = sqlite3.connect('banco.db')
    conn.execute(
        f"UPDATE cuentas SET saldo=saldo-{monto} WHERE usuario_id={session['user_id']}"
    )
    conn.execute(
        f"UPDATE cuentas SET saldo=saldo+{monto} WHERE numero='{destino}'"
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route('/admin/usuarios')
def listar_usuarios():
    # Sin verificación de rol — cualquier usuario autenticado puede acceder
    conn = sqlite3.connect('banco.db')
    usuarios = conn.execute(
        "SELECT id, username, password_hash, saldo, email FROM usuarios"
    ).fetchall()
    conn.close()
    return jsonify(usuarios)
```

**PREGUNTAS PARA LOS GRUPOS:**

1. Identifica TODAS las vulnerabilidades en el código (hay al menos 8). Para cada una: qué línea es, cuál es la vulnerabilidad, clasificación OWASP 2021, y severidad (Crítica/Alta/Media).

2. Construye el HTML completo del ataque CSRF que usaría un atacante para vaciar la cuenta de un usuario autenticado. ¿Dónde publicaría este HTML para que llegue a las víctimas?

3. El log registra `password={password}` en texto plano. ¿Qué riesgo específico genera esto además del problema evidente?

4. Reescribe las funciones `login()` y `transferir()` de forma segura.

5. ¿Qué impacto tendría en los clientes del banco si se explotan estas vulnerabilidades? ¿Viola alguna normativa peruana?

**PREGUNTAS DE ANDAMIAJE (docente circula y pregunta):**
- "¿Qué pasa si alguien envía `monto=-1000` en la transferencia?"
- "El `session['rol'] = 'cliente'` hardcodeado — ¿qué significa para los administradores del banco?"
- "Si el código está en GitHub, ¿qué pasa con el `DB_URL` con la contraseña?"

**PUESTA EN COMÚN — RESPUESTA MODELO:**

Vulnerabilidades encontradas:
1. `app.secret_key = "banco2024"` → Clave débil/hardcodeada → A02 Cryptographic Failures → CRÍTICO
2. `DB_PASS = "BancoAdmin2024"` + `DB_URL = f"postgresql://..."` → Credenciales hardcodeadas → A02 Cryptographic Failures → CRÍTICO
3. `hashlib.md5(password.encode()).hexdigest()` → Hash débil para contraseñas → A02 Cryptographic Failures → ALTO
4. `f"SELECT * FROM usuarios WHERE username='{username}'"` → SQL Injection → A03 Injection → CRÍTICO
5. `/transferir` sin CSRF token → CSRF en operación financiera → A01 Broken Access Control → CRÍTICO
6. `f"UPDATE cuentas SET saldo=saldo-{monto}"` → SQL Injection + sin validar monto (podría ser negativo) → A03 Injection → CRÍTICO
7. `/admin/usuarios` sin verificación de rol → Broken Access Control → A01 Broken Access Control → ALTO
8. `logging.debug(f"... password={password}")` → Contraseña en texto plano en logs → A02 Cryptographic Failures → ALTO
9. Sin `SESSION_COOKIE_SAMESITE` ni `SESSION_COOKIE_HTTPONLY` → A07 Identification Failures → MEDIO

HTML del ataque CSRF:
```html
<html>
<body onload="document.forms[0].submit()">
  <form action="https://banco.pe/transferir" method="POST" style="display:none">
    <input type="hidden" name="destino" value="cuenta-atacante-123456">
    <input type="hidden" name="monto" value="10000">
  </form>
  <p>Cargando tu estado de cuenta...</p>
</body>
</html>
```

login() y transferir() corregidos (incluir código completo con bcrypt, consultas parametrizadas, CSRF token, validación de monto).

---

## b) EJERCICIO INDIVIDUAL (15 min)

Completa los TODOs en este esqueleto de Flask:

```python
import secrets, bcrypt, os
from flask import Flask, request, session, jsonify
from functools import wraps

app = Flask(__name__)
# TODO 1: Leer SECRET_KEY de os.environ o generar con secrets.token_hex(32)
app.secret_key = "COMPLETAR"

# TODO 2: Configurar SESSION_COOKIE_HTTPONLY=True, SECURE=True, SAMESITE='Strict'

def requiere_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # TODO 3: Verificar autenticación (401 si no hay user_id)
            # TODO 4: Verificar que session['rol'] está en roles (403 si no)
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    import sqlite3
    conn = sqlite3.connect('app.db')
    # TODO 5: Consulta parametrizada (no f-string con username)
    user = None  # COMPLETAR
    conn.close()
    if user:
        # TODO 6: bcrypt.checkpw() para verificar contraseña
        # TODO 7: session.clear() antes de guardar datos (previene Session Fixation)
        session['user_id'] = user[0]
        session['rol'] = user[2]
        session['csrf_token'] = secrets.token_hex(32)
        return jsonify({"ok": True})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/transferir', methods=['POST'])
@requiere_login
def transferir():
    # TODO 8: Validar CSRF token desde session
    # TODO 9: Validar que monto es float > 0
    # TODO 10: Consultas parametrizadas para UPDATE
    pass
```

**Criterio de éxito:** El código no tiene f-strings con datos del usuario en SQL, usa bcrypt.checkpw(), valida el CSRF token, y tiene los decoradores configurados correctamente.

---

# 6. CIERRE (10 min) {#cierre}

## a) SÍNTESIS COLABORATIVA (4 min)

**Pregunta 1:** "¿Cuál es la diferencia fundamental entre CSRF y XSS?"

**Respuesta esperada:** XSS inyecta código malicioso EN el sitio víctima — el script se ejecuta en el navegador de la víctima dentro del contexto del sitio legítimo. CSRF usa el sitio víctima como intermediario — fuerza al navegador a hacer peticiones autenticadas SIN inyectar código en él. En XSS el atacante controla código que corre en el sitio; en CSRF el atacante controla peticiones que se originan desde otro sitio.

**Pregunta 2:** "¿Por qué MD5 y SHA-256 son inseguros para contraseñas aunque sean funciones criptográficas respetadas?"

**Respuesta esperada:** Son inseguros para contraseñas específicamente porque son diseñados para ser rápidos — en una GPU moderna pueden computarse miles de millones de hashes por segundo. Esto hace que ataques de fuerza bruta contra contraseñas comunes sean trivialmente rápidos. bcrypt/Argon2 son intencionalmente lentos y tienen salt automático, haciendo la fuerza bruta impráctica.

**Pregunta 3:** "¿Cuál es la diferencia entre autenticación y autorización, y cómo se relaciona con RBAC?"

**Respuesta esperada:** Autenticación verifica identidad: "¿Quién eres?" (login, contraseña, MFA). Autorización verifica permisos: "¿Qué puedes hacer?" (roles, ACLs). RBAC es un sistema de autorización: una vez autenticado, el rol del usuario determina qué acciones puede ejecutar.

## b) METACOGNICIÓN (3 min)

*"En silencio, respondan mentalmente: ¿Cuál de los tres temas de hoy (CSRF, contraseñas seguras, RBAC) me genera más dudas? ¿Pude completar el ejercicio individual? Si no completé algún TODO, ¿cuál fue el obstáculo? Esas dudas son exactamente las preguntas de la guía de trabajo para esta semana."*

## c) TAREA / PUENTE (3 min)

*"La semana que viene veremos Seguridad en APIs REST y autenticación con tokens JWT — que es el siguiente paso natural: en lugar de cookies de sesión, los sistemas modernos usan tokens firmados digitalmente. Verán cómo JWT resuelve algunos problemas de CSRF pero introduce nuevos desafíos. La tarea para hoy: completar la guía de trabajo S7 y el laboratorio en casa, que incluyen implementar la versión segura de TiendaApp con los 13 TODOs. Los entregables están en el repositorio del curso, carpeta semana-07/."*

---

# GUION VERBAL SUGERIDO {#guion-verbal}

**Momento 1 — Al explicar el ataque CSRF:**
*"Imaginen que tienen un empleado muy obediente que hace todo lo que le digan sin preguntar de dónde vienen las órdenes. Si alguien les envía una orden firmada con el sello de la empresa, la ejecuta. CSRF explota exactamente esa obediencia del navegador: el navegador siempre envía las cookies del dominio, sin preguntar si la petición fue iniciada por el usuario o por JavaScript de otro sitio."*

**Momento 2 — Al mostrar el HTML del ataque:**
*"Este formulario de 5 líneas, alojado en evil.com, puede vaciar la cuenta bancaria de cualquier persona que tenga una sesión activa en banco.com. No necesita JavaScript avanzado. No necesita que la víctima haga nada. Solo cargar la página. Eso es CSRF: la simplicidad del ataque vs. el impacto devastador."*

**Momento 3 — Al explicar bcrypt:**
*"MD5 convierte 'password123' siempre en el mismo hash — es determinístico. Una tabla con los 10 millones de contraseñas más comunes y sus MD5 cabe en 10GB. Buscar el hash de la víctima tarda microsegundos. bcrypt agrega un salt único para cada usuario y hace que el cálculo tarde 250ms intencionalmente. Eso suena poco, pero convierte un ataque que tomaría horas en uno que tomaría siglos."*

**Momento 4 — Al explicar variables de entorno:**
*"Las credenciales hardcodeadas en el código son una bomba de tiempo. Un día, alguien sube el repositorio a GitHub por error, o un colaborador nuevo tiene acceso al código, o el repositorio es comprometido. Con variables de entorno, las credenciales solo existen en el servidor de producción — nunca en el código."*

**Momento 5 — Al cerrar la sesión:**
*"Hoy vieron tres vulnerabilidades que forman una cadena de ataque. CSRF permite ejecutar acciones sin autorización del usuario. Contraseñas débiles permiten al atacante escalar a más cuentas cuando obtiene la BD. Sin RBAC, cualquier cuenta comprometida da acceso total. La seguridad siempre es en capas: cada control que implementan agrega una capa que el atacante debe superar."*

---

# CASOS REALES RECOMENDADOS {#casos-reales}

**1. ING Direct — CSRF Financiero (2008)**
Un investigador de seguridad descubrió que ING Direct era vulnerable a CSRF en su sistema de transferencias. Mediante una página web especialmente construida, era posible transferir fondos desde la cuenta de cualquier cliente autenticado. ING tuvo que implementar tokens CSRF y re-educar a su equipo de desarrollo. Fuente: Grossman, J. (2008). WhiteHat Security.

**2. Equifax — Breach de Datos (2017)**
147 millones de registros expuestos incluyendo nombres, SSN, fechas de nacimiento y números de tarjeta. La causa raíz fue una combinación de vulnerabilidades incluyendo credenciales de administrador débiles y falta de encriptación de datos sensibles. Multa total: $575 millones USD. Clasificación: A02:2021 Cryptographic Failures. Fuente: FTC Settlement Report, 2019.

**3. LinkedIn — Hashes SHA1 sin Salt (2012)**
6.5 millones de hashes SHA1 sin salt fueron publicados en foros de hackers. El 90% fueron crackeados en 24 horas usando GPUs con diccionarios de contraseñas comunes. Posteriormente se reveló que el número real era 117 millones. Fuente: LeakedSource analysis, 2016.

**4. Adobe — DES Reversible (2013)**
153 millones de contraseñas fueron almacenadas con DES (modo ECB) — técnicamente cifrado, no hash, pero reversible. Adobe además almacenó pistas de contraseña en texto plano junto a cada registro, haciendo trivial el descifrado. Fuente: Krebs on Security, 2013.

**5. GitHub — CSRF en Funcionalidad Crítica (2013)**
Un investigador descubrió que el mecanismo de CSRF de GitHub era bypasseable mediante ataques de DNS rebinding. Esto permitía que scripts maliciosos en el mismo subdominio ejecutaran acciones autenticadas. GitHub parcheó inmediatamente y pagó un bug bounty. Fuente: HackerOne report, 2013.

---

# EVALUACIÓN FORMATIVA {#evaluacion-formativa}

**Durante el rompe-hielo:** Observar si los estudiantes mencionan "cookies" espontáneamente al explicar cómo funciona el ataque — indica conocimiento previo de gestión de sesiones.

**Durante T1:** En la mini actividad del `<img src>`, los estudiantes que identifican que el problema es "GET para modificar estado" tienen comprensión arquitectural profunda.

**Durante T2:** Al explicar CSRF tokens, verificar que los estudiantes entienden POR QUÉ el atacante no puede conocer el token (no es porque esté cifrado — es porque nunca viaja al dominio del atacante).

**Durante T3:** Señal de comprensión avanzada: el estudiante menciona "timing attacks" al discutir por qué siempre hacer el checkpw aunque el usuario no exista.

**Durante la práctica grupal:** El grupo que identifica la vulnerabilidad del `session['rol'] = 'cliente'` hardcodeado es el más avanzado — es la vulnerabilidad más sutil.

**Señal de alarma:** Si un grupo propone "validar que el formulario vino de la misma página" verificando el campo Referer como ÚNICA defensa — necesita refuerzo sobre por qué Referer puede ser falsificado o estar ausente.

**Al cierre:** Las tres preguntas de síntesis son el formative assessment — el que no puede distinguir autenticación de autorización no dominó T5.

---

# REFERENCIAS APA 7 {#referencias}

OWASP Foundation. (2021). *OWASP Top Ten 2021: A01 Broken Access Control*. https://owasp.org/Top10/A01_2021-Broken_Access_Control/

OWASP Foundation. (2021). *OWASP Top Ten 2021: A02 Cryptographic Failures*. https://owasp.org/Top10/A02_2021-Cryptographic_Failures/

OWASP Foundation. (2023). *Cross-Site Request Forgery Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

Provos, N., & Mazières, D. (1999). *A future-adaptable password scheme*. Proceedings of the FREENIX Track of the 1999 USENIX Annual Technical Conference. https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf

IBM Security. (2023). *Cost of a Data Breach Report 2023*. IBM Corporation. https://www.ibm.com/reports/data-breach

National Institute of Standards and Technology. (2017). *Digital Identity Guidelines: Authentication and Lifecycle Management* (NIST Special Publication 800-63B). https://pages.nist.gov/800-63-3/sp800-63b.html

Stuttard, D., & Pinto, M. (2011). *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws* (2nd ed.). Wiley.

HackerOne. (2023). *The 2023 Hacker-Powered Security Report*. https://www.hackerone.com/resources/reporting/the-2023-hacker-powered-security-report

---

# RECURSOS REALES {#recursos}

**Documentación oficial:**
- OWASP CSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Flask-WTF CSRF Documentation: https://flask-wtf.readthedocs.io/en/stable/csrf.html
- Python bcrypt library: https://github.com/pyca/bcrypt
- python-dotenv: https://github.com/theskumar/python-dotenv

**Herramientas gratuitas:**
- CrackStation (demostración de hashes débiles): https://crackstation.net
- Have I Been Pwned (verificar si una contraseña fue expuesta): https://haveibeenpwned.com
- PortSwigger Web Security Academy — CSRF labs: https://portswigger.net/web-security/csrf
- GitGuardian (detecta secretos en repositorios): https://www.gitguardian.com

**Repositorios GitHub:**
- Flask-WTF (CSRF automático en Flask): https://github.com/wtforms/flask-wtf
- OWASP WebGoat (app vulnerable para aprender): https://github.com/WebGoat/WebGoat
- PayloadsAllTheThings — CSRF: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CSRF%20Injection

---

*Fin de la sesión — Semana 7 | Universidad Autónoma del Perú | Programación Segura DD281*
