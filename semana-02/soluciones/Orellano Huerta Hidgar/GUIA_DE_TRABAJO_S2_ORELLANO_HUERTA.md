# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO
## Programación Segura (DD281)

---

**Nombre del estudiante:** Orellano Huerta Hidgar

**Grupo / Sección:** Grupo 4

**Fecha:** 15 de junio de 2026

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
| **Confidencialidad** | Protege las credenciales, tokens y datos personales frente a accesos no autorizados. | Usar HTTPS/TLS y almacenar contraseñas con bcrypt o Argon2id, nunca en texto plano. |
| **Integridad** | Evita la modificación no autorizada de credenciales, roles y sesiones. | Usar consultas parametrizadas, cookies firmadas y registros de auditoría protegidos. |
| **Disponibilidad** | Mantiene el servicio de autenticación accesible para usuarios legítimos. | Aplicar rate limiting y bloqueo progresivo para reducir fuerza bruta sin bloquear permanentemente el servicio. |

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

Marca con ✓ las vulnerabilidades OWASP que se relacionan directamente con un login inseguro y explica brevemente por qué:

| # | Vulnerabilidad OWASP | ¿Relacionada con login? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | ☒ Sí ☐ No | Un usuario autenticado podría acceder a funciones de otro rol si no se verifica la autorización en cada solicitud. |
| A02 | Cryptographic Failures | ☒ Sí ☐ No | Ocurre si las contraseñas se almacenan de forma insegura o las credenciales viajan sin TLS. |
| A03 | Injection | ☒ Sí ☐ No | Una consulta SQL construida con entradas del formulario puede permitir omitir la contraseña. |
| A04 | Insecure Design | ☒ Sí ☐ No | Un diseño sin MFA, límites de intentos o recuperación segura mantiene riesgos aunque el código funcione. |
| A07 | Identification/Auth Failures | ☒ Sí ☐ No | Comprende credenciales débiles, sesiones inseguras, ausencia de MFA y ataques automatizados. |

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

¿Cómo aplicarías el principio de Mínimo Privilegio a un sistema de autenticación? Escribe al menos 3 aplicaciones concretas:

1. La cuenta de la aplicación en la base de datos tendrá solo permisos para las operaciones necesarias y no usará una cuenta administradora.

2. Cada sesión recibirá únicamente los permisos de su rol: votante, administrador electoral o auditor.

3. Los tokens tendrán alcance y duración mínimos; las acciones críticas exigirán reautenticación y MFA.

---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

Escribe todo lo que se te ocurra:

1. Guardar contraseñas en texto plano o con hashes rápidos y sin sal.
2. Enviar credenciales mediante HTTP o versiones obsoletas de TLS.
3. Construir consultas SQL concatenando la entrada del usuario.
4. No limitar intentos ni detectar ataques de fuerza bruta.
5. Mantener sesiones sin expiración o cookies inseguras.
6. Mostrar mensajes que revelan si un usuario existe.

*(Al final de la clase volveremos a esta lista para ver cuánto más podemos agregar)*

---

### B.2 PREGUNTAS DE DIAGNÓSTICO

Responde con lo que ya sabes (marca la opción más correcta):

**B.2.1** ¿Cómo se deben almacenar las contraseñas en una base de datos?

- ☐ a) En texto plano para facilitar la recuperación
- ☐ b) Cifradas con AES-256 para poder descifrarlas si el usuario las olvida
- ☒ c) Como hash unidireccional con sal aleatoria
- ☐ d) Codificadas en Base64 para "ofuscarlas"

**B.2.2** ¿Qué versión de TLS/SSL deben usar los servidores web en 2024?

- ☐ a) SSL 3.0 — es la versión estándar
- ☐ b) TLS 1.0 — compatible con todos los dispositivos
- ☒ c) TLS 1.2 mínimo, preferiblemente TLS 1.3
- ☐ d) La versión no importa, cualquier SSL es suficiente

**B.2.3** ¿Qué es un certificado SSL autofirmado (self-signed)?

