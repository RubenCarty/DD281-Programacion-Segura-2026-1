# SESIÓN COMPLETA — SEMANA 2 · PROGRAMACIÓN SEGURA (DD281)
# ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO

---

## ENCABEZADO DE LA SESIÓN

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) |
| **Semana** | 2 de 16 |
| **Tema** | Especificación Formal de Seguridad y Login Seguro |
| **Duración** | 3 horas (180 minutos) con 20 minutos de receso |
| **Modalidad** | Presencial / Híbrida |
| **Valor formativo** | Excelencia en la implementación técnica de controles de acceso |

---

## ALINEAMIENTO CON EL SÍLABO

La Semana 2 profundiza el modelado de seguridad iniciado en la Semana 1 (introducción a la programación segura, triada CIA, OWASP Top 10, principios de seguridad). El puente conceptual es directo: si en la Semana 1 el estudiante aprendió a **identificar** qué puede salir mal en un sistema, en la Semana 2 aprende a **especificar formalmente qué debe hacer bien** el mecanismo de autenticación, y a **implementarlo correctamente** usando CGI y SSL.

**Competencia del curso que se desarrolla:**
- Diseñar e implementar mecanismos de control de acceso seguros aplicando estándares de la industria.
- Identificar y mitigar los fallos A01 (Broken Access Control) y A07 (Identification/Authentication Failures) del OWASP Top 10 — vistos en la semana anterior.

---

## LOGRO DE APRENDIZAJE DE LA SESIÓN

> **"Al finalizar la sesión, el estudiante desarrolla las especificaciones formales de un caso de acceso a un sistema y elabora un login seguro con CGI y certificado SSL con excelencia, demostrando comprensión de los principios de manejo seguro de credenciales y cifrado de datos en tránsito."**

---



---

## MAPA DE LA SESIÓN (CRONOGRAMA DETALLADO)

```
┌──────────────────────────────────────────────────────────────────────┐
│  MINUTO  0 –  25  │ INICIO: Apertura, recuperación S1, diagnóstico   │
│  MINUTO 25 –  40  │ UTILIDAD: Por qué el login seguro importa HOY    │
│  MINUTO 40 – 100  │ TRANSFORMACIÓN Parte 1: Teoría + preguntas       │
│                   │   · Especificación formal                         │
│                   │   · Manejo seguro de credenciales                 │
│                   │   · SSL/TLS: fundamentos y funcionamiento         │
│  MINUTO 100– 120  │ ⏸ RECESO (20 minutos)                            │
│  MINUTO 120– 155  │ TRANSFORMACIÓN Parte 2 + PRÁCTICA                │
│                   │   · CGI: arquitectura y riesgos                   │
│                   │   · Demo en vivo: login inseguro → login seguro   │
│                   │   · Actividad colaborativa grupal                 │
│  MINUTO 155– 180  │ CIERRE: Síntesis + metacognición + tarea S3      │
└──────────────────────────────────────────────────────────────────────┘
```

---

# PARTE 1 — INICIO
## ⏱ Duración: 25 minutos

---

### 1.1 DINÁMICA DE APERTURA: "EL PEOR PASSWORD DEL MUNDO"
#### ⏱ 8 minutos | Individual + Plenario

**Instrucción para el docente:**
Antes de que lleguen, proyecta en pantalla la URL de la herramienta de seguridad de contraseñas del NIST o Kaspersky Password Checker. Escribe en la pizarra:

```
¿TU CONTRASEÑA SOBREVIVIRÍA HOY?
→ https://www.security.org/how-secure-is-my-password/
→ Las contraseñas más usadas del 2024: "123456", "password", "qwerty"
```

**GUION VERBAL — Apertura:**

> "Quiero que hagan algo antes de empezar. Piensen — no lo escriban, no lo digan en voz alta — en una contraseña que hayan usado alguna vez. Puede ser de redes sociales, de correo, de una universidad. Solo ténenla en mente. Ahora piénsenlo: si alguien tuviera una lista de las 10 millones de contraseñas más usadas en el mundo, ¿estaría la de ustedes ahí?"

*(Pausa de 5 segundos.)*

> "El año pasado, la filtración de datos de RockYou2024 expuso 10 mil millones de contraseñas únicas. Díez. Mil. Millones. Eso significa que si su contraseña no es robusta, ya está en alguna lista que algún atacante tiene. Y hoy vamos a aprender exactamente cómo se debe implementar un sistema de login que resista ese tipo de ataque. No de la manera que lo hace YouTube — de la manera que lo exige la industria."

**¿Para qué sirve esta dinámica?**
- Conecta el tema con una amenaza real y actual.
- Genera disonancia cognitiva: "¿qué tan seguros somos realmente?"
- Establece el tono: hoy hay consecuencias reales en cada línea de código.

---

### 1.2 PRESENTACIÓN DEL LOGRO DE APRENDIZAJE
#### ⏱ 3 minutos | Docente presenta + estudiantes reformulan

Escribe el logro en la pizarra. Luego di:

> "Leamos esto juntos. Ahora quiero que alguien me lo explique con sus propias palabras, como si se lo explicara a su mamá o a un amigo que no estudia sistemas. ¿Qué vamos a hacer hoy concretamente?"

*(Espera respuesta. Un voluntario debería poder decir algo como: "vamos a aprender a diseñar bien un sistema de login y a hacerlo seguro con certificados.")*

> "Exacto. No solo vamos a saber que el login debe ser seguro. Vamos a saber **por qué** cada parte del login es como es, **cómo** implementarlo correctamente, y **qué pasa** cuando se hace mal."

---

### 1.3 RECUPERACIÓN DE APRENDIZAJES — SEMANA 1
#### ⏱ 10 minutos | Quiz de recuperación activa + plenario

**Instrucción:** Proyecta estas preguntas una a una. Los estudiantes las responden en una hoja o en su guía de trabajo (Sección A). Luego se debate en plenario.

---

**PREGUNTA DE RECUPERACIÓN 1:**
> "En la Semana 1 estudiamos la Triada CIA. Dénme una aplicación directa al tema de hoy: autenticación y login. ¿Cómo se manifiesta cada pilar (C, I, A) en un sistema de login?"

**RESPUESTA DOCENTE ESPERADA:**
- **Confidencialidad**: Las contraseñas no deben almacenarse en texto plano. Las credenciales en tránsito deben ir cifradas (SSL/TLS). Nadie que no sea el propietario debe ver su contraseña.
- **Integridad**: El hash de la contraseña almacenado no debe poder ser alterado. Si alguien modifica la base de datos, los hashes no deben coincidir con contraseñas válidas inyectadas.
- **Disponibilidad**: El sistema de login debe estar disponible. Un ataque de fuerza bruta masivo o DoS al endpoint de login puede derribarlo. Se mitiga con rate limiting y bloqueo de cuentas.

---

