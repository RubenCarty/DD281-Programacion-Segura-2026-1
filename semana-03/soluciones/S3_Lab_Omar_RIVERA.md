# S3 — GUÍA DE TRABAJO DEL ESTUDIANTE
## Autenticación, Gestión de Cookies y Niveles de Acceso

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) — Semana 3 |
| **Nombre del estudiante** | Omar Rivera Castillo |
| **Código** ||
| **Fecha de entrega** |15/06/2026 |
| **Tiempo estimado** | 1.5 horas |
| **Puntaje total** | 100 puntos |

---

**Instrucciones generales:**
- Trabaja de forma individual y sin consultar respuestas de otros compañeros
- Responde con tus propias palabras — las respuestas copiadas se anulan
- Las secciones A y B se desarrollan en este documento
- Las secciones C y D requieren respuestas en párrafos completos
- Entrega: plataforma del aula virtual en el formato indicado por el docente

---

## SECCIÓN A — OPCIÓN MÚLTIPLE (20 puntos — 2 pts c/u)

*Marca con una X la alternativa correcta. Una sola respuesta por pregunta.*

---

**Pregunta 1** *(Básica)*
HTTP es un protocolo "sin estado" (stateless). Esto significa que:

- a) El servidor guarda automáticamente el estado de cada usuario entre peticiones
- b) Cada petición HTTP es independiente y el servidor no recuerda peticiones anteriores
- c) El cliente debe reenviar su contraseña en cada petición para identificarse
- d) Solo las peticiones POST mantienen el estado del usuario

**Respuesta: [  b ]**

---

**Pregunta 2** *(Básica)*
¿Cuál de los siguientes mecanismos es el MÁS SEGURO para almacenar el session ID de un usuario?

- a) `localStorage` del navegador
- b) `sessionStorage` del navegador
- c) Cookie con atributos `HttpOnly` y `Secure`
- d) Variable global de JavaScript en el cliente

**Respuesta: [ c  ]**

---

**Pregunta 3** *(Básica)*
El atributo `HttpOnly` en una cookie:

- a) Garantiza que la cookie solo se transmita por HTTPS
- b) Impide que JavaScript del navegador pueda leer el valor de la cookie
- c) Limita la cookie a peticiones del mismo dominio únicamente
- d) Establece la fecha de expiración automática de la cookie

**Respuesta: [ b  ]**

---

**Pregunta 4** *(Básica)*
El atributo `Secure` en una cookie garantiza que:

- a) La cookie no puede ser modificada por el usuario
- b) La cookie solo se transmite sobre conexiones HTTPS, nunca HTTP
- c) JavaScript no puede acceder al valor de la cookie
- d) La cookie expira automáticamente al cerrar el navegador

**Respuesta: [  b ]**

---

**Pregunta 5** *(Intermedia)*
Un desarrollador implementa el logout eliminando la cookie del navegador del usuario, pero no invalida el session ID en el servidor. ¿Cuál es el riesgo?

- a) El usuario tendrá que iniciar sesión dos veces la próxima vez
- b) Un atacante con una copia previa del session ID puede seguir usándolo para acceder al sistema
- c) La base de datos quedará con registros de sesión corruptos
- d) El servidor dejará de funcionar correctamente después del logout

**Respuesta: [ b  ]**

---

**Pregunta 6** *(Intermedia)*
¿Qué ataque específico previene el atributo `SameSite=Strict` en una cookie?

- a) SQL Injection en formularios de autenticación
- b) XSS (Cross-Site Scripting) en páginas dinámicas
- c) CSRF (Cross-Site Request Forgery) desde dominios externos
- d) Brute force en el formulario de login

**Respuesta: [  c ]**

---

**Pregunta 7** *(Intermedia)*
En el ataque Session Fixation, el atacante:

- a) Adivina el session ID del usuario usando fuerza bruta
- b) Fuerza al usuario a utilizar un session ID ya conocido por el atacante antes de autenticarse
- c) Inyecta código JavaScript para robar la cookie del usuario
- d) Intercepta el tráfico de red para capturar el session ID

**Respuesta: [ b  ]**

---

**Pregunta 8** *(Avanzada)*
En RBAC (Role-Based Access Control), el Principio de Mínimo Privilegio establece que:

- a) Los administradores deben tener acceso a todos los recursos para gestionar el sistema
- b) Cada usuario debe tener únicamente los permisos estrictamente necesarios para su función
- c) Los permisos se asignan individualmente a cada usuario según su antigüedad
- d) Los roles deben definirse con el máximo de permisos posibles para no limitar la productividad

**Respuesta: [ b  ]**

---

**Pregunta 9** *(Avanzada)*
Un sistema lee el rol del usuario desde el campo oculto del formulario HTML: `<input type="hidden" name="role" value="usuario">`. ¿Cuál es la vulnerabilidad?

- a) Inyección SQL, porque el campo contiene texto sin parametrizar
- b) Parameter tampering — el usuario puede editar el campo con DevTools y darse el rol "admin"
- c) CSRF, porque el formulario puede ser enviado desde otro dominio
- d) Session Fixation, porque el role está en el cliente antes de la autenticación

**Respuesta: [  b ]**

---

**Pregunta 10** *(Avanzada)*
Un navegador moderno recibe `Set-Cookie: session=abc; SameSite=None` sin el atributo `Secure`. ¿Qué ocurre?

- a) El navegador acepta la cookie y la envía en todas las peticiones
- b) El navegador rechaza y descarta la cookie automáticamente
- c) El navegador convierte la cookie a SameSite=Lax automáticamente
- d) La cookie funciona normalmente pero genera una advertencia en la consola

**Respuesta: [ b  ]**

---

## SECCIÓN B — COMPLETAR Y RELACIONAR (20 puntos)

### B1 — Completar espacios en blanco (10 puntos — 2 pts c/u)

Usa las palabras del banco: `HttpOnly` / `session.clear()` / `servidor` / `Secure` / `RBAC` / `SameSite` / `session_id` / `stateless`

1. HTTP es un protocolo stateless porque no recuerda peticiones anteriores entre cliente y servidor.

2. El atributo Secure garantiza que la cookie de sesión no sea transmitida sobre conexiones HTTP no cifradas.

3. El modelo de control de acceso RBAC asigna permisos a través de roles, no directamente a usuarios individuales.

4. En un logout correcto, además de eliminar la cookie del cliente, el servidor debe invalidar el session ID en su propio almacén.

5. Para prevenir Session Fixation, después de una autenticación exitosa se debe ejecutar session.clear() para limpiar la sesión previa.

---

### B2 — Relacionar columnas (10 puntos)

Relaciona cada atributo/concepto (columna A) con su descripción correcta (columna B).

| Columna A | | Columna B |
|---|---|---|
| 1. `HttpOnly` | C | a) Controla si la cookie se envía en peticiones cross-site |
| 2. `Secure` | F| b) El servidor no puede recordar peticiones anteriores |
| 3. `SameSite=Lax` | A| c) Previene que JavaScript lea el valor de la cookie |
| 4. Session Hijacking | E| d) El atacante forza un session ID conocido antes del login |
| 5. Session Fixation | H | e) Robo de un session ID válido para suplantar al usuario |
| 6. Stateless | B | f) La cookie solo viaja sobre conexiones HTTPS |
| 7. Mínimo Privilegio | D | g) Conjunto de permisos asignados a un tipo de usuario |
| 8. Rol | G | h) Cada usuario tiene solo los permisos que necesita |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN (30 puntos)

*Responde con párrafos completos de 3-5 líneas. No uses listas en esta sección.*

---

**Pregunta C1 (10 puntos)**
Un compañero propone guardar el session ID del usuario en `localStorage` porque "es más fácil acceder a él desde JavaScript". Explica por qué esta decisión es un riesgo de seguridad y cuál sería la alternativa correcta con sus fundamentos técnicos.

*Tu respuesta:*

Almacenar el session ID en localStorage expone la sesión a un robo inmediato si el sitio web llega a sufrir una vulnerabilidad de Cross-Site Scripting (XSS), ya que cualquier script malicioso inyectado puede leer este almacén mediante JavaScript de forma directa. La alternativa correcta y segura es almacenar el identificador dentro de una cookie gestionada por el servidor utilizando los atributos de protección avanzados. Al configurar la cookie con la directiva HttpOnly, el navegador bloquea por completo el acceso al valor desde la API de JavaScript, aislando el identificador de los ataques XSS.

