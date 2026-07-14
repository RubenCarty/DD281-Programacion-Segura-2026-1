# GUÍA DE TRABAJO — ESTUDIANTE

# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO

## Programación Segura (DD281)

---

**Nombre del estudiante:** Armando J. Carbajal Campomanes

**Grupo / Sección:** _____________________________________________________

**Fecha:** 13/06/2026

**Instrucciones generales:**

* Completa esta guía durante la sesión de clase en los momentos indicados por el docente.
* Sección A y B: durante la primera hora.
* Sección C y D: durante la segunda hora (después del receso).
* Sección E: actividad grupal práctica.
* Sección F: cierre y metacognición.

---

# SECCIÓN A — RECUPERACIÓN DE APRENDIZAJES (Semana 1)

## Responde antes de que el docente lo explique. Luego verifica tu respuesta.

---

### A.1 LA TRIADA CIA APLICADA AL LOGIN

Completa la tabla con la aplicación de cada pilar de la triada CIA al sistema de login:

| Pilar CIA            | ¿Cómo se manifiesta en un sistema de login?                      | Ejemplo concreto                                           |
| -------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| **Confidencialidad** | Protege los datos del usuario para que nadie más los vea.        | La contraseña viaja cifrada por HTTPS.                     |
| **Integridad**       | Evita que la información sea modificada sin permiso.             | Que nadie cambie los datos del login.                      |
| **Disponibilidad**   | El sistema debe estar funcionando cuando el usuario lo necesite. | El servidor de autenticación está disponible las 24 horas. |

---

### A.2 OWASP TOP 10 — RELACIÓN CON AUTENTICACIÓN

Marca con ✓ las vulnerabilidades OWASP que se relacionan directamente con un login inseguro y explica brevemente por qué:

| #   | Vulnerabilidad OWASP         | ¿Relacionada con login? | ¿Por qué?                                                   |
| --- | ---------------------------- | ----------------------- | ----------------------------------------------------------- |
| A01 | Broken Access Control        | ☑ Sí ☐ No               | Puede permitir que un usuario acceda sin autorización.      |
| A02 | Cryptographic Failures       | ☑ Sí ☐ No               | Un mal cifrado expone contraseñas y datos.                  |
| A03 | Injection                    | ☑ Sí ☐ No               | Un atacante puede alterar consultas del login.              |
| A04 | Insecure Design              | ☑ Sí ☐ No               | Un mal diseño puede generar fallas de seguridad.            |
| A07 | Identification/Auth Failures | ☑ Sí ☐ No               | Está relacionado directamente con errores de autenticación. |

---

### A.3 PRINCIPIO DE MÍNIMO PRIVILEGIO

¿Cómo aplicarías el principio de Mínimo Privilegio a un sistema de autenticación? Escribe al menos 3 aplicaciones concretas:

1. Cada usuario solo debe tener los permisos necesarios.

2. La base de datos no debe usar una cuenta con privilegios de administrador.

3. Los usuarios normales no deben acceder a funciones del administrador.

---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA: ¿QUÉ SÉ YA?

**Instrucción:** Antes de que el docente explique el tema, responde estas preguntas con lo que ya sabes. No hay respuestas incorrectas en este momento.

### B.1 ¿Qué hace que un login sea inseguro? (Lista libre)

Escribe todo lo que se te ocurra:

1. Contraseñas fáciles.
2. No usar HTTPS.
3. Guardar contraseñas en texto plano.
4. No limitar intentos de acceso.
5. Tener errores en el código.
6. No validar los datos ingresados.

*(Al final de la clase volveremos a esta lista para ver cuánto más podemos agregar)*

---

### B.2 PREGUNTAS DE DIAGNÓSTICO

Responde con lo que ya sabes (marca la opción más correcta):

**B.2.1** ¿Cómo se deben almacenar las contraseñas en una base de datos?

* ☐ a) En texto plano para facilitar la recuperación
* ☐ b) Cifradas con AES-256 para poder descifrarlas si el usuario las olvida
* ☑ c) Como hash unidireccional con sal aleatoria
* ☐ d) Codificadas en Base64 para "ofuscarlas"

**B.2.2** ¿Qué versión de TLS/SSL deben usar los servidores web en 2024?