**PREGUNTA DE RECUPERACIÓN 2:**
> "De la lista OWASP Top 10, ¿qué vulnerabilidades se relacionan directamente con un login inseguro? Mencionen al menos dos."

**RESPUESTA DOCENTE ESPERADA:**
- **A01 — Broken Access Control**: Si el login falla en verificar correctamente los privilegios, usuarios no autorizados pueden acceder a funciones restringidas.
- **A07 — Identification and Authentication Failures**: Directamente relacionado. Incluye: contraseñas débiles sin política, ausencia de MFA, sesiones que no expiran, credenciales por defecto no cambiadas.
- **A02 — Cryptographic Failures** (bonus): No cifrar la contraseña en tránsito o en reposo es un fallo criptográfico directo.

---

**PREGUNTA DE RECUPERACIÓN 3:**
> "¿Cuál es el principio de 'Mínimo Privilegio' y cómo lo aplicarías al diseño de un sistema de autenticación?"

**RESPUESTA DOCENTE ESPERADA:**
El Mínimo Privilegio dice que cada usuario/proceso debe tener solo los permisos necesarios para su función. Aplicado al login: (1) El usuario que consulta la BD para verificar credenciales debe tener permisos solo de SELECT, no INSERT ni DROP. (2) Un usuario normal del sistema no debe poder ver los datos de otros usuarios. (3) El proceso del servidor web no debe correr como root.

---

### 1.4 ACTIVIDAD DIAGNÓSTICA SOBRE EL TEMA DE HOY
#### ⏱ 4 minutos | Lluvia de ideas estructurada

> "Ahora sí: el tema de hoy es **login seguro y especificación formal de seguridad**. Sin que yo haya explicado nada todavía, díganme: ¿qué hace que un login sea inseguro? Quiero que me digan todo lo que se les ocurra. Yo lo escribo en la pizarra."

*(Escribe todo sin corregir. Cuando tengan 6-8 ideas, di:)*

> "Miren esta lista. Todo lo que dijeron es válido. Al final de la clase, vamos a volver a esta lista y veremos cuántas cosas más agregaríamos. Eso va a ser nuestra medida de cuánto aprendimos hoy."

*(Deja la lista visible en la pizarra durante toda la sesión.)*

---

# PARTE 2 — UTILIDAD
## ⏱ Duración: 15 minutos (Minutos 25–40)

---

### 2.1 EL PROBLEMA REAL QUE RESUELVE ESTE TEMA

**GUION VERBAL:**

> "Quiero mostrarles tres números que los van a poner en perspectiva."

Escribe en la pizarra:

```
81%   → de las brechas relacionadas con hacking usan credenciales robadas o débiles
       (Verizon DBIR 2023)

$4.45M → costo promedio de una brecha de datos en 2023
        (IBM Cost of a Data Breach Report 2023)

19 seg → tiempo promedio que tarda un script automatizado en probar 
         todas las contraseñas de 4 caracteres
```

> "El 81% de los ataques exitosos involucran credenciales comprometidas. No explotaron una vulnerabilidad de día cero. No usaron malware sofisticado. Simplemente tuvieron una contraseña válida — robada, filtrada o adivinada."

---

**CASO REAL — LinkedIn (2012 / 2016):**

> "En 2012, LinkedIn sufrió una brecha de datos. Dijeron que habían sido robadas 6.5 millones de contraseñas. En 2016, descubrieron que eran **117 millones**. ¿Por qué la discrepancia? Porque las contraseñas estaban hasheadas con SHA-1 **sin sal**. Sin sal, los atacantes pudieron usar tablas rainbow — bases de datos precomputadas de hashes — para romper el 90% de las contraseñas en días. LinkedIn pagó multas millonarias. El desarrollador que implementó el sistema de hash 'casi bien pero no del todo bien' no era un principiante. Era un profesional que no conocía las especificaciones correctas."

> "Ese es exactamente el tema de hoy. La diferencia entre un login 'que funciona' y un login 'que es seguro' puede parecer pequeña. Puede ser una línea de código. Pero las consecuencias son enormes."

---

**CONEXIÓN CON EL ROL PROFESIONAL:**

> "¿En qué trabajo van a usar esto? En **cualquier** trabajo donde escriban código. Si trabajas en una startup y te piden 'hacer el login', vas a recordar esta clase. Si trabajas en banca, en salud, en retail, en gobierno — todos tienen sistemas de autenticación. Y todos los que fallaron, fallaron porque alguien no supo lo que ustedes van a saber hoy."

---

# PARTE 3 — TRANSFORMACIÓN (Parte 1)
## ⏱ Duración: 60 minutos (Minutos 40–100)

---

### 3.1 ESPECIFICACIÓN FORMAL DE SEGURIDAD — ¿QUÉ ES Y POR QUÉ EXISTE?
#### ⏱ 15 minutos

**GUION VERBAL:**

> "Empecemos con el concepto más abstracto de hoy, porque todo lo demás cuelga de aquí: ¿qué es una especificación formal de seguridad?"

**DEFINICIÓN:**

> Una **Especificación Formal de Seguridad** es un documento estructurado y preciso que define, antes de codificar, **qué debe garantizar** un sistema en términos de seguridad: qué datos protege, quién puede acceder, bajo qué condiciones, con qué mecanismos, y cómo responde ante intentos de violación.

Escribe en la pizarra:

```
ESPECIFICACIÓN FORMAL DE SEGURIDAD
────────────────────────────────────
NO es: "el login debe ser seguro"
SÍ es: "Las credenciales se almacenarán como hash bcrypt 
        con factor de coste 12. El campo contraseña en 
        tránsito irá cifrado con TLS 1.3. Máximo 5 
        intentos fallidos antes de bloqueo temporal de 
        15 min. Las sesiones expiran a los 30 min 
        de inactividad."
```

> "¿Notan la diferencia? La primera 'especificación' no le dice nada a nadie. La segunda define exactamente qué hacer y le permite a cualquier desarrollador del equipo implementarlo sin ambigüedad — y a cualquier auditor verificar que se cumplió."

---

**PREGUNTA AL AULA 1:**
> "¿Por qué creen que muchos equipos de desarrollo NO escriben especificaciones de seguridad antes de codificar? ¿Qué razones darían para justificarlo?"

**RESPUESTA DOCENTE ESPERADA:**
Las razones más comunes son: (1) Presión de tiempo — "no hay tiempo para documentar, hay que entregar". (2) "El cliente no lo pide explícitamente". (3) "Lo arreglamos después si aparece un problema". (4) Falta de conocimiento — no saben qué especificar. Todas estas razones son válidas como contexto real, pero ninguna es aceptable como justificación técnica: el costo de corregir una vulnerabilidad descubierta en producción es 100x mayor que el costo de especificarla correctamente en diseño (IBM, documentado en clase S1). Además, normativas como GDPR, ISO 27001 y PCI-DSS exigen documentación de controles de seguridad — sin especificación formal, no hay cumplimiento regulatorio.

