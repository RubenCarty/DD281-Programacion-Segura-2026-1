# Investigación — Herramientas de Seguridad en Flask
**Programación Segura DD281 — Semana 7 — Tarea 3.2**

---

## Pregunta 1 — Flask-WTF

### ¿Qué es Flask-WTF y cómo protege contra CSRF con 3 líneas de código?

**Flask-WTF** es una extensión de Flask que integra WTForms (librería de validación de formularios) con protección CSRF automática. Su principal ventaja frente a la implementación manual es que genera, almacena y valida el token CSRF de forma transparente sin que el desarrollador tenga que escribir esa lógica en cada endpoint.

### Ejemplo mínimo con protección CSRF activada:

```python
# Instalación: pip install flask-wtf
from flask import Flask, render_template_string
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect  # Línea 1: importar CSRFProtect
from wtforms import StringField, FloatField, SubmitField

app = Flask(__name__)
app.secret_key = "clave-secreta-aqui"

# Línea 2: inicializar la protección CSRF global para TODA la aplicación
csrf = CSRFProtect(app)

class CompraForm(FlaskForm):
    producto = StringField('Producto')
    monto    = FloatField('Monto')
    submit   = SubmitField('Comprar')

@app.route('/comprar', methods=['GET', 'POST'])
def comprar():
    form = CompraForm()
    if form.validate_on_submit():  # Línea 3: validate_on_submit() valida el CSRF automáticamente
        return f"Comprando {form.producto.data} por S/. {form.monto.data}"
    # El template debe incluir {{ form.hidden_tag() }} para generar el campo CSRF oculto
    template = '''
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.producto.label }} {{ form.producto() }}
        {{ form.monto.label }} {{ form.monto() }}
        {{ form.submit() }}
    </form>
    '''
    return render_template_string(template, form=form)
```

### ¿Cómo genera y valida el token internamente?

1. **Generación:** Al instanciar el formulario con `FlaskForm()`, Flask-WTF llama a `generate_csrf()` que usa `secrets.token_bytes(32)` para crear un token aleatorio. Este token se almacena en la sesión de Flask bajo la clave `'csrf_token'`.

2. **Inclusión en el formulario:** `{{ form.hidden_tag() }}` renderiza un campo `<input type="hidden" name="csrf_token" value="...">` con el token. En APIs JSON, se puede obtener con `{{ csrf_token() }}` en el template.

3. **Validación:** Al enviar el formulario, `validate_on_submit()` internamente llama a `validate_csrf(token)` que compara el token del formulario con el de la sesión usando `hmac.compare_digest()` — igual que nuestro `secrets.compare_digest()` manual.

4. **Firmado HMAC:** Flask-WTF no solo compara los tokens; los firma con HMAC usando la `SECRET_KEY`. Esto significa que aunque un atacante robe un token, no puede generar tokens válidos sin conocer la clave secreta.

### ¿Cuándo conviene usar Flask-WTF vs implementación manual?

| Caso | Recomendación |
|------|---------------|
| Aplicación Flask tradicional con formularios HTML | **Flask-WTF** — integración automática, menos código, validación de formularios incluida |
| API REST/JSON sin sesiones (stateless, tokens JWT) | **Implementación manual** o **Double Submit Cookie** — Flask-WTF está orientado a sesiones y formularios |
| Proyecto pequeño/educativo (como este lab) | **Manual** — permite entender qué hace la protección internamente |
| Aplicación en producción con formularios | **Flask-WTF** — auditado, mantenido, integrado con Flask-Login |

---

## Pregunta 2 — Argon2 vs bcrypt

### ¿Cuál es la diferencia técnica entre Argon2 y bcrypt para almacenar contraseñas?

Ambos son algoritmos de hashing diseñados específicamente para contraseñas — lentos por diseño para que la fuerza bruta sea inviable. La diferencia clave está en los **parámetros de configuración** y en la **resistencia a hardware especializado**.

### Parámetros que tiene Argon2 y bcrypt NO tiene:

| Parámetro | bcrypt | Argon2 | Explicación |
|-----------|--------|--------|-------------|
| `cost` / `rounds` | ✅ | ✅ (time_cost) | Iteraciones de la función (tiempo de CPU) |
| `memory_cost` | ❌ | ✅ | **RAM requerida en KB** — esta es la diferencia crítica |
| `parallelism` | ❌ | ✅ | Número de hilos paralelos permitidos |
| Salt automático | ✅ | ✅ | Ambos generan salt único por hash |