- ☐ a) Un certificado gratuito de Let's Encrypt
- ☒ b) Un certificado creado por uno mismo sin validación de una CA externa
- ☐ c) Un certificado de mayor seguridad que el emitido por una CA
- ☐ d) El tipo de certificado requerido en producción

---

# SECCIÓN C — CONCEPTOS CLAVE DE LA SESIÓN
## Completa durante la explicación del docente

---

### C.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD

**C.1.1** Escribe con tus propias palabras qué es una especificación formal de seguridad:

Una especificación formal de seguridad es una descripción precisa, verificable y
no ambigua de los activos que se protegen, quién puede acceder, qué operaciones
se permiten, bajo qué condiciones y cómo responderá el sistema ante una violación.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

| | Ejemplo A | Ejemplo B |
|---|---|---|
| **Texto** | "El login debe ser seguro" | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** | No es formal porque “seguro” es subjetivo y no establece controles ni criterios verificables. | Es formal porque define el algoritmo, factor de coste, número de intentos y duración del bloqueo; todos son comprobables. |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente | ¿Qué define? |
|---|---|---|
| 1 | **Activos** | Datos, funciones y servicios que necesitan protección. |
| 2 | **Sujetos** | Usuarios, roles, procesos o sistemas que solicitan acceso. |
| 3 | **Objetos** | Recursos sobre los que los sujetos realizan acciones. |
| 4 | **Operaciones** | Acciones permitidas o denegadas para cada sujeto. |
| 5 | **Condiciones** | Requisitos que deben cumplirse para autorizar el acceso. |
| 6 | **Mecanismos** | Controles técnicos que hacen cumplir las reglas. |
| 7 | **Respuesta ante violación** | Detección, contención, registro, notificación y recuperación. |

---

### C.2 PREGUNTAS PARA MARCAR (Selección múltiple)

Marca la respuesta correcta. Solo hay una opción correcta por pregunta.

**C.2.1** ¿Cuál es el problema de almacenar contraseñas con SHA-1 SIN SAL?

- ☐ a) SHA-1 no produce un hash — produce texto cifrado
- ☐ b) SHA-1 es reversible — se puede obtener la contraseña original
- ☒ c) Los atacantes pueden usar tablas rainbow precomputadas para romper el hash
- ☐ d) SHA-1 produce hashes demasiado cortos para ser seguros

**C.2.2** ¿Qué ventaja fundamental tiene bcrypt sobre SHA-256 para almacenar contraseñas?

- ☐ a) Bcrypt produce hashes más largos que SHA-256
- ☒ b) Bcrypt incluye automáticamente sal aleatoria y es intencionalmente lento
- ☐ c) Bcrypt es un algoritmo de cifrado, no de hash
- ☐ d) Bcrypt es más rápido que SHA-256, mejorando el rendimiento del login

**C.2.3** ¿Qué es la "sal" (salt) en el contexto del hashing de contraseñas?

- ☐ a) Un algoritmo de cifrado adicional aplicado al hash
- ☐ b) La clave secreta usada para cifrar el hash antes de almacenarlo
- ☒ c) Un valor aleatorio único por usuario que se concatena a la contraseña antes de hashear
- ☐ d) El factor de coste que determina cuántas rondas de hashing se ejecutan

**C.2.4** ¿Por qué es un error de seguridad grave que el formulario de login use el método HTTP GET?

- ☐ a) Porque GET no puede transportar datos de texto
- ☒ b) Porque los parámetros GET viajan en la URL y quedan en logs del servidor y en el historial del navegador
- ☐ c) Porque GET es más lento que POST para transferir datos
- ☐ d) Porque GET no cifra los datos antes de enviarlos

**C.2.5** ¿Qué es Perfect Forward Secrecy (PFS) en TLS?

- ☐ a) Un mecanismo que cifra el certificado del servidor con una segunda clave
- ☐ b) La capacidad del servidor de descifrar tráfico pasado si se compromete la clave privada
- ☒ c) El uso de claves de sesión efímeras para que el compromiso de la clave privada del servidor no permita descifrar tráfico pasado
- ☐ d) La verificación automática de que el certificado SSL no ha expirado

