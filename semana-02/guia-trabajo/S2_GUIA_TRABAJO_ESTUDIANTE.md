# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO
## Programación Segura (DD281)

---

**Nombre del estudiante:** Wilder Nicanor Norabuena Ramirez

**Grupo / Sección:** VIII CICLO

**Fecha:** 14 de junio 2026

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
| **Confidencialidad** |Garantiza que las credenciales del usuario (usuario y contraseña) solo sean accesibles por el sistema y no se revelen a terceros. |Uso de cifrado TLS/SSL para proteger la transmisión de la contraseña en la red. |
| **Integridad** |Asegura que los datos de autenticación no sean alterados ni manipulados durante el proceso de validación. |Implementación de hash seguro (SHA-256, bcrypt) para almacenar contraseñas y verificar que no se modifiquen. |
| **Disponibilidad** |Garantiza que el servicio de login esté siempre accesible para los usuarios legítimos cuando lo necesiten. |Uso de balanceadores de carga y redundancia de servidores para evitar caídas del sistema de autenticación. |

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

Marca con ✓ las vulnerabilidades OWASP que se relacionan directamente con un login inseguro y explica brevemente por qué:

| # | Vulnerabilidad OWASP | ¿Relacionada con login? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | X Sí ☐ No |Un login inseguro puede permitir que usuarios sin privilegios accedan a recursos restringidos si no se aplican controles de acceso adecuados. |
| A02 | Cryptographic Failures | X Sí ☐ No |Si las contraseñas no se cifran correctamente en tránsito o almacenamiento, se compromete la confidencialidad del login. |
| A03 | Injection | X Sí ☐ No |Formularios de login mal protegidos pueden ser vulnerables a ataques de inyección SQL, permitiendo eludir la autenticación. |
| A04 | Insecure Design | X Sí ☐ No |Un diseño deficiente del flujo de autenticación (ej. sin MFA, sin bloqueo tras intentos fallidos) facilita ataques de fuerza bruta o robo de credenciales. |
| A07 | Identification/Auth Failures | X Sí ☐ No |Directamente vinculado al login: contraseñas débiles, falta de verificación de identidad y errores en el proceso de autenticación. |

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

¿Cómo aplicarías el principio de Mínimo Privilegio a un sistema de autenticación? Escribe al menos 3 aplicaciones concretas:

1. Asignar a cada usuario únicamente los permisos necesarios para cumplir sus funciones. Por ejemplo, un estudiante solo puede acceder a su perfil y notas, pero no a la administración del sistema.

2. Implementar privilegios con caducidad para tareas específicas. Por ejemplo, un técnico de soporte recibe acceso limitado al panel de usuarios solo durante el tiempo que dura la intervención.

3. Evitar que un mismo usuario tenga privilegios que puedan comprometer la seguridad si se combinan. Por ejemplo, quien aprueba pagos no debe ser el mismo que los registra en el sistema.

---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

Escribe todo lo que se te ocurra:

1. Contraseñas débiles
2. Falta de cifrado 
3. Almacenamiento inseguro
4. Ausencia de bloqueo
5. Sesiones mal gestionadas 
6. Falta de MFA 

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

Es como un “contrato” escrito en términos rigurosos que asegura que aspectos como confidencialidad, integridad y disponibilidad estén correctamente definidos y puedan ser evaluados antes de implementar el sistema.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

| | Ejemplo A | Ejemplo B |
|---|---|---|
| **Texto** | "El login debe ser seguro" | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** |No es formal porque es ambigua y genérica. No define criterios verificables ni parámetros técnicos; “seguro” puede interpretarse de muchas formas distintas. |Sí es formal porque establece requisitos precisos y medibles: algoritmo de hash, factor de coste, número máximo de intentos y tiempo de bloqueo. Estos parámetros pueden implementarse y verificarse objetivamente. |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente | ¿Qué define? |
|---|---|---|
| 1 | **Activos** |Los recursos que deben protegerse: datos, credenciales, sistemas, infraestructura. |
| 2 | **Sujetos** |Los actores que interactúan con el sistema: usuarios, administradores, atacantes potenciales. |
| 3 | **Objetos** |Los elementos sobre los que se realizan operaciones: bases de datos, archivos, sesiones, servicios. |
| 4 | **Operaciones** |Las acciones permitidas o restringidas: leer, escribir, modificar, autenticar, eliminar. |
| 5 | **Condiciones** |Las reglas o restricciones bajo las cuales se ejecutan las operaciones: políticas de acceso, roles, permisos. |
| 6 | **Mecanismos** |Los controles técnicos que implementan la seguridad: cifrado, autenticación multifactor, firewalls, hashing. |
| 7 | **Respuesta ante violación** |Las acciones que se toman si ocurre un incidente: alertas, bloqueo de cuentas, auditoría, recuperación. |

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
-  c) Una librería de JavaScript para crear formularios de login
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

