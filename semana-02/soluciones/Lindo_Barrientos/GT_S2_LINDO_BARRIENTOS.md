# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO
## Programación Segura (DD281)

---

**Nombre del estudiante:** LINDO BARRIENTOS JHONN VIEQUIER

**Grupo / Sección:** GRUPO 01 / SECCION 06

**Fecha:** 20/06/2026

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

| Pilar CIA | ¿Cómo se manifiesta en un sistema de login? | Ejemplo concreto |
|---|---|---|
| **Confidencialidad** | Las credenciales no deben ser visibles ni recuperables por terceros: viajan cifradas por el canal y se almacenan de forma irreversible. | La contraseña se envía sobre HTTPS (TLS) y se guarda como hash **bcrypt**, nunca en texto plano. |
| **Integridad** | Las credenciales, el rol y la consulta de autenticación no deben poder alterarse en tránsito ni manipularse desde la entrada del usuario. | Uso de **prepared statements** (parámetros `?`) que impiden modificar la lógica de la consulta vía inyección SQL. |
| **Disponibilidad** | El servicio de login debe seguir disponible para los usuarios legítimos, incluso bajo intentos de abuso. | **Rate limiting / bloqueo temporal** que frena la fuerza bruta sin tumbar el servicio para los demás usuarios. |

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

| # | Vulnerabilidad OWASP | ¿Relacionada con login? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | ☑ **Sí** | El login es la puerta del control de acceso; si falla la verificación de identidad o de rol, un atacante puede acceder a recursos o escalar privilegios. |
| A02 | Cryptographic Failures | ☑ **Sí** | Aplica directamente al almacenamiento de contraseñas (hash vs texto plano) y al cifrado del canal (TLS). |
| A03 | Injection | ☑ **Sí** | El campo usuario/contraseña es un vector clásico de **SQL Injection** si se concatena la entrada en la consulta. |
| A04 | Insecure Design | ☑ **Sí** | La ausencia de bloqueo de intentos, MFA o expiración de sesión son fallas de **diseño**, no de implementación. |
| A07 | Identification/Auth Failures | ☑ **Sí** | Es la categoría que describe directamente los fallos de autenticación: contraseñas débiles, sin MFA, sesiones que no expiran, enumeración de usuarios. |

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

1. La cuenta de base de datos que usa la aplicación de login tiene **solo permisos `SELECT` y `UPDATE`** sobre la tabla `usuarios`, nunca `DROP`, `DELETE` masivo ni privilegios de administrador del motor.

2. Cada usuario recibe el **rol mínimo necesario** (por defecto `estudiante`); los privilegios elevados (`docente`, `administrador`) se asignan de forma explícita y justificada.

3. El proceso del servidor/CGI se ejecuta con un **usuario del sistema sin privilegios** (no `root`), y la clave privada SSL tiene permisos `600` (solo lectura para su dueño).

---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

1. Guardar las contraseñas en texto plano (o con un hash débil sin sal).
2. No usar HTTPS: las credenciales viajan en claro y pueden ser interceptadas.
3. No limitar los intentos: permite ataques de fuerza bruta y diccionario.
4. Concatenar la entrada del usuario en la consulta SQL (SQL Injection).
5. Mensajes de error que revelan si el usuario existe (enumeración de usuarios).
6. No ofrecer segundo factor (MFA) ni expiración de sesión.

*(Al final de la clase volveremos a esta lista para ver cuánto más podemos agregar)*

---

### B.2 PREGUNTAS DE DIAGNÓSTICO

**B.2.1** ¿Cómo se deben almacenar las contraseñas en una base de datos?

- ☐ a) En texto plano para facilitar la recuperación
- ☐ b) Cifradas con AES-256 para poder descifrarlas si el usuario las olvida
- ☑ **c) Como hash unidireccional con sal aleatoria**
- ☐ d) Codificadas en Base64 para "ofuscarlas"

**B.2.2** ¿Qué versión de TLS/SSL deben usar los servidores web en 2024?

