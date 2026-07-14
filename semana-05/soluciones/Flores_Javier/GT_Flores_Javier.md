# PROGRAMACIÓN SEGURA — DD281
## Semana 5 | Vulnerabilidades OWASP: Inyección SQL, NoSQL y Command Injection

**Nombre:** Javier Flores Condeña **Código:** Grupo1 **Fecha:** 04/07/26

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

**Respuesta:** c) A03 — Inyección

---

**2.** ¿Qué carácter se usa más frecuentemente para iniciar un ataque de SQL Injection clásico?

- a) El símbolo `#`
- b) La barra diagonal `/`
- c) El apóstrofe `'`
- d) El guion bajo `_`

**Respuesta:** c) El apóstrofe `'`

---

**3.** ¿Cuál es el propósito del comentario `--` (doble guion) en un payload de SQL Injection?

- a) Insertar una nueva fila en la base de datos
- b) Comentar el resto de la consulta SQL para ignorar condiciones posteriores
- c) Cifrar la contraseña del usuario
- d) Activar el modo administrador de la base de datos

**Respuesta:** b) Comentar el resto...

---

**4.** ¿Cuál de los siguientes es un mecanismo de defensa primario contra SQL Injection?

- a) Usar contraseñas largas para la base de datos
- b) Consultas parametrizadas o prepared statements
- c) Cambiar el nombre de la tabla de usuarios
- d) Deshabilitar el acceso a internet

**Respuesta:** b) Consultas parametrizadas o prepared statements

---

**5.** En un ataque de Blind SQL Injection basado en tiempo, ¿qué función usa el atacante para inferir información?

- a) `SELECT * FROM`
- b) `UNION SELECT`
- c) `SLEEP()` o `WAITFOR DELAY`
- d) `DROP TABLE`

**Respuesta:** c) `SLEEP()` o `WAITFOR DELAY`

---

**6.** ¿Cuál de los siguientes payloads es característico de un ataque de NoSQL Injection en MongoDB?

- a) `' OR '1'='1`
- b) `{ "$gt": "" }`
- c) `1; DROP TABLE usuarios`
- d) `<script>alert('xss')</script>`

**Respuesta:** b) `{ "$gt": "" }`

---

**7.** En un ataque de Command Injection, ¿cuál operador permite ejecutar un segundo comando después del primero en Linux?

- a) El símbolo `%`
- b) El operador `==`
- c) El punto y coma `;` o el pipe `|`
- d) El símbolo `@`

**Respuesta:** c) `;` o `|`

---

**8.** Un desarrollador filtra la palabra "SELECT" del input del usuario para prevenir SQL Injection. ¿Por qué esta solución es insuficiente?

- a) Porque `SELECT` no es una palabra reservada de SQL
- b) Porque el atacante puede usar `SeLeCt`, `sELECT` u otras variantes con mayúsculas mezcladas o codificación
- c) Porque la base de datos no acepta la cláusula SELECT
- d) Porque la solución correcta es eliminar la base de datos

**Respuesta:** b) variantes

---

**9.** ¿Cuál es la diferencia fundamental entre una vulnerability assessment y un penetration test?

- a) No hay diferencia, son términos sinónimos
- b) La vulnerability assessment identifica y reporta fallos; el penetration test además los explota para demostrar impacto real
- c) El penetration test solo revisa el código fuente; la vulnerability assessment solo revisa la red
- d) La vulnerability assessment es ilegal; el penetration test es legal

**Respuesta:** b) assessment vs pentest

---

**10.** Un sistema rechaza el apóstrofe pero acepta consultas SQL con codificación URL. ¿Qué técnica usa el atacante?

- a) XSS reflejado
- b) CSRF
- c) Bypass de filtros mediante codificación (URL encoding: `%27` = `'`)
- d) Buffer overflow

**Respuesta:** c) URL encoding

---

## SECCIÓN B — COMPLETAR Y RELACIONAR
**20 puntos**

### B1. Complete los espacios en blanco
*10 puntos — 2 puntos por cada espacio correcto*

**1.** La vulnerabilidad OWASP A03:2021 se denomina Inyección y ocurre cuando datos no confiables se envían a un intérprete como parte de un comando o consulta.

**2.** En SQL Injection, el operador UNION permite concatenar resultados de una segunda consulta a la primera, lo que permite extraer datos de otras tablas.

