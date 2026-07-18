# S3 - GUIA DE TRABAJO DEL ESTUDIANTE
## Autenticacion, Gestion de Cookies y Niveles de Acceso

| Campo | Detalle |
|---|---|
| **Curso** | Programacion Segura (DD281) - Semana 3 |
| **Nombre del estudiante** | Hidgar Orellano Huerta |
| **Codigo** | 2221892872 |
| **Seccion** | 6 |
| **Fecha de entrega** | 21/06/2026 |
| **Tiempo estimado** | 1.5 horas |
| **Puntaje total** | 100 puntos |

---

**Instrucciones generales:**
- Trabaja de forma individual y sin consultar respuestas de otros companeros
- Responde con tus propias palabras - las respuestas copiadas se anulan
- Las secciones A y B se desarrollan en este documento
- Las secciones C y D requieren respuestas en parrafos completos
- Entrega: plataforma del aula virtual en el formato indicado por el docente

---

## SECCION A - OPCION MULTIPLE (20 puntos - 2 pts c/u)

*Marca con una X la alternativa correcta. Una sola respuesta por pregunta.*

---

**Pregunta 1** *(Basica)*
HTTP es un protocolo "sin estado" (stateless). Esto significa que:

- [ ] a) El servidor guarda automaticamente el estado de cada usuario entre peticiones
- [X] b) Cada peticion HTTP es independiente y el servidor no recuerda peticiones anteriores
- [ ] c) El cliente debe reenviar su contrasena en cada peticion para identificarse
- [ ] d) Solo las peticiones POST mantienen el estado del usuario

**Respuesta:** b)

---

**Pregunta 2** *(Basica)*
Cual de los siguientes mecanismos es el MAS SEGURO para almacenar el session ID de un usuario?

- [ ] a) `localStorage` del navegador
- [ ] b) `sessionStorage` del navegador
- [X] c) Cookie con atributos `HttpOnly` y `Secure`
- [ ] d) Variable global de JavaScript en el cliente

**Respuesta:** c)

---

**Pregunta 3** *(Basica)*
El atributo `HttpOnly` en una cookie:

- [ ] a) Garantiza que la cookie solo se transmita por HTTPS
- [X] b) Impide que JavaScript del navegador pueda leer el valor de la cookie
- [ ] c) Limita la cookie a peticiones del mismo dominio unicamente
- [ ] d) Establece la fecha de expiracion automatica de la cookie

**Respuesta:** b)

---

**Pregunta 4** *(Basica)*
El atributo `Secure` en una cookie garantiza que:

- [ ] a) La cookie no puede ser modificada por el usuario
- [X] b) La cookie solo se transmite sobre conexiones HTTPS, nunca HTTP
- [ ] c) JavaScript no puede acceder al valor de la cookie
- [ ] d) La cookie expira automaticamente al cerrar el navegador

**Respuesta:** b)

---

**Pregunta 5** *(Intermedia)*
Un desarrollador implementa el logout eliminando la cookie del navegador del usuario, pero no invalida el session ID en el servidor. Cual es el riesgo?

- [ ] a) El usuario tendra que iniciar sesion dos veces la proxima vez
- [X] b) Un atacante con una copia previa del session ID puede seguir usandolo para acceder al sistema
- [ ] c) La base de datos quedara con registros de sesion corruptos
- [ ] d) El servidor dejara de funcionar correctamente despues del logout

**Respuesta:** b)

---

**Pregunta 6** *(Intermedia)*
Que ataque especifico previene el atributo `SameSite=Strict` en una cookie?

- [ ] a) SQL Injection en formularios de autenticacion
- [ ] b) XSS (Cross-Site Scripting) en paginas dinamicas
- [X] c) CSRF (Cross-Site Request Forgery) desde dominios externos
- [ ] d) Brute force en el formulario de login

**Respuesta:** c)

---

**Pregunta 7** *(Intermedia)*
En el ataque Session Fixation, el atacante:

- [ ] a) Adivina el session ID del usuario usando fuerza bruta
- [X] b) Fuerza al usuario a utilizar un session ID ya conocido por el atacante antes de autenticarse
- [ ] c) Inyecta codigo JavaScript para robar la cookie del usuario
- [ ] d) Intercepta el trafico de red para capturar el session ID

**Respuesta:** b)

---

**Pregunta 8** *(Avanzada)*
En RBAC (Role-Based Access Control), el Principio de Minimo Privilegio establece que:

- [ ] a) Los administradores deben tener acceso a todos los recursos para gestionar el sistema
- [X] b) Cada usuario debe tener unicamente los permisos estrictamente necesarios para su funcion
- [ ] c) Los permisos se asignan individualmente a cada usuario segun su antiguedad
- [ ] d) Los roles deben definirse con el maximo de permisos posibles para no limitar la productividad