- ☐ a) SSL 3.0 — es la versión estándar
- ☐ b) TLS 1.0 — compatible con todos los dispositivos
- ☑ **c) TLS 1.2 mínimo, preferiblemente TLS 1.3**
- ☐ d) La versión no importa, cualquier SSL es suficiente

**B.2.3** ¿Qué es un certificado SSL autofirmado (self-signed)?

- ☐ a) Un certificado gratuito de Let's Encrypt
- ☑ **b) Un certificado creado por uno mismo sin validación de una CA externa**
- ☐ c) Un certificado de mayor seguridad que el emitido por una CA
- ☐ d) El tipo de certificado requerido en producción

---

# SECCIÓN C — CONCEPTOS CLAVE DE LA SESIÓN
## Completa durante la explicación del docente

---

### C.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD

**C.1.1** Escribe con tus propias palabras qué es una especificación formal de seguridad:

Es la definición **precisa, completa y verificable** de los requisitos de seguridad de un sistema, expresada en términos medibles (parámetros, valores, condiciones) en lugar de frases ambiguas. Establece **qué se protege, quién accede, bajo qué condiciones y con qué mecanismos**, de modo que cualquier ingeniero pueda implementarla y auditarla sin interpretar intenciones.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

| | Ejemplo A | Ejemplo B |
|---|---|---|
| **Texto** | "El login debe ser seguro" | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** | **No es formal:** es vaga y subjetiva. "Seguro" no es medible ni verificable; dos desarrolladores la implementarían de forma distinta y no se puede auditar el cumplimiento. | **Sí es formal:** define parámetros concretos (algoritmo, factor de coste, número de intentos, tiempo de bloqueo) que son medibles, implementables y auditables de forma objetiva. |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente | ¿Qué define? |
|---|---|---|
| 1 | **Activos** | Qué datos o recursos de valor se protegen (credenciales, datos personales, sesiones, registros). |
| 2 | **Sujetos** | Quiénes acceden al sistema y con qué roles diferenciados (usuario, docente, administrador). |
| 3 | **Objetos** | Los recursos concretos sobre los que se controla el acceso (tablas, endpoints, dashboards). |
| 4 | **Operaciones** | Las acciones permitidas o denegadas para cada sujeto (autenticarse, leer, modificar). |
| 5 | **Condiciones** | Las circunstancias bajo las que se permite o deniega el acceso (HTTPS activo, cuenta no bloqueada, horario, MFA superado). |
| 6 | **Mecanismos** | Los controles técnicos que hacen cumplir lo anterior (bcrypt, TLS 1.2+, prepared statements, bloqueo de intentos). |
| 7 | **Respuesta ante violación** | Qué ocurre cuando se detecta un intento de ataque (registro en log, bloqueo, mensaje genérico, alerta al administrador). |

---

### C.2 PREGUNTAS PARA MARCAR (Selección múltiple)

**C.2.1** ¿Cuál es el problema de almacenar contraseñas con SHA-1 SIN SAL?

- ☐ a) SHA-1 no produce un hash — produce texto cifrado
- ☐ b) SHA-1 es reversible — se puede obtener la contraseña original
- ☑ **c) Los atacantes pueden usar tablas rainbow precomputadas para romper el hash**
- ☐ d) SHA-1 produce hashes demasiado cortos para ser seguros

**C.2.2** ¿Qué ventaja fundamental tiene bcrypt sobre SHA-256 para almacenar contraseñas?

- ☐ a) Bcrypt produce hashes más largos que SHA-256
- ☑ **b) Bcrypt incluye automáticamente sal aleatoria y es intencionalmente lento**
- ☐ c) Bcrypt es un algoritmo de cifrado, no de hash
- ☐ d) Bcrypt es más rápido que SHA-256, mejorando el rendimiento del login

**C.2.3** ¿Qué es la "sal" (salt) en el contexto del hashing de contraseñas?

- ☐ a) Un algoritmo de cifrado adicional aplicado al hash
- ☐ b) La clave secreta usada para cifrar el hash antes de almacenarlo
- ☑ **c) Un valor aleatorio único por usuario que se concatena a la contraseña antes de hashear**
- ☐ d) El factor de coste que determina cuántas rondas de hashing se ejecutan

