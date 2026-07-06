# PROGRAMACIÓN SEGURA — DD281
## Semana 5 | Vulnerabilidades OWASP: Inyección SQL, NoSQL y Command Injection

**Nombre:** Wilder Norabuena Ramirez **Código:** 2231892424 **Fecha:** 04/07/2026

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

**Respuesta:** C

---

**2.** ¿Qué carácter se usa más frecuentemente para iniciar un ataque de SQL Injection clásico?

- a) El símbolo `#`
- b) La barra diagonal `/`
- c) El apóstrofe `'`
- d) El guion bajo `_`

**Respuesta:** C
---

**3.** ¿Cuál es el propósito del comentario `--` (doble guion) en un payload de SQL Injection?

- a) Insertar una nueva fila en la base de datos
- b) Comentar el resto de la consulta SQL para ignorar condiciones posteriores
- c) Cifrar la contraseña del usuario
- d) Activar el modo administrador de la base de datos

**Respuesta:** B

---

**4.** ¿Cuál de los siguientes es un mecanismo de defensa primario contra SQL Injection?

- a) Usar contraseñas largas para la base de datos
- b) Consultas parametrizadas o prepared statements
- c) Cambiar el nombre de la tabla de usuarios
- d) Deshabilitar el acceso a internet

**Respuesta:** B

---

**5.** En un ataque de Blind SQL Injection basado en tiempo, ¿qué función usa el atacante para inferir información?

- a) `SELECT * FROM`
- b) `UNION SELECT`
- c) `SLEEP()` o `WAITFOR DELAY`
- d) `DROP TABLE`

**Respuesta:** C

---

**6.** ¿Cuál de los siguientes payloads es característico de un ataque de NoSQL Injection en MongoDB?

- a) `' OR '1'='1`
- b) `{ "$gt": "" }`
- c) `1; DROP TABLE usuarios`
- d) `<script>alert('xss')</script>`

**Respuesta:** B

---

**7.** En un ataque de Command Injection, ¿cuál operador permite ejecutar un segundo comando después del primero en Linux?

- a) El símbolo `%`
- b) El operador `==`
- c) El punto y coma `;` o el pipe `|`
- d) El símbolo `@`

**Respuesta:** C

---

**8.** Un desarrollador filtra la palabra "SELECT" del input del usuario para prevenir SQL Injection. ¿Por qué esta solución es insuficiente?

- a) Porque `SELECT` no es una palabra reservada de SQL
- b) Porque el atacante puede usar `SeLeCt`, `sELECT` u otras variantes con mayúsculas mezcladas o codificación
- c) Porque la base de datos no acepta la cláusula SELECT
- d) Porque la solución correcta es eliminar la base de datos

**Respuesta:** B

---

**9.** ¿Cuál es la diferencia fundamental entre una vulnerability assessment y un penetration test?

- a) No hay diferencia, son términos sinónimos
- b) La vulnerability assessment identifica y reporta fallos; el penetration test además los explota para demostrar impacto real
- c) El penetration test solo revisa el código fuente; la vulnerability assessment solo revisa la red
- d) La vulnerability assessment es ilegal; el penetration test es legal

**Respuesta:** B

---

**10.** Un sistema rechaza el apóstrofe pero acepta consultas SQL con codificación URL. ¿Qué técnica usa el atacante?

- a) XSS reflejado
- b) CSRF
- c) Bypass de filtros mediante codificación (URL encoding: `%27` = `'`)
- d) Buffer overflow

**Respuesta:** C

---

## SECCIÓN B — COMPLETAR Y RELACIONAR
**20 puntos**

### B1. Complete los espacios en blanco
*10 puntos — 2 puntos por cada espacio correcto*

**1.** La vulnerabilidad OWASP A03:2021 se denomina **Inyección** y ocurre cuando datos no confiables se envían a un intérprete como parte de un **comando o consulta**.

**2.** En SQL Injection, el operador **UNION** permite concatenar resultados de una segunda consulta a la primera, lo que permite extraer datos de otras tablas.

**3.** La técnica de defensa que usa marcadores de posición `(?)` en lugar del valor directo del usuario se denomina **sentencia preparada** o consulta parametrizada.

**4.** En MongoDB, el operador **$gt** significa "mayor que" y puede usarse para que una condición siempre sea verdadera con el valor vacío `""`.

**5.** El ataque en que el input del usuario se ejecuta como un comando del sistema operativo se llama**Command** Injection y puede usarse para leer archivos del servidor con comandos como **cat /etc/passwd**.