**C.3.1** El proceso de almacenamiento de contraseñas usa HASHING (no cifrado), porque es un proceso UNIDIRECCIONAL que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor ALEATORIO y UNICO por usuario que elimina la posibilidad de usar TABLAS RAINBOW precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de PFS(siglas), lo que significa que si la clave privada del servidor se compromete, el tráfico PASADO no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la ENTRADA estándar del script, mientras que los parámetros GET llegan en la variable de entorno QUERY_STRING.

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el 301.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama PRINCIPIO DE MINIMO PRIVILEGIO.

**C.3.7** Un certificado SSL AUTOFIRMADO (autofirmado) es apropiado para PRUEBAS y ENTORNOS INTERNOS, pero NO para PRODUCCION porque los navegadores muestran una advertencia de seguridad.

**C.3.8** La organización OWASP clasifica como A07 los fallos de IDENTIFICACION y AUTENTICACION, que incluyen contraseñas débiles, ausencia de MFA y sesiones que no expiran.

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
| 1 |SQL Injection |El código construye la consulta SQL concatenando directamente los valores de user y pwd. Un atacante puede inyectar código malicioso para saltarse la autenticación. |Usar consultas parametrizadas (cursor.execute("SELECT ... WHERE usuario=%s AND clave=%s", (user, pwd))). |
| 2 |Contraseña hardcodeada |La contraseña de la base de datos (Admin@2024!) está escrita en el código fuente. Si el archivo se filtra, el atacante obtiene acceso directo. |Guardar credenciales en variables de entorno o un gestor seguro de secretos. |
| 3 |Almacenamiento inseguro de contraseñas |El sistema compara la contraseña en texto plano (clave='{pwd}'). Esto implica que las contraseñas están almacenadas sin hash en la base de datos. |Almacenar contraseñas con bcrypt/argon2id y comparar usando el hash. |
| 4 |Exposición de información sensible |El mensaje de error revela si el usuario existe: "Usuario: {user} no existe". Esto facilita ataques de enumeración de usuarios. |Mostrar un mensaje genérico: “Credenciales inválidas” sin indicar si el usuario existe. |
| 5 |Falta de sanitización de salida |El valor de user y los datos de row se imprimen directamente en HTML. Un atacante podría inyectar código malicioso (XSS). |Escapar las salidas con librerías seguras (ej. html.escape(user)) antes de mostrarlas en la página. |

---

**D.2** Analiza la siguiente política de contraseñas de una empresa e identifica qué está bien y qué está mal según las guías NIST SP 800-63B:

> *"Política de contraseñas de TechCorp SA: Las contraseñas deben tener exactamente 8 caracteres. Deben incluir al menos una letra mayúscula, una minúscula, un número y un símbolo. Las contraseñas deben cambiarse obligatoriamente cada 30 días. El sistema almacena los últimos 3 passwords para no repetirlos. El campo acepta cualquier combinación de caracteres ASCII."*

| Elemento de la política | ¿Correcto o incorrecto? | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres |❌ Incorrecto |NIST recomienda longitud mínima de 8 caracteres, pero no limitar a exactamente 8. Se debe permitir contraseñas más largas para mayor seguridad. |
| Cambio obligatorio cada 30 días |❌ Incorrecto |NIST desaconseja cambios periódicos forzados. Obligar a cambiar cada 30 días genera contraseñas más débiles y reutilización de patrones. Solo deben cambiarse si hay evidencia de compromiso. |
| Historial de 3 passwords |⚠️ Parcialmente correcto |NIST no enfatiza el historial como requisito principal. Puede ayudar a evitar reutilización inmediata, pero no es suficiente por sí solo. Se recomienda más foco en longitud y resistencia. |
| Complejidad obligatoria (mayus+minus+num+simb) |❌ Incorrecto |NIST recomienda permitir frases largas y fáciles de recordar en lugar de imponer reglas de complejidad. Las reglas rígidas llevan a contraseñas difíciles de recordar y patrones predecibles. |

---

### Nivel Avanzado

**D.3** Escenario profesional:

> *Eres el desarrollador líder de una startup fintech peruana que acaba de lanzar su MVP de una app de préstamos personales. El sistema tiene un módulo de login básico. La startup va a solicitar una licencia de operaciones a la SBS (Superintendencia de Banca, Seguros y AFP). La SBS exige cumplimiento con estándares mínimos de seguridad para sistemas financieros.*

**D.3.1** ¿Qué estándares internacionales de seguridad son relevantes para este contexto? Menciona al menos 3.

ISO/IEC 27001: Gestión de seguridad de la información.

PCI DSS: Seguridad en transacciones con tarjetas de pago.

NIST SP 800-63B: Directrices de autenticación digital.

ISO/IEC 22301: Continuidad del negocio.