---

**COMPONENTES DE UNA ESPECIFICACIÓN FORMAL DE SEGURIDAD:**

Proyecta o construye en la pizarra la siguiente estructura:

```
╔══════════════════════════════════════════════════════════════════╗
║         ESTRUCTURA DE UNA ESPECIFICACIÓN FORMAL DE SEGURIDAD    ║
╠══════════════════╦═══════════════════════════════════════════════╣
║ 1. ACTIVOS       ║ ¿Qué datos o recursos se protegen?            ║
║                  ║ Ej: credenciales, tokens de sesión, PII       ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 2. SUJETOS       ║ ¿Quién interactúa con el sistema?             ║
║                  ║ Ej: usuario anónimo, usuario autenticado,     ║
║                  ║     administrador, proceso automatizado       ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 3. OBJETOS       ║ ¿A qué recursos se controla el acceso?        ║
║                  ║ Ej: página de notas, endpoint /api/users      ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 4. OPERACIONES   ║ ¿Qué acciones están permitidas/denegadas?     ║
║                  ║ Ej: leer, escribir, eliminar, exportar        ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 5. CONDICIONES   ║ ¿Bajo qué circunstancias se permite/niega?    ║
║                  ║ Ej: solo con sesión activa + MFA verificado   ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 6. MECANISMOS    ║ ¿Con qué tecnología se implementa?            ║
║                  ║ Ej: bcrypt, TLS 1.3, JWT, OAuth 2.0          ║
╠══════════════════╬═══════════════════════════════════════════════╣
║ 7. RESPUESTA     ║ ¿Qué pasa si se viola la política?            ║
║ ANTE VIOLACIÓN   ║ Ej: log de seguridad, bloqueo, alerta SIEM   ║
╚══════════════════╩═══════════════════════════════════════════════╝
```

---

**PREGUNTA AL AULA 2:**
> "Trabajemos juntos. Imaginen que son el equipo de seguridad de una universidad peruana que va a lanzar su nuevo portal estudiantil online. Necesitan escribir la especificación formal para el módulo de login. ¿Qué pondrían en el campo 'SUJETOS'? ¿Quiénes interactúan con ese login?"

**RESPUESTA DOCENTE ESPERADA:**
Los sujetos de un portal universitario son: (1) **Estudiante activo** — matrícula vigente, accede a notas, horarios, pagos. (2) **Estudiante egresado** — acceso limitado a historial académico y constancias. (3) **Docente** — accede a registro de notas, asistencia, materiales de cursos. (4) **Personal administrativo** — accede a datos de matrícula, reportes. (5) **Administrador del sistema** — acceso total con trazabilidad completa. (6) **Visitante/no autenticado** — solo puede ver información pública, sin acceso al sistema. Cada sujeto debe tener su propia política de acceso — esto es el principio de control de acceso basado en roles (RBAC).

---

### 3.2 MANEJO SEGURO DE CREDENCIALES — LA CIENCIA DETRÁS DEL HASH
#### ⏱ 20 minutos

**GUION VERBAL:**

> "Ahora entramos al corazón técnico. Cuando un usuario crea una cuenta en un sistema, ¿dónde guardamos su contraseña? Piénsenlo. ¿En texto plano? ¿Cifrado? ¿Hasheado? ¿Y cuál es la diferencia?"

---

**PREGUNTA AL AULA 3:**
> "¿Cuál es la diferencia fundamental entre **cifrado** y **hash**? Que alguien me explique esto sin buscar en internet."

**RESPUESTA DOCENTE ESPERADA:**
- **Cifrado (Encryption)**: Es un proceso **bidireccional**. Se aplica una función y una clave para convertir texto claro en texto cifrado. Con la clave correcta, se puede revertir — obtener el texto original. Ejemplo: cifrar un mensaje para enviarlo a alguien que tiene la clave.
- **Hash**: Es un proceso **unidireccional**. Se aplica una función matemática al dato y se obtiene un valor de longitud fija (digest). NO es posible revertirlo matemáticamente para obtener el dato original. Ejemplo: MD5("password") = "5f4dcc3b5aa765d61d8327deb882cf99". No se puede ir de ese hash hacia "password".
- **Para contraseñas**: Se usa hash, NO cifrado. Porque si ciframos contraseñas y alguien roba la clave de cifrado, obtiene todas las contraseñas. Con hash, incluso si roban la base de datos, no pueden "deshacer" el hash directamente.

---

**Dibuja en la pizarra esta progresión:**

```
EVOLUCIÓN DEL ALMACENAMIENTO DE CONTRASEÑAS
════════════════════════════════════════════════════════════════════

NIVEL 0 (PÉSIMO): TEXTO PLANO
  BD: usuario=juan, password=miperro123
  Riesgo: cualquiera con acceso a la BD obtiene todas las contraseñas

NIVEL 1 (MAL): HASH SIMPLE (MD5 o SHA-1)
  BD: usuario=juan, hash=5f4dcc3b5aa765d61d8327deb882cf99
  Riesgo: tablas rainbow precomputan estos hashes. 
          90% de contraseñas comunes ya están en tablas.
          LinkedIn 2012 usó esto. 117M cuentas comprometidas.

NIVEL 2 (MEJOR): HASH CON SAL (SHA-256 + salt)
  Sal = string aleatorio único por usuario
  BD: usuario=juan, salt=xK9#mP2!qL, hash=SHA256("miperro123"+"xK9#mP2!qL")
  Riesgo: eliminamos tablas rainbow. Pero SHA-256 es rápido:
          GPU moderna calcula 10 BILLONES de hashes SHA-256 por segundo.
          Fuerza bruta es viable para contraseñas débiles.

NIVEL 3 (CORRECTO): HASH LENTO CON SAL (bcrypt / argon2 / scrypt)
  BD: usuario=juan, hash=$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN...
  El $ 12 $ = factor de coste (rounds). Con factor 12, cada hash 
  tarda ~250ms. Un atacante con GPU solo prueba ~4 passwords/segundo.
  Riesgo: reducido drásticamente. Es el estándar de la industria HOY.
```

---

**PREGUNTA AL AULA 4:**
> "Si bcrypt tarda 250ms en generar un hash y un sistema recibe 1000 logins por segundo, ¿hay un problema de rendimiento? ¿Cómo lo resolverían?"

