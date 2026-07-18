# GUÍA DE TRABAJO — ESTUDIANTE
# SEMANA 2: ESPECIFICACIÓN FORMAL DE SEGURIDAD Y LOGIN SEGURO

**Nombre del estudiante:** Javier Flores Condeña  
**Grupo / Sección:** GRUPO 1  
**Fecha:** 15/06/2026

---

# SECCIÓN A — RECUPERACIÓN DE APRENDIZAJES

## A.1 LA TRIADA CIA APLICADA AL LOGIN

| Pilar CIA | ¿Cómo se manifiesta en un sistema de login? | Ejemplo concreto |
|---|---|---|
| Confidencialidad | Protege credenciales y sesiones. | HTTPS + bcrypt. |
| Integridad | Evita modificaciones no autorizadas. | Validación y auditoría. |
| Disponibilidad | Garantiza acceso al servicio. | Alta disponibilidad y protección DoS. |

## A.2 OWASP TOP 10

| # | Vulnerabilidad | ¿Relacionada? | ¿Por qué? |
|---|---|---|---|
| A01 | Broken Access Control | Sí | Permite accesos indebidos. |
| A02 | Cryptographic Failures | Sí | Expone credenciales. |
| A03 | Injection | Sí | Permite bypass del login. |
| A04 | Insecure Design | Sí | Diseño inseguro del login. |
| A07 | Identification/Auth Failures | Sí | Falla directa de autenticación. |

## A.3 Mínimo privilegio

1. Usuarios con permisos mínimos.
2. Cuenta BD con privilegios limitados.
3. Roles separados para administración.

---

# SECCIÓN B — ACTIVIDAD DIAGNÓSTICA

## B.1 ¿Qué hace inseguro un login?

1. Contraseñas débiles.
2. Uso de HTTP.
3. Falta de MFA.
4. SQL Injection.
5. Contraseñas en texto plano.
6. Sin bloqueo por intentos.

## B.2 Respuestas

- B.2.1 → c
- B.2.2 → c
- B.2.3 → b

---

# SECCIÓN C — CONCEPTOS CLAVE

## C.1.1

Una especificación formal de seguridad es un conjunto de requisitos verificables que define cómo proteger un sistema mediante controles y mecanismos técnicos.

## C.1.2

| Ejemplo A | Ejemplo B |
|---|---|
| No es formal porque es ambiguo. | Es formal porque define controles medibles. |

## C.1.3

| Componente | ¿Qué define? |
|---|---|
| Activos | Información protegida. |
| Sujetos | Quién accede. |
| Objetos | Recursos protegidos. |
| Operaciones | Acciones permitidas. |
| Condiciones | Requisitos de acceso. |
| Mecanismos | Controles técnicos. |
| Respuesta ante violación | Acciones correctivas. |

## C.2 Respuestas

1. c
2. b
3. c
4. b
5. c
6. c
7. d
8. b
9. b
10. b

## C.3 Completar

- C.3.1 → hashing / unidireccional
- C.3.2 → aleatorio / único / tablas rainbow
- C.3.3 → PFS / pasado
- C.3.4 → entrada estándar / QUERY_STRING
- C.3.5 → 301
- C.3.6 → Mínimo Privilegio
- C.3.7 → autofirmado / pruebas / laboratorios / producción
- C.3.8 → identificación / autenticación

---

# SECCIÓN D — ANÁLISIS

## D.1 Código analizado

```python
#!/usr/bin/env python3
import cgi
import pymysql

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
user = form.getvalue("user")
pwd  = form.getvalue("pwd")

conn = pymysql.connect(host="db.empresa.com", user="admin",
                       password="Admin@2024!", database="empresa")
cursor = conn.cursor()
sql = f"SELECT * FROM empleados WHERE usuario='{user}' AND clave='{pwd}'"
cursor.execute(sql)
row = cursor.fetchone()

if row:
    print(f"<h1>Acceso concedido a: {user}</h1>")
    print(f"<p>Datos del empleado: {row}</p>")
else:
    print(f"<h1>Acceso denegado. Usuario: {user} no existe.</h1>")
conn.close()
```

### Vulnerabilidades

| # | Vulnerabilidad | Riesgo | Corrección |
|---|---|---|---|
| 1 | SQL Injection | Manipulación de consultas. | Queries parametrizadas. |
| 2 | Contraseñas en texto plano | Robo de credenciales. | bcrypt o Argon2id. |
| 3 | Credenciales hardcodeadas | Exposición de BD. | Variables de entorno. |
| 4 | Divulgación de información | Filtrado de datos. | Mensajes genéricos. |
| 5 | Sin validación de entradas | XSS e inyecciones. | Sanitización. |

## D.2 Política NIST

| Elemento | Correcto | ¿Por qué? |
|---|---|---|
| Exactamente 8 caracteres | No | Debe permitirse más longitud. |
| Cambio cada 30 días | No | Solo ante compromiso. |
| Historial de 3 passwords | Sí | Evita reutilización inmediata. |
| Complejidad obligatoria | No | NIST prioriza longitud. |

## D.3 Startup Fintech

### D.3.1

- ISO 27001
- NIST SP 800-63B
- OWASP ASVS

### D.3.2