* ☐ a) SSL 3.0 — es la versión estándar
* ☐ b) TLS 1.0 — compatible con todos los dispositivos
* ☑ c) TLS 1.2 mínimo, preferiblemente TLS 1.3
* ☐ d) La versión no importa, cualquier SSL es suficiente

**B.2.3** ¿Qué es un certificado SSL autofirmado (self-signed)?

* ☐ a) Un certificado gratuito de Let's Encrypt
* ☑ b) Un certificado creado por uno mismo sin validación de una CA externa
* ☐ c) Un certificado de mayor seguridad que el emitido por una CA
* ☐ d) El tipo de certificado requerido en producción

---

# SECCIÓN C — CONCEPTOS CLAVE DE LA SESIÓN

## Completa durante la explicación del docente

---

### C.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD

**C.1.1** Escribe con tus propias palabras qué es una especificación formal de seguridad:

Es un conjunto de reglas y requisitos que indican cómo debe protegerse un sistema.

Sirve para establecer medidas claras de seguridad.

Ayuda a reducir errores y vulnerabilidades.

**C.1.2** ¿Cuál es la diferencia entre estas dos "especificaciones"? ¿Por qué una es formal y la otra no?

|                                                    | Ejemplo A                                 | Ejemplo B                                                                                                               |
| -------------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Texto**                                          | "El login debe ser seguro"                | "Las contraseñas se almacenarán como hash bcrypt con factor de coste 12. Máximo 5 intentos antes de bloqueo de 15 min." |
| **¿Por qué es o no es una especificación formal?** | Es muy general y no explica cómo hacerlo. | Es específica y define medidas concretas de seguridad.                                                                  |

**C.1.3** Completa los 7 componentes de una especificación formal de seguridad:

| # | Componente                   | ¿Qué define?                                          |
| - | ---------------------------- | ----------------------------------------------------- |
| 1 | **Activos**                  | Los datos que se deben proteger.                      |
| 2 | **Sujetos**                  | Quiénes usan el sistema.                              |
| 3 | **Objetos**                  | Los recursos a los que se accede.                     |
| 4 | **Operaciones**              | Las acciones permitidas o prohibidas.                 |
| 5 | **Condiciones**              | Los requisitos para permitir el acceso.               |
| 6 | **Mecanismos**               | Las herramientas o métodos de protección.             |
| 7 | **Respuesta ante violación** | Las acciones cuando ocurre un incidente de seguridad. |

---
### C.2 PREGUNTAS PARA MARCAR (Selección múltiple)

Marca la respuesta correcta. Solo hay una opción correcta por pregunta.

**C.2.1** ¿Cuál es el problema de almacenar contraseñas con SHA-1 SIN SAL?

* ☐ a) SHA-1 no produce un hash — produce texto cifrado
* ☐ b) SHA-1 es reversible — se puede obtener la contraseña original
* ☑ c) Los atacantes pueden usar tablas rainbow precomputadas para romper el hash
* ☐ d) SHA-1 produce hashes demasiado cortos para ser seguros

**C.2.2** ¿Qué ventaja fundamental tiene bcrypt sobre SHA-256 para almacenar contraseñas?

* ☐ a) Bcrypt produce hashes más largos que SHA-256
* ☑ b) Bcrypt incluye automáticamente sal aleatoria y es intencionalmente lento
* ☐ c) Bcrypt es un algoritmo de cifrado, no de hash
* ☐ d) Bcrypt es más rápido que SHA-256, mejorando el rendimiento del login

**C.2.3** ¿Qué es la "sal" (salt) en el contexto del hashing de contraseñas?

* ☐ a) Un algoritmo de cifrado adicional aplicado al hash
* ☐ b) La clave secreta usada para cifrar el hash antes de almacenarlo
* ☑ c) Un valor aleatorio único por usuario que se concatena a la contraseña antes de hashear
* ☐ d) El factor de coste que determina cuántas rondas de hashing se ejecutan

**C.2.4** ¿Por qué es un error de seguridad grave que el formulario de login use el método HTTP GET?

* ☐ a) Porque GET no puede transportar datos de texto
* ☑ b) Porque los parámetros GET viajan en la URL y quedan en logs del servidor y en el historial del navegador
* ☐ c) Porque GET es más lento que POST para transferir datos
* ☐ d) Porque GET no cifra los datos antes de enviarlos

**C.2.5** ¿Qué es Perfect Forward Secrecy (PFS) en TLS?

