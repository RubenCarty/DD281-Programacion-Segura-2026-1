# INFORME — LABORATORIO SEMANA 5
# Programación Segura — DD281

**Nombre:** OMAR RIVERA CASTILLO
**Código:** 2221895826
**Fecha de entrega:** 06/07/2026

---

## PARTE 1 — Exploración: el entorno vulnerable

### Pregunta de reflexión 1.3

**¿Cuántas vulnerabilidades identificas? ¿En qué línea/endpoint está cada una?**

Se identificaron **4 vulnerabilidades** en `app_vulnerable.py`:

| # | Endpoint | Tipo de vulnerabilidad | Causa raíz |
|---|---|---|---|
| 1 | `POST /login` | SQL Injection clásico (autenticación) | Concatenación de `usuario` y `password` directamente en el string SQL con f-string |
| 2 | `GET /buscar` | SQL Injection UNION-based | Concatenación de `categoria` en el `WHERE` de un `SELECT` |
| 3 | `GET /diagnostico` | OS Command Injection | `subprocess.run(f"ping -c 2 {host}", shell=True, ...)` interpreta el input como comandos de shell |
| 4 | `GET /perfil/<id>` | SQL Injection ciega (Blind, boolean-based) | El parámetro `filtro` se concatena sin sanitizar en una condición `WHERE ... AND (filtro)`, y los errores de BD se silencian |

**¿Qué tienen en común todas?**

Las cuatro comparten la misma causa raíz: **mezclar datos de entrada del usuario con código ejecutable (SQL o comandos de shell) mediante concatenación de strings**, en lugar de mantener una separación estricta entre "código" y "datos". Ninguna de ellas valida, sanitiza ni escapa el input antes de usarlo, y todas confían implícitamente en que el usuario enviará datos "bien portados". Adicionalmente, los endpoints 1 y 2 agravan el problema exponiendo la query SQL generada (`query_debug`) y los mensajes de error de la base de datos directamente en la respuesta, lo que facilita enormemente la explotación (SQLi basado en errores).

---

## PARTE 2 — Aplicación: explotar y defender

### Punto de verificación 2.1 — Login

| Prueba | Payload | Resultado |
|---|---|---|
| Prueba 1 (login normal) | `usuario: juan`, `password: juan2024` | ✅ Acceso concedido — `"Bienvenido juan"`, rol `cliente` |
| Prueba 2 (bypass con comentario) | `usuario: admin'--`, `password: cualquiercosa` | ✅ **Acceso concedido como admin sin conocer la contraseña.** La query resultante fue `...WHERE usuario='admin'--' AND password='cualquiercosa'`; el `--` comenta el resto de la condición, así que solo se evalúa `usuario='admin'` |
| Prueba 3 (OR injection) | `usuario: ' OR '1'='1'--`, `password: ""` | ✅ **Acceso concedido como el primer usuario de la tabla (admin)**, porque la condición `'1'='1'` es siempre verdadera para todas las filas y el registro con `id` más bajo es el que retorna `fetchone()` |

**Conclusión:** ambos ataques bypasean completamente la autenticación sin necesidad de conocer ninguna credencial válida.

### Pregunta de análisis 2.2 — UNION-based SQLi

**¿Cuántas columnas tiene la tabla `productos`?**

5 columnas: `id, nombre, precio, categoria, stock`.

**¿Por qué es importante saberlo para el UNION attack?**

Porque la sentencia `UNION SELECT` de SQL exige que **el número de columnas y su orden/tipo sean compatibles** entre el `SELECT` original y el `SELECT` inyectado; si no coinciden, el motor de base de datos devuelve un error (`SELECTs to the left and right of UNION do not have the same number of result columns`). Por eso, antes de construir el ataque hay que determinarlo primero con `ORDER BY N` (probando N creciente hasta que la consulta falle), y solo entonces se puede alinear el `UNION SELECT id, usuario, password, rol, email FROM usuarios` con las 5 columnas esperadas por `productos`, logrando así "camuflar" los datos de la tabla `usuarios` como si fueran resultados de productos.

