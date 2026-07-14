# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO
## Programación Segura (DD281)

---

**Nombre del estudiante: OMAR RIVERA CASTILLO

**Grupo / Sección: 02
**Fecha:** 14/06/2026

**Instrucciones generales:**
- Completa esta guía durante la sesión de clase en los momentos indicados por el docente.
- Sección A y B: durante la primera hora.
- Sección C y D: durante la segunda hora (después del receso).
- Sección E: actividad grupal práctica.
- Sección F: cierre y metacognición.

---

# SECCIÓN A — RECUPERACIÓN DE APRENDIZAJES (Semana 1)
## Responde antes de que el docente lo explique. Luego verifica tu respuesta.

---

### A.1 LA TRIADA CIA APLICADA AL LOGIN

Completa la tabla con la aplicación de cada pilar de la triada CIA al sistema de login:

| Pilar CIA | ¿Cómo se manifiesta en un sistema de login? | Ejemplo concreto |
|---|---|---|
| **Confidencialidad** |Garantiza que las credenciales de acceso (usuario y contraseña) e identificadores de sesión no sean expuestos a terceros no autorizados durante el tránsito o almacenamiento. | Uso de TLS 1.3 para cifrar el canal de comunicación y almacenamiento de contraseñas mediante hashing con sal.|
| **Integridad** | Asegura que las credenciales o los tokens de sesión no sean alterados o manipulados maliciosamente durante su trayecto o validación en el servidor.|Empleo de JSON Web Tokens (JWT) firmados criptográficamente con un algoritmo como RS256 para evitar la suplantación de identidad. |
| **Disponibilidad** | Garantiza que el servicio de autenticación permanezca accesible y funcional para los usuarios legítimos, incluso bajo ataques de denegación de servicio.|Implementación de Rate Limiting (limitación de tasa) por IP y captcha para mitigar ataques de fuerza bruta o de denegación de servicio (DoS). |

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

Marca con ✓ las vulnerabilidades OWASP que se relacionan directamente con un login inseguro y explica brevemente por qué:

| # | Vulnerabilidad OWASP | ¿Relacionada con login? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | ☐X Sí ☐ No |Si el mecanismo de login genera un token de sesión predecible o mal estructurado |
| A02 | Cryptographic Failures | ☐X Sí ☐ No | Directamente relacionada. Ocurre si el login transmite credenciales por HTTP en texto plano, utiliza algoritmos obsoletos como MD5 o guarda contraseñas sin sal.|
| A03 | Injection | ☐ XSí ☐ No |Los campos de entrada del formulario de login (username / password) son vectores clásicos para ataques de SQL Injection (SQLi) si los datos no se sanitizan ni se usan consultas preparadas. |
| A04 | Insecure Design | ☐X Sí ☐ No | Se presenta si el flujo de autenticación carece estructuralmente de mecanismos defensivos esenciales desde su concepción.|
| A07 | Identification/Auth Failures | ☐X Sí ☐ No | Es la categoría núcleo del login. Incluye la permisión de contraseñas sumamente débiles, vulnerabilidad a credential stuffing (relleno de credenciales) y falta de invalidación de sesiones tras el logout.|

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

¿Cómo aplicarías el principio de Mínimo Privilegio a un sistema de autenticación? Escribe al menos 3 aplicaciones concretas:

1. Restricción de privilegios en la conexión a la Base de Datos

2.Uso de Roles y Ámbitos Mínimos post-autenticación
3. Segregación de funciones del propio servicio de login
---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

Escribe todo lo que se te ocurra:

1. Guardar contraseñas en texto plano o con algoritmos obsoletos (MD5, SHA-1).
2. Enviar los datos mediante el método HTTP GET o usar HTTP sin cifrar en lugar de HTTPS.
3. Permitir un número infinito de intentos de inicio de sesión (vulnerable a fuerza bruta).
4. Mostrar mensajes de error demasiado específicos como "El usuario existe pero      la contraseña es incorrecta".
5. No implementar un segundo factor de autenticación (MFA/2FA) para cuentas críticas.
6. Reutilizar tokens de sesión perpetuos que no expiran por inactividad.

*(Al final de la clase volveremos a esta lista para ver cuánto más podemos agregar)*

---

### B.2 PREGUNTAS DE DIAGNÓSTICO