**RESPUESTA DOCENTE ESPERADA:**
Sí, existe un trade-off real entre seguridad y rendimiento. La solución no es reducir el factor de coste de bcrypt — eso debilita la seguridad. Las soluciones correctas son: (1) **Caché de sesión**: después del primer login exitoso se emite un token (JWT o cookie de sesión). Las solicitudes posteriores usan el token, no la contraseña, eliminando el hash en cada request. (2) **Hardware dedicado o GPU para hashing**: si el volumen es muy alto, se puede dedicar hardware específico. (3) **Argon2**: el ganador del Password Hashing Competition 2015, diseñado específicamente para resistir ataques con GPU/ASIC. Es paralelizable en el servidor pero no beneficia al atacante de la misma manera. (4) **Escalado horizontal**: múltiples instancias del servicio de autenticación. El factor de coste se elige para que sea LENTO para el atacante, pero MANEJABLE para el sistema — el balance depende del contexto.

---

**CÓDIGO COMPARATIVO — bcrypt en Python:**

```python
# ══════════════════════════════════════════════════════════════════
# MANEJO SEGURO DE CONTRASEÑAS — bcrypt en Python
# Librería: pip install bcrypt
# ══════════════════════════════════════════════════════════════════

import bcrypt
import time

# ── MAL: almacenar en texto plano ─────────────────────────────────
password_plano = "miperro123"
# ¡Nunca almacenen esto directamente en la BD!

# ── BIEN: hash con bcrypt ─────────────────────────────────────────
def crear_hash(password: str) -> bytes:
    """
    bcrypt genera automáticamente una sal aleatoria.
    El factor de coste 12 significa 2^12 = 4096 rondas de hashing.
    """
    salt = bcrypt.gensalt(rounds=12)      # Sal aleatoria automática
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verificar_password(password: str, hashed: bytes) -> bool:
    """
    bcrypt.checkpw extrae la sal del hash almacenado y aplica 
    el mismo proceso. NO se necesita almacenar la sal por separado.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# ── Demo de tiempo ─────────────────────────────────────────────────
inicio = time.time()
hash_generado = crear_hash(password_plano)
fin = time.time()

print(f"Hash generado: {hash_generado}")
print(f"Tiempo de hash: {(fin - inicio)*1000:.0f}ms")
# → Tiempo de hash: ~250ms (intencional — dificulta ataques bruta)

# ── Verificación ───────────────────────────────────────────────────
print(f"¿Contraseña correcta? {verificar_password('miperro123', hash_generado)}")  # True
print(f"¿Contraseña incorrecta? {verificar_password('otrapass', hash_generado)}")  # False

# ── Lo que se almacena en la BD ────────────────────────────────────
# $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN83ZPyqnRh3b5Ur/Ov5C
#  │   │  │                                                        │
#  │   │  └── Sal (22 chars base64)                               │
#  │   └───── Factor de coste (12)                                │
#  └───────── Versión de bcrypt (2b)                              │
```

---

**PREGUNTA AL AULA 5:**
> "En el hash de bcrypt que ven en el código — `$2b$12$LQv3c1yq...` — el factor de coste está visible. ¿Es un problema de seguridad que un atacante sepa que es factor 12?"

**RESPUESTA DOCENTE ESPERADA:**
No es un problema de seguridad significativo saber el factor de coste. Bcrypt sigue el principio de Kerckhoffs: la seguridad no debe depender del secreto del algoritmo, sino de la clave (la contraseña del usuario). Saber que es factor 12 no le dice al atacante nada sobre la contraseña. Lo que sí hace es informarle cuánto tiempo tardará cada intento de fuerza bruta — pero eso también lo puede calcular simplemente ejecutando bcrypt. La sal sí está en el hash y no es un secreto en bcrypt, pero cumple su función de hacer que cada hash sea único aunque dos usuarios tengan la misma contraseña.

---

### 3.3 SSL/TLS — BLINDAJE EN TRÁNSITO
#### ⏱ 25 minutos

**GUION VERBAL:**

> "Hasta ahora hablamos de cómo proteger la contraseña **en reposo** — almacenada en la base de datos. Pero hay otro vector de ataque igual de crítico: ¿qué pasa con la contraseña mientras viaja del navegador al servidor?"

---

**PREGUNTA AL AULA 6:**
> "Sin SSL, cuando un usuario escribe su contraseña en un formulario y da Enter, ¿qué viaja por la red? ¿Cómo viaja? ¿Quién podría verlo?"

**RESPUESTA DOCENTE ESPERADA:**
Sin SSL (es decir, usando HTTP puro): (1) Los datos del formulario viajan como texto plano en los paquetes TCP/IP. (2) Cualquier persona en la red intermedia puede ver ese tráfico: el proveedor de internet (ISP), administradores de redes WiFi (incluyendo el café donde se conectaron), routers intermedios, y cualquier atacante ejecutando un ataque de tipo **Man-in-the-Middle (MitM)** con herramientas como Wireshark o tcpdump. (3) Un atacante con Wireshark en la misma red WiFi puede capturar literalmente el valor del campo `password` del formulario. Esto es trivial de ejecutar — no requiere habilidades avanzadas.

---

**DIAGRAMA EN PIZARRA — SSL/TLS Handshake simplificado:**

```
SIN SSL (HTTP puro):
Cliente ──────────── "usuario=juan&password=miperro123" ──────────── Servidor
                                     │
                              [CUALQUIERA EN LA RED PUEDE VER ESTO]

CON SSL/TLS (HTTPS):
                    ┌─── TLS HANDSHAKE ───┐
Cliente ──(1) ClientHello──────────────────────────────→ Servidor
Client ←──(2) ServerHello + Certificado ──────────────── Servidor  
                                                          (contiene clave pública)
Cliente  (3) Verifica certificado con CA
         (4) Genera PreMasterSecret
Cliente ──(5) PreMasterSecret cifrado con clave pública─→ Servidor
              [Solo el servidor puede descifrarlo]
         (6) Ambos derivan las mismas llaves de sesión (simétricas)
Cliente ──────── DATOS CIFRADOS CON CLAVE DE SESIÓN ──────────── Servidor
                [Un atacante solo ve datos cifrados, inútiles sin la clave]
```

---

**CONCEPTOS CLAVE — TLS vs SSL:**

> "Antes de seguir, aclaremos algo que confunde a muchos: ¿SSL y TLS son lo mismo?"

| Versión | Estado | Usar/No usar |
|---|---|---|
| SSL 2.0 | Obsoleto desde 1996 | ❌ Nunca |
| SSL 3.0 | Obsoleto — Vulnerable a POODLE | ❌ Nunca |
| TLS 1.0 | Obsoleto — Vulnerable a BEAST | ❌ Nunca |
| TLS 1.1 | Deprecado 2020 por RFC 8996 | ❌ No usar |
| TLS 1.2 | Aceptable — Aún en uso amplio | ⚠️ Solo si necesario |
| TLS 1.3 | **Estándar actual** — Mayor velocidad y seguridad | ✅ Preferido |

> "Cuando alguien dice 'certificado SSL', técnicamente hoy se refiere a TLS. SSL está muerto. Pero el término coloquial persiste. Lo importante es que usen TLS 1.2 mínimo, TLS 1.3 preferiblemente."

---