**El parámetro `memory_cost` es la ventaja principal de Argon2:**

bcrypt solo requiere ~4KB de RAM por hash. Esto significa que una GPU moderna con miles de núcleos puede calcular bcrypt en paralelo masivamente, reduciendo el tiempo efectivo de cracking.

Argon2 puede configurarse para requerir cientos de MB de RAM por hash (e.g., `memory_cost=65536` = 64MB). Una GPU con 8GB de VRAM solo puede ejecutar ~128 instancias paralelas, comparado con miles en bcrypt. Esto hace que el hardware especializado (ASIC, GPU farms) pierda su ventaja.

### Variantes de Argon2:

- **Argon2d:** Resistente a GPU/ASIC (acceso dependiente de datos). No recomendado si hay riesgo de side-channel attacks (timing attacks en el servidor).
- **Argon2i:** Resistente a side-channel attacks (acceso independiente de datos). Para entornos donde el servidor podría ser observado.
- **Argon2id:** **RECOMENDADO** — híbrido de d e i. Resistente a GPU Y a side-channel en la primera mitad del cómputo.

### ¿Cuál recomienda OWASP en su Password Storage Cheat Sheet de 2024?

OWASP recomienda el siguiente orden de preferencia (2024):

1. **Argon2id** — primera opción (parámetros mínimos: `m=19456` KB, `t=2`, `p=1`)
2. **scrypt** — segunda opción si Argon2 no está disponible
3. **bcrypt** — tercera opción (factor de costo mínimo: 10, recomendado 12+)
4. **PBKDF2** — solo si se necesita conformidad FIPS; con SHA-256 y 600,000+ iteraciones

MD5 y SHA-1/SHA-256 simples **no son aceptables** para contraseñas en ningún escenario de producción.

### ¿Cómo migrar de bcrypt a Argon2 sin forzar a todos los usuarios a cambiar su contraseña?

La migración se hace de forma **transparente en el login**, rehashing solo cuando el usuario se autentica exitosamente:

```python
# pip install argon2-cffi bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import bcrypt

ph = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)

def verificar_y_migrar(password: str, hash_almacenado: str, user_id: int, conn):
    """
    Verifica la contraseña con el algoritmo actual y migra a Argon2 si es bcrypt.
    Devuelve True si la contraseña es correcta, False si no.
    """
    # Detectar el algoritmo por el prefijo del hash
    if hash_almacenado.startswith('$2b$') or hash_almacenado.startswith('$2a$'):
        # Es un hash bcrypt — verificar con bcrypt
        es_valida = bcrypt.checkpw(password.encode(), hash_almacenado.encode())
        
        if es_valida:
            # ¡Login exitoso! Rehashear con Argon2 aprovechando que tenemos la contraseña en claro
            nuevo_hash = ph.hash(password)
            conn.execute(
                "UPDATE usuarios SET password_hash = ? WHERE id = ?",
                (nuevo_hash, user_id)
            )
            conn.commit()
            print(f"Usuario {user_id} migrado a Argon2id")
        
        return es_valida
    
    elif hash_almacenado.startswith('$argon2'):
        # Ya es Argon2 — verificar directamente
        try:
            ph.verify(hash_almacenado, password)
            # Opcional: rehash si los parámetros de Argon2 cambiaron
            if ph.check_needs_rehash(hash_almacenado):
                nuevo_hash = ph.hash(password)
                conn.execute("UPDATE usuarios SET password_hash = ? WHERE id = ?", (nuevo_hash, user_id))
                conn.commit()
            return True
        except VerifyMismatchError:
            return False
    
    else:
        raise ValueError(f"Algoritmo de hash desconocido: {hash_almacenado[:10]}")
```

**Resultado:** Los usuarios con hashes bcrypt migran automáticamente a Argon2 la próxima vez que hacen login. Los que no han iniciado sesión en meses aún tendrán bcrypt (que sigue siendo aceptable). Opcionalmente, se puede forzar a los usuarios inactivos a cambiar su contraseña tras un período definido.

