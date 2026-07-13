# PROGRAMACIÓN SEGURA — DD281
## Semana 5 | Vulnerabilidades OWASP: Inyección SQL, NoSQL y Command Injection

**Nombre:** _______________________ **Código:** __________ **Fecha:** __________

**Tiempo estimado:** 90 minutos | **Puntaje total:** 100 puntos

**Instrucciones:** Responda con letra clara. Justifique sus respuestas en las secciones C y D.

---

## SECCIÓN A — OPCIÓN MÚLTIPLE
**20 puntos — 2 puntos por pregunta**

*Marque con una X la alternativa correcta. Solo una respuesta es válida por pregunta.*

---

**1.** ¿Cuál es la posición de la vulnerabilidad de Inyección en el OWASP Top 10 2021?

- a) A01 — Control de Acceso Roto
- b) A02 — Fallos Criptográficos
- c) A03 — Inyección
- d) A05 — Mala Configuración de Seguridad

**Respuesta:** _____

---

**2.** ¿Qué carácter se usa más frecuentemente para iniciar un ataque de SQL Injection clásico?

- a) El símbolo `#`
- b) La barra diagonal `/`
- c) El apóstrofe `'`
- d) El guion bajo `_`

**Respuesta:** _____

---

**3.** ¿Cuál es el propósito del comentario `--` (doble guion) en un payload de SQL Injection?

- a) Insertar una nueva fila en la base de datos
- b) Comentar el resto de la consulta SQL para ignorar condiciones posteriores
- c) Cifrar la contraseña del usuario
- d) Activar el modo administrador de la base de datos

**Respuesta:** _____

---

**4.** ¿Cuál de los siguientes es un mecanismo de defensa primario contra SQL Injection?

- a) Usar contraseñas largas para la base de datos
- b) Consultas parametrizadas o prepared statements
- c) Cambiar el nombre de la tabla de usuarios
- d) Deshabilitar el acceso a internet

**Respuesta:** _____

---

**5.** En un ataque de Blind SQL Injection basado en tiempo, ¿qué función usa el atacante para inferir información?

- a) `SELECT * FROM`
- b) `UNION SELECT`
- c) `SLEEP()` o `WAITFOR DELAY`
- d) `DROP TABLE`

**Respuesta:** _____

---

**6.** ¿Cuál de los siguientes payloads es característico de un ataque de NoSQL Injection en MongoDB?

- a) `' OR '1'='1`
- b) `{ "$gt": "" }`
- c) `1; DROP TABLE usuarios`
- d) `<script>alert('xss')</script>`

**Respuesta:** _____

---

**7.** En un ataque de Command Injection, ¿cuál operador permite ejecutar un segundo comando después del primero en Linux?

- a) El símbolo `%`
- b) El operador `==`
- c) El punto y coma `;` o el pipe `|`
- d) El símbolo `@`

**Respuesta:** _____

---

**8.** Un desarrollador filtra la palabra "SELECT" del input del usuario para prevenir SQL Injection. ¿Por qué esta solución es insuficiente?

- a) Porque `SELECT` no es una palabra reservada de SQL
- b) Porque el atacante puede usar `SeLeCt`, `sELECT` u otras variantes con mayúsculas mezcladas o codificación
- c) Porque la base de datos no acepta la cláusula SELECT
- d) Porque la solución correcta es eliminar la base de datos

**Respuesta:** _____

---

**9.** ¿Cuál es la diferencia fundamental entre una vulnerability assessment y un penetration test?

- a) No hay diferencia, son términos sinónimos
- b) La vulnerability assessment identifica y reporta fallos; el penetration test además los explota para demostrar impacto real
- c) El penetration test solo revisa el código fuente; la vulnerability assessment solo revisa la red
- d) La vulnerability assessment es ilegal; el penetration test es legal

**Respuesta:** _____

---

**10.** Un sistema rechaza el apóstrofe pero acepta consultas SQL con codificación URL. ¿Qué técnica usa el atacante?

- a) XSS reflejado
- b) CSRF
- c) Bypass de filtros mediante codificación (URL encoding: `%27` = `'`)
- d) Buffer overflow

**Respuesta:** _____

---

## SECCIÓN B — COMPLETAR Y RELACIONAR
**20 puntos**

### B1. Complete los espacios en blanco
*10 puntos — 2 puntos por cada espacio correcto*

**1.** La vulnerabilidad OWASP A03:2021 se denomina _________________________ y ocurre cuando datos no confiables se envían a un intérprete como parte de un _________________________.

**2.** En SQL Injection, el operador _________________________ permite concatenar resultados de una segunda consulta a la primera, lo que permite extraer datos de otras tablas.

**3.** La técnica de defensa que usa marcadores de posición `(?)` en lugar del valor directo del usuario se denomina _________________________ o consulta parametrizada.