Responde con lo que ya sabes (marca la opción más correcta):

**B.2.1** ¿Cómo se deben almacenar las contraseñas en una base de datos?

- ☐ a) En texto plano para facilitar la recuperación
- ☐ b) Cifradas con AES-256 para poder descifrarlas si el usuario las olvida
- ☐X c) Como hash unidireccional con sal aleatoria
- ☐ d) Codificadas en Base64 para "ofuscarlas"

**B.2.2** ¿Qué versión de TLS/SSL deben usar los servidores web en 2024?

- ☐ a) SSL 3.0 — es la versión estándar
- ☐ b) TLS 1.0 — compatible con todos los dispositivos
- ☐X c) TLS 1.2 mínimo, preferiblemente TLS 1.3
- ☐ d) La versión no importa, cualquier SSL es suficiente

**B.2.3** ¿Qué es un certificado SSL autofirmado (self-signed)?

- ☐ a) Un certificado gratuito de Let's Encrypt
- ☐X b) Un certificado creado por uno mismo sin validación de una CA externa
- ☐ c) Un certificado de mayor seguridad que el emitido por una CA
- ☐ d) El tipo de certificado requerido en producción

---

# SECCIÓN C — CONCEPTOS CLAVE DE LA SESIÓN
## Completa durante la explicación del docente

---

### C.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD

**C.1.1** Escribe con tus propias palabras qué es una especificación formal de seguridad:

Una especificación formal de seguridad es un documento técnico y normativo preciso que define exactamente las reglas de seguridad, los mecanismos tecnológicos, las restricciones de acceso y los procedimientos de respuesta ante incidentes que rigen un sistema, eliminando cualquier ambigüedad en su implementación.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

| | Ejemplo A | Ejemplo B |
|---|---|---|
| **Texto** | "El login debe ser seguro" | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** | Es un requerimiento ambiguo, subjetivo y carente de métricas técnicas. No especifica mecanismos, algoritmos ni directrices claras para el desarrollador.|Define de forma exacta, cuantitativa y verificable el algoritmo de seguridad (bcrypt), el parámetro de configuración (cost=12) y la regla de control de acceso ante fallos recurrentes. |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente | ¿Qué define? |
|---|---|---|
| 1 | **Activos** | Los elementos de valor a proteger (credenciales, tokens de sesión, datos sensibles del usuario)|
| 2 | **Sujetos** |Las entidades e identidades que interactúan con el sistema (Usuarios finales, Administradores, API clients). |
| 3 | **Objetos** | Los recursos del sistema sobre los cuales los sujetos desean realizar acciones (Base de datos de usuarios, endpoints de autenticación).|
| 4 | **Operaciones** | Las acciones explícitamente permitidas o prohibidas (Iniciar sesión, restablecer contraseña, refrescar token).|
| 5 | **Condiciones** | Las restricciones bajo las cuales se permiten las operaciones (Horarios, origen de IP, validación previa de MFA).|
| 6 | **Mecanismos** | Las tecnologías y configuraciones específicas aplicadas para asegurar el sistema (Algoritmo Argon2id, TLS 1.3, HTTPS).|
| 7 | **Respuesta ante violación** | Las contramedidas automatizadas y registros que se ejecutan al detectar anomalías o ataques (Bloqueo de cuenta, logs SIEM).|

---

### C.2 PREGUNTAS PARA MARCAR (Selección múltiple)

Marca la respuesta correcta. Solo hay una opción correcta por pregunta.

**C.2.1** ¿Cuál es el problema de almacenar contraseñas con SHA-1 SIN SAL?

- ☐ a) SHA-1 no produce un hash — produce texto cifrado
- ☐ b) SHA-1 es reversible — se puede obtener la contraseña original
- ☐Xc) Los atacantes pueden usar tablas rainbow precomputadas para romper el hash
- ☐ d) SHA-1 produce hashes demasiado cortos para ser seguros

**C.2.2** ¿Qué ventaja fundamental tiene bcrypt sobre SHA-256 para almacenar contraseñas?

- ☐ a) Bcrypt produce hashes más largos que SHA-256
- ☐Xb) Bcrypt incluye automáticamente sal aleatoria y es intencionalmente lento
- ☐ c) Bcrypt es un algoritmo de cifrado, no de hash
- ☐ d) Bcrypt es más rápido que SHA-256, mejorando el rendimiento del login