**C.2.6** ¿Cuál de los siguientes es el estándar de hash de contraseñas más recomendado hoy?

- ☐ a) MD5 con sal de 16 bytes
- ☐ b) SHA-512 sin sal
- ☒ c) bcrypt (factor 12+) o argon2id
- ☐ d) AES-256 con clave de 32 bytes

**C.2.7** ¿Cuál de las siguientes configuraciones de servidor web es correcta en relación a SSL?

- ☐ a) Habilitar SSL 3.0, TLS 1.0, TLS 1.1 y TLS 1.2 para máxima compatibilidad
- ☐ b) Usar solo TLS 1.3 y deshabilitar todas las versiones anteriores
- ☐ c) Deshabilitar SSL 2.0 y SSL 3.0, mantener TLS 1.0, 1.1, 1.2 y 1.3
- ☒ d) Usar TLS 1.2 y TLS 1.3, deshabilitar versiones anteriores

**C.2.8** ¿Qué es CGI (Common Gateway Interface)?

- ☐ a) Un framework de Python para desarrollo web seguro
- ☒ b) Un protocolo estándar que define cómo un servidor web pasa solicitudes a programas externos para generar respuestas dinámicas
- ☐ c) Una librería de JavaScript para crear formularios de login
- ☐ d) Un tipo de certificado SSL para servidores compartidos

**C.2.9** Un atacante ejecuta el siguiente input en el campo de usuario de un login CGI inseguro: `admin' --`. ¿Qué tipo de ataque es este y qué efecto tendría?

- ☐ a) XSS — inyecta código JavaScript en la página
- ☒ b) SQL Injection — el `'--` cierra la query y comenta el resto, posiblemente bypasseando la verificación de contraseña
- ☐ c) CSRF — falsifica una solicitud de otro dominio
- ☐ d) Path Traversal — intenta acceder a archivos del sistema

**C.2.10** ¿Cuál es el propósito del header HTTP `Strict-Transport-Security`?

- ☐ a) Obliga al servidor a responder solo con JSON
- ☒ b) Le indica al navegador que siempre use HTTPS para ese dominio, incluso si el usuario escribe HTTP
- ☐ c) Restringe el origen de las solicitudes al dominio del servidor
- ☐ d) Cifra automáticamente todos los cookies del servidor

---

### C.3 PREGUNTAS DE COMPLETAR

Completa los espacios en blanco con la palabra o frase correcta:

**C.3.1** El proceso de almacenamiento de contraseñas usa **hashing** (no cifrado), porque es un proceso **unidireccional** que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor **aleatorio** y **único** por usuario que elimina la posibilidad de usar **tablas rainbow** precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de **PFS** (siglas), lo que significa que si la clave privada del servidor se compromete, el tráfico **pasado** no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la **entrada** estándar del script, mientras que los parámetros GET llegan en la variable de entorno **QUERY_STRING**.

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el **301**.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama **mínimo privilegio**.

**C.3.7** Un certificado SSL **self-signed** (autofirmado) es apropiado para **desarrollo** y **pruebas internas**, pero NO para **producción pública** porque los navegadores muestran una advertencia de seguridad.

**C.3.8** La organización OWASP clasifica como A07 los fallos de **identificación** y **autenticación**, que incluyen contraseñas débiles, ausencia de MFA y sesiones que no expiran.

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
| 1 | SQL Injection | `user` y `pwd` se insertan directamente en la consulta, permitiendo omitir el login o extraer datos. | Usar consultas parametrizadas y validar longitud y formato de entradas. |
| 2 | Contraseñas en texto plano | La consulta compara directamente `clave`; una fuga revelaría todas las contraseñas. | Guardar hashes Argon2id o bcrypt y verificarlos con una biblioteca especializada. |
| 3 | Credenciales de BD expuestas y cuenta `admin` | La clave está en el código y la cuenta tiene privilegios excesivos. | Usar variables de entorno o un gestor de secretos y una cuenta de mínimo privilegio. |
| 4 | XSS reflejado | `user` se imprime sin escape y podría contener HTML o JavaScript malicioso. | Escapar la salida con plantillas de autoescape y aplicar Content Security Policy. |
| 5 | Divulgación de información | Los mensajes permiten enumerar usuarios y muestran toda la fila del empleado. | Usar “Credenciales inválidas” y nunca imprimir registros internos. |