**3.** La técnica de defensa que usa marcadores de posición `(?)` en lugar del valor directo del usuario se denomina Prepared Statement (Sentencia Preparada) o consulta parametrizada.

**4.** En MongoDB, el operador $gt significa "mayor que" y puede usarse para que una condición siempre sea verdadera con el valor vacío `""`.

**5.** El ataque en que el input del usuario se ejecuta como un comando del sistema operativo se llama Command Injection Injection y puede usarse para leer archivos del servidor con comandos como cat /etc/passwd (en sistemas Linux)..

---

### B2. Relacione las columnas
*10 puntos — 2 puntos por cada relación correcta*

| Columna A — Término | | Columna B — Definición / Ejemplo |
|---|---|---|
| 1. SQL Injection clásico | c | a) `'; SELECT SLEEP(5)--` |
| 2. Blind SQLi time-based | a | b) `{ "$where": "this.password.length > 0" }` |
| 3. UNION-based SQLi | e | c) `' OR '1'='1` |
| 4. NoSQL Injection | b | d) `127.0.0.1; cat /etc/passwd` |
| 5. Command Injection | d | e) `' UNION SELECT username, password FROM admin--` |
| 6. Prepared Statement | f | f) `cursor.execute("SELECT * FROM u WHERE id=?", (user_id,))` |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN
**30 puntos**

### C1. (8 puntos)

Un desarrollador junior argumenta: *"No necesito usar prepared statements porque ya valido que el input solo contenga letras y números"*.

¿Está en lo correcto? Justifique su respuesta mencionando al menos dos escenarios donde esta validación sería insuficiente.

**Respuesta:**

No, porque validar solo letras y números no garantiza que la aplicación esté protegida. Un cambio en el código o una validación incompleta puede permitir ataques de SQL Injection. Además, otros parámetros de la consulta podrían seguir siendo vulnerables. Lo correcto es usar Prepared Statements, ya que separan los datos del usuario del código SQL y ofrecen una protección mucho más segura.

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

La aplicación es vulnerable a SQL Injection, porque concatena directamente el dato ingresado por el usuario en la consulta SQL.

**(b) Tipo específico de inyección:**

SQL Injection clásica (In-band o Error-based).

**(c) Payload que explotaría la vulnerabilidad:**

' OR '1'='1' --

**(d) Código corregido:**

```python
@app.route('/buscar')
def buscar_producto():
    categoria = request.args.get('categoria')
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    query = "SELECT nombre, precio FROM productos WHERE categoria = ?"
    resultados = cursor.execute(query, (categoria,)).fetchall()

    return jsonify(resultados)



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

Se está realizando un ataque de Blind SQL Injection. El atacante prueba condiciones verdaderas ('1'='1) y falsas ('1'='2) para comparar las respuestas del sistema y verificar si la aplicación es vulnerable antes de extraer información.

**(b)** ¿Qué información está intentando obtener el atacante con la tercera consulta? *(5 puntos)*

(b) ¿Qué información está intentando obtener el atacante con la tercera consulta?

Está intentando identificar la versión de la base de datos, comprobando si el primer carácter del resultado de version() es el número 5. Con esa información puede planificar ataques más específicos.

---

## SECCIÓN D — AVANZADO Y DE CASO
**30 puntos**

**Caso profesional:** BancoDigital S.A. contrató a tu equipo para realizar un penetration test de su portal web. Durante la fase de discovery, encontraron que el endpoint `/api/transferencia` acepta parámetros JSON para consultar el saldo. Al enviar el payload `{"cuenta": {"$ne": null}}` recibieron una respuesta con todos los saldos del banco. Además, el endpoint `/utils/diagnostico` permite ejecutar un ping y devuelve el resultado en pantalla.

---

### D1. (10 puntos)

Describe con detalle técnico qué vulnerabilidades existen en cada endpoint, cómo las clasificarías según OWASP A03:2021, y cuál sería el impacto de negocio si fueran explotadas en producción.

**Endpoint `/api/transferencia`:**

Presenta una NoSQL Injection, ya que acepta operadores como $ne sin validarlos. Se clasifica como OWASP A03:2021 – Inyección, porque permite acceder a información no autorizada de la base de datos.

**Endpoint `/utils/diagnostico`:**

Presenta una Command Injection, debido a que ejecuta comandos del sistema operativo con datos proporcionados por el usuario. También pertenece a OWASP A03:2021 – Inyección.

**Impacto de negocio (ambos endpoints):**

Un atacante podría acceder a información confidencial de los clientes, modificar datos o ejecutar comandos en el servidor. Esto puede generar pérdidas económicas, afectar la continuidad del servicio y dañar la reputación del banco.

---

### D2. (10 puntos)

Diseño e implementación: ¿Cómo implementarías el endpoint `/api/transferencia` de forma segura usando validación de esquema (schema validation) para prevenir NoSQL Injection? Describe el enfoque, menciona la librería o técnica que usarías y proporciona pseudocódigo o código real.

**Enfoque y librería:**

Usaría Pydantic para validar que el campo cuenta sea únicamente una cadena de texto y no acepte operadores de MongoDB como $ne o $gt. Además, utilizaría consultas seguras y validación de entradas antes de acceder a la base de datos.

**Código o pseudocódigo seguro:**

```python
from pydantic import BaseModel