* ☐ a) Un mecanismo que cifra el certificado del servidor con una segunda clave
* ☐ b) La capacidad del servidor de descifrar tráfico pasado si se compromete la clave privada
* ☑ c) El uso de claves de sesión efímeras para que el compromiso de la clave privada del servidor no permita descifrar tráfico pasado
* ☐ d) La verificación automática de que el certificado SSL no ha expirado

**C.2.6** ¿Cuál de los siguientes es el estándar de hash de contraseñas más recomendado hoy?

* ☐ a) MD5 con sal de 16 bytes
* ☐ b) SHA-512 sin sal
* ☑ c) bcrypt (factor 12+) o argon2id
* ☐ d) AES-256 con clave de 32 bytes

**C.2.7** ¿Cuál de las siguientes configuraciones de servidor web es correcta en relación a SSL?

* ☐ a) Habilitar SSL 3.0, TLS 1.0, TLS 1.1 y TLS 1.2 para máxima compatibilidad
* ☐ b) Usar solo TLS 1.3 y deshabilitar todas las versiones anteriores
* ☐ c) Deshabilitar SSL 2.0 y SSL 3.0, mantener TLS 1.0, 1.1, 1.2 y 1.3
* ☑ d) Usar TLS 1.2 y TLS 1.3, deshabilitar versiones anteriores

**C.2.8** ¿Qué es CGI (Common Gateway Interface)?

* ☐ a) Un framework de Python para desarrollo web seguro
* ☑ b) Un protocolo estándar que define cómo un servidor web pasa solicitudes a programas externos para generar respuestas dinámicas
* ☐ c) Una librería de JavaScript para crear formularios de login
* ☐ d) Un tipo de certificado SSL para servidores compartidos

**C.2.9** Un atacante ejecuta el siguiente input en el campo de usuario de un login CGI inseguro: `admin' --`. ¿Qué tipo de ataque es este y qué efecto tendría?

* ☐ a) XSS — inyecta código JavaScript en la página
* ☑ b) SQL Injection — el `'--` cierra la query y comenta el resto, posiblemente bypasseando la verificación de contraseña
* ☐ c) CSRF — falsifica una solicitud de otro dominio
* ☐ d) Path Traversal — intenta acceder a archivos del sistema

**C.2.10** ¿Cuál es el propósito del header HTTP `Strict-Transport-Security`?

* ☐ a) Obliga al servidor a responder solo con JSON
* ☑ b) Le indica al navegador que siempre use HTTPS para ese dominio, incluso si el usuario escribe HTTP
* ☐ c) Restringe el origen de las solicitudes al dominio del servidor
* ☐ d) Cifra automáticamente todos los cookies del servidor

---

### C.3 PREGUNTAS DE COMPLETAR

Completa los espacios en blanco con la palabra o frase correcta:

**C.3.1** El proceso de almacenamiento de contraseñas usa **hashing** (no cifrado), porque es un proceso **unidireccional** que no permite obtener el dato original.

**C.3.2** La "sal" en bcrypt es un valor **aleatorio** y **único** por usuario que elimina la posibilidad de usar **tablas rainbow** precomputadas.

**C.3.3** TLS 1.3 hace obligatorio el uso de **PFS** (siglas), lo que significa que si la clave privada del servidor se compromete, el tráfico **pasado** no puede ser descifrado.

**C.3.4** En CGI, los datos del formulario POST se reciben a través de la **entrada** estándar del script, mientras que los parámetros GET llegan en la variable de entorno **QUERY_STRING**.

**C.3.5** El código de respuesta HTTP que se debe usar para redirigir permanentemente HTTP a HTTPS es el **301**.

**C.3.6** El principio de seguridad que dice que cada usuario o proceso debe tener solo los permisos mínimos necesarios se llama **Mínimo Privilegio**.

**C.3.7** Un certificado SSL **autofirmado** (autofirmado) es apropiado para **pruebas** y **desarrollo**, pero NO para **producción** porque los navegadores muestran una advertencia de seguridad.

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