---

**D.2** Analiza la siguiente política de contraseñas de una empresa e identifica qué está bien y qué está mal según las guías NIST SP 800-63B:

> *"Política de contraseñas de TechCorp SA: Las contraseñas deben tener exactamente 8 caracteres. Deben incluir al menos una letra mayúscula, una minúscula, un número y un símbolo. Las contraseñas deben cambiarse obligatoriamente cada 30 días. El sistema almacena los últimos 3 passwords para no repetirlos. El campo acepta cualquier combinación de caracteres ASCII."*

| Elemento de la política | ¿Correcto o incorrecto? | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres | **Incorrecto** | Limita demasiado el espacio de búsqueda. NIST vigente exige mínimo 15 si la contraseña es el único factor, o mínimo 8 si forma parte de MFA, y recomienda admitir al menos 64 caracteres. |
| Cambio obligatorio cada 30 días | **Incorrecto** | Los cambios periódicos generan patrones predecibles. Debe exigirse cambio cuando exista evidencia de compromiso. |
| Historial de 3 passwords | **Insuficiente** | No corrige el problema de la rotación periódica. Es preferible bloquear contraseñas comunes o filtradas. |
| Complejidad obligatoria (mayus+minus+num+simb) | **Incorrecto** | NIST desaconseja reglas rígidas de composición y prioriza longitud, blocklist, MFA y detección de credenciales comprometidas. |

---

### Nivel Avanzado

**D.3** Escenario profesional:

> *Eres el desarrollador líder de una startup fintech peruana que acaba de lanzar su MVP de una app de préstamos personales. El sistema tiene un módulo de login básico. La startup va a solicitar una licencia de operaciones a la SBS (Superintendencia de Banca, Seguros y AFP). La SBS exige cumplimiento con estándares mínimos de seguridad para sistemas financieros.*

**D.3.1** ¿Qué estándares internacionales de seguridad son relevantes para este contexto? Menciona al menos 3.

1. ISO/IEC 27001 e ISO/IEC 27002 para gestión y controles de seguridad.
2. NIST Cybersecurity Framework 2.0 y NIST SP 800-63B para riesgos y autenticación.
3. OWASP ASVS y OWASP Top 10 para requisitos y riesgos de aplicaciones web.
También resulta relevante PCI DSS si se procesan datos de tarjetas, además de la
Ley peruana N.° 29733 y los requisitos aplicables de la SBS.

**D.3.2** Diseña la especificación formal de seguridad completa para el módulo de login de esta fintech. Usa la estructura de 7 componentes vista en clase:

| Componente | Tu especificación |
|---|---|
| **Activos a proteger** | Credenciales, datos personales y financieros, tokens, sesiones, claves, logs y disponibilidad del servicio. |
| **Sujetos (roles)** | Cliente, analista, operador, administrador, auditor y servicios internos autenticados. |
| **Objetos (recursos controlados)** | Cuenta, perfil, solicitudes de préstamo, datos financieros, consola administrativa, API y logs. |
| **Operaciones permitidas/denegadas** | El cliente gestiona solo sus datos; el personal accede según su función; el auditor tiene lectura controlada. Se deniega por defecto todo acceso no autorizado. |
| **Condiciones de acceso** | Cuenta activa, TLS, credenciales válidas, MFA, rol autorizado, sesión vigente y evaluación de riesgo. Las operaciones críticas requieren reautenticación. |
| **Mecanismos técnicos** | Argon2id o bcrypt; TLS 1.2/1.3; MFA; RBAC; consultas parametrizadas; rate limiting; cookies seguras; CSRF; HSTS; gestor de secretos; logs y alertas. |
| **Respuesta ante violación** | Bloqueo progresivo, invalidación de sesiones, alerta al SOC, preservación de evidencias, rotación de secretos, contención, análisis y recuperación. |