| Componente | Especificación |
|---|---|
| Activos | Credenciales, sesiones, datos personales. |
| Sujetos | Cliente, operador, administrador. |
| Objetos | Portal, API y BD. |
| Operaciones | Login, logout, recuperación. |
| Condiciones | Credenciales válidas y MFA. |
| Mecanismos | TLS 1.3, bcrypt 12+, MFA. |
| Respuesta | Bloqueo, alertas y auditoría. |

### D.3.3

Bcrypt incorpora sal automática, factor de costo configurable y resistencia a ataques de fuerza bruta. MD5 y SHA-256 son demasiado rápidos para contraseñas. AES es cifrado reversible y no debe utilizarse para almacenar contraseñas.

## D.4 Caso Adobe

### D.4.1

Adobe almacenaba contraseñas usando cifrado reversible en lugar de hashing robusto.

### D.4.2

Las pistas de contraseña ayudaron a inferir las credenciales reales.

### D.4.3

Debió utilizar bcrypt o Argon2id con sal única por usuario.

---

# SECCIÓN E — ACTIVIDAD COLABORATIVA

## E.1 Especificación Formal


**Sistema asignado:** Portal de clientes Fintech

### Activos
- Credenciales
- Tokens de sesión
- Datos personales

### Sujetos
- Cliente
- Analista
- Administrador

### Objetos
- Portal web
- Base de datos

### Mecanismos técnicos

- Hash: bcrypt costo 12
- TLS: 1.3
- Longitud mínima: 12 caracteres
- Máximo intentos: 5
- Bloqueo: 15 minutos
- MFA: Sí (TOTP)

### Condiciones de acceso

- Usuario válido
- Contraseña correcta
- MFA aprobado

### Logging

- Intentos exitosos
- Intentos fallidos
- Bloqueos de cuenta

### Respuesta ante violación

- Bloqueo temporal
- Alerta SOC
- Registro de auditoría

## E.2 Justificación

| Decisión | Justificación |
|---|---|
| bcrypt | Resistencia a fuerza bruta. |
| TLS 1.3 | Mayor seguridad. |
| Bloqueo 5 intentos | Reduce ataques de diccionario. |
| MFA | Mitiga robo de credenciales. |

## E.3 CASO EXTREMO — ANÁLISIS GRUPAL
Respondan juntos: ¿Qué pasaría si un atacante obtiene acceso directo a la base de datos de su sistema (sin pasar por el login)? ¿Qué información podría obtener y qué NO podría obtener con la especificación que diseñaron?

### Lo que podría obtener

- Hashes de contraseñas
- Datos almacenados

### Lo que el atacante NO PODRÍA obtener (gracias a su especificación):

- Contraseñas originales
- Sesiones activas protegidas

---

# SECCIÓN F — CIERRE Y METACOGNICIÓN
## F.1 LISTA REVISADA (Volvemos a la Sección B.1)
Vuelve a tu lista de la Sección B.1 (¿qué hace inseguro un login?). Ahora agrega todo lo que descubriste durante la clase:

Nuevas razones identificadas durante la clase:

7. SQL Injection
8. Falta de TLS
9. Sin MFA
10. Hash inseguro
11. Mensajes detallados
12. Ausencia de auditoría

## F.2 PREGUNTAS DE SÍNTESIS
Responde brevemente:

### F.2.1 ¿Cuál es la diferencia esencial entre hash y cifrado? ¿Por qué se usa hash para contraseñas?

El hash es un proceso unidireccional; el cifrado es reversible mediante una clave.

### F.2.2 ¿Qué hace bcrypt diferente a SHA-256 para resistir ataques de fuerza bruta?

Bcrypt es lento y configurable, dificultando la fuerza bruta.

### F.2.3 ¿Qué versión de TLS deben usar y por qué las anteriores están descartadas?

TLS 1.2 o 1.3 porque versiones anteriores presentan vulnerabilidades conocidas.

### F.2.4 ¿Cuál fue el error más crítico del código CGI inseguro que analizamos hoy?

La vulnerabilidad más crítica fue SQL Injection.

## F.3 METACOGNICIÓN PERSONAL (Solo para ti)
Responde honestamente. Nadie más verá estas respuestas:

### ¿Qué fue lo más sorprendente o revelador de la sesión de hoy?

Comprendí la importancia de proteger correctamente las contraseñas.

### F.3.2 ¿Qué concepto todavía no tienes completamente claro?

Necesito profundizar en PFS.

### F.3.3 ¿Qué error de seguridad en código hoy reconoces que podrías haber cometido (o has cometido) antes de esta clase?

Podría haber utilizado hashes rápidos como SHA-256 para contraseñas.

### F.3.4 ¿Cómo cambiaría tu forma de implementar un login después de esta sesión?
Implementaría MFA, TLS 1.3 y bcrypt desde el inicio.

## F.4 Auditoría

**Sistema auditado:** Microsoft 365

| Criterio | Resultado | Herramienta |
|---|---|---|
| Usa HTTPS? | Sí | Navegador |
| ¿Qué versión de TLS usa? | 1.3 | SSL Labs |
| ¿Calificación SSL Labs? | A | SSL Labs |
| POST/GET | POST | Inspección |
| Bloqueo | Sí | Manual |
| MFA | Sí | Portal |
| Error genérico | Sí | Manual |

### Observación

El sistema implementa múltiples controles de autenticación.

### Recomendación

Mantener MFA obligatorio para todos los usuarios.
