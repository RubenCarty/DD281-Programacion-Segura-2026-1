# S3 — GUÍA DE TRABAJO DEL ESTUDIANTE
## Autenticación, Gestión de Cookies y Niveles de Acceso

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) — Semana 3 |
| **Nombre del estudiante** |Javier Flores Condeña |
| **Código** | Grupo 1 |
| **Fecha de entrega** | 17/06/26 |
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

**Respuesta: [ b]** 

---

**Pregunta 2** *(Básica)*
¿Cuál de los siguientes mecanismos es el MÁS SEGURO para almacenar el session ID de un usuario?

- a) `localStorage` del navegador
- b) `sessionStorage` del navegador
- c) Cookie con atributos `HttpOnly` y `Secure`
- d) Variable global de JavaScript en el cliente

**Respuesta: [ c]** 
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

Usa las palabras del banco: `HttpOnly` / `session.clear()` / `servidor` / `Secure` / `RBAC` / `SameSite` / `session_id` / `stateless`

1. HTTP es un protocolo **stateless** porque no recuerda peticiones anteriores entre cliente y servidor.

2. El atributo **Secure** garantiza que la cookie de sesión no sea transmitida sobre conexiones HTTP no cifradas.

3. El modelo de control de acceso **RBAC** asigna permisos a través de roles, no directamente a usuarios individuales.

4. En un logout correcto, además de eliminar la cookie del cliente, el **servidor** debe invalidar el session ID en su propio almacén.

5. Para prevenir Session Fixation, después de una autenticación exitosa se debe ejecutar **session.clear()** para limpiar la sesión previa.

---

### B2 — Relacionar columnas (10 puntos)

Relaciona cada atributo/concepto (columna A) con su descripción correcta (columna B).

| Columna A | | Columna B |
|---|---|---|
| 1. `HttpOnly` | c | a) Controla si la cookie se envía en peticiones cross-site |
| 2. `Secure` | f | b) El servidor no puede recordar peticiones anteriores |
| 3. `SameSite=Lax` | a | c) Previene que JavaScript lea el valor de la cookie |
| 4. Session Hijacking | e | d) El atacante forza un session ID conocido antes del login |
| 5. Session Fixation | d | e) Robo de un session ID válido para suplantar al usuario |
| 6. Stateless | b | f) La cookie solo viaja sobre conexiones HTTPS |
| 7. Mínimo Privilegio | h | g) Conjunto de permisos asignados a un tipo de usuario |
| 8. Rol | g | h) Cada usuario tiene solo los permisos que necesita |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN (30 puntos)

*Responde con párrafos completos de 3-5 líneas. No uses listas en esta sección.*

---

**Pregunta C1 (10 puntos)**
Un compañero propone guardar el session ID del usuario en `localStorage` porque "es más fácil acceder a él desde JavaScript". Explica por qué esta decisión es un riesgo de seguridad y cuál sería la alternativa correcta con sus fundamentos técnicos.

*Respuesta:*

Guardar el session ID en `localStorage` es riesgoso porque cualquier script JavaScript que se ejecute en la página, incluyendo uno inyectado mediante XSS, puede leerlo y enviarlo a un atacante. Si el atacante obtiene ese identificador, puede secuestrar la sesión del usuario. La alternativa correcta es almacenar el identificador en una cookie con los atributos `HttpOnly`, `Secure` y `SameSite`, reduciendo significativamente la exposición frente a XSS y CSRF.

---

**Pregunta C2 (10 puntos)**
Compara el ataque **Session Hijacking** con el ataque **Session Fixation**: en qué se diferencian en su mecánica, qué tienen en común en su objetivo final, y cuál es la medida técnica específica que previene cada uno.

*Respuesta:*

Session Hijacking consiste en robar un session ID válido después de que el usuario se autentica, mientras que Session Fixation busca que la víctima utilice un session ID conocido previamente por el atacante. Ambos ataques tienen como objetivo tomar control de una sesión legítima. El primero se previene con cookies seguras, HTTPS y protección contra XSS; el segundo regenerando el session ID tras el inicio de sesión y eliminando sesiones previas.

---

**Mini caso de análisis — Para preguntas C3a y C3b**

> El equipo de desarrollo de **RetailFácil** (una tienda online peruana) implementó el siguiente sistema de autenticación:
>
> - Al hacer login, el servidor crea una cookie: `Set-Cookie: uid=456; role=comprador; Path=/`
> - Los precios se envían como campos ocultos en el formulario: `<input type="hidden" name="precio" value="299.00">`
> - Al hacer clic en "pagar", el backend lee `request.form['precio']` y procesa ese valor como el precio real
> - La sesión no tiene tiempo de expiración configurado

**Pregunta C3a (5 puntos)**
Identifica los problemas de seguridad presentes en el diseño de RetailFácil y explica cómo cada uno podría ser explotado por un atacante.

*Respuesta:*

RetailFácil presenta varios problemas de seguridad. El rol del usuario se almacena en una cookie manipulable por el cliente, permitiendo escalamiento de privilegios. El precio se recibe desde un campo oculto que puede modificarse con DevTools para pagar menos. Además, la sesión no expira, aumentando el riesgo de secuestro de sesión y accesos no autorizados.

**Pregunta C3b (5 puntos)**
Propón cómo debería reimplementarse este sistema de manera segura, explicando el principio de seguridad que aplica en cada corrección.