---

### B2. Relacione las columnas
*10 puntos — 2 puntos por cada relación correcta*

| Columna A — Término | | Columna B — Definición / Ejemplo |
|---|---|---|
| 1. SQL Injection clásico | **C** | a) `'; SELECT SLEEP(5)--` |
| 2. Blind SQLi time-based |**A** | b) `{ "$where": "this.password.length > 0" }` |
| 3. UNION-based SQLi | **E** | c) `' OR '1'='1` |
| 4. NoSQL Injection | **B** | d) `127.0.0.1; cat /etc/passwd` |
| 5. Command Injection | **D** | e) `' UNION SELECT username, password FROM admin--` |
| 6. Prepared Statement | **F** | f) `cursor.execute("SELECT * FROM u WHERE id=?", (user_id,))` |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN
**30 puntos**

### C1. (8 puntos)

Un desarrollador junior argumenta: *"No necesito usar prepared statements porque ya valido que el input solo contenga letras y números"*.

¿Está en lo correcto? Justifique su respuesta mencionando al menos dos escenarios donde esta validación sería insuficiente.

**Respuesta:**

No, el desarrollador no está en lo correcto. Usar listas blancas (solo letras y números) es una buena medida de defensa en profundidad, pero no sustituye a las sentencias preparadas por varias razones:

- a) Requerimientos del negocio cambiantes: Si en el futuro se necesita permitir caracteres especiales (por ejemplo, correos electrónicos con @ o apellidos como O'Connor), el filtro se romperá o los desarrolladores lo desactivarán, dejando el sistema vulnerable inmediatamente.

- b) Contexto numérico sin comillas: Si el input se inyecta en una variable de tipo entero que la base de datos lee sin comillas (SELECT * FROM usuarios WHERE id = [INPUT]), permitir espacios junto con letras y números permitiría inyectar payloads como 1 OR 1, alterando la lógica de la consulta sin necesidad de caracteres especiales.

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

El código concatena directamente la entrada del usuario (categoria) en la cadena de la consulta SQL sin ningún tipo de validación, sanitización ni parametrización.

**(b) Tipo específico de inyección:**

SQL Injection clásico basado en errores o booleanos (dependiendo de cómo se reflejen los resultados en la interfaz).

**(c) Payload que explotaría la vulnerabilidad:**

' OR '1'='1 (Esto terminaría generando la consulta: SELECT nombre, precio FROM productos WHERE categoria = '' OR '1'='1').
**(d) Código corregido:**

```python
@app.route('/buscar')
def buscar_producto():
    categoria = request.args.get('categoria')
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    # Se utiliza una consulta parametrizada con el marcador '?'
    query = "SELECT nombre, precio FROM productos WHERE categoria = ?"
    # Se pasa la variable 'categoria' como una tupla en la ejecución
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

**(a) ¿Qué tipo de ataque está ocurriendo? Explique el patrón que observa. (5 puntos)**

Está ocurriendo un ataque de Blind SQL Injection (Inyección Ciega), específicamente del tipo basado en booleanos. El atacante inyecta condiciones lógicas ('1'='1 que es verdadera y '1'='2 que es falsa) para observar si el comportamiento, contenido o tamaño de la respuesta HTTP cambia, verificando así que la vulnerabilidad existe sin recibir errores de sintaxis explícitos de la base de datos.

**(b) ¿Qué información está intentando obtener el atacante con la tercera consulta? (5 puntos)**

El atacante está intentando extraer la versión del motor de la base de datos letra por letra. Al usar SUBSTRING(version(),1,1)='5, le pregunta a la base de datos: "¿El primer carácter de tu versión es el número 5?". Si la página carga normalmente, la respuesta es "Sí"; de lo contrario, probará con el número 4, 6, etc.

## SECCIÓN D — AVANZADO Y DE CASO
**30 puntos**

**Caso profesional:** BancoDigital S.A. contrató a tu equipo para realizar un penetration test de su portal web. Durante la fase de discovery, encontraron que el endpoint `/api/transferencia` acepta parámetros JSON para consultar el saldo. Al enviar el payload `{"cuenta": {"$ne": null}}` recibieron una respuesta con todos los saldos del banco. Además, el endpoint `/utils/diagnostico` permite ejecutar un ping y devuelve el resultado en pantalla.

---

### D1. (10 puntos)

Describe con detalle técnico qué vulnerabilidades existen en cada endpoint, cómo las clasificarías según OWASP A03:2021, y cuál sería el impacto de negocio si fueran explotadas en producción.

**Endpoint `/api/transferencia`:**

Sufre de NoSQL Injection. Al pasar objetos JSON anidados con operadores nativos de MongoDB (como $ne: no igual), el backend interpreta el operador lógicamente en lugar de como una cadena de texto. Se clasifica en A03:2021 (Inyección).

**Endpoint `/utils/diagnostico`:**

Sufre de Command Injection (Inyección de Comandos del Sistema Operativo). La entrada del usuario se concatena directamente en un llamado a la consola del servidor subyacente (shell). Se clasifica en A03:2021 (Inyección).

**Impacto de negocio (ambos endpoints):**

El riesgo es crítico. La inyección NoSQL expone información financiera altamente confidencial (saldos bancarios), lo que llevaría a demandas, pérdida de confianza del cliente y sanciones regulatorias. El Command Injection es aún peor: permite al atacante obtener control total (RCE) sobre el servidor, pudiendo moverse lateralmente en la red interna del BancoDigital, exfiltrar bases de datos completas e implantar malware.

---

### D2. (10 puntos)

Diseño e implementación: ¿Cómo implementarías el endpoint `/api/transferencia` de forma segura usando validación de esquema (schema validation) para prevenir NoSQL Injection? Describe el enfoque, menciona la librería o técnica que usarías y proporciona pseudocódigo o código real.

**Enfoque y librería:**

El enfoque seguro es implementar Schema Validation (Validación de Esquema) estricta antes de que los datos toquen el driver de la base de datos. En Python, usaría la librería Pydantic para forzar que el valor recibido en el parámetro "cuenta" sea estrictamente de tipo string (cadena de texto) y rechazar cualquier entrada que sea un diccionario, objeto o array.

**Código o pseudocódigo seguro:**

```python
# Tu implementación aquí
from flask import request, jsonify
from pydantic import BaseModel, ValidationError