---

## Pregunta 3 — flask-limiter

### ¿Qué es flask-limiter y cómo previene ataques de fuerza bruta en `/login`?

**flask-limiter** es una extensión de Flask que aplica rate limiting (limitación de tasa) a los endpoints de la aplicación. Permite definir cuántas peticiones puede hacer un cliente (identificado por IP u otro criterio) en un período de tiempo determinado.

Sin rate limiting, un atacante puede intentar millones de contraseñas contra `/login` automáticamente. flask-limiter añade una capa que detecta y bloquea este comportamiento.

### Ejemplo mínimo que limita el login a 5 intentos por IP por minuto:

```python
# pip install flask-limiter
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "mi-clave-secreta"

# Inicializar el limitador — usa la IP del cliente como clave por defecto
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],  # límites globales opcionales
    storage_uri="memory://"  # backend en memoria (solo para desarrollo)
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 intentos por IP por minuto
@limiter.limit("20 per hour")   # Y máximo 20 por hora (protección adicional)
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # ... verificación de credenciales ...
    return jsonify({"mensaje": "Login correcto"})

# Manejador personalizado para cuando se excede el límite
@app.errorhandler(429)
def ratelimit_exceeded(e):
    return jsonify({
        "error": "Demasiados intentos. Espera 1 minuto antes de intentar de nuevo.",
        "retry_after": e.description
    }), 429
```

### ¿Qué respuesta HTTP devuelve cuando se excede el límite?

**HTTP 429 Too Many Requests** — definido en RFC 6585.

Respuesta típica:
```
HTTP/1.1 429 TOO MANY REQUESTS
Content-Type: application/json
Retry-After: 60
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1721000060

{"error": "Demasiados intentos. Espera 1 minuto antes de intentar de nuevo."}
```

El header `Retry-After` indica cuántos segundos debe esperar el cliente antes de reintentar.

### ¿Qué backends de almacenamiento soporta flask-limiter?

| Backend | URI | Uso recomendado |
|---------|-----|-----------------|
| **Memoria** | `memory://` | Solo desarrollo — se reinicia con la app, no comparte estado entre workers |
| **Redis** | `redis://localhost:6379` | **Producción** — persistente, compartido entre múltiples workers/procesos |
| **Memcached** | `memcached://localhost:11211` | Alternativa a Redis, menor persistencia |
| **MongoDB** | `mongodb://localhost:27017` | Para proyectos que ya usan MongoDB |
| **Redis Cluster** | `redis+cluster://` | Producción de alta disponibilidad |

**Para producción siempre usar Redis** — con múltiples workers (Gunicorn, uWSGI), el backend en memoria no es compartido y cada worker tiene su propio contador independiente, permitiendo hasta `workers × 5` intentos en vez de 5.

### ¿Por qué limitar por IP no es suficiente en todos los casos?

**1. IPs compartidas / NAT:** Muchos usuarios en una oficina, universidad o red corporativa comparten la misma IP pública. Si un solo usuario malicioso de esa red consume el límite, bloquea a todos los demás.

**2. Botnets y proxies:** Un atacante con acceso a una botnet de miles de dispositivos comprometidos puede distribuir los intentos — 1 intento por IP — evitando el límite por IP completamente. Cada nodo de la botnet tiene su propia IP.

**3. IPv6 y rangos de IP:** Los usuarios de IPv6 pueden tener millones de IPs disponibles en su prefijo /64. El limitador por IP exacta no cubre este caso.

**Soluciones complementarias:**

- **Limitar también por username:** si el username "admin" recibe 5 intentos fallidos en 1 minuto (desde cualquier IP), bloquearlo temporalmente. Esto detiene botnets.
- **CAPTCHA progresivo:** activar CAPTCHA tras 3 intentos fallidos, independientemente de la IP.
- **Alertas por comportamiento anómalo:** detectar patrones como muchos usernames diferentes desde la misma IP (password spray attack).
- **Autenticación multifactor (MFA):** incluso si la contraseña es crackeada, el atacante no puede completar el login sin el segundo factor.
- **Bloqueo temporal de cuenta:** bloquear la cuenta por 15 minutos tras N intentos fallidos (con precaución — puede ser usado para DoS contra usuarios legítimos).