*Respuesta:*

El rol debe gestionarse exclusivamente en el servidor mediante RBAC y nunca confiar en datos enviados por el cliente. Los precios deben consultarse desde la base de datos usando el identificador del producto. También se debe configurar expiración de sesión, regeneración de identificadores y cookies con atributos `HttpOnly`, `Secure` y `SameSite`.

---

## SECCIÓN D — PREGUNTAS AVANZADAS Y DE CASO (30 puntos)

---

### Caso profesional (15 puntos)

> **SaludNet Perú** es una startup de telemedicina que permite a pacientes ver sus resultados de laboratorio y a médicos acceder a historias clínicas. El sistema usa una cookie de sesión sin `HttpOnly` ni `Secure`. El sistema tiene tres tipos de usuarios: paciente, médico y administrador.
>
> Un auditor de seguridad detectó que un médico puede acceder a la historia clínica de cualquier paciente simplemente cambiando el parámetro en la URL: `/historia?paciente_id=1023` → `/historia?paciente_id=1024`. También encontró que la cookie de sesión puede leerse con JavaScript y que el sistema funciona sobre HTTP sin redirigir a HTTPS.

**Pregunta D1 (5 puntos)**
¿Qué vulnerabilidades del OWASP Top 10 están presentes en SaludNet Perú? Nómbralas por su código y nombre, y explica brevemente cómo se manifiesta cada una en el caso.

*Respuesta:*

Se observa A01:2021 Broken Access Control porque un médico puede acceder a historias clínicas de otros pacientes modificando un parámetro de la URL. También existe A07:2021 Identification and Authentication Failures debido a una gestión insegura de sesiones. Adicionalmente, la ausencia de HTTPS y de atributos seguros en las cookies facilita el robo de sesiones y la exposición de información sensible.

**Pregunta D2 (5 puntos)**
Diseña el esquema RBAC completo para SaludNet Perú: define los roles necesarios y los permisos específicos de cada uno. Luego escribe el pseudocódigo o código Python del decorador que verificaría el acceso antes de mostrar una historia clínica.

*Respuesta:*

Roles: Paciente (ver su propia información), Médico (ver historias de pacientes asignados) y Administrador (gestión total del sistema). El decorador debe validar que el usuario autenticado posea el rol requerido antes de permitir el acceso.

```python
def requiere_rol(*roles):
    def decorador(f):
        def wrapper(*args, **kwargs):
            if session.get("rol") not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorador
```


**Pregunta D3 (5 puntos)**
Si un médico puede leer la cookie de sesión de un paciente mediante una vulnerabilidad XSS, ¿cómo puede un atacante usar esa cookie para acceder al sistema como ese paciente? Describe el ataque paso a paso y qué atributo de cookie lo hubiera prevenido.

*Respuesta:*

Si existe una vulnerabilidad XSS, un atacante puede ejecutar JavaScript que lea la cookie de sesión del paciente y la envíe a un servidor bajo su control. Luego puede cargar esa cookie en su navegador y acceder al sistema como la víctima. El atributo `HttpOnly` habría impedido que JavaScript accediera al valor de la cookie.

---

**Pregunta D4 — Diseño y propuesta (8 puntos)**
> "¿Cómo implementarías la gestión de sesiones para un sistema bancario en Flask que debe cumplir estos requisitos: sesión que expira a los 15 minutos de inactividad, cookie segura contra XSS y CSRF, logout que invalide la sesión en el servidor, y RBAC con roles cliente/operador/admin?"

Escribe el código Python/Flask completo que implementa esa gestión. Comenta cada decisión de seguridad.

*Código:*

```python
from flask import Flask, session, redirect, request, abort
from functools import wraps
from datetime import timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=15),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Strict"
)

sesiones_activas = {}

def requiere_rol(*roles):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("rol") not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorador

@app.route("/login")
def login():
    session.clear()
    session["user_id"] = 1
    session["rol"] = "cliente"
    session.permanent = True
    token = secrets.token_urlsafe(32)
    sesiones_activas[token] = session["user_id"]
    session["token"] = token
    return "OK"

@app.route("/logout")
def logout():
    token = session.get("token")
    if token in sesiones_activas:
        del sesiones_activas[token]
    session.clear()
    return redirect("/")

@app.route("/admin")
@requiere_rol("admin")
def admin():
    return "Panel Administrador"
```

---

**Pregunta D5 — Pensamiento crítico (7 puntos)**
> "¿Qué pasaría si un sistema implementa HttpOnly y Secure en las cookies, pero guarda el session ID con baja entropía (ej: un número secuencial como session_id=1001, 1002, 1003...)?"

Explica el tipo de ataque que esto habilitaría, cómo lo ejecutaría un atacante, y cuál es el estándar correcto para generar session IDs seguros.

*Respuesta:*

Un session ID secuencial permite ataques de predicción o fuerza bruta sobre sesiones activas. Un atacante podría probar identificadores consecutivos hasta encontrar una sesión válida y asumir la identidad de otro usuario. Los session ID deben generarse mediante generadores criptográficamente seguros, con alta entropía y valores aleatorios imposibles de predecir.

---

*Universidad Autónoma del Perú — DD281 Programación Segura — Semana 3 — 2026-1*