**C.2.4** ¿Por qué es un error de seguridad grave que el formulario de login use el método HTTP GET?

- ☐ a) Porque GET no puede transportar datos de texto
- ☑ **b) Porque los parámetros GET viajan en la URL y quedan en logs del servidor y en el historial del navegador**
- ☐ c) Porque GET es más lento que POST para transferir datos
- ☐ d) Porque GET no cifra los datos antes de enviarlos

**C.2.5** ¿Qué es Perfect Forward Secrecy (PFS) en TLS?

- ☐ a) Un mecanismo que cifra el certificado del servidor con una segunda clave
- ☐ b) La capacidad del servidor de descifrar tráfico pasado si se compromete la clave privada
- ☑ **c) El uso de claves de sesión efímeras para que el compromiso de la clave privada del servidor no permita descifrar tráfico pasado**
- ☐ d) La verificación automática de que el certificado SSL no ha expirado

**C.2.6** ¿Cuál de los siguientes es el estándar de hash de contraseñas más recomendado hoy?

- ☐ a) MD5 con sal de 16 bytes
- ☐ b) SHA-512 sin sal
- ☑ **c) bcrypt (factor 12+) o argon2id**
- ☐ d) AES-256 con clave de 32 bytes

**C.2.7** ¿Cuál de las siguientes configuraciones de servidor web es correcta en relación a SSL?

- ☐ a) Habilitar SSL 3.0, TLS 1.0, TLS 1.1 y TLS 1.2 para máxima compatibilidad
- ☐ b) Usar solo TLS 1.3 y deshabilitar todas las versiones anteriores
- ☐ c) Deshabilitar SSL 2.0 y SSL 3.0, mantener TLS 1.0, 1.1, 1.2 y 1.3
- ☑ **d) Usar TLS 1.2 y TLS 1.3, deshabilitar versiones anteriores**

**C.2.8** ¿Qué es CGI (Common Gateway Interface)?

- ☐ a) Un framework de Python para desarrollo web seguro
- ☑ **b) Un protocolo estándar que define cómo un servidor web pasa solicitudes a programas externos para generar respuestas dinámicas**
- ☐ c) Una librería de JavaScript para crear formularios de login
- ☐ d) Un tipo de certificado SSL para servidores compartidos

**C.2.9** Un atacante ejecuta el siguiente input en el campo de usuario de un login CGI inseguro: `admin' --`. ¿Qué tipo de ataque es este y qué efecto tendría?

- ☐ a) XSS — inyecta código JavaScript en la página
- ☑ **b) SQL Injection — el `'--` cierra la query y comenta el resto, posiblemente bypasseando la verificación de contraseña**
- ☐ c) CSRF — falsifica una solicitud de otro dominio
- ☐ d) Path Traversal — intenta acceder a archivos del sistema

**C.2.10** ¿Cuál es el propósito del header HTTP `Strict-Transport-Security`?

- ☐ a) Obliga al servidor a responder solo con JSON
- ☑ **b) Le indica al navegador que siempre use HTTPS para ese dominio, incluso si el usuario escribe HTTP**
- ☐ c) Restringe el origen de las solicitudes al dominio del servidor
- ☐ d) Cifra automáticamente todos los cookies del servidor

---

### C.3 PREGUNTAS DE COMPLETAR

**C.3.1** El proceso de almacenamiento de contraseñas usa **hash** (no cifrado), porque es un proceso **unidireccional (irreversible)** que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor **aleatorio** y **único** por usuario que elimina la posibilidad de usar **tablas rainbow** precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de **PFS (Perfect Forward Secrecy)** (siglas), lo que significa que si la clave privada del servidor se compromete, el tráfico **pasado (capturado previamente)** no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la **entrada estándar (STDIN)** del script, mientras que los parámetros GET llegan en la variable de entorno **`QUERY_STRING`**.

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el **301 (Moved Permanently)**.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama **mínimo privilegio**.

