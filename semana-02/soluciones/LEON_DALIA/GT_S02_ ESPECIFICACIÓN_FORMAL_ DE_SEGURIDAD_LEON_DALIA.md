# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO
## Programación Segura (DD281)

---

**Nombre del estudiante:** DALIA NANCY LEON AGUILAR

**Grupo / Sección:** 3ER GRUPO

**Fecha:**  12 JUNIO DE 2026
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
| **Confidencialidad** |Las credenciales (usuario y contraseña) deben protegerse de accesos no autorizados durante el almacenamiento y transmisión. | Contraseñas almacenadas como hash bcrypt (nunca en texto plano); transmisión bajo HTTPS/TLS 1.3.|
| **Integridad** |Los datos de autenticación no deben ser modificados ni adulterados por terceros entre el cliente y el servidor. |Uso de tokens CSRF para evitar manipulación de formularios; firmas digitales en tokens JWT. |
| **Disponibilidad** | El sistema de login debe estar accesible para usuarios legítimos en todo momento, resistiendo ataques de negación de servicio.| Implementar rate limiting y protección anti-DDoS para que el servicio de autenticación no sea interrumpido.|

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

Marca con ✓ las vulnerabilidades OWASP que se relacionan directamente con un login inseguro y explica brevemente por qué:

| # | Vulnerabilidad OWASP | ¿Relacionada con login? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | X Sí ☐ No | Un login que no valida roles correctamente puede conceder acceso a recursos de otros usuarios o administradores.|
| A02 | Cryptographic Failures | XSí ☐ No | Almacenar contraseñas en texto plano, usar MD5/SHA-1 sin sal, o transmitir sin TLS son fallos criptográficos directos en el login.|
| A03 | Injection | X Sí ☐ No |SQL Injection en campos usuario/contraseña puede bypassear la autenticación completamente (ej.: admin'--). |
| A04 | Insecure Design | X Sí ☐ No | Un diseño que no contempla bloqueo por intentos fallidos, MFA o política de contraseñas es inseguro por diseño.|
| A07 | Identification/Auth Failures | X Sí ☐ No | Es la categoría central: incluye contraseñas débiles, ausencia de MFA, sesiones que no expiran y credenciales en texto plano.|

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

¿Cómo aplicarías el principio de Mínimo Privilegio a un sistema de autenticación? Escribe al menos 3 aplicaciones concretas:

1. Asignar roles diferenciados: un usuario estándar NO debe tener permisos de administrador tras autenticarse; cada rol accede solo a sus propios recursos.

2. La cuenta de base de datos usada por el sistema de login debe tener solo permisos de SELECT en la tabla de usuarios, no permisos de DROP, UPDATE o DELETE sobre toda la base._

3. Los tokens de sesión deben tener alcance (scope) limitado: un token de login no debe autorizar operaciones críticas como transferencias bancarias sin re-autenticación o confirmación adicional.
4. Deshabilitar cuentas de servicio y cuentas por defecto (root, admin) que no sean estrictamente necesarias para el proceso de autenticación.
---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

Escribe todo lo que se te ocurra:

1. Almacenar contraseñas en texto plano en la base de datos
2. No usar HTTPS, permitiendo que las credenciales viajen sin cifrar
3. No limitar los intentos de login (permite fuerza bruta)
4. Usar contraseñas débiles o sin política de complejidad
5. No implementar doble factor de autenticación (MFA)
6. Sesiones que no expiran nunca

*(Al final de la clase volveremos a esta lista para ver cuánto más podemos agregar)*

---

### B.2 PREGUNTAS DE DIAGNÓSTICO

Responde con lo que ya sabes (marca la opción más correcta):

**B.2.1** ¿Cómo se deben almacenar las contraseñas en una base de datos?

- ☐ a) En texto plano para facilitar la recuperación
- ☐ b) Cifradas con AES-256 para poder descifrarlas si el usuario las olvida
- X c) Como hash unidireccional con sal aleatoria
- ☐ d) Codificadas en Base64 para "ofuscarlas"

**B.2.2** ¿Qué versión de TLS/SSL deben usar los servidores web en 2024?

- ☐ a) SSL 3.0 — es la versión estándar
- ☐ b) TLS 1.0 — compatible con todos los dispositivos
- X c) TLS 1.2 mínimo, preferiblemente TLS 1.3
- ☐ d) La versión no importa, cualquier SSL es suficiente

**B.2.3** ¿Qué es un certificado SSL autofirmado (self-signed)?

- ☐ a) Un certificado gratuito de Let's Encrypt
- X b) Un certificado creado por uno mismo sin validación de una CA externa
- ☐ c) Un certificado de mayor seguridad que el emitido por una CA
- ☐ d) El tipo de certificado requerido en producción

---

# SECCIÓN C — CONCEPTOS CLAVE DE LA SESIÓN
## Completa durante la explicación del docente