**PREGUNTA AL AULA 7:**
> "¿Qué es una Autoridad Certificadora (CA) y por qué un navegador confía en un certificado HTTPS? ¿Cómo sabe el navegador que el certificado no es falso?"

**RESPUESTA DOCENTE ESPERADA:**
Una Autoridad Certificadora (CA — Certificate Authority) es una organización de confianza que emite certificados digitales después de verificar la identidad del solicitante. El proceso: (1) El dueño del dominio genera un par de claves (pública/privada) y envía su clave pública + datos del dominio a la CA en un CSR (Certificate Signing Request). (2) La CA verifica que el solicitante controla realmente ese dominio (Domain Validation) o también verifica la identidad legal de la organización (Organization Validation / Extended Validation). (3) La CA firma digitalmente el certificado con su propia clave privada. (4) El navegador tiene pre-instalada una lista de CAs de confianza (Root CAs) — Mozilla, Google, Apple la mantienen. Al visitar un sitio HTTPS, el navegador verifica que la firma del certificado sea válida usando la clave pública de la CA. Si la cadena de confianza es válida y el dominio coincide, muestra el candado. Si alguien crea un certificado falso sin la firma de una CA reconocida, el navegador muestra una advertencia de "certificado no confiable". Let's Encrypt es una CA gratuita y automatizada — emite certificados de Domain Validation válidos y de confianza universal.

---

**CERTIFICADO AUTOFIRMADO vs CA:**

```
╔════════════════════════════════════════════════════════════════════╗
║  TIPO DE CERTIFICADO    │ USO CORRECTO           │ PROBLEMA        ║
╠════════════════════════════════════════════════════════════════════╣
║  Autofirmado (self-     │ Desarrollo local,      │ Navegador       ║
║  signed)                │ laboratorios internos, │ muestra alerta. ║
║                         │ pruebas internas       │ NO usar en      ║
║                         │                        │ producción      ║
╠════════════════════════════════════════════════════════════════════╣
║  Let's Encrypt (CA      │ Producción web pública │ Gratis, válido  ║
║  gratuita)              │ con dominio propio     │ 90 días, se     ║
║                         │                        │ renueva auto    ║
╠════════════════════════════════════════════════════════════════════╣
║  DigiCert/Sectigo/      │ Producción enterprise, │ Costo anual.    ║
║  GlobalSign (CA paga)   │ e-commerce, banca,     │ Mayor garantía  ║
║                         │ gobierno               │ y SLA           ║
╚════════════════════════════════════════════════════════════════════╝
```

---

**GENERAR CERTIFICADO AUTOFIRMADO — Comandos OpenSSL:**

```bash
# ══════════════════════════════════════════════════════════════════
# GENERACIÓN DE CERTIFICADO SSL AUTOFIRMADO CON OPENSSL
# Para uso en laboratorio / desarrollo local
# ══════════════════════════════════════════════════════════════════

# Paso 1: Generar clave privada RSA de 2048 bits
openssl genrsa -out server.key 2048

# Paso 2: Generar Certificate Signing Request (CSR)
openssl req -new -key server.key -out server.csr \
  -subj "/C=PE/ST=Lima/L=Lima/O=Universidad Autonoma/CN=localhost"

# Paso 3: Autofirmar el certificado (válido 365 días)
openssl x509 -req -days 365 -in server.csr \
  -signkey server.key -out server.crt

# Resultado: dos archivos críticos
# server.key → Clave privada (NUNCA compartir, NUNCA subir a GitHub)
# server.crt → Certificado público (se comparte con los clientes)

# Paso 4: Verificar el certificado generado
openssl x509 -in server.crt -text -noout | grep -E "Subject:|Validity"
```

> **Advertencia crítica para estudiantes:** La clave privada (`server.key`) debe protegerse con permisos restrictivos: `chmod 600 server.key`. Si esta clave se filtra, cualquiera puede suplantar su servidor. En producción, nunca va en el repositorio Git — va en el servidor con acceso solo para root o el usuario del servicio web.

---

## ⏸ RECESO — 20 MINUTOS

> Antes del receso, lanza esta pregunta para reflexionar durante el descanso:
> "Cuando vuelvan, quiero que alguien me explique: si SSL protege los datos en tránsito, ¿puede un atacante que ya tiene acceso al servidor descifrar el tráfico TLS grabado anteriormente? Piénsenlo."

*(La respuesta depende de si se usa Perfect Forward Secrecy — TLS 1.3 la implementa obligatoriamente. Se retoma al inicio de la segunda parte.)*

---

# PARTE 3 — TRANSFORMACIÓN (Parte 2)
## ⏱ Duración: 35 minutos (Minutos 120–155)

---

**Retoma del receso — Pregunta de la pausa:**

**PREGUNTA AL AULA 8:**
> "¿Alguien puede responder la pregunta que lanzamos antes del receso? Si un atacante grabó tráfico TLS hace 6 meses y hoy consigue la clave privada del servidor, ¿puede descifrar ese tráfico grabado?"

**RESPUESTA DOCENTE ESPERADA:**
Depende de la versión de TLS y el cipher suite usado. (1) **TLS 1.2 sin PFS**: Si se usaron algoritmos RSA key exchange (RSA directo para el intercambio de clave), sí — el atacante que tenga la clave privada del servidor puede descifrar tráfico grabado anteriormente. Esto se llama el ataque "retroactivo" y fue relevante en casos como las revelaciones Snowden. (2) **TLS 1.2 con PFS o TLS 1.3**: Usan Diffie-Hellman Ephemeral (DHE o ECDHE) — se generan claves efímeras para cada sesión que se destruyen al terminar. Incluso con la clave privada del servidor, NO se puede descifrar tráfico pasado. TLS 1.3 hace PFS **obligatorio**. Esta es una razón fundamental para migrar a TLS 1.3.

---

### 3.4 CGI — ARQUITECTURA, FUNCIONAMIENTO Y VECTORES DE RIESGO
#### ⏱ 15 minutos

**GUION VERBAL:**

> "Ahora hablemos de CGI — Common Gateway Interface. Es una de las tecnologías más antiguas de la web y una de las más malentendidas en términos de seguridad. Antes de implementar el login con CGI, necesitamos entender exactamente qué es y dónde están sus riesgos."

---

**DEFINICIÓN Y ARQUITECTURA CGI:**

> **CGI (Common Gateway Interface)** es un protocolo estándar que define cómo un servidor web pasa solicitudes HTTP a programas externos (scripts) para generar respuestas dinámicas.

```
FLUJO CGI:
                                           ┌──────────────────┐
                                           │   Script CGI     │
Browser ──HTTP Request──→ Servidor Web ──→ │  (Python/Perl/C) │
                                           │                  │
Browser ←──HTTP Response─ Servidor Web ←── │  Lee stdin/env   │
                                           │  Escribe stdout  │
                                           └──────────────────┘

Variables de entorno que CGI expone al script:
  REQUEST_METHOD  → GET, POST
  QUERY_STRING    → parámetros en URL (?user=juan&pass=...)
  CONTENT_LENGTH  → longitud del body POST
  REMOTE_ADDR     → IP del cliente
  HTTP_COOKIE     → cookies de la solicitud
```