**C.3.7** Un certificado SSL **autofirmado** (autofirmado) es apropiado para **desarrollo** y **pruebas en laboratorio (entornos internos)**, pero NO para **producción** porque los navegadores muestran una advertencia de seguridad.

**C.3.8** La organización OWASP clasifica como A07 los fallos de **identificación** y **autenticación**, que incluyen contraseñas débiles, ausencia de MFA y sesiones que no expiran.

---

# SECCIÓN D — PREGUNTAS DE ANÁLISIS

### Nivel Intermedio

**D.1** Identifica y describe **5 vulnerabilidades** de seguridad específicas del fragmento:

| # | Vulnerabilidad identificada | Descripción del riesgo | Cómo corregirla |
|---|---|---|---|
| 1 | **SQL Injection** (`sql = f"... usuario='{user}' ..."`) | La entrada se concatena directamente en la consulta; un atacante con `admin' --` bypassea la verificación o extrae/destruye datos. | Usar **prepared statements** con parámetros: `cursor.execute("... WHERE usuario=%s AND clave=%s", (user, pwd))`. |
| 2 | **Contraseña comparada en texto plano** (`clave='{pwd}'`) | La BD guarda y compara contraseñas sin hash; una fuga de la BD expone todas las credenciales. | Almacenar **hash bcrypt** y verificar con `bcrypt.checkpw()`. |
| 3 | **Credenciales hardcodeadas en el código** (`password="Admin@2024!"`) | Cualquiera con acceso al fuente (o al repositorio) obtiene la clave de la BD de producción. | Leer credenciales desde **variables de entorno** o un gestor de secretos; nunca en el código. |
| 4 | **XSS reflejado** (`{user}` y `{row}` impresos sin escapar) | Un input como `<script>...</script>` se ejecuta en el navegador de la víctima. | Escapar toda salida con `html.escape()` antes de imprimirla. |
| 5 | **Enumeración de usuarios + exposición de datos** (`"Usuario: {user} no existe"` y `Datos del empleado: {row}`) | Revela si el usuario existe (facilita ataques dirigidos) y filtra el registro completo del empleado. | Mensaje **genérico** ("Credenciales incorrectas") y no devolver datos sensibles en la respuesta. |

*(Vulnerabilidades adicionales presentes: ausencia de HTTPS, sin rate limiting/bloqueo, sin logging de intentos.)*

---

**D.2** Análisis de la política de contraseñas según NIST SP 800-63B:

| Elemento de la política | ¿Correcto o incorrecto? | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres | **Incorrecto** | NIST exige un **mínimo** de 8 (idealmente permitir hasta 64+). Fijar la longitud "exacta" en 8 reduce drásticamente la entropía y prohíbe frases de paso largas, que son más seguras. |
| Cambio obligatorio cada 30 días | **Incorrecto** | NIST **desaconseja** la expiración periódica sin evidencia de compromiso: induce a los usuarios a crear patrones débiles (`Clave01`, `Clave02`). Solo se debe forzar el cambio ante sospecha de fuga. |
| Historial de 3 passwords | **Parcialmente correcto / aceptable** | Evitar la reutilización inmediata es razonable, pero NIST no lo prioriza; es una medida menor frente a la longitud y la verificación contra listas de contraseñas comprometidas. |
| Complejidad obligatoria (mayús+minús+núm+símb) | **Incorrecto** | NIST recomienda **no imponer reglas de composición**. Lo eficaz es exigir longitud y **comparar contra listas de contraseñas filtradas/comunes**, no obligar combinaciones que el usuario termina anotando. |

---

### Nivel Avanzado

**D.3** Escenario profesional — fintech peruana ante la SBS.

**D.3.1** Estándares internacionales relevantes (al menos 3):