**C.2.3** ¿Qué es la "sal" (salt) en el contexto del hashing de contraseñas?

- ☐ a) Un algoritmo de cifrado adicional aplicado al hash
- ☐ b) La clave secreta usada para cifrar el hash antes de almacenarlo
- ☐X c) Un valor aleatorio único por usuario que se concatena a la contraseña antes de hashear
- ☐ d) El factor de coste que determina cuántas rondas de hashing se ejecutan

**C.2.4** ¿Por qué es un error de seguridad grave que el formulario de login use el método HTTP GET?

- ☐ a) Porque GET no puede transportar datos de texto
- ☐X b) Porque los parámetros GET viajan en la URL y quedan en logs del servidor y en el historial del navegador
- ☐ c) Porque GET es más lento que POST para transferir datos
- ☐ d) Porque GET no cifra los datos antes de enviarlos

**C.2.5** ¿Qué es Perfect Forward Secrecy (PFS) en TLS?

- ☐ a) Un mecanismo que cifra el certificado del servidor con una segunda clave
- ☐ b) La capacidad del servidor de descifrar tráfico pasado si se compromete la clave privada
- ☐X c) El uso de claves de sesión efímeras para que el compromiso de la clave privada del servidor no permita descifrar tráfico pasado
- ☐ d) La verificación automática de que el certificado SSL no ha expirado

**C.2.6** ¿Cuál de los siguientes es el estándar de hash de contraseñas más recomendado hoy?

- ☐ a) MD5 con sal de 16 bytes
- ☐ b) SHA-512 sin sal
- ☐X c) bcrypt (factor 12+) o argon2id
- ☐ d) AES-256 con clave de 32 bytes

**C.2.7** ¿Cuál de las siguientes configuraciones de servidor web es correcta en relación a SSL?

- ☐ a) Habilitar SSL 3.0, TLS 1.0, TLS 1.1 y TLS 1.2 para máxima compatibilidad
- ☐ b) Usar solo TLS 1.3 y deshabilitar todas las versiones anteriores
- ☐ c) Deshabilitar SSL 2.0 y SSL 3.0, mantener TLS 1.0, 1.1, 1.2 y 1.3
- ☐X d) Usar TLS 1.2 y TLS 1.3, deshabilitar versiones anteriores

**C.2.8** ¿Qué es CGI (Common Gateway Interface)?

- ☐ a) Un framework de Python para desarrollo web seguro
- ☐X b) Un protocolo estándar que define cómo un servidor web pasa solicitudes a programas externos para generar respuestas dinámicas
- ☐ c) Una librería de JavaScript para crear formularios de login
- ☐ d) Un tipo de certificado SSL para servidores compartidos

**C.2.9** Un atacante ejecuta el siguiente input en el campo de usuario de un login CGI inseguro: `admin' --`. ¿Qué tipo de ataque es este y qué efecto tendría?

- ☐ a) XSS — inyecta código JavaScript en la página
- ☐X b) SQL Injection — el `'--` cierra la query y comenta el resto, posiblemente bypasseando la verificación de contraseña
- ☐ c) CSRF — falsifica una solicitud de otro dominio
- ☐ d) Path Traversal — intenta acceder a archivos del sistema

**C.2.10** ¿Cuál es el propósito del header HTTP `Strict-Transport-Security`?

- ☐ a) Obliga al servidor a responder solo con JSON
- ☐ b)X Le indica al navegador que siempre use HTTPS para ese dominio, incluso si el usuario escribe HTTP
- ☐ c) Restringe el origen de las solicitudes al dominio del servidor
- ☐ d) Cifra automáticamente todos los cookies del servidor

---

### C.3 PREGUNTAS DE COMPLETAR

Completa los espacios en blanco con la palabra o frase correcta:

**C.3.1** El proceso de almacenamiento de contraseñas usa hashing (no cifrado), porque es un proceso unidireccional que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor aleatorio y único  por usuario que elimina la posibilidad de usar tablas rainbow precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de PFS (siglas), lo que significa que si la clave privada del servidor se compromete, el tráfico histórico / pasado no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la entrada estándar del script, mientras que los parámetros GET llegan en la variable de entorno QUERY_STRING..

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el 301.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama Mínimo Privilegio.