---

**VECTORES DE RIESGO EN CGI:**

Construye esta tabla con los estudiantes — pregunta antes de completar cada fila:

```
╔═══════════════════════════════════════════════════════════════════╗
║  RIESGO EN CGI           │ DESCRIPCIÓN             │ MITIGACIÓN   ║
╠═══════════════════════════════════════════════════════════════════╣
║  Inyección de comandos   │ El script pasa input     │ Validar y    ║
║  (Command Injection)     │ del usuario directamente │ sanitizar    ║
║                          │ a una función shell      │ toda entrada ║
╠═══════════════════════════════════════════════════════════════════╣
║  Exposición de variables │ Variables de entorno con │ Nunca exponer║
║  de entorno              │ datos sensibles visibles │ en output    ║
╠═══════════════════════════════════════════════════════════════════╣
║  Traversal de path       │ Input con "../" para     │ Validar paths║
║  (Path Traversal)        │ acceder a archivos fuera │ con realpath ║
║                          │ del directorio web       │             ║
╠═══════════════════════════════════════════════════════════════════╣
║  Credenciales en URL     │ Parámetros de login en   │ Usar POST,   ║
║  (QUERY_STRING)          │ GET quedan en logs del   │ nunca GET    ║
║                          │ servidor                 │ para login   ║
╠═══════════════════════════════════════════════════════════════════╣
║  Ausencia de HTTPS       │ Sin SSL, las credenciales│ Forzar HTTPS ║
║                          │ en POST viajan en claro  │ redirect 301 ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

**PREGUNTA AL AULA 9:**
> "¿Por qué es un error crítico de seguridad enviar el formulario de login con el método HTTP GET en lugar de POST?"

**RESPUESTA DOCENTE ESPERADA:**
Hay múltiples razones: (1) **Logs del servidor**: Con GET, los parámetros van en la URL (`/login.cgi?user=juan&password=miperro123`). Todos los servidores web logean la URL completa. Significa que la contraseña queda en texto plano en los archivos de log — que típicamente tienen menor protección que la base de datos. (2) **Historial del navegador**: Las URLs con GET quedan en el historial del navegador. Si el usuario usa una computadora pública, alguien podría ver la contraseña en el historial. (3) **Caché**: Los servidores proxy y CDNs pueden cachear URLs GET. (4) **Referrer header**: Si la página de login tiene recursos externos (imágenes, scripts), el navegador puede enviar la URL completa en el header `Referer` a esos servidores externos. Con POST, los parámetros van en el body de la solicitud HTTP, que no se logea de la misma forma, no queda en historial, y no se cachea.

---

### 3.5 DEMO EN VIVO — DE LOGIN INSEGURO A LOGIN SEGURO CON CGI + SSL
#### ⏱ 20 minutos

> "Ahora vamos a ver código. Primero el código que NO deben escribir, luego el código correcto. Quiero que identifiquen los errores antes de que yo los diga."

**Proyecta el Código Inseguro:**

```python
#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# login_INSEGURO.cgi — CÓDIGO CON MÚLTIPLES VULNERABILIDADES
# PROPÓSITO DIDÁCTICO: Identificar qué está mal
# ══════════════════════════════════════════════════════════════════
import cgi
import os
import mysql.connector   # Suponemos BD MySQL

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
usuario  = form.getvalue("usuario")   # Sin validación
password = form.getvalue("password")  # Sin validación

# ❌ ERROR 1: Query concatenada — SQL Injection
conn = mysql.connector.connect(host="localhost", user="root",
                               password="root123", database="usuarios_db")
cursor = conn.cursor()
sql = f"SELECT * FROM usuarios WHERE user='{usuario}' AND pass='{password}'"
cursor.execute(sql)
resultado = cursor.fetchone()

# ❌ ERROR 2: Contraseña comparada en texto plano (guardada sin hash)
if resultado:
    print(f"<h1>Bienvenido {usuario}</h1>")
    print(f"<p>Su contraseña es: {password}</p>")  # ❌ ERROR 3: Expone contraseña
else:
    print("<h1>Credenciales incorrectas</h1>")
    # ❌ ERROR 4: Sin rate limiting ni bloqueo de intentos
    # ❌ ERROR 5: Sin logging de intento fallido
```

---

**PREGUNTA AL AULA 10:**
> "Antes de que yo diga algo: identifiquen todos los errores que puedan ver en este código. Les doy 3 minutos. Escríbanlos en su guía de trabajo."

**RESPUESTA DOCENTE ESPERADA (lista completa de errores):**
1. **SQL Injection**: La query usa f-string con input directo — clásico SQL Injection. Un atacante puede escribir `' OR '1'='1` en el campo usuario y bypass completo del login.
2. **Contraseña en texto plano**: `pass='{password}'` implica que la contraseña se almacena sin hash en la BD.
3. **Exposición de contraseña en output HTML**: `print(f"<p>Su contraseña es: {password}</p>")` — nunca mostrar datos sensibles.
4. **Sin rate limiting**: No hay control de intentos. Un atacante puede intentar millones de combinaciones.
5. **Sin logging de seguridad**: Los intentos fallidos no se registran — no hay forma de detectar un ataque de fuerza bruta.
6. **Credenciales de BD hardcodeadas**: `password="root123"` en código — si el código fuente se expone, la BD queda comprometida.
7. **Conexión como root a la BD**: El usuario `root` tiene todos los privilegios — violación del principio de mínimo privilegio.
8. **Sin verificación de método HTTP**: El script no verifica que la solicitud sea POST — aceptaría credenciales por GET.
9. **Sin HTTPS**: Si el servidor no fuerza HTTPS, las credenciales viajan en texto claro.

---

**Proyecta el Código Seguro (referencia al laboratorio — código completo en documento de laboratorio):**

```python
#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# login_seguro.cgi — IMPLEMENTACIÓN CON PRÁCTICAS CORRECTAS
# ══════════════════════════════════════════════════════════════════
import cgi
import os
import sqlite3
import bcrypt
import html
import hmac
import hashlib
import time
import logging
from datetime import datetime