1. **ISO/IEC 27001** — Sistema de Gestión de Seguridad de la Información (SGSI).
2. **PCI DSS** — obligatorio si la app maneja datos de tarjetas de pago.
3. **NIST SP 800-63B** — guías de autenticación y manejo de contraseñas.
4. **OWASP ASVS** — estándar de verificación de seguridad en aplicaciones (nivel 2/3 para fintech).
5. **Marco regulatorio peruano de la SBS** — normativa de gestión de seguridad de la información y ciberseguridad para entidades supervisadas (p. ej. el Reglamento de Gestión de la Seguridad de la Información y Ciberseguridad de la SBS).

**D.3.2** Especificación formal de seguridad del módulo de login (7 componentes):

| Componente | Tu especificación |
|---|---|
| **Activos a proteger** | Credenciales de clientes, datos personales y financieros (DNI, cuentas, montos de préstamo), tokens de sesión, registros de auditoría. |
| **Sujetos (roles)** | Cliente, Analista de crédito, Administrador del sistema, Auditor (solo lectura de logs). |
| **Objetos (recursos controlados)** | Tabla de usuarios, endpoint de autenticación, dashboard de cliente, panel administrativo, registros de transacciones. |
| **Operaciones permitidas/denegadas** | Cliente: solo autenticarse y operar su propia cuenta. Admin: gestionar usuarios pero sin ver contraseñas. Nadie puede leer hashes ni desactivar el logging. |
| **Condiciones de acceso** | HTTPS (TLS 1.2+) obligatorio; cuenta activa y no bloqueada; **MFA superado**; sesión vigente (timeout por inactividad). |
| **Mecanismos técnicos** | Hash **bcrypt factor 12** (o argon2id); TLS 1.2/1.3 con PFS; prepared statements; bloqueo tras 5 intentos por 15 min; MFA (OTP/app); cifrado en reposo de datos sensibles. |
| **Respuesta ante violación** | Registro del evento en log de auditoría inmutable, bloqueo temporal de la cuenta, mensaje genérico al usuario, alerta al equipo de seguridad y, ante patrón de ataque, bloqueo por IP. |

**D.3.3** Justificación de bcrypt frente a MD5, SHA-256 o AES en un sistema financiero:

- Frente a **MD5/SHA-256**: estos son hashes **rápidos**, diseñados para velocidad, lo que los hace ideales para que un atacante pruebe miles de millones de combinaciones por segundo (GPU). **bcrypt es intencionalmente lento** y tiene un **factor de coste ajustable**, encareciendo enormemente la fuerza bruta. Además, bcrypt **incorpora sal aleatoria por usuario** de forma automática, eliminando las tablas rainbow; MD5/SHA-256 requieren añadir sal manualmente y aun así siguen siendo demasiado rápidos.
- Frente a **AES**: AES es **cifrado reversible**, no hash. Implica gestionar una clave que, si se filtra, permite **descifrar todas las contraseñas**. Para autenticación nunca se necesita recuperar la contraseña original, solo verificarla, por lo que un proceso **unidireccional (hash)** es lo correcto.
- **Cumplimiento normativo**: NIST SP 800-63B, OWASP ASVS y las exigencias de la SBS apuntan a funciones de derivación de clave robustas (bcrypt/argon2id/PBKDF2), no a hashes rápidos ni a cifrado reversible para contraseñas.

---

**D.4** Pregunta de investigación — brecha de Adobe (2013):

**D.4.1** ¿Cómo almacenaba Adobe las contraseñas y por qué fue grave?

Adobe **no hasheaba** las contraseñas: las **cifraba con un algoritmo simétrico (3DES) en modo ECB usando una única clave** para todos los usuarios. Fue grave por dos razones: (1) al ser cifrado, es **reversible** —quien obtuviera la clave podría descifrar todo—; y (2) el modo **ECB produce el mismo bloque cifrado para la misma contraseña**, de modo que todos los usuarios con idéntica contraseña tenían idéntico texto cifrado, revelando patrones.

**D.4.2** ¿Por qué el "hint" (pista) empeoró el ataque?

Adobe guardó las **pistas de contraseña en texto plano** junto a los datos cifrados. Como el modo ECB agrupaba a los usuarios con la misma contraseña, bastaba leer las pistas de ese grupo para **deducir la contraseña común**; una sola pista acertada "rompía" a todos los que compartían esa clave.