# Definimos el esquema estricto esperado
class ConsultaSaldoRequest(BaseModel):
    cuenta: str

@app.route('/api/transferencia', methods=['POST'])
def consultar_saldo():
    try:
        # Pydantic validará que 'cuenta' sea un string y no un objeto como {"$ne": null}
        datos_validados = ConsultaSaldoRequest(**request.json)
        
        # Uso seguro en la consulta a la BD
        cuenta_segura = datos_validados.cuenta
        resultado = db.cuentas.find_one({"cuenta": cuenta_segura})
        
        return jsonify({"saldo": resultado.get("saldo")})
        
    except ValidationError:
        return jsonify({"error": "Formato de cuenta inválido. Se esperaba texto."}), 400

```

---

### D3. Pensamiento crítico (10 puntos)

Un ingeniero de seguridad propone como solución al Command Injection del endpoint `/utils/diagnostico` simplemente limitar el input a solo direcciones IP con la expresión regular:

```
^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$
```

¿Esta solución es completamente segura? ¿Qué riesgos permanecen? ¿Qué solución propones tú?

**¿Es completamente segura? Justificación:**

No, la expresión regular por sí sola no constituye una solución robusta. Aunque la regex exige el formato estructural de una IP y mitiga el Command Injection clásico (porque evita que el atacante introduzca punto y coma ;, pipes | o ampersands &), no resuelve la vulnerabilidad arquitectónica de invocar comandos del sistema operativo.

**Riesgos que permanecen:**

El sistema sigue siendo vulnerable a SSRF (Server-Side Request Forgery). El atacante podría ingresar IPs privadas o de la infraestructura de red interna del banco (ej. 192.168.1.10, 127.0.0.1 o IPs de metadatos de AWS/GCP). Esto permite al atacante usar el servidor como "puente" para escanear puertos internos, evadir firewalls y descubrir servicios ocultos.

**Tu solución propuesta:**

1) Descartar completamente el uso de shells del sistema (como os.system() o subprocess.run(..., shell=True)).

2) Usar una librería nativa y segura para operaciones de red. Si se necesita verificar conectividad en Python, se pueden usar librerías de sockets o paquetes ICMP dedicados que no pasan por el intérprete de comandos bash/cmd.

3) Implementar un validación lógica de IPs, bloqueando (mediante listas negras de rangos) el acceso a cualquier red interna o loopback, permitiendo diagnosticar únicamente direcciones públicas justificadas.

---

*Universidad Autónoma del Perú | Ingeniería de Sistemas | Ciclo VIII*
*Programación Segura — DD281 | Semana 5*