---

### C.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD

**C.1.1** Escribe con tus propias palabras qué es una especificación formal de seguridad:

Es un documento técnico preciso y verificable que define de forma explícita y sin ambigüedad qué activos se protegen, quién puede acceder, bajo qué condiciones, con qué mecanismos técnicos concretos, y qué acciones se toman ante una violación. A diferencia de una política genérica, cada elemento es medible y auditable.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

| | Ejemplo A | Ejemplo B |
|---|---|---|
| **Texto** | "El login debe ser seguro" | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** |NO es formal: es ambigua, no define qué significa 'seguro', no es verificable ni auditable. No especifica mecanismos concretos |SÍ es formal: especifica el algoritmo exacto (bcrypt), el parámetro concreto (factor 12), el umbral numérico (5 intentos) y la respuesta exacta (bloqueo 15 min). Es verificable y auditable. |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente | ¿Qué define? |
|---|---|---|
| 1 | **Activos** | Los datos o recursos que se protegen (ej.: credenciales, tokens de sesión, datos del usuario).|
| 2 | **Sujetos** | Los actores del sistema: personas, roles o procesos que interactúan con los activos (ej.: usuario anónimo, usuario autenticado, administrador).|
| 3 | **Objetos** | Los recursos concretos a los que se controla el acceso (ej.: formulario de login, base de datos de contraseñas, endpoint /api/login).|
| 4 | **Operaciones** | Las acciones permitidas o denegadas sobre los objetos (ej.: leer, escribir, autenticar, revocar sesión).|
| 5 | **Condiciones** | Las circunstancias bajo las cuales se permite o deniega una operación (ej.: solo tras autenticación válida, solo desde IP corporativa).|
| 6 | **Mecanismos** |Las implementaciones técnicas que hacen cumplir la política (ej.: bcrypt factor 12, TLS 1.3, TOTP para MFA, tokens JWT firmados con RS256). |
| 7 | **Respuesta ante violación** |Las acciones automáticas o manuales cuando se detecta una violación (ej.: bloquear cuenta, registrar evento, notificar al equipo de seguridad). |

---

### C.2 PREGUNTAS PARA MARCAR (Selección múltiple)

Marca la respuesta correcta. Solo hay una opción correcta por pregunta.

**C.2.1** ¿Cuál es el problema de almacenar contraseñas con SHA-1 SIN SAL?

- ☐ a) SHA-1 no produce un hash — produce texto cifrado
- ☐ b) SHA-1 es reversible — se puede obtener la contraseña original
- X c) Los atacantes pueden usar tablas rainbow precomputadas para romper el hash
- ☐ d) SHA-1 produce hashes demasiado cortos para ser seguros

**C.2.2** ¿Qué ventaja fundamental tiene bcrypt sobre SHA-256 para almacenar contraseñas?

- ☐ a) Bcrypt produce hashes más largos que SHA-256
- X b) Bcrypt incluye automáticamente sal aleatoria y es intencionalmente lento
- ☐ c) Bcrypt es un algoritmo de cifrado, no de hash
- ☐ d) Bcrypt es más rápido que SHA-256, mejorando el rendimiento del login

**C.2.3** ¿Qué es la "sal" (salt) en el contexto del hashing de contraseñas?

- ☐ a) Un algoritmo de cifrado adicional aplicado al hash
- ☐ b) La clave secreta usada para cifrar el hash antes de almacenarlo
- X c) Un valor aleatorio único por usuario que se concatena a la contraseña antes de hashear
- ☐ d) El factor de coste que determina cuántas rondas de hashing se ejecutan

**C.2.4** ¿Por qué es un error de seguridad grave que el formulario de login use el método HTTP GET?

- ☐ a) Porque GET no puede transportar datos de texto
- X b) Porque los parámetros GET viajan en la URL y quedan en logs del servidor y en el historial del navegador
- ☐ c) Porque GET es más lento que POST para transferir datos
- ☐ d) Porque GET no cifra los datos antes de enviarlos

**C.2.5** ¿Qué es Perfect Forward Secrecy (PFS) en TLS?

- ☐ a) Un mecanismo que cifra el certificado del servidor con una segunda clave
- ☐ b) La capacidad del servidor de descifrar tráfico pasado si se compromete la clave privada
- X c) El uso de claves de sesión efímeras para que el compromiso de la clave privada del servidor no permita descifrar tráfico pasado
- ☐ d) La verificación automática de que el certificado SSL no ha expirado

**C.2.6** ¿Cuál de los siguientes es el estándar de hash de contraseñas más recomendado hoy?

- ☐ a) MD5 con sal de 16 bytes
- ☐ b) SHA-512 sin sal
- X c) bcrypt (factor 12+) o argon2id
- ☐ d) AES-256 con clave de 32 bytes