**D.4.3** ¿Qué debió hacer Adobe?

Aplicar **hashing unidireccional con sal única por usuario** (bcrypt/scrypt/argon2id), **nunca almacenar pistas de contraseña** en texto plano, y no usar una clave de cifrado compartida ni modos sin difusión como ECB.

---

# SECCIÓN E — ACTIVIDAD COLABORATIVA: ESPECIFICACIÓN FORMAL DE SEGURIDAD

> **Nota:** Esta sección es grupal y depende del sistema que asigne el docente. A continuación, un modelo completo usando como ejemplo el **Portal Académico Universitario (intranet del estudiante)**. Ajusta los integrantes y el sistema a lo que te asignen.

**Integrantes del grupo:**
1. Jhonn Viequier Lindo Barrientos
2. _(completar)_
3. _(completar)_
4. _(completar)_

**Sistema asignado:** Portal Académico Universitario — Módulo de Login _(ajustar al asignado)_

---

### E.1 ESPECIFICACIÓN FORMAL — MÓDULO DE LOGIN

```
╔══════════════════════════════════════════════════════════════════════╗
║        ESPECIFICACIÓN FORMAL DE SEGURIDAD — MÓDULO LOGIN            ║
║        Sistema: Portal Académico Universitario                       ║
╠══════════════════════════════════════════════════════════════════════╣
║ ACTIVOS                                                              ║
║ (¿Qué datos se protegen en el proceso de login?)                     ║
║                                                                      ║
║ ● Credenciales (usuario + hash de contraseña)                        ║
║ ● Datos personales y académicos (notas, matrícula, pagos)            ║
║ ● Tokens de sesión y registros de auditoría                          ║
╠══════════════════════════════════════════════════════════════════════╣
║ SUJETOS                                                              ║
║ (¿Quiénes acceden? ¿Con qué roles diferenciados?)                   ║
║                                                                      ║
║ Rol 1: Estudiante      → Permisos: ver/operar su propia info         ║
║ Rol 2: Docente         → Permisos: gestionar notas de sus cursos     ║
║ Rol 3: Administrador   → Permisos: gestión de usuarios (sin ver pwd) ║
╠══════════════════════════════════════════════════════════════════════╣
║ OBJETOS                                                              ║
║ (¿A qué recursos controla el acceso el módulo de login?)            ║
║                                                                      ║
║ ● Tabla de usuarios y endpoint de autenticación                      ║
║ ● Dashboards por rol y registros académicos                          ║
╠══════════════════════════════════════════════════════════════════════╣
║ MECANISMOS TÉCNICOS                                                  ║
║                                                                      ║
║ Algoritmo hash: bcrypt            Factor/parámetros: coste 12         ║
║ Protocolo TLS: TLS 1.2 / 1.3      Cipher suites: ECDHE+AESGCM (PFS)   ║
║ Política de contraseñas:                                             ║
║   Longitud mínima: 12  Complejidad: longitud + lista de comprometidas║
║ Política de bloqueo:                                                 ║
║   Máx intentos: 5  Duración bloqueo: 15 min  Tipo: temporal          ║
║ Expiración de sesión: inactividad 15 min / máximo 8 h                ║
║ MFA: ☐ No ☑ Sí → Tipo: OTP por app autenticadora                     ║
╠══════════════════════════════════════════════════════════════════════╣
║ CONDICIONES DE ACCESO                                                ║
║ (Bajo qué circunstancias se permite/deniega el acceso)              ║
║                                                                      ║
║ ● Solo sobre HTTPS, con cuenta activa y no bloqueada                  ║
║ ● Tras superar MFA y con sesión vigente                              ║
╠══════════════════════════════════════════════════════════════════════╣
║ LOGGING DE SEGURIDAD                                                 ║
║ (¿Qué eventos se registran? ¿Con qué datos?)                        ║
║                                                                      ║
║ Evento 1: AUTH_SUCCESS (usuario, rol, IP, fecha/hora)                ║
║ Evento 2: AUTH_FAILURE (usuario, intento n/5, IP, fecha/hora)        ║
║ Evento 3: CUENTA_BLOQUEADA (usuario, IP, hasta cuándo)               ║
╠══════════════════════════════════════════════════════════════════════╣
║ RESPUESTA ANTE VIOLACIÓN                                             ║
║ (¿Qué ocurre cuando se detecta un intento de ataque?)               ║
║                                                                      ║
║ ● Bloqueo temporal de la cuenta + mensaje genérico al usuario        ║
║ ● Registro en log + alerta al administrador; bloqueo por IP si       ║
║   se detecta patrón de fuerza bruta                                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### E.2 JUSTIFICACIÓN DE DECISIONES DE DISEÑO

| Decisión técnica tomada | Justificación (¿por qué esta y no otra?) |
|---|---|
| Algoritmo de hash elegido | **bcrypt (factor 12):** lento por diseño y con sal automática por usuario, resiste fuerza bruta y rainbow tables, a diferencia de MD5/SHA-256 que son rápidos. |
| Versión de TLS elegida | **TLS 1.2 mínimo, idealmente 1.3:** garantiza cifrado fuerte y PFS; las versiones SSL/TLS 1.0/1.1 tienen vulnerabilidades conocidas (POODLE, BEAST) y están descartadas. |
| Política de bloqueo definida | **5 intentos / 15 min temporal:** frena fuerza bruta sin permitir un DoS permanente sobre la cuenta de un usuario legítimo; el bloqueo es temporal, no definitivo. |
| Decisión sobre MFA | **MFA activado (OTP):** un segundo factor reduce el impacto del robo de contraseñas; crítico al manejar datos académicos y de pago. |

---

### E.3 CASO EXTREMO — ANÁLISIS GRUPAL

**Lo que el atacante PODRÍA obtener:**

Los registros de la tabla `usuarios` (nombres de usuario, roles, estados) y los **hashes bcrypt** de las contraseñas. Con esos hashes podría intentar fuerza bruta **offline**, aunque el coste 12 lo hace lento y costoso. También vería la estructura de la BD.

**Lo que el atacante NO PODRÍA obtener (gracias a su especificación):**

Las **contraseñas en claro** (son hashes irreversibles con sal única, no descifrables). Tampoco podría reutilizar los hashes en otro sistema ni deducir contraseñas comunes (cada hash es distinto aunque la contraseña coincida). Si los datos sensibles están **cifrados en reposo**, su contenido seguiría protegido sin la clave.

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN

### F.1 LISTA REVISADA (Volvemos a la Sección B.1)

**Nuevas razones identificadas durante la clase:**

7. Usar hashes rápidos (MD5/SHA-1) o sin sal, vulnerables a rainbow tables.
8. No prevenir **timing attacks** (revelar por el tiempo de respuesta si el usuario existe).
9. Falta de headers de seguridad HTTP (HSTS, X-Frame-Options, X-Content-Type-Options).
10. Usar certificados/SSL obsoletos o versiones TLS antiguas (1.0/1.1).
11. No registrar (loggear) los eventos de autenticación para detección y auditoría.
12. Exponer información excesiva en la respuesta (datos del registro, versión del servidor).

---

### F.2 PREGUNTAS DE SÍNTESIS

**F.2.1** ¿Diferencia entre hash y cifrado? ¿Por qué hash para contraseñas?

El **cifrado es reversible** (con la clave se recupera el dato original); el **hash es unidireccional** (no se puede revertir). Para contraseñas se usa **hash** porque el sistema nunca necesita recuperar la contraseña original, solo verificar que coincide; así, aunque la BD se filtre, las contraseñas no se pueden recuperar.

**F.2.2** ¿Qué hace bcrypt diferente a SHA-256 contra fuerza bruta?

bcrypt es **intencionalmente lento** y tiene un **factor de coste ajustable**, que encarece cada intento; además **integra sal aleatoria por usuario**. SHA-256 es rápido (millones de hashes por segundo en GPU) y no salea por sí solo, por lo que es mucho más fácil de atacar por fuerza bruta.

**F.2.3** ¿Qué versión de TLS usar y por qué se descartan las anteriores?

**TLS 1.2 como mínimo, idealmente TLS 1.3.** SSL 2.0/3.0 y TLS 1.0/1.1 tienen vulnerabilidades conocidas (POODLE, BEAST), cifrados débiles y no garantizan PFS, por lo que están oficialmente deprecados.

**F.2.4** ¿Cuál fue el error más crítico del CGI inseguro analizado?

La **SQL Injection** por concatenar la entrada del usuario en la consulta (`f"... usuario='{user}' ..."`): permite bypassear la autenticación con `admin' --` o `' OR '1'='1`, e incluso extraer o destruir datos. Es el de mayor impacto porque compromete directamente el control de acceso.