**C.3.7** Un certificado SSL autofirmado (autofirmado) es apropiado para entornos de desarrollo y pruebas internas, pero NO para producción porque los navegadores muestran una advertencia de seguridad.

**C.3.8** La organización OWASP clasifica como A07 los fallos de Identificación y Autenticación, que incluyen contraseñas débiles, ausencia de MFA y sesiones que no expiran.

---

# SECCIÓN D — PREGUNTAS DE ANÁLISIS

### Nivel Intermedio

**D.1** Lee el siguiente fragmento de código Python CGI. Identifica y describe **5 vulnerabilidades** de seguridad específicas que contiene:

```python
#!/usr/bin/env python3
import cgi
import pymysql

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
user = form.getvalue("user")
pwd  = form.getvalue("pwd")

conn = pymysql.connect(host="db.empresa.com", user="admin", 
                       password="Admin@2024!", database="empresa")
cursor = conn.cursor()
sql = f"SELECT * FROM empleados WHERE usuario='{user}' AND clave='{pwd}'"
cursor.execute(sql)
row = cursor.fetchone()

if row:
    print(f"<h1>Acceso concedido a: {user}</h1>")
    print(f"<p>Datos del empleado: {row}</p>")
else:
    print(f"<h1>Acceso denegado. Usuario: {user} no existe.</h1>")
conn.close()
```

| # | Vulnerabilidad identificada | Descripción del riesgo | Cómo corregirla |
|---|---|---|---|
| 1 | Inyección SQL (SQLi)|Al concatenar variables (f"...") directo en la consulta SQL, un atacante puede ingresar admin' -- saltándose por completo la verificación de contraseña. |Usar consultas preparadas (parameterized queries) pasándole los argumentos como tupla al método cursor.execute(). |
| 2 |Almacenamiento de claves en texto plano | La consulta busca la clave directamente por coincidencia de texto, infiriendo que la base de datos guarda los passwords expuestos.| Hashear las contraseñas con bcrypt o Argon2id antes de guardarlas y usar funciones de verificación segura en el login.|
| 3 |Exposición de Credenciales Críticas (Hardcoded) | Las credenciales de la BD (user="admin", password="Admin@2024!") están escritas directamente en el código fuente, expuestas a fugas de repositorios.| Mover las credenciales a variables de entorno (.env) y cargarlas dinámicamente con un gestor de secretos de forma externa.|
| 4 | Cross-Site Scripting (XSS) Reflejado|Imprime la variable user directamente en el HTML de respuesta sin sanitizar. Un atacante puede inyectar código JavaScript malicioso. | Escapar y sanitizar las salidas HTML utilizando la librería nativa html.escape(user) antes de renderizarlas en pantalla.|
| 5 |Fuga de Información (Information Disclosure) | Al imprimir la estructura interna de la fila devuelta (f"{row}"), expone nombres de columnas y datos internos al cliente.| Limitar la salida de datos. Enviar únicamente un mensaje genérico de éxito y estructurar un objeto de sesión controlado sin datos crudos.|

---

**D.2** Analiza la siguiente política de contraseñas de una empresa e identifica qué está bien y qué está mal según las guías NIST SP 800-63B:

> *"Política de contraseñas de TechCorp SA: Las contraseñas deben tener exactamente 8 caracteres. Deben incluir al menos una letra mayúscula, una minúscula, un número y un símbolo. Las contraseñas deben cambiarse obligatoriamente cada 30 días. El sistema almacena los últimos 3 passwords para no repetirlos. El campo acepta cualquier combinación de caracteres ASCII."*

| Elemento de la política | ¿Correcto o incorrecto? | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres |Incorrecto | : NIST prohíbe la rotación periódica arbitraria de contraseñas sin una razón específica. Los cambios forzados hacen que los usuarios elijan variaciones predecibles (ej. Password1!, Password2!), lo que facilita los ataques. Solo se deben cambiar si hay evidencia de compromiso.|
| Cambio obligatorio cada 30 días | Incorrecto| Al ser un historial excesivamente corto, facilita que el usuario vuelva a su contraseña original rápidamente mediante rotaciones falsas consecuativas.|
| Historial de 3 passwords | Incorrecto|  Al eliminar la rotación periódica obligatoria, el control del historial pierde su propósito principal. Además, un historial de solo 3 contraseñas es sumamente fácil de evadir por los usuarios si intentan reutilizar su clave antigua.|
| Complejidad obligatoria (mayus+minus+num+simb) | Incorrecto| NIST desaconseja las reglas de composición obligatoria. Estas reglas reducen el espacio de búsqueda para los atacantes (porque saben que los símbolos suelen ir al final y las mayúsculas al inicio) y dificultan que los usuarios recuerden contraseñas largas y naturales.|