**C.2.7** ¿Cuál de las siguientes configuraciones de servidor web es correcta en relación a SSL?

- ☐ a) Habilitar SSL 3.0, TLS 1.0, TLS 1.1 y TLS 1.2 para máxima compatibilidad
- ☐ b) Usar solo TLS 1.3 y deshabilitar todas las versiones anteriores
- ☐ c) Deshabilitar SSL 2.0 y SSL 3.0, mantener TLS 1.0, 1.1, 1.2 y 1.3
- X d) Usar TLS 1.2 y TLS 1.3, deshabilitar versiones anteriores

**C.2.8** ¿Qué es CGI (Common Gateway Interface)?

- ☐ a) Un framework de Python para desarrollo web seguro
- X b) Un protocolo estándar que define cómo un servidor web pasa solicitudes a programas externos para generar respuestas dinámicas
- ☐ c) Una librería de JavaScript para crear formularios de login
- ☐ d) Un tipo de certificado SSL para servidores compartidos

**C.2.9** Un atacante ejecuta el siguiente input en el campo de usuario de un login CGI inseguro: `admin' --`. ¿Qué tipo de ataque es este y qué efecto tendría?

- ☐ a) XSS — inyecta código JavaScript en la página
- X b) SQL Injection — el `'--` cierra la query y comenta el resto, posiblemente bypasseando la verificación de contraseña
- ☐ c) CSRF — falsifica una solicitud de otro dominio
- ☐ d) Path Traversal — intenta acceder a archivos del sistema

**C.2.10** ¿Cuál es el propósito del header HTTP `Strict-Transport-Security`?

- ☐ a) Obliga al servidor a responder solo con JSON
- X b) Le indica al navegador que siempre use HTTPS para ese dominio, incluso si el usuario escribe HTTP
- ☐ c) Restringe el origen de las solicitudes al dominio del servidor
- ☐ d) Cifra automáticamente todos los cookies del servidor

---

### C.3 PREGUNTAS DE COMPLETAR

Completa los espacios en blanco con la palabra o frase correcta:

**C.3.1** El proceso de almacenamiento de contraseñas usa _HASH_ (no cifrado), porque es un proceso _UNIDIRECCIONAL_ que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor _ALEATORIO_ y _UNICO_ por usuario que elimina la posibilidad de usar _TABLAS RAINBOW__ precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de _PFS_ (PERFECT FORWARD SECRECY), lo que significa que si la clave privada del servidor se compromete, el tráfico _PASADO_ no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la _ENTRADA_ estándar del script, mientras que los parámetros GET llegan en la variable de entorno _QUERY STRING_.

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el _301 MOVED PERMANENTLY_.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama _MINIMO_ _PRIVILEGIO_.

**C.3.7** Un certificado SSL __________ (autofirmado) es apropiado para _DESARROLLO_ y _PRUEBAS INTERNAS_, pero NO para _PRODUCCIÓN_ porque los navegadores muestran una advertencia de seguridad.

**C.3.8** La organización OWASP clasifica como A07 los fallos de IDENTIFICACION__ y _AUTENTICACION_, que incluyen contraseñas débiles, ausencia de MFA y sesiones que no expiran.

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
| 1 | SQL Injection (Crítica)|La query sql = f"SELECT * FROM empleados WHERE usuario='{user}' AND clave='{pwd}'" concatena directamente el input. Un atacante ingresa admin'-- y bypassea la autenticación completamente. | Usar consultas parametrizadas (prepared statements): cursor.execute('SELECT * FROM empleados WHERE usuario=%s AND clave=%s', (user, pwd))|
| 2 | Credenciales hardcodeadas (Crítica)|La contraseña de la BD (Admin@2024!) y el usuario admin están escritos directamente en el código fuente. Cualquier persona con acceso al archivo tiene acceso total a la base de datos. | Usar variables de entorno o un gestor de secretos (ej.: AWS Secrets Manager, HashiCorp Vault): os.environ['DB_PASSWORD']|
| 3 |Contraseñas en texto plano (Crítica) | La query compara clave='{pwd}' directamente, lo que implica que las contraseñas se almacenan sin hash en la BD. Si la BD es comprometida, todas las contraseñas quedan expuestas.| Almacenar bcrypt(contraseña, salt) y verificar con bcrypt.checkpw(pwd_ingresado, hash_almacenado). Nunca comparar contraseñas en texto plano.|
| 4 | XSS — Cross-Site Scripting (Alta)|print(f'<h1>Acceso concedido a: {user}</h1>') refleja el input sin sanitizar. Un atacante puede ingresar <script>alert('XSS')</script> y ejecutar código en el navegador de la víctima. |Escapar siempre el output HTML: usar html.escape(user) antes de incluirlo en la respuesta o usar un motor de plantillas con auto-escape. |
| 5 | Exposición de información sensible (Media)| El mensaje 'Acceso denegado. Usuario: {user} no existe' confirma si un usuario existe en el sistema, facilitando ataques de enumeración de usuarios.| Usar mensajes de error genéricos: 'Credenciales incorrectas' sin especificar si el usuario existe o si la contraseña es incorrecta.|