---

### F.3 METACOGNICIÓN PERSONAL (Solo para ti)

> _Respuestas personales — ajústalas a tu propia experiencia._

**F.3.1** ¿Qué fue lo más sorprendente o revelador de la sesión?

Que bcrypt sea **lento a propósito** y que eso sea una **característica de seguridad**, no un defecto de rendimiento. Cambia por completo la intuición de que "más rápido es mejor".

**F.3.2** ¿Qué concepto todavía no tienes completamente claro?

El detalle de cómo TLS 1.3 negocia las claves efímeras para lograr **Perfect Forward Secrecy**; entiendo el qué, quiero profundizar en el cómo del intercambio (ECDHE).

**F.3.3** ¿Qué error de seguridad reconoces que podrías haber cometido antes?

Construir consultas SQL concatenando variables (f-strings) y mostrar mensajes de error que revelan si el usuario existe; antes lo veía como "ayuda al usuario", ahora como una fuga de información.

**F.3.4** ¿Cómo cambiaría tu forma de implementar un login?

Usaría siempre **prepared statements**, **bcrypt con sal**, **HTTPS con TLS 1.2+**, **bloqueo de intentos**, **mensajes genéricos**, **headers de seguridad** y **logging**, tratando la especificación formal como punto de partida, no como un añadido al final.