**4.** En MongoDB, el operador _________________________ significa "mayor que" y puede usarse para que una condición siempre sea verdadera con el valor vacío `""`.

**5.** El ataque en que el input del usuario se ejecuta como un comando del sistema operativo se llama _________________________ Injection y puede usarse para leer archivos del servidor con comandos como _________________________.

---

### B2. Relacione las columnas
*10 puntos — 2 puntos por cada relación correcta*

| Columna A — Término | | Columna B — Definición / Ejemplo |
|---|---|---|
| 1. SQL Injection clásico | _____ | a) `'; SELECT SLEEP(5)--` |
| 2. Blind SQLi time-based | _____ | b) `{ "$where": "this.password.length > 0" }` |
| 3. UNION-based SQLi | _____ | c) `' OR '1'='1` |
| 4. NoSQL Injection | _____ | d) `127.0.0.1; cat /etc/passwd` |
| 5. Command Injection | _____ | e) `' UNION SELECT username, password FROM admin--` |
| 6. Prepared Statement | _____ | f) `cursor.execute("SELECT * FROM u WHERE id=?", (user_id,))` |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN
**30 puntos**

### C1. (8 puntos)

Un desarrollador junior argumenta: *"No necesito usar prepared statements porque ya valido que el input solo contenga letras y números"*.

¿Está en lo correcto? Justifique su respuesta mencionando al menos dos escenarios donde esta validación sería insuficiente.

**Respuesta:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### C2. (12 puntos)

Analice el siguiente fragmento de código Python e identifique:

**(a)** la vulnerabilidad presente
**(b)** el tipo específico de inyección
**(c)** un payload que la explotaría
**(d)** la corrección aplicando buenas prácticas

```python
@app.route('/buscar')
def buscar_producto():
    categoria = request.args.get('categoria')
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    query = "SELECT nombre, precio FROM productos WHERE categoria = '" + categoria + "'"
    resultados = cursor.execute(query).fetchall()
    return jsonify(resultados)
```

**(a) Vulnerabilidad:**

_______________________________________________________________________________

_______________________________________________________________________________

**(b) Tipo específico de inyección:**

_______________________________________________________________________________

_______________________________________________________________________________

**(c) Payload que explotaría la vulnerabilidad:**

_______________________________________________________________________________

_______________________________________________________________________________

**(d) Código corregido:**

```python
@app.route('/buscar')
def buscar_producto():




```

---

### C3. Mini caso de análisis — LogiTech (10 puntos)

La empresa LogiTech recibió una alerta de su sistema IDS. En los logs de acceso encontraron estas solicitudes en secuencia:

```
GET /buscar?q=test' AND '1'='1
GET /buscar?q=test' AND '1'='2
GET /buscar?q=test' AND SUBSTRING(version(),1,1)='5
```

**(a)** ¿Qué tipo de ataque está ocurriendo? Explique el patrón que observa. *(5 puntos)*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**(b)** ¿Qué información está intentando obtener el atacante con la tercera consulta? *(5 puntos)*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

## SECCIÓN D — AVANZADO Y DE CASO
**30 puntos**

**Caso profesional:** BancoDigital S.A. contrató a tu equipo para realizar un penetration test de su portal web. Durante la fase de discovery, encontraron que el endpoint `/api/transferencia` acepta parámetros JSON para consultar el saldo. Al enviar el payload `{"cuenta": {"$ne": null}}` recibieron una respuesta con todos los saldos del banco. Además, el endpoint `/utils/diagnostico` permite ejecutar un ping y devuelve el resultado en pantalla.

---

### D1. (10 puntos)

Describe con detalle técnico qué vulnerabilidades existen en cada endpoint, cómo las clasificarías según OWASP A03:2021, y cuál sería el impacto de negocio si fueran explotadas en producción.

**Endpoint `/api/transferencia`:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**Endpoint `/utils/diagnostico`:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**Impacto de negocio (ambos endpoints):**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### D2. (10 puntos)

Diseño e implementación: ¿Cómo implementarías el endpoint `/api/transferencia` de forma segura usando validación de esquema (schema validation) para prevenir NoSQL Injection? Describe el enfoque, menciona la librería o técnica que usarías y proporciona pseudocódigo o código real.

**Enfoque y librería:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**Código o pseudocódigo seguro:**

```python
# Tu implementación aquí




```

---

### D3. Pensamiento crítico (10 puntos)

Un ingeniero de seguridad propone como solución al Command Injection del endpoint `/utils/diagnostico` simplemente limitar el input a solo direcciones IP con la expresión regular:

```
^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$
```

¿Esta solución es completamente segura? ¿Qué riesgos permanecen? ¿Qué solución propones tú?

**¿Es completamente segura? Justificación:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**Riesgos que permanecen:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

**Tu solución propuesta:**

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

*Universidad Autónoma del Perú | Ingeniería de Sistemas | Ciclo VIII*
*Programación Segura — DD281 | Semana 5*