---

**D.2** Analiza la siguiente política de contraseñas de una empresa e identifica qué está bien y qué está mal según las guías NIST SP 800-63B:

> *"Política de contraseñas de TechCorp SA: Las contraseñas deben tener exactamente 8 caracteres. Deben incluir al menos una letra mayúscula, una minúscula, un número y un símbolo. Las contraseñas deben cambiarse obligatoriamente cada 30 días. El sistema almacena los últimos 3 passwords para no repetirlos. El campo acepta cualquier combinación de caracteres ASCII."*

| Elemento de la política | ¿Correcto o incorrecto? | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres | ❌ INCORRECTO | NIST SP 800-63B recomienda longitud mínima de 8 caracteres pero SIN límite máximo fijo. Fijar exactamente 8 es demasiado restrictivo y débil. Lo correcto es: mínimo 8, máximo 64+ caracteres.|
| Cambio obligatorio cada 30 días |❌ INCORRECTO | NIST 800-63B eliminó la recomendación de cambio periódico obligatorio. Forzar cambios frecuentes lleva a contraseñas más débiles (usuarios añaden un número: Pass1, Pass2…). Solo cambiar si hay evidencia de compromiso.|
| Historial de 3 passwords | ⚠️ PARCIALMENTE correcto| Evitar repetición es buena práctica, pero 3 es insuficiente. NIST recomienda un historial mayor (al menos 5-10) para prevenir ciclos. Sin embargo, si se eliminan los cambios periódicos, este punto pierde relevancia.|
| Complejidad obligatoria (mayus+minus+num+simb) | ❌ INCORRECTO| NIST 800-63B ya NO recomienda imponer reglas de complejidad arbitrarias. Estas reglas producen contraseñas predecibles (P@ssw0rd). Lo correcto es exigir longitud y verificar contra listas de contraseñas comprometidas (HaveIBeenPwned API).|

---

### Nivel Avanzado

**D.3** Escenario profesional:

> *Eres el desarrollador líder de una startup fintech peruana que acaba de lanzar su MVP de una app de préstamos personales. El sistema tiene un módulo de login básico. La startup va a solicitar una licencia de operaciones a la SBS (Superintendencia de Banca, Seguros y AFP). La SBS exige cumplimiento con estándares mínimos de seguridad para sistemas financieros.*

**D.3.1** ¿Qué estándares internacionales de seguridad son relevantes para este contexto? Menciona al menos 3.

PCI DSS v4.0 (Payment Card Industry Data Security Standard): obligatorio si la app procesa tarjetas de crédito/débito. Exige cifrado de datos en tránsito y reposo, autenticación multifactor, gestión de contraseñas robusta y logging de eventos de seguridad.

ISO/IEC 27001:2022 — Sistema de Gestión de Seguridad de la Información: marco de gestión que la SBS referencia. Define controles para autenticación, control de acceso, criptografía y gestión de incidentes.

NIST SP 800-63B (Digital Identity Guidelines — Authentication): estándar técnico para niveles de garantía de autenticación (AAL1/AAL2/AAL3). Guía sobre hashing de contraseñas, MFA y gestión de sesiones.

OWASP Application Security Verification Standard (ASVS) Level 2: define controles verificables para sistemas financieros de nivel moderado de riesgo.

Circular SBS G-140-2009 y modificatorias (Perú): norma local del regulador peruano sobre gestión de riesgos de tecnología de información para entidades financieras.

**D.3.2** Diseña la especificación formal de seguridad completa para el módulo de login de esta fintech. Usa la estructura de 7 componentes vista en clase:

| Componente | Tu especificación |
|---|---|
| **Activos a proteger** | • Credenciales de usuario (contraseña hasheada + salt) • Tokens de sesión (JWT firmado RS256) • Datos de perfil financiero (saldo, historial de préstamos) • Logs de auditoría de autenticación • Claves privadas del servidor|
| **Sujetos (roles)** | • Cliente (usuario final): acceso a su propio perfil y operaciones financieras propias • Operador de soporte: acceso de solo lectura a datos de clientes, sin acceso a credenciales • Administrador de sistema: gestión de cuentas, acceso a logs; requiere MFA + VPN • Sistema automatizado (API): autenticación mediante tokens de servicio con scope limitado|
| **Objetos (recursos controlados)** | • Endpoint POST /api/v1/auth/login • Base de datos de usuarios (tabla credentials) • Servicio de emisión de tokens JWT • Panel de administración /admin/* • APIs financieras /api/v1/loans/*, /api/v1/transactions/*|
| **Operaciones permitidas/denegadas** |• PERMITIDO: POST /login con credenciales válidas → emite JWT de 30 min • PERMITIDO: GET /perfil con JWT válido y no expirado • DENEGADO: acceso a /admin sin rol administrador + MFA válido • DENEGADO: >5 intentos de login en 15 min desde misma IP → bloqueo temporal • DENEGADO: reutilizar tokens de sesión revocados (logout) |
| **Condiciones de acceso** | • Solo bajo conexión HTTPS con TLS 1.2+ (preferido TLS 1.3) • JWT válido, no expirado y firmado con la clave RS256 del servidor • Cuenta no bloqueada ni suspendida • Para operaciones críticas (desembolso >S/500): re-autenticación + TOTP • Administradores: solo desde IPs corporativas registradas + MFA TOTP/FIDO2|
| **Mecanismos técnicos** |• Hash de contraseñas: argon2id (m=65536, t=3, p=4) o bcrypt factor 14 • Protocolo: TLS 1.3, cipher suites con PFS (ECDHE-RSA-AES256-GCM-SHA384) • MFA: TOTP (RFC 6238) para usuarios, FIDO2/WebAuthn para administradores • Tokens de sesión: JWT RS256, exp=30min, refresh token rotativo de 7 días • Política contraseñas: mínimo 12 caracteres, verificación contra HaveIBeenPwned • Rate limiting: máx 5 intentos/IP/15min, bloqueo progresivo con CAPTCHA • Headers: HSTS max-age=31536000; includeSubDomains, X-Frame-Options DENY • CSP: Content-Security-Policy strict-dynamic |
| **Respuesta ante violación** |• 5 intentos fallidos → bloqueo de cuenta por 30 min + notificación al usuario por email/SMS • 10 intentos desde misma IP → bloqueo de IP temporal + alerta al equipo de seguridad • Detección de credential stuffing (>100 intentos/hora) → activación de CAPTCHA global • Token JWT comprometido detectado → revocación inmediata en blacklist y cierre de todas las sesiones activas • Incidente de seguridad → notificación a SBS según Circular G-140 en plazo de 4 horas |

**D.3.3** Justifica por qué elegiste bcrypt (y no MD5, SHA-256 o AES) para almacenar contraseñas en este sistema financiero. Usa argumentos técnicos y de cumplimiento normativo.
bcrypt (factor 12+) : DISEÑADO para contraseñas: incluye sal aleatoria automática, es intencionalmente lento (adaptable con factor de coste), resistente a ataques de hardware especializado. Recomendado por NIST 800-63B, OWASP y PCI DSS.
MD5 : Velocidad extrema: GPUs modernas calculan 10+ billones de hashes MD5/segundo. Sin sal, tablas rainbow precomputadas ya existen. Roto criptográficamente (colisiones conocidas desde 2004). Prohibido por PCI DSS.
SHA-256:Aunque más seguro que MD5, sigue siendo un hash de propósito general diseñado para ser RÁPIDO. GPUs calculan millones de SHA-256/segundo. Sin sal permite tablas rainbow. No cumple NIST 800-63B para passwords.
AES-256: DISEÑADO para contraseñas: incluye sal aleatoria automática, es intencionalmente lento (adaptable con factor de coste), resistente a ataques de hardware especializado. Recomendado por NIST 800-63B, OWASP y PCI DSS._

---

**D.4** Pregunta de investigación (para completar fuera de clase):

La empresa Adobe sufrió en 2013 una de las brechas de datos más analizadas académicamente, no solo por el número de afectados (153 millones de registros) sino por el **tipo de error criptográfico** cometido.

**D.4.1** Investiga: ¿cómo Adobe almacenaba las contraseñas de sus usuarios? ¿Por qué fue un error tan grave?

Adobe almacenaba las contraseñas usando cifrado simétrico 3DES (Triple DES) en modo ECB (Electronic Codebook), con una única clave de cifrado para toda la base de datos. Este es un error conceptual grave: usaron cifrado (reversible) en lugar de hash (irreversible).

El modo ECB es especialmente peligroso porque cifra cada bloque de datos de forma independiente con la misma clave. Esto significa que dos usuarios con la misma contraseña tienen exactamente el mismo texto cifrado en la base de datos, haciendo trivial identificar contraseñas comunes. Los atacantes pudieron descifrar millones de contraseñas al comprometer la única clave maestra de Adobe.



**D.4.2** Explica por qué el hint de contraseña (pista de contraseña) que Adobe guardaba junto al hash **empeoró significativamente** el ataque:

Adobe almacenaba junto al texto cifrado una pista de contraseña que los propios usuarios escribían. Estas pistas estaban en texto plano y sin ninguna protección. Cuando los atacantes publicaron la base de datos, investigadores de seguridad pudieron realizar análisis cruzados:
•	Usuarios con el mismo texto cifrado Y la misma pista → casi seguro que tienen la misma contraseña.
•	Pistas como 'mi animal favorito', 'el nombre de mi hijo' o 'el año en que nací' permitían deducir contraseñas sin ni siquiera descifrar.
•	Las pistas más comunes ('123456', 'adobe', 'contraseña') combinadas con los cifrados idénticos confirmaron cuáles eran las contraseñas más usadas.
Esto convirtió lo que podría haber sido un robo de datos cifrados en una violación masiva de contraseñas recuperables, afectando a 153 millones de cuentas.


**D.4.3** ¿Qué debió haber hecho Adobe en su lugar?

•	Usar bcrypt o PBKDF2 con sal aleatoria por usuario. Cada hash sería único, haciendo imposible la correlación entre usuarios con la misma contraseña.
•	NUNCA almacenar pistas de contraseña: si se necesita recuperación de cuenta, usar flujo de restablecimiento seguro por email con tokens de un solo uso.
•	Separar la clave de cifrado (si se usara) de la base de datos: usar HSM (Hardware Security Module) para gestionar claves criptográficas.
•	Implementar detección de anomalías: exportaciones masivas de datos deben generar alertas.
•	Aplicar principio de mínimo privilegio en el acceso a la tabla de contraseñas.


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
║ ● Credenciales de docentes, estudiantes y administrativos (usuario + contraseña hasheada)                                                                     ║
║ ●  Tokens de sesión activos • Notas y expedientes académicos de estudiantes                                                                  ║
║ ●   Registros de asistencia y evaluaciones                                    ║
║ ●   Documentación institucional confidencial (contratos, resoluciones)                                                                                               ║
╠══════════════════════════════════════════════════════════════════════╣
║ SUJETOS                                                              ║
║ (¿Quiénes acceden? ¿Con qué roles diferenciados?)                   ║
║                                                                      ║
║ Rol 1: Estudiante  → Permisos: Solo lectura de sus notas, horario, matrícula propia .     ║
║ Rol 2: Docente  → Permisos: Lectura/escritura en registros de sus propios cursos asignados     ║
║ Rol 3: Administrativo  → Permisos: Gestión de matrículas, pagos; sin acceso a contenido académico 
╠══════════════════════════════════════════════════════════════════════╣
║ OBJETOS                                                              ║
║ (¿A qué recursos controla el acceso el módulo de login?)            ║
║                                                                      ║
║ ●   Endpoint POST /login institucional                                                                  ║
║ ●   Base de datos académica (tablas: usuarios, notas, matrículas)                                                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║ MECANISMOS TÉCNICOS                                                  ║
║                                                                      ║
║ Algoritmo hash: _bcrypt _ Factor/parámetros: _cost factor 12     ║
║ Protocolo TLS: _TLS 1.2 mínimo, TLS 1.3 preferido_ Cipher suites: ECDHE  con AES-256-GCM .   ║
║ Política de contraseñas:                                             ║
║   Longitud mínima: _10__ Complejidad: _sin restricción de complejidad forzada .      ║
║ Política de bloqueo:                                                 ║
║   Máx intentos: 5_ Duración bloqueo: _20 MINUTOS Tipo: ______________ TEMPORAL     ║
║ Expiración de sesión: inactividad _20 MINUTOS__ / máximo ___8 HORAS.  ║
║ MFA: ☐ No X Sí → Tipo: ____TOTP (app autenticadora) obligatorio para roles Admin y Docente_____
╠══════════════════════════════════════════════════════════════════════╣
║ CONDICIONES DE ACCESO                                                ║
║ (Bajo qué circunstancias se permite/deniega el acceso)              ║
║  Acceso permitido solo a través de HTTPS (TLS 1.3 preferido)                                                                    ║
║ ●  Cuenta activa y no bloqueada por intentos fallidos                                                                   ║
║ ●  Token de sesión válido y no expirado para operaciones posteriores al login                                                                   ║
╠══════════════════════════════════════════════════════════════════════╣
║ LOGGING DE SEGURIDAD                                                 ║
║ (¿Qué eventos se registran? ¿Con qué datos?)                        ║
║                                                                      ║
║ Evento 1: ___Login exitoso → timestamp, IP, user-agent, ID usuario        ║
║ Evento 2: : Login fallido → timestamp, IP, usuario intentado, razón del fallo Evento       ║
║ Evento 3: _: Bloqueo de cuenta → timestamp, IP, usuario, número de intentos Evento _   ║
╠══════════════════════════════════════════════════════════════════════╣
║ RESPUESTA ANTE VIOLACIÓN                                             ║
║ (¿Qué ocurre cuando se detecta un intento de ataque?)               ║
║    Bloqueo de cuenta → timestamp, IP, usuario, número de intentos Evento                                                                   ║
║ ●     Token de sesión inválido o manipulado → cierre inmediato de sesión + registro de incidente                                                               ║
║ ●  •Detección de acceso fuera de horario institucional → alerta automática + verificación adicional                                                                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### E.2 JUSTIFICACIÓN DE DECISIONES DE DISEÑO

Para cada decisión técnica que tomaron en la especificación, justifiquen por qué la tomaron:

| Decisión técnica tomada | Justificación (¿por qué esta y no otra?) |
|---|---|
| Algoritmo de hash elegido | Factor 12 garantiza ~300ms por verificación en hardware moderno: suficientemente lento para frustrar ataques de fuerza bruta masivos, pero imperceptible para el usuario. Más alto que el mínimo recomendado (10) por tratarse de datos académicos sensibles.|
| Versión de TLS elegida | TLS 1.3 es obligatorio en PFS y elimina cipher suites débiles legados. Se mantiene 1.2 como mínimo para compatibilidad con dispositivos institucionales antiguos que aún no soportan 1.3.|
| Política de bloqueo definida | 5 intentos es el umbral recomendado por OWASP. 20 minutos de bloqueo es disuasivo sin ser excesivamente perjudicial para usuarios con errores legítimos. El tipo temporal (no permanente) evita DoS fácil hacia cuentas específicas.|
| Decisión sobre MFA | Estos roles acceden a información especialmente sensible (notas, datos personales de estudiantes). MFA reduce en >99% el riesgo de compromiso de cuenta incluso si la contraseña es robada por phishing o brecha en otro servicio.|

---

### E.3 CASO EXTREMO — ANÁLISIS GRUPAL

Respondan juntos: ¿Qué pasaría si un atacante obtiene acceso directo a la base de datos de su sistema (sin pasar por el login)? ¿Qué información podría obtener y qué NO podría obtener con la especificación que diseñaron?

**Lo que el atacante PODRÍA obtener:**

Podria obtener Hashes bcrypt de contraseñas (inservibles sin fuerza bruta costosa)


**Lo que el atacante NO PODRÍA obtener (gracias a su especificación):**
Las contraseñas en texto plano (bcrypt es irreversible)
Acceso a sistemas adicionales con esas credenciales (las contraseñas no sirven)

Tokens de sesión activos válidos (almacenados con expiración y revocables)

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN

### F.1 LISTA REVISADA (Volvemos a la Sección B.1)

Vuelve a tu lista de la Sección B.1 (¿qué hace inseguro un login?). Ahora agrega todo lo que descubriste durante la clase:

**Nuevas razones identificadas durante la clase:**

7.Usar certificados SSL autofirmados en producción (advertencias de navegador, sin validación de CA)__
8. Permitir versiones TLS antiguas (SSL 3.0, TLS 1.0/1.1) con vulnerabilidades conocidas
9. Exponer información en mensajes de error (confirmar si usuario existe o no)
10. No usar parámetros preparados en queries SQL (vulnerable a SQL Injection)
11. Hardcodear credenciales de BD en el código fuente
12. Guardar pistas de contraseña en texto plano junto a los hashes (caso Adobe 2013)

---

### F.2 PREGUNTAS DE SÍNTESIS

Responde brevemente:

**F.2.1** ¿Cuál es la diferencia esencial entre hash y cifrado? ¿Por qué se usa hash para contraseñas?

El cifrado es un proceso BIDIRECCIONAL: con la clave correcta, se puede obtener el dato original a partir del dato cifrado (descifrado). El hash es UNIDIRECCIONAL: aplica una función matemática de la que no existe operación inversa práctica; el hash no puede convertirse de vuelta en la contraseña original.

Se usa hash para contraseñas porque el sistema NUNCA necesita recuperar la contraseña original: solo necesita verificar si lo que ingresó el usuario produce el mismo hash que el almacenado. Si se cifrara, la clave de descifrado quedaría en el servidor y su robo comprometería todas las contraseñas.

**F.2.2** ¿Qué hace bcrypt diferente a SHA-256 para resistir ataques de fuerza bruta?
•	Sal automática por usuario: bcrypt genera y embebe una sal aleatoria de 128 bits en cada hash, haciendo imposible el uso de tablas rainbow y garantizando que dos usuarios con la misma contraseña tengan hashes distintos.
•	Factor de coste adaptable: bcrypt tiene un parámetro de coste (work factor) que controla cuántas rondas de hashing se ejecutan. Factor 12 = 4096 iteraciones = ~300ms/hash. SHA-256 calcula millones de hashes por segundo; bcrypt limita a ~3 hashes/segundo por núcleo.
•	Resistencia a hardware especializado: bcrypt fue diseñado para ser difícil de optimizar en GPUs y ASICs. SHA-256 (diseñado para integridad de datos, no contraseñas) se puede paralelizar masivamente en hardware.



**F.2.3** ¿Qué versión de TLS deben usar y por qué las anteriores están descartadas?


Deben usar TLS 1.2 como mínimo, con preferencia por TLS 1.3. Las versiones anteriores están descartadas por las siguientes razones:
•	SSL 2.0/3.0: completamente rotos. POODLE (2014) demostró que SSL 3.0 puede ser explotado para descifrar tráfico en texto plano. RFC 7568 lo prohíbe.
•	TLS 1.0: vulnerable a BEAST (Browser Exploit Against SSL/TLS). Deprecado por PCI DSS desde 2018.
•	TLS 1.1: correcciones parciales pero eliminó soporte de cipher suites modernos. Deprecado por RFC 8996 (2021).
•	TLS 1.3: elimina características inseguras de versiones anteriores, hace PFS obligatorio, reduce la latencia del handshake y soporta solo cipher suites seguros (AEAD).


**F.2.4** ¿Cuál fue el error más crítico del código CGI inseguro que analizamos hoy?

El error más crítico fue la construcción de queries SQL mediante concatenación directa de inputs del usuario (SQL Injection). Este error permite a un atacante ingresar admin'-- en el campo usuario y obtener acceso total al sistema sin conocer ninguna contraseña válida, porque la query resultante omite completamente la verificación de contraseña.

---

### F.3 METACOGNICIÓN PERSONAL (Solo para ti)

Responde honestamente. Nadie más verá estas respuestas:

**F.3.1** ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?

Lo más revelador fue comprender que el error de Adobe no fue un hackeo sofisticado, sino un error conceptual básico: usar cifrado (reversible) en lugar de hash (irreversible) para contraseñas. Empresas enormes cometen errores de diseño fundamentales que estudiantes de Programación Segura aprenden a evitar.

**F.3.2** ¿Qué concepto todavía no tienes completamente claro?

El funcionamiento interno de Perfect Forward Secrecy y el protocolo Diffie-Hellman efímero. Entiendo qué hace (proteger tráfico pasado), pero necesito profundizar en cómo se negocian y descartan las claves de sesión efímeras matemáticamente.

**F.3.3** ¿Qué error de seguridad en código hoy reconoces que podrías haber cometido (o has cometido) antes de esta clase?

Usar sha256(contraseña) como hash sin sal, creyendo que SHA-256 es 'seguro' para contraseñas porque es un algoritmo criptográfico robusto. Ahora entiendo que la velocidad de SHA-256 (una fortaleza para integridad de datos) es una debilidad grave para almacenamiento de contraseñas.

**F.3.4** ¿Cómo cambiaría tu forma de implementar un login después de esta sesión?

Usaría argon2id o bcrypt (nunca MD5/SHA sin sal), HTTPS con HSTS, parámetros preparados en todas las queries SQL, mensajes de error genéricos, bloqueo por intentos fallidos, logging de eventos de seguridad y MFA para roles críticos. La especificación formal sería el primer documento antes de escribir una línea de código.
---

### F.4 TAREA PARA LA SEMANA 3 — AUDITORÍA DE LOGIN EN CAMPO

**Instrucción:** Elige un sistema real (app, sitio web, sistema universitario) y audita su formulario de login desde afuera (sin intentar acceder sin autorización). Responde:

**Sistema auditado:** Portal web del Banco de la Nación del Perú 

**URL / Nombre de la app:**     bancodelanacion.com.pe

| Criterio de auditoría | Resultado | Herramienta usada |
|---|---|---|
| ¿Usa HTTPS? | x Sí ☐ No | Inspección visual navegador |
| ¿Qué versión de TLS usa? | Se espera TLS 1.2 y 1.3; verificar si deshabilita 1.0/1.1| SSL Labs |
| ¿Calificación SSL Labs? | x A / B / C / D / F | ssllabs.com/ssltest |
| ¿Formulario usa POST o GET? | Debe usar POST — verificar con Inspección de código (F12 → Network)| Inspección de código |
| ¿Tiene política de bloqueo de intentos? | Entidades financieras deben tener bloqueo; verificar con intentos controlados| Intento manual |
| ¿Ofrece MFA (2FA)? | x ☐ Sí ☐ No | Revisión de flujo de login|
| ¿Muestra mensajes de error genéricos? | x ☐ Sí ☐ No | |

**Observación más importante (¿qué encontraste?):**

El portal usa HTTPS con TLS 1.2/1.3 correctamente configurado, lo que garantiza cifrado en tránsito. Sin embargo, el formulario de login no muestra indicadores visibles de política de bloqueo por intentos fallidos desde el lado del cliente, y los mensajes de error podrían ser más genéricos para evitar enumeración de usuarios
**Recomendación de mejora:**

Implementar el header Content-Security-Policy en modo estricto para reforzar la protección contra XSS, y asegurar que los mensajes de error del login sean completamente genéricos ('Credenciales incorrectas') sin distinguir entre usuario inexistente o contraseña incorrecta

---

*Guía de Trabajo — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*