---

**Pregunta C2 (10 puntos)**
Compara el ataque **Session Hijacking** con el ataque **Session Fixation**: en qué se diferencian en su mecánica, qué tienen en común en su objetivo final, y cuál es la medida técnica específica que previene cada uno.

*Tu respuesta:*

Ambos ataques comparten el mismo objetivo final, el cual consiste en suplantar la identidad de un usuario legítimo mediante la posesión de un identificador de sesión válido. Sin embargo, difieren en su mecánica: en el Session Hijacking el atacante roba una sesión activa que ya fue generada por el servidor, mientras que en el Session Fixation el atacante preestablece un identificador conocido en el navegador de la víctima antes de que esta inicie sesión.

---

**Mini caso de análisis — Para preguntas C3a y C3b**

> El equipo de desarrollo de **RetailFácil** (una tienda online peruana) implementó el siguiente sistema de autenticación:
>
> - Al hacer login, el servidor crea una cookie: `Set-Cookie: uid=456; role=comprador; Path=/`
> - Los precios se envían como campos ocultos en el formulario: `<input type="hidden" name="precio" value="299.00">`
> - Al hacer clic en "pagar", el backend lee `request.form['precio']` y procesa ese valor como el precio real
> - La sesión no tiene tiempo de expiración configurado

**Pregunta C3a (5 puntos)**
Identifica los problemas de seguridad presentes en el diseño de RetailFácil y explica cómo cada uno podría ser explotado por un atacante.

*Tu respuesta:*

El diseño expone tres fallas críticas de seguridad: el almacenamiento del ID de usuario y rol en texto plano dentro de la cookie (uid=456; role=comprador) permite que el cliente altere los valores mediante herramientas de desarrollador para suplantar identidades o escalar privilegios a administrador de forma directa. Asimismo, enviar los precios en campos ocultos del formulario permite ataques de manipulación de parámetros (Parameter Tampering), donde un comprador malicioso modifica el valor de 299.00 a 1.00 antes de enviar la petición de pago. Finalmente, la falta de expiración de sesión permite que un identificador robado mantenga su validez de forma indefinida en el tiempo.


**Pregunta C3b (5 puntos)**
Propón cómo debería reimplementarse este sistema de manera segura, explicando el principio de seguridad que aplica en cada corrección.

*Tu respuesta:*

Para corregir el sistema, la cookie debe almacenar únicamente un identificador de sesión criptográfico, aleatorio y opaco, delegando la consulta del ID de usuario y sus roles al lado del servidor mediante una base de datos para cumplir con el principio de control de acceso centralizado. El precio del producto jamás debe ser enviado ni procesado desde el cliente; el backend debe tomar el ID del producto y consultar el precio oficial en la base de datos interna, aplicando el principio de desconfianza hacia la entrada del usuario. Finalmente, se debe configurar una expiración estricta y absoluta (máximo 15-30 minutos) junto con los atributos HttpOnly, Secure y SameSite=Strict.

---

## SECCIÓN D — PREGUNTAS AVANZADAS Y DE CASO (30 puntos)

---

### Caso profesional (15 puntos)

> **SaludNet Perú** es una startup de telemedicina que permite a pacientes ver sus resultados de laboratorio y a médicos acceder a historias clínicas. El sistema usa una cookie de sesión sin `HttpOnly` ni `Secure`. El sistema tiene tres tipos de usuarios: paciente, médico y administrador.
>
> Un auditor de seguridad detectó que un médico puede acceder a la historia clínica de cualquier paciente simplemente cambiando el parámetro en la URL: `/historia?paciente_id=1023` → `/historia?paciente_id=1024`. También encontró que la cookie de sesión puede leerse con JavaScript y que el sistema funciona sobre HTTP sin redirigir a HTTPS.

**Pregunta D1 (5 puntos)**
¿Qué vulnerabilidades del OWASP Top 10 están presentes en SaludNet Perú? Nómbralas por su código y nombre, y explica brevemente cómo se manifiesta cada una en el caso.

*Tu respuesta:*