# Configuración de logging de seguridad
logging.basicConfig(
    filename='/var/log/app/auth.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

print("Content-Type: text/html; charset=utf-8")
print("Strict-Transport-Security: max-age=31536000; includeSubDomains")
print("X-Content-Type-Options: nosniff")
print("X-Frame-Options: DENY")
print()   # Línea en blanco obligatoria entre headers y body

# ── 1. VERIFICAR MÉTODO HTTP ───────────────────────────────────────
if os.environ.get('REQUEST_METHOD') != 'POST':
    print("<h2>Método no permitido</h2>")
    exit(1)

# ── 2. VERIFICAR HTTPS ─────────────────────────────────────────────
if os.environ.get('HTTPS') != 'on':
    print("<h2>Acceso denegado — Se requiere HTTPS</h2>")
    exit(1)

# ── 3. OBTENER Y SANITIZAR INPUTS ──────────────────────────────────
form = cgi.FieldStorage()
usuario  = html.escape(str(form.getvalue("usuario", "")).strip())
password = str(form.getvalue("password", ""))

# Validación básica de longitud
if not usuario or not password:
    print("<h2>Datos incompletos</h2>")
    exit(1)

if len(usuario) > 50 or len(password) > 128:
    print("<h2>Datos inválidos</h2>")
    exit(1)

# ── 4. CONSULTA CON PREPARED STATEMENT ─────────────────────────────
IP_CLIENTE = os.environ.get('REMOTE_ADDR', 'unknown')

try:
    conn = sqlite3.connect('/var/app/db/usuarios.db')
    cursor = conn.cursor()
    # Parámetro ? — nunca concatenación directa
    cursor.execute("SELECT id, hash_password FROM usuarios WHERE usuario = ?", 
                   (usuario,))
    fila = cursor.fetchone()
finally:
    conn.close()

# ── 5. VERIFICAR CONTRASEÑA CON BCRYPT ────────────────────────────
# Siempre tomamos el mismo tiempo (evita timing attacks)
hash_dummy = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCOYzinvalidhashXXXXXXXXXXXXXX'
hash_bd = fila[1].encode('utf-8') if fila else hash_dummy

try:
    password_valido = bcrypt.checkpw(password.encode('utf-8'), hash_bd)
except Exception:
    password_valido = False

# ── 6. RESPUESTA Y LOGGING ─────────────────────────────────────────
if fila and password_valido:
    logging.info(f"AUTH_SUCCESS user={usuario} ip={IP_CLIENTE}")
    # Generar token de sesión — (en producción usar JWT o biblioteca de sesiones)
    print(f"<h2>Bienvenido</h2>")
    print(f"<p>Sesión iniciada correctamente.</p>")
else:
    logging.warning(f"AUTH_FAILURE user={usuario} ip={IP_CLIENTE}")
    time.sleep(1)  # Pequeña penalización para fuerza bruta
    print("<h2>Credenciales incorrectas</h2>")
    print("<p>Por favor, verifica tu usuario y contraseña.</p>")
```

---

# PARTE 4 — PRÁCTICA
## ⏱ Integrada en Transformación + Cierre

### 4.1 ACTIVIDAD COLABORATIVA: "ESPECIFICAMOS JUNTOS"
#### ⏱ 20 minutos | Grupos de 3-4 personas | Producto: Especificación Formal

**Instrucción:**

> "Vamos a trabajar en grupos. Tienen 15 minutos para desarrollar una especificación formal de seguridad completa para el módulo de login de uno de los siguientes sistemas. Cada grupo elige uno:"

```
SISTEMA A — Portal de notas de universidad pública peruana
SISTEMA B — Plataforma de e-commerce de retail (ropa deportiva)  
SISTEMA C — Sistema de historia clínica de clínica privada
SISTEMA D — App de delivery de comida (estilo Rappi/PedidosYa)
SISTEMA E — Sistema de votación estudiantil de un gremio universitario
```

**Estructura que deben completar (proyectar):**

```markdown
## ESPECIFICACIÓN FORMAL DE SEGURIDAD — MÓDULO LOGIN
### Sistema: [nombre del sistema elegido]
### Equipo: [nombres]

| Componente | Especificación |
|---|---|
| **Activos** | ¿Qué datos se protegen? |
| **Sujetos** | ¿Quiénes acceden? ¿Con qué roles? |
| **Objetos** | ¿A qué recursos controla acceso el login? |
| **Mecanismo de hash** | Algoritmo + parámetros |
| **Protocolo de cifrado** | Versión de TLS, cipher suites |
| **Política de contraseñas** | Longitud mínima, complejidad, historial |
| **Política de bloqueo** | Intentos antes de bloqueo, duración |
| **Expiración de sesión** | Tiempo de inactividad, máx duración |
| **Logging de seguridad** | ¿Qué eventos se registran? |
| **MFA** | ¿Se requiere? ¿Qué tipo? |
| **Respuesta ante violación** | ¿Qué ocurre si detectan un ataque? |
```

**Después de 15 minutos:** Cada grupo presenta su especificación en 2 minutos. El docente hace preguntas retadoras a cada grupo.

**Preguntas retadoras por sistema:**
- Sistema A: "¿Por qué en una universidad pública el riesgo de SQL Injection en el login es especialmente alto?"
- Sistema B: "¿Qué normativa de seguridad aplica si almacenan datos de tarjetas de crédito?"
- Sistema C: "¿Qué regulación peruana o internacional protege la historia clínica digital?"
- Sistema D: "¿Cómo manejarían que el cliente tiene tanto app móvil como web? ¿Misma especificación?"
- Sistema E: "¿Cómo garantizarían que nadie vote más de una vez y que los votos sean anónimos?"

---

# PARTE 5 — CIERRE
## ⏱ Duración: 25 minutos (Minutos 155–180)

---

### 5.1 ACTIVIDAD FINAL: "VOLVEMOS A LA LISTA"
#### ⏱ 5 minutos

> "¿Recuerdan la lista que escribimos al inicio — las razones por las que un login puede ser inseguro? Volvamos a ella."

*(Señala la pizarra donde quedó la lista del inicio.)*

> "¿Qué agregaríamos ahora que no estaba al principio? ¿Qué reformularíamos mejor?"

*(Agrega las nuevas ideas en color diferente. Visibiliza el aprendizaje.)*

---

### 5.2 CONSTRUCCIÓN COLECTIVA DE IDEAS PRINCIPALES
#### ⏱ 8 minutos

> "Antes de cerrar, quiero que construyamos juntos el mapa de lo que aprendimos. Les voy preguntando y van completando su guía de trabajo."

**5 preguntas de síntesis (los estudiantes responden, el docente complementa):**

1. "¿Cuál es la diferencia entre cifrado y hash y por qué importa en el login?"
2. "¿Qué hace bcrypt que SHA-256 no hace para proteger contraseñas?"
3. "¿Para qué sirve TLS y qué versión deben usar hoy?"
4. "¿Qué es una especificación formal de seguridad y qué contiene?"
5. "¿Cuál fue el error más crítico del código CGI inseguro que vimos?"

---

### 5.3 METACOGNICIÓN
#### ⏱ 5 minutos | Individual, escrito en guía de trabajo

> "Tómense 3 minutos para responder estas preguntas en su guía de trabajo. Nadie más las va a ver — son para ustedes."

```
1. ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?
2. ¿Qué concepto todavía no tienes del todo claro?
3. ¿Qué error de seguridad en código has cometido o podrías cometer 
   en el futuro que hoy ya reconoces?
4. ¿Cómo cambiaría tu forma de implementar un login después de hoy?
```

---

### 5.4 TAREA Y CONTINUACIÓN — SEMANA 3
#### ⏱ 4 minutos

**Tarea individual (presentar al inicio de la Semana 3):**

> "Para la próxima semana, quiero que busquen un sistema real — puede ser una app, un sitio web, un sistema universitario — y auditen su formulario de login desde afuera. Respondan estas preguntas:"

```
TAREA DE AUDITORÍA DE LOGIN (S2 → S3)
──────────────────────────────────────
1. ¿El sitio usa HTTPS? ¿Qué versión de TLS? 
   (Pueden verificar con https://www.ssllabs.com/ssltest/)
   
2. ¿El formulario usa método POST o GET?
   (Inspeccionar código fuente: clic derecho → Ver fuente)
   
3. ¿Tiene política de bloqueo de intentos? 
   (Intenten 3 veces una contraseña incorrecta — ¿qué pasa?)
   
4. ¿Ofrece autenticación de dos factores?

5. ¿Qué tan bueno es su certificado SSL?
   (SSL Labs da nota de A a F)

Documento de entrega: máximo 1 página + capturas de pantalla.
Traigan el sistema más inseguro que encuentren.
```

---

### 5.5 SÍNTESIS FINAL DEL DOCENTE
#### ⏱ 3 minutos

**GUION VERBAL — Cierre:**

> "Hoy aprendieron algo que la mayoría de tutoriales de internet nunca les va a enseñar: que implementar un login no es escribir cuatro líneas de PHP que comparen un usuario con una contraseña. Un login seguro es el resultado de decisiones de ingeniería muy específicas — qué algoritmo de hash usar, con qué parámetros, cómo cifrar el canal, cómo manejar los intentos fallidos, cómo no filtrar información en los mensajes de error."

> "LinkedIn pensó que tenía un login seguro en 2012. No lo tenía. Cometieron un error técnico que parece pequeño — olvidaron la sal en el hash — y 117 millones de usuarios pagaron las consecuencias. La diferencia entre ellos y un buen desarrollador no era inteligencia ni experiencia. Era conocer exactamente las especificaciones correctas. Y eso es lo que ustedes tienen ahora."

> "La semana que viene continuamos con el control de acceso, roles y permisos — el siguiente paso después de autenticar a alguien es decidir qué puede hacer. Nos vemos."

---

## EVALUACIÓN FORMATIVA SUGERIDA

| Momento | Instrumento | Propósito |
|---|---|---|
| Inicio | Preguntas de recuperación S1 | Verificar retención de la semana anterior |
| Transformación | Preguntas al aula (10 preguntas) | Verificar comprensión en tiempo real |
| Práctica | Especificación formal grupal | Verificar aplicación de conceptos |
| Cierre | Metacognición escrita | Autorregulación del aprendizaje |
| Tarea S3 | Auditoría de login real | Aplicación autónoma en entorno real |

---

## CASOS REALES RECOMENDADOS

| Caso | Año | Vulnerabilidad | Impacto |
|---|---|---|---|
| LinkedIn | 2012/2016 | Hash SHA-1 sin sal | 117M cuentas comprometidas |
| RockYou | 2009 | Contraseñas en texto plano | 32M contraseñas expuestas |
| Adobe | 2013 | 3DES cifrado (reversible) mal aplicado | 153M registros, contraseñas relacionadas con hints |
| Colonial Pipeline | 2021 | VPN sin MFA | Parálisis de suministro combustible 6 días |
| Uber | 2016 | Credenciales en repositorio GitHub | 57M registros de usuarios y conductores |

---

## REFERENCIAS EN APA 7

Barker, E. (2020). *Guideline for using cryptographic standards in the federal government: Cryptographic mechanisms* (NIST SP 800-175B Rev. 1). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-175Br1

Bernstein, D. J., & Lange, T. (2017). Post-quantum cryptography. *Nature*, 549(7671), 188–194. https://doi.org/10.1038/nature23461

OWASP Foundation. (2021). *OWASP Top 10 — 2021*. https://owasp.org/Top10/

Provos, N., & Mazières, D. (1999). *A future-adaptable password scheme*. USENIX Annual Technical Conference. https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf

Rescorla, E. (2018). *The Transport Layer Security (TLS) protocol version 1.3* (RFC 8446). Internet Engineering Task Force. https://datatracker.ietf.org/doc/html/rfc8446

Sweigart, A. (2020). *Automate the boring stuff with Python* (2nd ed.). No Starch Press.

Verizon. (2023). *2023 Data breach investigations report*. https://www.verizon.com/business/resources/reports/dbir/

Wheeler, D. (2016). *zxcvbn: Low-budget password strength estimation*. USENIX Security Symposium. https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/wheeler

---

## RECURSOS REALES Y LINKS ÚTILES

### Documentación oficial:
- **TLS 1.3 RFC 8446**: https://datatracker.ietf.org/doc/html/rfc8446
- **NIST Password Guidelines (SP 800-63B)**: https://pages.nist.gov/800-63-3/sp800-63b.html
- **OWASP Authentication Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- **OWASP Password Storage Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **OpenSSL Documentation**: https://www.openssl.org/docs/

### Herramientas:
- **SSL Labs Test**: https://www.ssllabs.com/ssltest/ — analiza la configuración SSL de cualquier servidor
- **Have I Been Pwned**: https://haveibeenpwned.com — verifica si un email fue parte de una filtración
- **Security.org Password Checker**: https://www.security.org/how-secure-is-my-password/
- **Bcrypt generator online**: https://bcrypt-generator.com (solo para entender, nunca usar online con contraseñas reales)

### GitHub — Proyectos de referencia:
- **OWASP WebGoat** (app deliberadamente insegura para aprender): https://github.com/WebGoat/WebGoat
- **OWASP Security Shepherd**: https://github.com/OWASP/SecurityShepherd
- **Awesome CGI Security**: https://github.com/nicowillis/awesome-cgi (referencias CGI)
- **Python CGI Examples**: https://github.com/python/cpython/tree/main/Lib/cgi.py

### Lecturas complementarias:
- **"How bcrypt works"** (Mauricio Leal): https://www.authenticationworld.com/Authentication-articles/how-bcrypt-works.html
- **"TLS 1.3 explained"** (Cloudflare Blog): https://blog.cloudflare.com/tls-1-3-overview-and-q-and-a/
- **NIST's deprecation of SHA-1**: https://csrc.nist.gov/projects/hash-functions

---

*Documento preparado para el curso Programación Segura (DD281) — Semana 2*
*Universidad Autónoma del Perú — 2026-1*