**Respuesta:** b)

---

**Pregunta 9** *(Avanzada)*
Un sistema lee el rol del usuario desde el campo oculto del formulario HTML: `<input type="hidden" name="role" value="usuario">`. Cual es la vulnerabilidad?

- [ ] a) Inyeccion SQL, porque el campo contiene texto sin parametrizar
- [X] b) Parameter tampering - el usuario puede editar el campo con DevTools y darse el rol "admin"
- [ ] c) CSRF, porque el formulario puede ser enviado desde otro dominio
- [ ] d) Session Fixation, porque el role esta en el cliente antes de la autenticacion

**Respuesta:** b)

---

**Pregunta 10** *(Avanzada)*
Un navegador moderno recibe `Set-Cookie: session=abc; SameSite=None` sin el atributo `Secure`. Que ocurre?

- [ ] a) El navegador acepta la cookie y la envia en todas las peticiones
- [X] b) El navegador rechaza y descarta la cookie automaticamente
- [ ] c) El navegador convierte la cookie a SameSite=Lax automaticamente
- [ ] d) La cookie funciona normalmente pero genera una advertencia en la consola

**Respuesta:** b)

---

## SECCION B - COMPLETAR Y RELACIONAR (20 puntos)

### B1 - Completar espacios en blanco (10 puntos - 2 pts c/u)

Usa las palabras del banco: `HttpOnly` / `session.clear()` / `servidor` / `Secure` / `RBAC` / `SameSite` / `session_id` / `stateless`

1. HTTP es un protocolo _____**stateless**_____ porque no recuerda peticiones anteriores entre cliente y servidor.

2. El atributo _____**Secure**_____ garantiza que la cookie de sesion no sea transmitida sobre conexiones HTTP no cifradas.

3. El modelo de control de acceso _____**RBAC**_____ asigna permisos a traves de roles, no directamente a usuarios individuales.

4. En un logout correcto, ademas de eliminar la cookie del cliente, el _____**servidor**_____ debe invalidar el session ID en su propio almacen.

5. Para prevenir Session Fixation, despues de una autenticacion exitosa se debe ejecutar _____**session.clear()**_____ para limpiar la sesion previa.

---

### B2 - Relacionar columnas (10 puntos)

Relaciona cada atributo/concepto (columna A) con su descripcion correcta (columna B).

| Columna A | Respuesta | Columna B |
|---|---|---|
| 1. `HttpOnly` | __c__ | a) Controla si la cookie se envia en peticiones cross-site |
| 2. `Secure` | __f__ | b) El servidor no puede recordar peticiones anteriores |
| 3. `SameSite=Lax` | __a__ | c) Previene que JavaScript lea el valor de la cookie |
| 4. Session Hijacking | __e__ | d) El atacante forza un session ID conocido antes del login |
| 5. Session Fixation | __d__ | e) Robo de un session ID valido para suplantar al usuario |
| 6. Stateless | __b__ | f) La cookie solo viaja sobre conexiones HTTPS |
| 7. Minimo Privilegio | __h__ | g) Conjunto de permisos asignados a un tipo de usuario |
| 8. Rol | __g__ | h) Cada usuario tiene solo los permisos que necesita |

---

## SECCION C - ANALISIS Y REFLEXION (30 puntos)

*Responde con parrafos completos de 3-5 lineas. No uses listas en esta seccion.*

---

**Pregunta C1 (10 puntos)**
Un companero propone guardar el session ID del usuario en `localStorage` porque "es mas facil acceder a el desde JavaScript". Explica por que esta decision es un riesgo de seguridad y cual seria la alternativa correcta con sus fundamentos tecnicos.

*Tu respuesta:*

Guardar el session ID en `localStorage` es riesgoso porque cualquier JavaScript ejecutado en la pagina podria leerlo. Si aparece una vulnerabilidad XSS, el atacante podria extraer ese valor y reutilizarlo para suplantar la sesion del usuario. La alternativa correcta es usar una cookie de sesion con `HttpOnly`, `Secure` y `SameSite`, porque reduce el acceso desde JavaScript, exige transporte seguro por HTTPS en produccion y limita el envio de cookies en solicitudes cross-site.

---

**Pregunta C2 (10 puntos)**
Compara el ataque **Session Hijacking** con el ataque **Session Fixation**: en que se diferencian en su mecanica, que tienen en comun en su objetivo final, y cual es la medida tecnica especifica que previene cada uno.

*Tu respuesta:*