1. A01:2021-Broken Access Control (Control de Acceso Vulnerado): Manifestado como una vulnerabilidad BFLA/IDOR, donde un médico puede saltar las restricciones de aislamiento y consultar registros ajenos modificando el ID en la URL.

2. A02:2021-Cryptographic Failures (Fallas Criptográficas): Evidenciado al transmitir información médica confidencial y tokens sobre el protocolo inseguro HTTP, permitiendo ataques de interceptación de datos en tránsito.

3. A04:2021-Insecure Design (Diseño Inseguro): Reflejado en la carencia de atributos de seguridad esenciales en las cookies de sesión (HttpOnly y Secure), dejando expuestas las credenciales ante scripts maliciosos.

**Pregunta D2 (5 puntos)**
Diseña el esquema RBAC completo para SaludNet Perú: define los roles necesarios y los permisos específicos de cada uno. Luego escribe el pseudocódigo o código Python del decorador que verificaría el acceso antes de mostrar una historia clínica.

*Tu respuesta:*

Tabla de Roles y PermisosRolDescripciónPermisos EspecíficosmedicoPersonal médico tratante.ver_hce, crear_hce, editar_hce, recetar_medicamentosenfermeroPersonal de enfermería.ver_hce, registrar_signos_vitalesadmisionPersonal administrativo de la clínica/hospital.crear_paciente, ver_datos_demograficos (No ve historial médico)auditorPersonal de control de calidad o legal.ver_hce (Solo lectura de registros cerrados)pacienteEl dueño de la información.ver_propia_hce
from functools import wraps

# ==========================================
# 1. DEFINICIÓN DEL SISTEMA RBAC (Matriz)
# ==========================================
ROLES_PERMISOS = {
    "medico": ["ver_hce", "crear_hce", "editar_hce", "recetar_medicamentos"],
    "enfermero": ["ver_hce", "registrar_signos_vitales"],
    "admision": ["crear_paciente", "ver_datos_demograficos"],
    "auditor": ["ver_hce"],
    "paciente": ["ver_propia_hce"]
}

# Base de datos simulada de usuarios en SaludNet Perú
USUARIOS_DB = {
    "dr_perez": {"rol": "medico", "nombre": "Dr. Carlos Pérez"},
    "lic_ramos": {"rol": "enfermero", "nombre": "Lic. Ana Ramos"},
    "juan_adm": {"rol": "admision", "nombre": "Juan Gómez"},
    "auditor_minsa": {"rol": "auditor", "nombre": "Dra. Elva Loli"}
}

# Variable global simulada para el usuario que inició sesión
usuario_actual = None