---

### F.4 TAREA PARA LA SEMANA 3 — AUDITORÍA DE LOGIN EN CAMPO

> **Nota:** Debes realizar tu propia auditoría. El valor de TLS y la calificación SSL Labs cambian con el tiempo, así que ejecútalos tú mismo en `ssllabs.com/ssltest`. A continuación, un **ejemplo de cómo completarlo** (datos ilustrativos).

**Sistema auditado:** Intranet del Estudiante — Universidad _(el sistema que elijas)_

**URL / Nombre de la app:** _(completar con la URL real)_

| Criterio de auditoría | Resultado | Herramienta usada |
|---|---|---|
| ¿Usa HTTPS? | ☑ Sí ☐ No | Barra del navegador (candado) |
| ¿Qué versión de TLS usa? | TLS 1.2 / 1.3 _(verificar)_ | SSL Labs |
| ¿Calificación SSL Labs? | A / B / C / D / F _(tu resultado)_ | ssllabs.com/ssltest |
| ¿Formulario usa POST o GET? | POST _(verificar en código)_ | Inspección de código (F12) |
| ¿Tiene política de bloqueo de intentos? | Sí/No _(probar con cuenta propia)_ | Intento manual |
| ¿Ofrece MFA (2FA)? | ☐ Sí ☐ No _(verificar)_ | Observación |
| ¿Muestra mensajes de error genéricos? | ☐ Sí ☐ No _(verificar)_ | Observación |

**Observación más importante (¿qué encontraste?):**

_(Ejemplo)_ El formulario envía las credenciales por POST sobre HTTPS, pero el mensaje de error distingue entre "usuario no existe" y "contraseña incorrecta", lo que habilita enumeración de usuarios.

**Recomendación de mejora:**

_(Ejemplo)_ Unificar el mensaje de error en uno genérico ("Credenciales incorrectas"), añadir bloqueo temporal tras varios intentos y habilitar MFA.

---

*Guía de Trabajo — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*