Session Hijacking ocurre cuando el atacante roba o captura un session ID valido de un usuario que ya inicio sesion. Session Fixation ocurre antes del login, cuando el atacante intenta que la victima use un session ID conocido y luego se autentique con el. Ambos buscan suplantar al usuario dentro del sistema. Para reducir hijacking se usan HTTPS, `HttpOnly`, `Secure`, alta entropia y expiracion; para reducir fixation se debe regenerar o limpiar la sesion con `session.clear()` antes de guardar los datos del usuario autenticado.

---

**Mini caso de analisis - Para preguntas C3a y C3b**

> El equipo de desarrollo de **RetailFacil** (una tienda online peruana) implemento el siguiente sistema de autenticacion:
>
> - Al hacer login, el servidor crea una cookie: `Set-Cookie: uid=456; role=comprador; Path=/`
> - Los precios se envian como campos ocultos en el formulario: `<input type="hidden" name="precio" value="299.00">`
> - Al hacer clic en "pagar", el backend lee `request.form['precio']` y procesa ese valor como el precio real
> - La sesion no tiene tiempo de expiracion configurado

**Pregunta C3a (5 puntos)**
Identifica los problemas de seguridad presentes en el diseno de RetailFacil y explica como cada uno podria ser explotado por un atacante.

*Tu respuesta:*

RetailFacil confia en datos que estan en el cliente. El `uid` y el `role` viajan directamente en una cookie visible o manipulable, por lo que un atacante podria intentar modificar el rol. El precio tambien viene en un campo oculto, pero los campos ocultos se pueden cambiar con DevTools antes de enviar el formulario. Ademas, una sesion sin expiracion aumenta el riesgo si una cookie queda expuesta o se usa en una computadora compartida.

**Pregunta C3b (5 puntos)**
Propón como deberia reimplementarse este sistema de manera segura, explicando el principio de seguridad que aplica en cada correccion.

*Tu respuesta:*

El sistema debe guardar solo un identificador de sesion opaco y aleatorio en una cookie segura; los roles y permisos deben consultarse en el servidor. El precio debe calcularse en backend desde la base de datos usando el ID del producto, nunca desde un campo oculto enviado por el usuario. Tambien debe existir expiracion de sesion y logout que invalide el estado del servidor. Con esto se aplica minimo privilegio, validacion del lado servidor y el principio de no confiar en datos controlados por el cliente.

---

## SECCION D - PREGUNTAS AVANZADAS Y DE CASO (30 puntos)

---

### Caso profesional (15 puntos)

> **SaludNet Peru** es una startup de telemedicina que permite a pacientes ver sus resultados de laboratorio y a medicos acceder a historias clinicas. El sistema usa una cookie de sesion sin `HttpOnly` ni `Secure`. El sistema tiene tres tipos de usuarios: paciente, medico y administrador.
>
> Un auditor de seguridad detecto que un medico puede acceder a la historia clinica de cualquier paciente simplemente cambiando el parametro en la URL: `/historia?paciente_id=1023` -> `/historia?paciente_id=1024`. Tambien encontro que la cookie de sesion puede leerse con JavaScript y que el sistema funciona sobre HTTP sin redirigir a HTTPS.

**Pregunta D1 (5 puntos)**
Que vulnerabilidades del OWASP Top 10 estan presentes en SaludNet Peru? Nombralas por su codigo y nombre, y explica brevemente como se manifiesta cada una en el caso.

*Tu respuesta:*

En SaludNet Peru aparece A01:2021 Broken Access Control, porque un medico puede cambiar `paciente_id` en la URL y acceder a historias clinicas de pacientes que no necesariamente le corresponden. Tambien se observa A02:2021 Cryptographic Failures, porque el sistema funciona sobre HTTP y transmite informacion sensible sin cifrado en transito. Ademas, las cookies sin `HttpOnly` ni `Secure` reflejan una mala configuracion de seguridad que facilita robo de sesion si existe XSS o interceptacion de trafico.

**Pregunta D2 (5 puntos)**
Disena el esquema RBAC completo para SaludNet Peru: define los roles necesarios y los permisos especificos de cada uno. Luego escribe el pseudocodigo o codigo Python del decorador que verificaria el acceso antes de mostrar una historia clinica.

*Tu respuesta:*

Los roles necesarios son `paciente`, `medico` y `administrador`. El paciente solo puede ver su propia historia y resultados. El medico solo puede ver historias de pacientes asignados a su atencion. El administrador gestiona usuarios, roles y auditoria, y cualquier acceso especial debe quedar registrado.