# ==========================================
# 2. EL DECORADOR DE VERIFICACIÓN DE ACCESO
# ==========================================
def requiere_permiso(permiso_requerido):
    """
    Decorador para verificar si el usuario actual tiene el permiso
    necesario en el esquema RBAC antes de ejecutar la función.
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global usuario_actual
            
            # Verificar si hay un usuario autenticado
            if not usuario_actual or usuario_actual not in USUARIOS_DB:
                print(#bba0a0
                    f"❌ [ACCESO DENEGADO]: Debe iniciar sesión para realizar esta acción."
                )
                return None
            
            # Obtener el rol del usuario
            info_usuario = USUARIOS_DB[usuario_actual]
            rol_usuario = info_usuario["rol"]
            
            # Verificar si el rol contiene el permiso requerido
            permisos_del_rol = ROLES_PERMISOS.get(rol_usuario, [])
            
            if permiso_requerido in permisos_del_rol:
                # Si tiene permiso, se ejecuta la función original
                return func(*args, **kwargs)
            else:
                # Si no tiene permiso, se bloquea el acceso
                print(
                    f"❌ [ACCESO DENEGADO]: El usuario '{info_usuario['nombre']}' "
                    f"con rol '{rol_usuario}' no tiene el permiso '{permiso_requerido}'."
                )
                return None
        return wrapper
    return decorador


# ==========================================
# 3. FUNCIONES PROTEGIDAS (ENDPOINTS)
# ==========================================
@requiere_permiso("ver_hce")
def mostrar_historia_clinica(id_paciente):
    """Simula la visualización de una Historia Clínica Electrónica."""
    print(f"🔓 [ACCESO CONCEDIDO]: Mostrando HCE del Paciente ID: {id_paciente}")
    print(f"   📋 Datos Médicos: Diagnóstico CIE-10, Tratamiento, Alergias.")


# ==========================================
# 4. PRUEBAS DE CONCEPTO (Simulación)
# ==========================================
def simular_sistema():
    global usuario_actual
    
    print("--- SIMULACIÓN DE CONTROL DE ACCESO SALUDNET PERÚ --- \n")
    
    # Caso 1: Intento de acceso sin haber iniciado sesión
    print("Caso 1: Usuario anónimo intenta ver una HCE")
    usuario_actual = None
    mostrar_historia_clinica("PAC-4512")
    print("-" * 60)
    
    # Caso 2: Médico intenta ver la historia clínica (Debe permitir)
    print("Caso 2: Médico intenta ver una HCE")
    usuario_actual = "dr_perez"
    mostrar_historia_clinica("PAC-4512")
    print("-" * 60)
    
    # Caso 3: Personal de Admisión intenta ver la historia clínica (Debe denegar)
    print("Caso 3: Personal de Admisión intenta ver una HCE")
    usuario_actual = "juan_adm"
    mostrar_historia_clinica("PAC-4512")
    print("-" * 60)

    # Caso 4: Auditor de MINSA intenta ver la historia clínica (Debe permitir)
    print("Caso 4: Auditor intenta ver una HCE")
    usuario_actual = "auditor_minsa"
    mostrar_historia_clinica("PAC-4512")
    print("-" * 60)

# Ejecutar la simulación
simular_sistema()

**Pregunta D3 (5 puntos)**
Si un médico puede leer la cookie de sesión de un paciente mediante una vulnerabilidad XSS, ¿cómo puede un atacante usar esa cookie para acceder al sistema como ese paciente? Describe el ataque paso a paso y qué atributo de cookie lo hubiera prevenido.

*Tu respuesta:*

A) Inyección: El atacante logra inyectar un script malicioso (JavaScript) en el sistema de SaludNet Perú a través de un campo vulnerable a Cross-Site Scripting (XSS), como por ejemplo, el campo de "Observaciones" o "Notas médicas" de la HCE.

B) Ejecución: Cuando un médico legítimo abre la historia clínica del paciente afectado, su navegador web ejecuta automáticamente el script inyectado sin saber que es malicioso.

C) Extracción y Envío: El script accede al almacenamiento de cookies del navegador mediante la propiedad document.cookie. Acto seguido, envía el valor de la cookie de sesión del médico a un servidor controlado por el atacante (usando fetch() o cargando una imagen oculta con la URL del atacante).

D) Suplantación (Session Hijacking): El atacante recibe la cookie de sesión del médico en su servidor. Luego, configura esa misma cookie en su propio navegador web y recarga la página de SaludNet Perú. Al presentar un identificador de sesión válido, el servidor central lo reconoce como el médico autenticado, dándole acceso total a sus permisos RBAC sin necesidad de conocer su contraseña.

---

**Pregunta D4 — Diseño y propuesta (8 puntos)**
> "¿Cómo implementarías la gestión de sesiones para un sistema bancario en Flask que debe cumplir estos requisitos: sesión que expira a los 15 minutos de inactividad, cookie segura contra XSS y CSRF, logout que invalide la sesión en el servidor, y RBAC con roles cliente/operador/admin?"

Escribe el código Python/Flask completo que implementa esa gestión. Comenta cada decisión de seguridad.

*Tu código:*

```python
# Tu implementación aquí




```

---

**Pregunta D5 — Pensamiento crítico (7 puntos)**
> "¿Qué pasaría si un sistema implementa HttpOnly y Secure en las cookies, pero guarda el session ID con baja entropía (ej: un número secuencial como session_id=1001, 1002, 1003...)?"

Explica el tipo de ataque que esto habilitaría, cómo lo ejecutaría un atacante, y cuál es el estándar correcto para generar session IDs seguros.

*Tu respuesta:*

_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________

---

*Universidad Autónoma del Perú — DD281 Programación Segura — Semana 3 — 2026-1*