**Resultado obtenido con el ataque:**

```
?categoria=nada' UNION SELECT id,usuario,password,rol,email FROM usuarios--
```

Devolvió las 4 filas completas de la tabla `usuarios`, incluyendo usuario y contraseña en texto plano (por ejemplo, `admin / AdminPass123`), mostrados en los campos `nombre` y `precio` de la respuesta JSON.

### Punto de verificación 2.3 — Command Injection

**¿Pudiste listar los archivos del servidor? ¿Qué información sensible encontraste?**

Sí. El payload `?host=127.0.0.1; ls -la` ejecuta el `ping` normal y **además** ejecuta `ls -la` como un segundo comando independiente, porque `subprocess.run(..., shell=True)` invoca una shell que interpreta `;` como separador de comandos. El listado de archivos expone la existencia de `tienda.db` (la base de datos completa), el código fuente de la aplicación (`app_vulnerable.py`) y cualquier otro archivo del directorio de trabajo del servidor. Con `printenv` sería posible además filtrar variables de entorno que en un entorno real podrían contener credenciales, tokens de API o cadenas de conexión a bases de datos.

### Punto de verificación 2.4 — `app_segura.py`

Los 7 `TODO` fueron completados:

1. **Validación de longitud:** usuario ≤ 50 caracteres, password ≤ 128 caracteres (y no vacíos); si falla, responde `400`.
2. **Validación de formato del usuario:** `re.match(r'^[a-zA-Z0-9_]{3,50}$', usuario)` — rechaza cualquier carácter especial como comillas (`'`) que necesitaría un ataque SQLi.
3. **Prepared statement en login:** `cursor.execute("SELECT ... WHERE usuario=? AND password=?", (usuario, password))`. El driver de SQLite envía la consulta y los datos por separado, así que un valor como `admin'--` se trata siempre como texto literal, nunca como sintaxis SQL.
4. **Validación de categoría:** `re.match(r'^[a-z_]{1,30}$', categoria)` — bloquea comillas, espacios y palabras clave SQL.
5. **Prepared statement en búsqueda:** `cursor.execute("SELECT ... WHERE categoria=?", (categoria,))`.
6. **Validación de IP:** `ipaddress.ip_address(host_raw)` rechaza cualquier valor que no sea una IP bien formada (esto por sí solo ya bloquea `; ls -la`), y además se descartan explícitamente IPs privadas, loopback, reservadas, link-local y multicast para evitar problemas tipo SSRF.
7. **Ejecución sin shell:** `subprocess.run(["ping", "-c", "2", str(ip)], shell=False, ...)`. Al pasar los argumentos como **lista** y no usar `shell=True`, el sistema operativo nunca invoca un intérprete de shell, por lo que caracteres como `;`, `&&` o `|` se pasan literalmente como argumento de `ping` (que los rechaza) en vez de ejecutarse como comandos.

**Verificación realizada (con Flask test client):**

| Ataque | `app_vulnerable.py` | `app_segura.py` |
|---|---|---|
| `admin'--` | Bypass exitoso (200, rol admin) | Rechazado (400, "Credenciales inválidas") |
| `' OR '1'='1'--` | Bypass exitoso (200, rol admin) | Rechazado (400) |
| UNION SELECT sobre `usuarios` | Extrae 4 usuarios/contraseñas | Rechazado (400, "Categoría inválida") |
| `; echo HACKEADO` en `/diagnostico` | Ejecuta el comando extra | Rechazado (400, "Host inválido: debe ser una dirección IP") |
| IP privada (`192.168.1.1`) en `/diagnostico` | (no aplicaba en la versión vulnerable) | Rechazado (400, "No se permiten IPs privadas...") |