```python
from functools import wraps
from flask import session, abort

PACIENTES_ASIGNADOS = {
    "medico_01": {"1023", "1024"},
}

def puede_ver_historia(user, paciente_id):
    if user["role"] == "administrador":
        return True
    if user["role"] == "paciente":
        return user["paciente_id"] == paciente_id
    if user["role"] == "medico":
        return paciente_id in PACIENTES_ASIGNADOS.get(user["id"], set())
    return False

def requiere_historia(f):
    @wraps(f)
    def wrapper(paciente_id, *args, **kwargs):
        user = session.get("user")
        if not user:
            abort(401)
        if not puede_ver_historia(user, paciente_id):
            abort(403)
        return f(paciente_id, *args, **kwargs)
    return wrapper
```

**Pregunta D3 (5 puntos)**
Si un medico puede leer la cookie de sesion de un paciente mediante una vulnerabilidad XSS, como puede un atacante usar esa cookie para acceder al sistema como ese paciente? Describe el ataque paso a paso y que atributo de cookie lo hubiera prevenido.

*Tu respuesta:*

Si existe XSS y la cookie no tiene `HttpOnly`, el atacante puede ejecutar JavaScript como `document.cookie` para leer el session ID del paciente. Luego copia ese valor y lo coloca en su navegador o en una herramienta HTTP como cookie de sesion. Si el servidor acepta esa cookie sin controles adicionales, el atacante queda autenticado como el paciente. El atributo que hubiera prevenido la lectura de la cookie desde JavaScript es `HttpOnly`; tambien se debe usar `Secure`, expiracion y rotacion de sesion.

---

**Pregunta D4 - Diseno y propuesta (8 puntos)**
> "Como implementarias la gestion de sesiones para un sistema bancario en Flask que debe cumplir estos requisitos: sesion que expira a los 15 minutos de inactividad, cookie segura contra XSS y CSRF, logout que invalide la sesion en el servidor, y RBAC con roles cliente/operador/admin?"

Escribe el codigo Python/Flask completo que implementa esa gestion. Comenta cada decision de seguridad.

*Tu codigo:*

```python
from datetime import timedelta
from functools import wraps
from flask import Flask, session, redirect, url_for, request, abort
import secrets

app = Flask(__name__)
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=15),
    SESSION_COOKIE_HTTPONLY=True,    # Protege la cookie contra lectura por JavaScript en XSS.
    SESSION_COOKIE_SECURE=True,      # En produccion obliga envio solo por HTTPS.
    SESSION_COOKIE_SAMESITE="Strict" # Reduce CSRF en operaciones sensibles.
)

USERS = {
    "cliente@test.com": {"password": "Cliente2026!", "role": "cliente"},
    "operador@test.com": {"password": "Operador2026!", "role": "operador"},
    "admin@test.com": {"password": "Admin2026!", "role": "admin"},
}

def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            session.permanent = True
            if session.get("role") not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.post("/login")
def login():
    email = request.form.get("email", "")
    user = USERS.get(email)
    if not user or user["password"] != request.form.get("password", ""):
        abort(401)
    session.clear()  # Evita Session Fixation.
    session["user_id"] = email
    session["role"] = user["role"]
    session.permanent = True
    return redirect(url_for("dashboard"))

@app.post("/logout")
def logout():
    session.clear()  # Invalida la sesion del lado servidor/framework.
    return redirect(url_for("login"))

@app.get("/cuentas")
@require_role("cliente", "operador", "admin")
def cuentas():
    return "Modulo de cuentas"

@app.get("/operaciones")
@require_role("operador", "admin")
def operaciones():
    return "Modulo de operaciones"

@app.get("/admin")
@require_role("admin")
def admin():
    return "Administracion bancaria"
```

---

**Pregunta D5 - Pensamiento critico (7 puntos)**
> "Que pasaria si un sistema implementa HttpOnly y Secure en las cookies, pero guarda el session ID con baja entropia (ej: un numero secuencial como session_id=1001, 1002, 1003...)?"

Explica el tipo de ataque que esto habilitaria, como lo ejecutaria un atacante, y cual es el estandar correcto para generar session IDs seguros.

*Tu respuesta:*

Aunque la cookie tenga `HttpOnly` y `Secure`, un session ID con baja entropia sigue siendo vulnerable porque puede adivinarse. Si los valores son secuenciales como `1001`, `1002` y `1003`, un atacante podria probar numeros cercanos hasta encontrar una sesion activa. Esto habilita session guessing o prediccion de sesiones. El estandar correcto es generar session IDs largos, aleatorios, no predecibles y con entropia criptografica, por ejemplo mediante generadores seguros como `secrets.token_urlsafe(32)` o el mecanismo seguro del framework.

---

*Universidad Autonoma del Peru - DD281 Programacion Segura - Semana 3 - 2026-1*