---

### Nivel Avanzado

**D.3** Escenario profesional:

> *Eres el desarrollador líder de una startup fintech peruana que acaba de lanzar su MVP de una app de préstamos personales. El sistema tiene un módulo de login básico. La startup va a solicitar una licencia de operaciones a la SBS (Superintendencia de Banca, Seguros y AFP). La SBS exige cumplimiento con estándares mínimos de seguridad para sistemas financieros.*

**D.3.1** ¿Qué estándares internacionales de seguridad son relevantes para este contexto? Menciona al menos 3.

1. PCI-DSS (Payment Card Industry Data Security Standard): Requisito indispensable si la fintech procesa, almacena o transmite datos de tarjetas de pago/crédito.

2. ISO/IEC 27001: Estándar internacional para Sistemas de Gestión de la Seguridad de la Información (SGSI), alineado estrechamente con las exigencias de gestión de riesgos de la SBS.

3. NIST SP 800-63B: Directrices fundamentales de autenticación de identidades que aseguran un marco normativo moderno frente a auditorías estatales

**D.3.2** Diseña la especificación formal de seguridad completa para el módulo de login de esta fintech. Usa la estructura de 7 componentes vista en clase:

| Componente | Tu especificación |
|---|---|
| **Activos a proteger** |Credenciales de acceso de los clientes, tokens de autenticación (JWT accesos y refresh), registros de auditoría de inicio de sesión. |
| **Sujetos (roles)** |Cliente Fintech (Acceso a su portal), Administrador de Sistemas (Gestión técnica), Auditor Interno/SBS (Solo lectura de reportes logs). |
| **Objetos (recursos controlados)** |Endpoint REST /api/v1/auth/login, Tabla de credenciales en base de datos cifrada, Servidor de Autorización de Sesiones. |
| **Operaciones permitidas/denegadas** |Permitidas: Envío de JSON estructurado por POST para autenticación, solicitud de renovación de sesión con Refresh Token válido.


Denegadas: Intentos de login concurrentes desde zonas geográficas distintas simultáneamente. |
| **Condiciones de acceso** |Canal de transmisión obligatorio cifrado bajo TLS 1.3. El cliente debe proveer credenciales válidas y superar el desafío OTP (MFA) si el dispositivo no está enrolado previamente. |
| **Mecanismos técnicos** |Almacenamiento de credenciales mediante algoritmo Argon2id (o en su defecto bcrypt con factor de costo 12). Implementación de cabeceras de seguridad estrictas como HSTS. |
| **Respuesta ante violación** |Bloqueo temporal y automatizado de la cuenta de usuario tras 5 intentos fallidos consecutivos por un lapso de 30 minutos. |

**D.3.3** Justifica por qué elegiste bcrypt (y no MD5, SHA-256 o AES) para almacenar contraseñas en este sistema financiero. Usa argumentos técnicos y de cumplimiento normativo.

Para proteger las contraseñas se descartan MD5 y SHA-256 por ser funciones hash de propósito general demasiado rápidas ante ataques de fuerza bruta con GPUs, y se rechaza AES por ser un cifrado bidireccional que requiere una clave maestra reversible. En su lugar, se elige bcrypt (o Argon2id) debido a su factor de trabajo configurable que ralentiza deliberadamente el cálculo en hardware especializado, mitigando filtraciones masivas y cumpliendo con las estrictas auditorías técnicas exigidas por la SBS para plataformas financieras

---

**D.4** Pregunta de investigación (para completar fuera de clase):

La empresa Adobe sufrió en 2013 una de las brechas de datos más analizadas académicamente, no solo por el número de afectados (153 millones de registros) sino por el **tipo de error criptográfico** cometido.

**D.4.1** Investiga: ¿cómo Adobe almacenaba las contraseñas de sus usuarios? ¿Por qué fue un error tan grave?