| # | Vulnerabilidad identificada               | Descripción del riesgo                                     | Cómo corregirla                                        |
| - | ----------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------ |
| 1 | SQL Injection                             | Un atacante puede modificar la consulta SQL.               | Usar consultas preparadas o parametrizadas.            |
| 2 | Contraseñas en texto plano                | Las claves se comparan directamente y no están protegidas. | Almacenar contraseñas con bcrypt o argon2id.           |
| 3 | Credenciales de la base de datos visibles | El usuario y contraseña están escritos en el código.       | Guardarlas en variables de entorno o archivos seguros. |
| 4 | Exposición de información                 | Muestra datos del empleado y mensajes específicos.         | Mostrar mensajes genéricos y limitar la información.   |
| 5 | No valida la entrada del usuario          | Se aceptan datos sin ningún control.                       | Validar y filtrar los datos recibidos.                 |

---

**D.2** Analiza la siguiente política de contraseñas de una empresa e identifica qué está bien y qué está mal según las guías NIST SP 800-63B:

> *"Política de contraseñas de TechCorp SA: Las contraseñas deben tener exactamente 8 caracteres. Deben incluir al menos una letra mayúscula, una minúscula, un número y un símbolo. Las contraseñas deben cambiarse obligatoriamente cada 30 días. El sistema almacena los últimos 3 passwords para no repetirlos. El campo acepta cualquier combinación de caracteres ASCII."*

| Elemento de la política                        | ¿Correcto o incorrecto? | ¿Por qué?                                                           |
| ---------------------------------------------- | ----------------------- | ------------------------------------------------------------------- |
| Exactamente 8 caracteres                       | Incorrecto              | Es mejor permitir contraseñas más largas.                           |
| Cambio obligatorio cada 30 días                | Incorrecto              | Solo se recomienda cambiarla cuando exista riesgo o compromiso.     |
| Historial de 3 passwords                       | Correcto                | Ayuda a evitar que se reutilicen las mismas contraseñas.            |
| Complejidad obligatoria (mayus+minus+num+simb) | Incorrecto              | NIST recomienda priorizar contraseñas largas y fáciles de recordar. |

---

### Nivel Avanzado

**D.3** Escenario profesional:

> *Eres el desarrollador líder de una startup fintech peruana que acaba de lanzar su MVP de una app de préstamos personales. El sistema tiene un módulo de login básico. La startup va a solicitar una licencia de operaciones a la SBS (Superintendencia de Banca, Seguros y AFP). La SBS exige cumplimiento con estándares mínimos de seguridad para sistemas financieros.*

**D.3.1** ¿Qué estándares internacionales de seguridad son relevantes para este contexto? Menciona al menos 3.

ISO/IEC 27001 para gestión de seguridad.

NIST SP 800-63B para autenticación digital.

OWASP Top 10 para prevenir vulnerabilidades comunes.

---

**D.3.2** Diseña la especificación formal de seguridad completa para el módulo de login de esta fintech. Usa la estructura de 7 componentes vista en clase:

| Componente                           | Tu especificación                                                     |
| ------------------------------------ | --------------------------------------------------------------------- |
| **Activos a proteger**               | Datos personales, contraseñas y cuentas de usuarios.                  |
| **Sujetos (roles)**                  | Cliente, administrador y personal autorizado.                         |
| **Objetos (recursos controlados)**   | Base de datos, sistema de login y panel administrativo.               |
| **Operaciones permitidas/denegadas** | Permitir autenticación válida y bloquear accesos no autorizados.      |
| **Condiciones de acceso**            | Usuario y contraseña correctos, conexión segura y límite de intentos. |
| **Mecanismos técnicos**              | HTTPS, bcrypt, bloqueo por intentos y registro de eventos.            |
| **Respuesta ante violación**         | Bloquear la cuenta temporalmente y registrar el incidente.            |

**D.3.3** Justifica por qué elegiste bcrypt (y no MD5, SHA-256 o AES) para almacenar contraseñas en este sistema financiero. Usa argumentos técnicos y de cumplimiento normativo.

Elegí bcrypt porque está diseñado para almacenar contraseñas de forma segura.

Incluye una sal automática y es más lento, lo que dificulta ataques de fuerza bruta.

MD5 y SHA-256 no son la mejor opción para contraseñas porque pueden romperse más fácilmente.

AES es un algoritmo de cifrado y no está pensado para almacenar contraseñas.

---

**D.4** Pregunta de investigación (para completar fuera de clase):

La empresa Adobe sufrió en 2013 una de las brechas de datos más analizadas académicamente, no solo por el número de afectados (153 millones de registros) sino por el **tipo de error criptográfico** cometido.

**D.4.1** Investiga: ¿cómo Adobe almacenaba las contraseñas de sus usuarios? ¿Por qué fue un error tan grave?

