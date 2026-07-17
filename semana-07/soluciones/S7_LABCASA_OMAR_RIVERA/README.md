# Lab Casa — Semana 7: CSRF, Exposición de Datos Sensibles y Controles de Acceso
**Programación Segura DD281 — Universidad Autónoma del Perú**

---

## Estructura del laboratorio

```
semana-07/lab-casa/
├── app_vulnerable.py       — Código original con análisis de vulnerabilidades en comentarios
├── ataque_csrf.html        — Archivo del atacante CSRF (Tarea 1.2), comentado línea a línea
├── app_segura.py           — Implementación segura con los 13 TODOs completados (Tarea 2.1)
├── app_double_submit.py    — Patrón Double Submit Cookie (Tarea 3.1)
├── .env.example            — Plantilla para crear tu .env local
├── .env                    — (NO subir — en .gitignore) Contiene SECRET_KEY real
├── .gitignore              — Excluye .env, __pycache__, etc.
├── pruebas_seguridad.md    — Evidencia de los 3 ataques rechazados (Tarea 2.2)
└── investigacion.md        — Flask-WTF, Argon2 vs bcrypt, flask-limiter (Tarea 3.2)
```

---

## Configuración rápida

### 1. Instalar dependencias
```bash
pip install flask flask-wtf bcrypt python-dotenv argon2-cffi flask-limiter
```

### 2. Crear el archivo `.env`
```bash
# Generar una clave secreta aleatoria
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
```
> ⚠️ El archivo `.env` está en `.gitignore` — nunca se sube a GitHub.

### 3. Ejecutar la aplicación vulnerable (puerto 5003)
```bash
python app_vulnerable.py
```

### 4. Ejecutar la aplicación segura (puerto 5004)
```bash
python app_segura.py
```

### 5. Ejecutar el Double Submit Cookie (puerto 5005)
```bash
python app_double_submit.py
```

---

## Tarea 1.1 — Tabla de vulnerabilidades

| Línea/Función | Vulnerabilidad | OWASP | Riesgo | ¿Cómo se explota? |
|---|---|---|---|---|
| `app.secret_key = "tienda2024"` | Clave secreta hardcodeada y débil | A05 - Security Misconfiguration | ALTO | El atacante lee el código fuente, forja cookies de sesión |
| Configuración global (sin SameSite/HttpOnly) | Cookies sin protección | A05 - Security Misconfiguration | ALTO | Cookie accesible por JavaScript (XSS) y enviada cross-site (CSRF) |
| `hashlib.md5(password.encode())` (línea 62) | MD5 para contraseñas — sin salt | A02 - Cryptographic Failures | CRÍTICO | CrackStation crackea ambos hashes en <1 segundo con tablas rainbow |
| `f"SELECT * FROM usuarios WHERE username='{username}'"` (línea 65) | SQL Injection en login | A03 - Injection | CRÍTICO | Username = `' OR '1'='1'--` → acceso sin contraseña |
| `# Sin CSRF token` (línea 82) | Sin protección CSRF en /comprar | A01 - Broken Access Control | ALTO | evil.com fuerza un POST con la cookie de la víctima → compra no autorizada |
| `f"UPDATE usuarios SET saldo=saldo-{monto}"` (línea 87) | SQL Injection en comprar | A03 - Injection | ALTO | Campo monto o producto con SQL malicioso manipula la BD |
| `/admin/pedidos` sin verificación de rol | Broken Access Control / sin RBAC | A01 - Broken Access Control | ALTO | Cualquier usuario autenticado (cliente) ve todos los pedidos del admin |
| `'21232f297a57a5a743894a0e4a801fc3'` en datos | Datos sensibles expuestos (MD5 reversible) | A02 - Cryptographic Failures | CRÍTICO | Hash MD5 en código fuente → contraseñas reales visibles en tablas rainbow |

---

## Tarea 1.3 — Contraseñas MD5 crackeadas

Resultados de CrackStation (https://crackstation.net):

| Hash MD5 | Contraseña real |
|----------|----------------|
| `21232f297a57a5a743894a0e4a801fc3` | **admin** |
| `5f4dcc3b5aa765d61d8327deb882cf99` | **password** |

**Tiempo:** Menos de 1 segundo — encontradas por coincidencia en tablas rainbow precomputadas.

**Reflexión:** MD5 fue diseñado para verificar integridad de archivos, no para almacenar contraseñas. Una GPU RTX 4090 puede calcular ~164,000 millones de hashes MD5 por segundo. Para una contraseña de 8 caracteres con letras y números (62^8 ≈ 218 billones de combinaciones), tardaría solo ~22 minutos en fuerza bruta. Con tablas rainbow, contraseñas comunes se encuentran en millisegundos. bcrypt con rounds=12 tarda ~250ms por intento → con la misma GPU, 8 caracteres tomarían siglos.

---

## Tarea 2.3 — Reflexión Final: Defensa en Profundidad

¿Por qué un sistema de pagos necesita las 3 protecciones simultáneamente?

Cada protección defiende un vector de ataque distinto. Eliminar cualquiera de las tres deja expuesta una ruta de compromiso completa, incluso si las otras dos funcionan perfectamente.

**Escenario A — CSRF + bcrypt, sin RBAC:**
Maria se autentica correctamente con bcrypt y su sesión tiene un CSRF token válido. Sin embargo, cualquier usuario autenticado puede acceder a `/admin/pedidos`. Un cliente registrado simplemente inicia sesión con su propia cuenta (legítima, bcrypt verifica bien), y accede directamente a los datos de todos los pedidos sin necesitar robar la sesión de nadie. El atacante no necesita CSRF ni crackear contraseñas: su propia sesión legítima le da acceso a datos de otros usuarios. Una brecha de confidencialidad total.

**Escenario B — CSRF + RBAC, sin bcrypt:**
Los tokens CSRF funcionan y los roles están bien implementados. Pero las contraseñas están almacenadas en MD5. Un atacante que obtiene un volcado de la base de datos (por SQL injection en otra ruta, o un backup expuesto) crackea todas las contraseñas en minutos con CrackStation o una GPU. Ahora tiene credenciales reales de admin y cliente. Hace login legítimo como admin, pasa el CSRF token correctamente, y tiene acceso total al sistema. El RBAC y CSRF no sirven de nada si las credenciales están comprometidas.

**Escenario C — bcrypt + RBAC, sin CSRF:**
Las contraseñas son inquebrantables y los roles están bien separados. Sin embargo, maria está autenticada en TiendaApp y visita evil.com. El sitio malicioso carga `ataque_csrf.html` que hace un POST automático a `/comprar`. El navegador envía la cookie de sesión de maria (porque no hay SameSite ni validación de token CSRF). TiendaApp verifica la cookie → sesión válida → descuenta S/. 500 del saldo de maria sin que ella haya hecho nada. bcrypt y RBAC no intervienen en este flujo.

**Conclusión:** La defensa en profundidad reconoce que ningún control de seguridad es infalible. Implementar múltiples capas independientes garantiza que comprometer una sola capa no sea suficiente para vulnerar el sistema completo — un atacante debe superar simultáneamente CSRF tokens, contraseñas bcrypt Y control de roles para tener éxito.