class Transferencia(BaseModel):
    cuenta: str

@app.post("/api/transferencia")
def transferencia(datos: Transferencia):
    saldo = db.cuentas.find_one({"cuenta": datos.cuenta})
    return saldo




```

---

### D3. Pensamiento crítico (10 puntos)

Un ingeniero de seguridad propone como solución al Command Injection del endpoint `/utils/diagnostico` simplemente limitar el input a solo direcciones IP con la expresión regular:

```
^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$
```

¿Esta solución es completamente segura? ¿Qué riesgos permanecen? ¿Qué solución propones tú?

**¿Es completamente segura? Justificación:**

No. La expresión regular ayuda a validar el formato de la IP, pero por sí sola no elimina el riesgo de Command Injection ni otros posibles ataques.

**Riesgos que permanecen:**

Pueden existir errores en la validación, abuso de la funcionalidad o vulnerabilidades si el comando se ejecuta directamente en el sistema operativo.

**Tu solución propuesta:**

Evitar ejecutar comandos mediante el shell, usar funciones seguras como subprocess.run() con shell=False, validar la entrada con una lista blanca de direcciones permitidas y aplicar el principio de mínimos privilegios en el servidor.

---

*Universidad Autónoma del Perú | Ingeniería de Sistemas | Ciclo VIII*
*Programación Segura — DD281 | Semana 5*


# RESPUESTAS DESARROLLADAS

## B1
1. Inyección; comando o consulta.
2. UNION.
3. Prepared Statement.
4. $gt.
5. Command; cat /etc/passwd.

## B2
1-c, 2-a, 3-e, 4-b, 5-d, 6-f.

## C1
No. Validar caracteres no elimina el riesgo. Puede haber bypass mediante codificaciones, fallos en otros parámetros, cambios futuros en la lógica o concatenaciones inseguras. La defensa correcta son consultas parametrizadas y validación por lista blanca.

## C2
(a) Vulnerabilidad: SQL Injection.
(b) SQL Injection clásica.
(c) Payload: `' OR '1'='1' --`
(d)
```python
@app.route('/buscar')
def buscar_producto():
    categoria=request.args.get("categoria")
    conn=sqlite3.connect("tienda.db")
    cur=conn.cursor()
    cur.execute("SELECT nombre, precio FROM productos WHERE categoria=?", (categoria,))
    return jsonify(cur.fetchall())
```

## C3
(a) Es un ataque Blind SQL Injection. El atacante compara respuestas verdaderas/falsas para inferir información.
(b) Intenta descubrir la versión de la base de datos verificando si el primer carácter de `version()` es 5.

## D1
/api/transferencia: NoSQL Injection mediante operadores MongoDB ($ne). Clasificación: OWASP A03:2021 Inyección.
/utils/diagnostico: Command Injection por ejecución de comandos del SO. Clasificación: OWASP A03:2021.
Impacto: fuga masiva de datos, ejecución remota, compromiso del servidor, pérdidas económicas y reputacionales.

## D2
Usar validación de esquema con Pydantic/Marshmallow y aceptar solo tipos esperados.
```python
from pydantic import BaseModel
class Req(BaseModel):
    cuenta:str

req=Req(**request.json)
db.cuentas.find_one({"cuenta":req.cuenta})
```

## D3
No es completamente segura. Aunque restringe el formato, puede haber abuso de la funcionalidad, SSRF interno o errores en la ejecución del comando.
La solución correcta es evitar invocar el shell, usar `subprocess.run([...], shell=False)`, lista blanca de destinos permitidos, validación estricta, mínimos privilegios y auditoría.