El almacenamiento de contraseñas de Adobe con el algoritmo simétrico Triple DES (3DES) en modo ECB y sin sal causó un desastre criptográfico crítico por dos razones: al ser un cifrado reversible, comprometer la clave maestra exponía todas las contraseñas en texto plano, y al usar el modo ECB (que carece de difusión), contraseñas idénticas producían textos cifrados idénticos, permitiendo a los atacantes deducir patrones masivos fácilmente.

**D.4.2** Explica por qué el hint de contraseña (pista de contraseña) que Adobe guardaba junto al hash **empeoró significativamente** el ataque:

Adobe guardaba la pista de la contraseña en texto plano junto al bloque cifrado. Dado que miles de usuarios compartían contraseñas idénticas (identificadas por el patrón ECB mencionado), los atacantes cruzaron las pistas legibles de unos usuarios para adivinar con precisión quirúrgica las contraseñas de millones de cuentas adicionales que compartían el mismo bloque cifrado pero que no tenían pistas obvias.

**D.4.3** ¿Qué debió haber hecho Adobe en su lugar?

Debió usar una función de derivación de claves adaptativa e irreversible como bcrypt, scrypt o PBKDF2, aplicando adicionalmente un valor de sal (salt) aleatorio único por cada usuario para neutralizar por completo cualquier deducción de patrones visuales o ataques criptográficos correlativos

---

# SECCIÓN E — ACTIVIDAD COLABORATIVA: ESPECIFICACIÓN FORMAL DE SEGURIDAD

**Integrantes del grupo:**
1. ____________________________________________________________
2. ____________________________________________________________
3. ____________________________________________________________
4. ____________________________________________________________

**Sistema asignado:** ____________________________________________________________

---

### E.1 ESPECIFICACIÓN FORMAL — MÓDULO DE LOGIN

Completa esta especificación para el sistema asignado por el docente:

```
╔══════════════════════════════════════════════════════════════════════╗
║        ESPECIFICACIÓN FORMAL DE SEGURIDAD — MÓDULO LOGIN            ║
║        Sistema: ________________________________________________     ║
╠══════════════════════════════════════════════════════════════════════╣
║ ACTIVOS                                                              ║
║ (¿Qué datos se protegen en el proceso de login?)                     ║
║                                                                      ║
║ ●                                                                    ║
║ ●                                                                    ║
║ ●                                                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ SUJETOS                                                              ║
║ (¿Quiénes acceden? ¿Con qué roles diferenciados?)                   ║
║                                                                      ║
║ Rol 1: ___________________ → Permisos: _________________________     ║
║ Rol 2: ___________________ → Permisos: _________________________     ║
║ Rol 3: ___________________ → Permisos: _________________________     ║
╠══════════════════════════════════════════════════════════════════════╣
║ OBJETOS                                                              ║
║ (¿A qué recursos controla el acceso el módulo de login?)            ║
║                                                                      ║
║ ●                                                                    ║
║ ●                                                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ MECANISMOS TÉCNICOS                                                  ║
║                                                                      ║
║ Algoritmo hash: _________________ Factor/parámetros: ___________     ║
║ Protocolo TLS: __________________ Cipher suites: _______________     ║
║ Política de contraseñas:                                             ║
║   Longitud mínima: ___ Complejidad: ___________________________      ║
║ Política de bloqueo:                                                 ║
║   Máx intentos: ___ Duración bloqueo: ____ Tipo: ______________      ║
║ Expiración de sesión: inactividad ___ / máximo _____________        ║
║ MFA: ☐ No ☐ Sí → Tipo: ______________________________________       ║
╠══════════════════════════════════════════════════════════════════════╣
║ CONDICIONES DE ACCESO                                                ║
║ (Bajo qué circunstancias se permite/deniega el acceso)              ║
║                                                                      ║
║ ●                                                                    ║
║ ●                                                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ LOGGING DE SEGURIDAD                                                 ║
║ (¿Qué eventos se registran? ¿Con qué datos?)                        ║
║                                                                      ║
║ Evento 1: ___________________________________________________        ║
║ Evento 2: ___________________________________________________        ║
║ Evento 3: ___________________________________________________        ║
╠══════════════════════════════════════════════════════════════════════╣
║ RESPUESTA ANTE VIOLACIÓN                                             ║
║ (¿Qué ocurre cuando se detecta un intento de ataque?)               ║
║                                                                      ║
║ ●                                                                    ║
║ ●                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### E.2 JUSTIFICACIÓN DE DECISIONES DE DISEÑO

Para cada decisión técnica que tomaron en la especificación, justifiquen por qué la tomaron:

| Decisión técnica tomada | Justificación (¿por qué esta y no otra?) |
|---|---|
| Algoritmo de hash elegido | |
| Versión de TLS elegida | |
| Política de bloqueo definida | |
| Decisión sobre MFA | |

---

### E.3 CASO EXTREMO — ANÁLISIS GRUPAL

Respondan juntos: ¿Qué pasaría si un atacante obtiene acceso directo a la base de datos de su sistema (sin pasar por el login)? ¿Qué información podría obtener y qué NO podría obtener con la especificación que diseñaron?

**Lo que el atacante PODRÍA obtener:**

_________________________________________________________________________

_________________________________________________________________________

**Lo que el atacante NO PODRÍA obtener (gracias a su especificación):**

_________________________________________________________________________

_________________________________________________________________________

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN

### F.1 LISTA REVISADA (Volvemos a la Sección B.1)

Vuelve a tu lista de la Sección B.1 (¿qué hace inseguro un login?). Ahora agrega todo lo que descubriste durante la clase:

**Nuevas razones identificadas durante la clase:**

7. _______________________________________________
8. _______________________________________________
9. _______________________________________________
10. _______________________________________________
11. _______________________________________________
12. _______________________________________________

---

### F.2 PREGUNTAS DE SÍNTESIS

Responde brevemente:

**F.2.1** ¿Cuál es la diferencia esencial entre hash y cifrado? ¿Por qué se usa hash para contraseñas?

_________________________________________________________________________

_________________________________________________________________________

**F.2.2** ¿Qué hace bcrypt diferente a SHA-256 para resistir ataques de fuerza bruta?

_________________________________________________________________________

_________________________________________________________________________

**F.2.3** ¿Qué versión de TLS deben usar y por qué las anteriores están descartadas?

_________________________________________________________________________

_________________________________________________________________________

**F.2.4** ¿Cuál fue el error más crítico del código CGI inseguro que analizamos hoy?

_________________________________________________________________________

_________________________________________________________________________

---

### F.3 METACOGNICIÓN PERSONAL (Solo para ti)

Responde honestamente. Nadie más verá estas respuestas:

**F.3.1** ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?

_________________________________________________________________________

_________________________________________________________________________

**F.3.2** ¿Qué concepto todavía no tienes completamente claro?

_________________________________________________________________________

_________________________________________________________________________

**F.3.3** ¿Qué error de seguridad en código hoy reconoces que podrías haber cometido (o has cometido) antes de esta clase?

_________________________________________________________________________

_________________________________________________________________________

**F.3.4** ¿Cómo cambiaría tu forma de implementar un login después de esta sesión?

_________________________________________________________________________

_________________________________________________________________________

---

### F.4 TAREA PARA LA SEMANA 3 — AUDITORÍA DE LOGIN EN CAMPO

**Instrucción:** Elige un sistema real (app, sitio web, sistema universitario) y audita su formulario de login desde afuera (sin intentar acceder sin autorización). Responde:

**Sistema auditado:** ___________________________________________________________

**URL / Nombre de la app:** ______________________________________________________

| Criterio de auditoría | Resultado | Herramienta usada |
|---|---|---|
| ¿Usa HTTPS? | ☐ Sí ☐ No | |
| ¿Qué versión de TLS usa? | | SSL Labs |
| ¿Calificación SSL Labs? | A / B / C / D / F | ssllabs.com/ssltest |
| ¿Formulario usa POST o GET? | | Inspección de código |
| ¿Tiene política de bloqueo de intentos? | | Intento manual |
| ¿Ofrece MFA (2FA)? | ☐ Sí ☐ No | |
| ¿Muestra mensajes de error genéricos? | ☐ Sí ☐ No | |

**Observación más importante (¿qué encontraste?):**

_________________________________________________________________________

_________________________________________________________________________

**Recomendación de mejora:**

_________________________________________________________________________

_________________________________________________________________________

---

*Guía de Trabajo — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*