Todos los ataques que funcionaban contra `app_vulnerable.py` fueron bloqueados por `app_segura.py`, mientras que las peticiones legítimas (login correcto, búsqueda por categoría válida) siguen funcionando con normalidad.

---

## PARTE 3 — Desafío: Blind SQL Injection manual

### Nota metodológica importante

Durante la implementación se detectó que la técnica propuesta originalmente en el enunciado (inyectar en la cláusula `ORDER BY` del endpoint `/perfil`) **no es explotable en la práctica**: SQLite (como la mayoría de motores) omite evaluar la expresión de `ORDER BY` cuando el conjunto de resultados tiene una sola fila, ya que no hay nada que ordenar. Esto se comprobó empíricamente: tanto una condición verdadera como una falsa dentro del `CASE WHEN` devolvían siempre `existe: True`, sin ninguna diferencia observable.

Para que el ataque fuera realmente demostrable, se ajustó el endpoint vulnerable para inyectar la condición booleana directamente en la cláusula `WHERE` (parámetro `filtro` en vez de `orden`): `WHERE id={user_id} AND ({filtro})`. Esta es la variante estándar de "boolean-based blind SQLi": si la condición inyectada es verdadera, la fila sigue existiendo y la API responde `existe: true`; si es falsa, la fila deja de cumplir el `WHERE` y la API responde `existe: false`. Con este ajuste, la técnica del enunciado (usar `CASE WHEN ... THEN ... ELSE ...`) sí funciona de forma consistente.

### Desafío 3.1 — Pruebas booleanas

```
GET /perfil/1?filtro=1=1        → {"existe": true,  "usuario": "admin"}
GET /perfil/1?filtro=1=2        → {"existe": false}
```

Esto confirma que el canal booleano (`existe` true/false) es observable y explotable sin necesidad de ver ningún mensaje de error de la base de datos.

### Desafío 3.2 — Script `blind_sqli.py`

Se ejecutó el script de extracción automática contra `app_vulnerable.py`, probando en cada posición todos los caracteres de `CHARS` con el payload:

```
1=1 AND SUBSTR((SELECT password FROM usuarios WHERE id=1),{posicion},1)='{caracter}'
```

**Resultado de la ejecución:**

```
Posición 1: 'A'  -> A
Posición 2: 'd'  -> Ad
Posición 3: 'm'  -> Adm
Posición 4: 'i'  -> Admi
Posición 5: 'n'  -> Admin
Posición 6: 'P'  -> AdminP
Posición 7: 'a'  -> AdminPa
Posición 8: 's'  -> AdminPas
Posición 9: 's'  -> AdminPass
Posición 10: '1' -> AdminPass1
Posición 11: '2' -> AdminPass12
Posición 12: '3' -> AdminPass123
Fin de la contraseña en posición 13

Total de peticiones HTTP realizadas: 379
Contraseña extraída: 'AdminPass123'
```

La contraseña extraída (`AdminPass123`) coincide exactamente con el valor sembrado en `setup_db.py`, confirmando que el ataque de Blind SQLi automatizado funciona de extremo a extremo.

### Preguntas de reflexión final

**1. ¿Cuántas peticiones HTTP se necesitaron para extraer la contraseña? ¿Qué implica esto sobre los logs del servidor?**

Se necesitaron **379 peticiones HTTP** para extraer una contraseña de 12 caracteres (el alfabeto de prueba tiene 68 caracteres posibles por posición, en el peor caso). Esto implica que un ataque de Blind SQLi, aunque más lento que uno basado en errores, sigue siendo completamente viable de forma automatizada (segundos a minutos). Desde el punto de vista defensivo, esto significa que:
- Un volumen alto y anómalo de peticiones muy similares hacia un mismo endpoint, en un lapso corto, desde una misma IP/sesión, es una señal clara de ataque que **debería** aparecer en los logs y disparar alertas.
- Si el servidor no registra el detalle de los parámetros de consulta (`filtro`, `orden`, etc.) en sus logs, es imposible investigar el ataque después del hecho — por eso es crítico loguear las peticiones sospechosas (sin loguear datos sensibles como contraseñas).
- La ausencia de rate limiting o de un WAF permitió que las 379 peticiones se realizaran sin ninguna fricción.