Adobe utilizaba un cifrado que no era el más adecuado para proteger contraseñas.

Esto permitió que muchos atacantes pudieran descubrirlas con mayor facilidad.

Además, millones de cuentas quedaron expuestas.

**D.4.2** Explica por qué el hint de contraseña (pista de contraseña) que Adobe guardaba junto al hash **empeoró significativamente** el ataque:

Las pistas daban información adicional sobre la contraseña.

Eso ayudó a los atacantes a descubrir muchas claves más rápido.

**D.4.3** ¿Qué debió haber hecho Adobe en su lugar?

Debió almacenar las contraseñas usando bcrypt o un método similar.

También debió evitar guardar pistas de contraseña y aplicar mejores medidas de seguridad.

---

# SECCIÓN E — ACTIVIDAD COLABORATIVA: ESPECIFICACIÓN FORMAL DE SEGURIDAD

**Integrantes del grupo:**

1. Armando Carbajal Campomanes
2. ---
3. ---
4. ---

**Sistema asignado:** ____________________________________________________________

---

### E.1 ESPECIFICACIÓN FORMAL — MÓDULO DE LOGIN

Completa esta especificación para el sistema asignado por el docente:

```text
╔══════════════════════════════════════════════════════════════════════╗
║        ESPECIFICACIÓN FORMAL DE SEGURIDAD — MÓDULO LOGIN            ║
║        Sistema: Sistema de préstamos personales                     ║
╠══════════════════════════════════════════════════════════════════════╣
║ ACTIVOS                                                              ║
║ (¿Qué datos se protegen en el proceso de login?)                     ║
║                                                                      ║
║ ● Usuarios y contraseñas                                             ║
║ ● Datos personales                                                    ║
║ ● Información de las sesiones                                         ║
╠══════════════════════════════════════════════════════════════════════╣
║ SUJETOS                                                              ║
║ (¿Quiénes acceden? ¿Con qué roles diferenciados?)                   ║
║                                                                      ║
║ Rol 1: Cliente       → Permisos: Iniciar sesión y ver su cuenta      ║
║ Rol 2: Administrador → Permisos: Gestionar el sistema                ║
║ Rol 3: Soporte       → Permisos: Revisar incidencias                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ OBJETOS                                                              ║
║ (¿A qué recursos controla el acceso el módulo de login?)            ║
║                                                                      ║
║ ● Base de datos de usuarios                                          ║
║ ● Panel y servicios del sistema                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║ MECANISMOS TÉCNICOS                                                  ║
║                                                                      ║
║ Algoritmo hash: bcrypt            Factor/parámetros: 12             ║
║ Protocolo TLS: TLS 1.3           Cipher suites: Seguras             ║
║ Política de contraseñas:                                            ║
║   Longitud mínima: 8  Complejidad: Letras, números y símbolos       ║
║ Política de bloqueo:                                                ║
║   Máx intentos: 5 Duración bloqueo: 15 min Tipo: Temporal           ║
║ Expiración de sesión: inactividad 15 min / máximo 8 horas           ║
║ MFA: ☐ No ☑ Sí → Tipo: Código enviado al celular o correo           ║
╠══════════════════════════════════════════════════════════════════════╣
║ CONDICIONES DE ACCESO                                                ║
║ (Bajo qué circunstancias se permite/deniega el acceso)              ║
║                                                                      ║
║ ● Credenciales válidas y conexión segura                            ║
║ ● Se bloquea el acceso después de varios intentos fallidos          ║
╠══════════════════════════════════════════════════════════════════════╣
║ LOGGING DE SEGURIDAD                                                 ║
║ (¿Qué eventos se registran? ¿Con qué datos?)                        ║
║                                                                      ║
║ Evento 1: Inicio de sesión exitoso                                  ║
║ Evento 2: Intentos fallidos de acceso                               ║
║ Evento 3: Bloqueo de cuenta o actividad sospechosa                  ║
╠══════════════════════════════════════════════════════════════════════╣
║ RESPUESTA ANTE VIOLACIÓN                                             ║
║ (¿Qué ocurre cuando se detecta un intento de ataque?)               ║
║                                                                      ║
║ ● Se bloquea temporalmente la cuenta                                ║
║ ● Se registra el evento y se notifica al administrador              ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### E.2 JUSTIFICACIÓN DE DECISIONES DE DISEÑO

Para cada decisión técnica que tomaron en la especificación, justifiquen por qué la tomaron:

| Decisión técnica tomada      | Justificación (¿por qué esta y no otra?)                                  |
| ---------------------------- | ------------------------------------------------------------------------- |
| Algoritmo de hash elegido    | Porque bcrypt protege mejor las contraseñas y es recomendado actualmente. |
| Versión de TLS elegida       | TLS 1.3 brinda una conexión más segura que las versiones antiguas.        |
| Política de bloqueo definida | Ayuda a evitar ataques de fuerza bruta.                                   |
| Decisión sobre MFA           | Agrega una capa extra de seguridad al inicio de sesión.                   |

---

### E.3 CASO EXTREMO — ANÁLISIS GRUPAL

Respondan juntos: ¿Qué pasaría si un atacante obtiene acceso directo a la base de datos de su sistema (sin pasar por el login)? ¿Qué información podría obtener y qué NO podría obtener con la especificación que diseñaron?

**Lo que el atacante PODRÍA obtener:**

Podría ver algunos datos almacenados de los usuarios.

También podría obtener los hashes de las contraseñas y registros del sistema.

**Lo que el atacante NO PODRÍA obtener (gracias a su especificación):**

No podría conocer fácilmente las contraseñas originales porque están protegidas con bcrypt.

Tampoco podría ingresar al sistema solo con los hashes debido a las medidas de seguridad implementadas.

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN

### F.1 LISTA REVISADA (Volvemos a la Sección B.1)

Vuelve a tu lista de la Sección B.1 (¿qué hace inseguro un login?). Ahora agrega todo lo que descubriste durante la clase:

**Nuevas razones identificadas durante la clase:**

7. No usar hash para las contraseñas.
8. Usar métodos inseguros como HTTP GET.
9. No tener límite de intentos de acceso.
10. Utilizar versiones antiguas de SSL o TLS.
11. No validar los datos ingresados por el usuario.
12. No usar autenticación de dos factores.

---

### F.2 PREGUNTAS DE SÍNTESIS

Responde brevemente:

**F.2.1** ¿Cuál es la diferencia esencial entre hash y cifrado? ¿Por qué se usa hash para contraseñas?

El hash es un proceso que no permite recuperar el dato original, mientras que el cifrado sí puede revertirse con una clave.

Se usa hash para contraseñas porque ofrece mayor protección en caso de que la base de datos sea comprometida.

**F.2.2** ¿Qué hace bcrypt diferente a SHA-256 para resistir ataques de fuerza bruta?

Bcrypt incluye una sal automática y está diseñado para ser más lento.

Esto hace que probar miles de contraseñas sea mucho más difícil para un atacante.

**F.2.3** ¿Qué versión de TLS deben usar y por qué las anteriores están descartadas?

Se recomienda usar TLS 1.2 como mínimo y de preferencia TLS 1.3.

Las versiones anteriores tienen vulnerabilidades conocidas y ya no son seguras.

**F.2.4** ¿Cuál fue el error más crítico del código CGI inseguro que analizamos hoy?

El error más grave fue la posibilidad de realizar una inyección SQL.

Esto podía permitir que un atacante ingresara sin conocer la contraseña.

---

### F.3 METACOGNICIÓN PERSONAL (Solo para ti)

Responde honestamente. Nadie más verá estas respuestas:

**F.3.1** ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?

Me sorprendió saber que una contraseña puede quedar expuesta si no se almacena correctamente.

También me llamó la atención cómo una pequeña falla puede afectar todo el sistema.

**F.3.2** ¿Qué concepto todavía no tienes completamente claro?

Todavía me gustaría entender mejor cómo funcionan algunos protocolos de seguridad como TLS.

También quisiera practicar más el tema del hashing.

**F.3.3** ¿Qué error de seguridad en código hoy reconoces que podrías haber cometido (o has cometido) antes de esta clase?

Probablemente hubiera guardado contraseñas sin usar un algoritmo adecuado.

También no conocía el riesgo de construir consultas SQL directamente.

**F.3.4** ¿Cómo cambiaría tu forma de implementar un login después de esta sesión?

Usaría bcrypt para las contraseñas y conexiones HTTPS.

Además, validaría los datos, limitaría los intentos de acceso y aplicaría mejores medidas de seguridad.

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