OWASP ASVS: Estándar de verificación de seguridad de aplicaciones.

**D.3.2** Diseña la especificación formal de seguridad completa para el módulo de login de esta fintech. Usa la estructura de 7 componentes vista en clase:

| Componente | Tu especificación |
|---|---|
| **Activos a proteger** |Credenciales de usuarios (contraseñas, tokens MFA), datos personales y financieros, sesiones activas, logs de acceso. |
| **Sujetos (roles)** |Usuarios clientes, administradores del sistema, auditores internos, atacantes potenciales externos. |
| **Objetos (recursos controlados)** |Base de datos de usuarios, servidor de autenticación, API de login, tokens de sesión, registros de auditoría. |
| **Operaciones permitidas/denegadas** |Permitidas: iniciar sesión, cerrar sesión, recuperar contraseña, validar MFA. Denegadas: acceso sin credenciales válidas, manipulación de tokens, consultas directas a la base de datos de credenciales. |
| **Condiciones de acceso** |Credenciales válidas con hash seguro (bcrypt/argon2id), MFA obligatorio, conexión cifrada TLS 1.3, límite de intentos fallidos (máx. 5 antes de bloqueo temporal). |
| **Mecanismos técnicos** |Hashing con sal aleatoria, autenticación multifactor, TLS 1.3 con Perfect Forward Secrecy, protección contra fuerza bruta, sanitización de entradas, gestión segura de sesiones (expiración, regeneración de tokens). |
| **Respuesta ante violación** |Bloqueo inmediato de cuenta tras intentos sospechosos, alertas al SOC (Security Operations Center), registro en logs de auditoría, análisis forense, notificación al usuario y reporte a SBS si compromete datos financieros. |

**D.3.3** Justifica por qué elegiste bcrypt (y no MD5, SHA-256 o AES) para almacenar contraseñas en este sistema financiero. Usa argumentos técnicos y de cumplimiento normativo.

Argumentos técnicos
. Bcrypt es intencionalmente lento y configurable, lo que dificulta ataques de fuerza bruta.

. Incluye sal aleatoria integrada, evitando ataques con tablas rainbow.

. Es un hash unidireccional, por lo que las contraseñas no pueden revertirse ni descifrarse.

. Tiene amplia adopción y soporte en sistemas críticos, a diferencia de MD5 (obsoleto), SHA-256 (rápido y sin sal por defecto) o AES (reversible).

Argumentos normativos
. NIST SP 800-63B recomienda bcrypt, scrypt o argon2id para contraseñas; desaconseja MD5 y SHA-1.

. ISO/IEC 27001 y OWASP ASVS exigen almacenamiento resistente a ataques offline, lo que bcrypt cumple.

. SBS Perú requiere alineación con estándares internacionales, y bcrypt demuestra cumplimiento en auditorías de sistemas financieros.
---

**D.4** Pregunta de investigación (para completar fuera de clase):

La empresa Adobe sufrió en 2013 una de las brechas de datos más analizadas académicamente, no solo por el número de afectados (153 millones de registros) sino por el **tipo de error criptográfico** cometido.

**D.4.1** Investiga: ¿cómo Adobe almacenaba las contraseñas de sus usuarios? ¿Por qué fue un error tan grave?

Adobe no almacenaba las contraseñas con un hash seguro (como bcrypt o Argon2). En su lugar, las guardaba como contraseñas cifradas simétricamente con la misma clave. Esto fue un error grave porque:

. El cifrado es reversible: si la clave se filtra, todas las contraseñas pueden descifrarse.

. No había uso de sal aleatoria, lo que permitió a los atacantes correlacionar contraseñas iguales.

. Se expusieron 153 millones de registros, lo que convirtió el incidente en uno de los más estudiados en seguridad.

**D.4.2** Explica por qué el hint de contraseña (pista de contraseña) que Adobe guardaba junto al hash **empeoró significativamente** el ataque:

Adobe almacenaba junto al hash/cifrado un hint de contraseña (pista) escrito por el usuario.

. Muchas pistas eran extremadamente reveladoras (“mi perro”, “fecha de nacimiento”, etc.).

. Los atacantes pudieron usar esas pistas para adivinar contraseñas sin necesidad de romper el cifrado.

. En combinación con el cifrado reversible, los hints facilitaron ataques masivos de descifrado y correlación de cuentas.

**D.4.3** ¿Qué debió haber hecho Adobe en su lugar?

. Usar un algoritmo de hash seguro y lento como bcrypt o argon2id, con sal aleatoria por usuario.

. No almacenar hints de contraseña en texto plano junto al hash.

. Implementar autenticación multifactor (MFA) para reducir el impacto de contraseñas comprometidas.

. Cumplir con estándares como NIST SP 800-63B y OWASP ASVS, que prohíben almacenamiento reversible de contraseñas.

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