**2. Si la contraseña estuviera hasheada con bcrypt, ¿seguiría siendo útil el ataque? ¿Por qué?**

Sí seguiría siendo útil, pero cambiaría el objetivo: en lugar de extraer la contraseña en texto plano carácter por carácter (que ya no existiría en la BD), el atacante extraería el **hash bcrypt completo** almacenado (por ejemplo, `SUBSTR((SELECT password FROM usuarios WHERE id=1), posicion, 1)`). El hash es una cadena larga y de apariencia aleatoria, pero sigue siendo un dato extraíble byte a byte con la misma técnica de Blind SQLi. Una vez obtenido el hash completo, el atacante tendría que intentar crackearlo offline (fuerza bruta o diccionario), lo cual con bcrypt es deliberadamente lento y costoso (factor de coste configurable), a diferencia de un hash rápido como MD5/SHA1. En resumen: **bcrypt no evita la fuga de datos vía SQLi**, solo dificulta mucho más su explotación posterior. La verdadera mitigación de este ataque es cerrar la vulnerabilidad de inyección, no solo hashear contraseñas.

**3. ¿Cómo implementarías rate limiting para dificultar este tipo de ataque?**

- **Limitar peticiones por IP/sesión y por endpoint** (por ejemplo, con `Flask-Limiter`): un límite razonable como "10 peticiones por minuto" a `/perfil/<id>` haría que extraer una contraseña de 12 caracteres pasara de tomar segundos a tomar horas, y generaría una ventana enorme para detectar el ataque.
- **Delay incremental / backoff** ante respuestas repetidas de "no existe" desde el mismo origen, para penalizar intentos fallidos consecutivos.
- **CAPTCHA o autenticación adicional** en endpoints sensibles tras un número de intentos sospechosos.
- **Bloqueo temporal (throttling) o baneo automático de IP** cuando se detecta un patrón de fuerza bruta (muchas peticiones casi idénticas variando solo un parámetro).
- Complementariamente (no sustituye al rate limiting, pero refuerza la defensa en profundidad): **WAF** con reglas para detectar patrones típicos de SQLi (`UNION`, `SUBSTR`, `CASE WHEN`, comillas simples, `--`) y, sobre todo, **corregir la causa raíz** con prepared statements — el rate limiting solo dificulta la explotación, no la elimina.

---

## Conclusiones generales

1. La causa común de las tres familias de vulnerabilidades (SQLi clásico, UNION-based y Command Injection) es la **concatenación de input de usuario dentro de código ejecutable**. La solución universal es separar siempre datos de código: **prepared statements/consultas parametrizadas** para SQL, y **listas de argumentos sin `shell=True`** para comandos del sistema.
2. La **validación de entrada** (whitelisting de formato, longitud, tipo) es una capa de defensa adicional que reduce la superficie de ataque incluso antes de llegar a la capa de datos, pero **no reemplaza** a las consultas parametrizadas — ambas controles deben aplicarse juntas (defensa en profundidad).
3. Los ataques "ciegos" (Blind SQLi) demuestran que **no mostrar mensajes de error no es suficiente** para proteger una aplicación: basta con un canal de observación indirecto (en este caso, un campo booleano `existe`) para que un atacante automatizado extraiga datos completos de la base de datos, con suficiente tiempo y peticiones.
4. El **rate limiting** y el monitoreo de logs son controles complementarios importantes, pero la única mitigación real y definitiva contra la inyección es escribir el código de forma segura desde el diseño (prepared statements, validación estricta, principio de menor privilegio en la ejecución de comandos del sistema).