**D.3.3** Justifica por qué elegiste bcrypt (y no MD5, SHA-256 o AES) para almacenar contraseñas en este sistema financiero. Usa argumentos técnicos y de cumplimiento normativo.

bcrypt está diseñado para contraseñas: incorpora una sal única y un factor de coste
que hace cada intento deliberadamente lento. MD5 y SHA-256 son hashes rápidos y
permiten probar grandes cantidades de contraseñas con GPU. AES es reversible; si se
compromete su clave se recuperan todas las contraseñas. bcrypt es un hash adaptativo,
unidireccional y ampliamente aceptado por las guías de seguridad. En un sistema nuevo
también se evaluaría Argon2id por su resistencia basada en memoria.

---

**D.4** Pregunta de investigación (para completar fuera de clase):

La empresa Adobe sufrió en 2013 una de las brechas de datos más analizadas académicamente, no solo por el número de afectados (153 millones de registros) sino por el **tipo de error criptográfico** cometido.

**D.4.1** Investiga: ¿cómo Adobe almacenaba las contraseñas de sus usuarios? ¿Por qué fue un error tan grave?

Adobe almacenaba las contraseñas mediante cifrado reversible, no con un hash
adaptativo. Los análisis públicos identificaron cifrado simétrico en modo ECB y sin
una sal individual efectiva. Esto permitía agrupar contraseñas iguales, analizarlas
por frecuencia y recuperarlas si se obtenía la clave de cifrado.

**D.4.2** Explica por qué el hint de contraseña (pista de contraseña) que Adobe guardaba junto al hash **empeoró significativamente** el ataque:

Las pistas estaban disponibles sin protección suficiente. Un atacante podía agrupar
cuentas con el mismo texto cifrado y usar pistas reveladoras para deducir una
contraseña común, aplicándola después a todas las cuentas del mismo grupo.

**D.4.3** ¿Qué debió haber hecho Adobe en su lugar?

Debió utilizar un algoritmo como bcrypt, scrypt, PBKDF2 o Argon2id, con sal aleatoria
y única, coste calibrado y, opcionalmente, un `pepper` fuera de la base de datos.
Además, no debió guardar pistas accesibles sin autenticación y debió aplicar MFA,
mínimo privilegio, segmentación, monitoreo y respuesta a incidentes.

---

# SECCIÓN E — ACTIVIDAD COLABORATIVA: ESPECIFICACIÓN FORMAL DE SEGURIDAD

**Integrantes del grupo:**
1. Orellano Huerta Hidgar
2. ____________________________________________________________
3. ____________________________________________________________
4. ____________________________________________________________

**Sistema asignado:** PS-P4 — UQ·CivicVote | Sistema de votación electrónica mejorado con tecnología blockchain

---

### E.1 ESPECIFICACIÓN FORMAL — MÓDULO DE LOGIN

Completa esta especificación para el sistema asignado por el docente:

```
╔══════════════════════════════════════════════════════════════════════╗
║        ESPECIFICACIÓN FORMAL DE SEGURIDAD — MÓDULO LOGIN             ║
║        Sistema: PS-P4 — UQ·CivicVote                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ ACTIVOS                                                              ║
║ (¿Qué datos se protegen en el proceso de login?)                     ║
║                                                                      ║
║ ● Credenciales, MFA, tokens y sesiones.                              ║
║ ● Identidad, padrón y claves públicas de votantes.                   ║
║ ● Privacidad del voto, blockchain y registros de auditoría.          ║
╠══════════════════════════════════════════════════════════════════════╣
║ SUJETOS                                                              ║
║ (¿Quiénes acceden? ¿Con qué roles diferenciados?)                    ║
║                                                                      ║
║ Rol 1: Votante → votar una vez, obtener y verificar comprobante.     ║
║ Rol 2: Administrador → configurar y gestionar elecciones.            ║
║ Rol 3: Auditor → validar cadena y logs en modo de solo lectura.      ║
╠══════════════════════════════════════════════════════════════════════╣
║ OBJETOS                                                              ║
║ (¿A qué recursos controla el acceso el módulo de login?)             ║
║                                                                      ║
║ ● Cuentas, elecciones, candidatos, padrón y claves públicas.         ║
║ ● Boletas, comprobantes, blockchain, panel administrativo y logs.    ║
╠══════════════════════════════════════════════════════════════════════╣
║ MECANISMOS TÉCNICOS                                                  ║
║                                                                      ║
║ Algoritmo hash: bcrypt              Factor/parámetros: coste 12+     ║
║ Protocolo TLS: TLS 1.3/1.2          Cipher suites: ECDHE + AEAD      ║
║ Política de contraseñas:                                             ║
║   Longitud mínima: 15  Complejidad: sin reglas rígidas; blocklist    ║
║ Política de bloqueo:                                                 ║
║   Máx intentos: 5   Duración bloqueo: 15 min  Tipo: progresivo       ║
║ Expiración de sesión: inactividad 15 min / máximo 12 horas           ║
║ MFA: ☐ No ☒ Sí → Tipo: WebAuthn/passkey o TOTP                      ║
╠══════════════════════════════════════════════════════════════════════╣
║ CONDICIONES DE ACCESO                                                ║
║ (Bajo qué circunstancias se permite/deniega el acceso)              ║
║                                                                      ║
║ ● Permitir con HTTPS, cuenta activa, credenciales y MFA válidos.     ║
║ ● Para votar: estar en padrón, elección abierta y no haber votado.   ║
╠══════════════════════════════════════════════════════════════════════╣
║ LOGGING DE SEGURIDAD                                                 ║
║ (¿Qué eventos se registran? ¿Con qué datos?)                        ║
║                                                                      ║
║ Evento 1: Login exitoso/fallido, fecha, ID seudónimo, IP y resultado.║
║ Evento 2: Cambios de rol, apertura/cierre y configuración electoral. ║
║ Evento 3: Doble voto, firma inválida o alteración de la cadena.       ║
╠══════════════════════════════════════════════════════════════════════╣
║ RESPUESTA ANTE VIOLACIÓN                                             ║
║ (¿Qué ocurre cuando se detecta un intento de ataque?)               ║
║                                                                      ║
║ ● Bloqueo progresivo, revocación de sesiones y alerta al auditor.    ║
║ ● Preservar evidencia, contener, rotar secretos y recuperar.         ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### E.2 JUSTIFICACIÓN DE DECISIONES DE DISEÑO

Para cada decisión técnica que tomaron en la especificación, justifiquen por qué la tomaron:

| Decisión técnica tomada | Justificación (¿por qué esta y no otra?) |
|---|---|
| Algoritmo de hash elegido | bcrypt con coste 12+ incluye sal y es deliberadamente lento, a diferencia de hashes rápidos como SHA-256. |
| Versión de TLS elegida | TLS 1.3 ofrece algoritmos modernos y PFS; TLS 1.2 queda solo para compatibilidad con suites ECDHE-AEAD. |
| Política de bloqueo definida | Cinco fallos, espera progresiva y bloqueo temporal de 15 minutos reducen fuerza bruta sin facilitar un bloqueo permanente de cuentas. |
| Decisión sobre MFA | Sí, porque una elección es de alto impacto. WebAuthn resiste phishing y TOTP sirve como alternativa. |

---

### E.3 CASO EXTREMO — ANÁLISIS GRUPAL

Respondan juntos: ¿Qué pasaría si un atacante obtiene acceso directo a la base de datos de su sistema (sin pasar por el login)? ¿Qué información podría obtener y qué NO podría obtener con la especificación que diseñaron?

**Lo que el atacante PODRÍA obtener:**

Identificadores y datos del padrón que no estén cifrados, hashes de contraseñas,
claves públicas, estados de participación, boletas cifradas o hashes, bloques,
marcas de tiempo y otros metadatos almacenados.

**Lo que el atacante NO PODRÍA obtener (gracias a su especificación):**

No obtendría directamente las contraseñas originales ni las claves privadas de los
votantes. Tampoco debería conocer la relación identidad-candidato si esos datos están
separados y anonimizados. Una modificación de votos sería detectable porque alteraría
los hashes de la blockchain.

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN

### F.1 LISTA REVISADA (Volvemos a la Sección B.1)

Vuelve a tu lista de la Sección B.1 (¿qué hace inseguro un login?). Ahora agrega todo lo que descubriste durante la clase:

**Nuevas razones identificadas durante la clase:**

7. No usar MFA en cuentas o acciones de alto impacto.
8. Usar cookies sin atributos `Secure`, `HttpOnly` o `SameSite`.
9. No rotar el identificador de sesión después del login.
10. No expirar ni revocar sesiones.
11. Permitir contraseñas comunes o previamente filtradas.
12. Registrar contraseñas, tokens u OTP en los logs.

---

### F.2 PREGUNTAS DE SÍNTESIS

Responde brevemente:

**F.2.1** ¿Cuál es la diferencia esencial entre hash y cifrado? ¿Por qué se usa hash para contraseñas?

El cifrado es reversible mediante una clave, mientras que el hash es unidireccional.
Para contraseñas se usa un hash adaptativo con sal, porque permite verificar la
coincidencia sin almacenar ni recuperar el valor original.

**F.2.2** ¿Qué hace bcrypt diferente a SHA-256 para resistir ataques de fuerza bruta?

bcrypt incorpora sal y un factor de coste configurable que lo hace deliberadamente
lento. SHA-256 está diseñado para ser rápido, lo que facilita probar millones de
contraseñas con GPU.

**F.2.3** ¿Qué versión de TLS deben usar y por qué las anteriores están descartadas?

Se debe preferir TLS 1.3 y permitir TLS 1.2 solo con configuración segura. SSL 2/3 y
TLS 1.0/1.1 están obsoletos porque admiten algoritmos o diseños débiles y ya no
cumplen las prácticas actuales.

**F.2.4** ¿Cuál fue el error más crítico del código CGI inseguro que analizamos hoy?

La SQL Injection producida al insertar directamente `user` y `pwd` en la consulta.
Este error podría permitir omitir completamente la autenticación y comprometer la
base de datos.

---

### F.3 METACOGNICIÓN PERSONAL (Solo para ti)

Responde honestamente. Nadie más verá estas respuestas:

**F.3.1** ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?

Lo más revelador fue comprender que las contraseñas no deben cifrarse para poder
recuperarlas, sino almacenarse mediante un hash especializado. También entendí que
la seguridad depende del diseño completo y no de un solo algoritmo.

**F.3.2** ¿Qué concepto todavía no tienes completamente claro?

Necesito reforzar la gestión del ciclo de vida de claves criptográficas y la
diferencia práctica entre firma, cifrado y anonimización en el protocolo de votación.

**F.3.3** ¿Qué error de seguridad en código hoy reconoces que podrías haber cometido (o has cometido) antes de esta clase?

Podría haber construido una consulta SQL concatenando los campos del formulario o
usado SHA-256 directamente para contraseñas, pensando que cualquier hash era seguro.

**F.3.4** ¿Cómo cambiaría tu forma de implementar un login después de esta sesión?

Primero definiría activos, roles, amenazas y condiciones medibles. Después aplicaría
consultas parametrizadas, bcrypt/Argon2id, MFA, TLS, sesiones seguras, rate limiting,
mensajes genéricos, mínimo privilegio, logging y pruebas de abuso.



*Guía de Trabajo — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*
