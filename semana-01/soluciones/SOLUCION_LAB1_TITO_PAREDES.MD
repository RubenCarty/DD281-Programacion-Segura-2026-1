# UNIVERSIDAD AUTÓNOMA DEL PERÚ
**Facultad de Ingeniería y Arquitectura | Ingeniería de Sistemas**  
**Hoja de Trabajo - Programación Segura - Semana 1**  

* **Ciclo:** VIII  
* **Curso:** Programación Segura    
* **Estudiante:** Arian Alexey Ricardo Tito 
* **Docente:** Ruben Quispe Llacctarimay  

---

## Sección A: Completar la Frase

1. La **Autenticación** es el proceso de verificar la identidad de un usuario antes de permitirle el acceso a un sistema.
2. La **Integridad** garantiza que la información no sea modificada sin autorización por parte de personas no autorizadas.
3. La **Disponibilidad** asegura que los sistemas y datos estén disponibles para los usuarios autorizados en el momento en que los necesitan.
4. Una **Vulnerabilidad** es una debilidad en el diseño, implementación o configuración de un sistema que puede ser explotada por un atacante.
5. Una **Amenaza** es cualquier circunstancia o evento con el potencial de causar daño a un activo de información.
6. El **Riesgo** se define como la combinación de la probabilidad de que ocurra un evento adverso y el impacto resultante sobre los activos.
7. **OWASP** son las siglas de *Open Web Application Security Project*, una fundación sin fines de lucro que publica el Top 10 de vulnerabilidades web.
8. La **Autorización** define qué recursos o acciones puede ejecutar un usuario dentro del sistema una vez que ya ha sido autenticado.
9. Un **Activo** es cualquier recurso de valor para la organización, como datos, sistemas, infraestructura o personas.
10. El principio de **Mínimo Privilegio** establece que cada usuario debe tener únicamente los permisos necesarios para realizar su trabajo.
11. La **Seguridad por Diseño** de un sistema consiste en definir los requerimientos de seguridad desde las fases iniciales del desarrollo del software.
12. Un **Control de seguridad** es un mecanismo, proceso o tecnología implementado para reducir la probabilidad o el impacto de una amenaza o vulnerabilidad.
13. La **Ingeniería social** es una técnica de ataque que manipula a las personas para obtener información confidencial aprovechando su confianza.
14. El **No repudio** garantiza que las acciones realizadas en un sistema puedan atribuirse de forma inequívoca e irrefutable a quien las ejecutó.
15. El **Modelado** de amenazas es una técnica sistemática para identificar y priorizar posibles ataques contra un sistema antes de construirlo.
16. La criptografía **Asimétrica** utiliza un par de claves—una pública y una privada— para cifrar y descifrar información de forma segura.
17. Una función de **Hash** transforma datos de cualquier tamaño en una cadena de longitud fija, siendo un proceso matemáticamente irreversible.
18. En los **Casos de uso** seguros se documenta el flujo que el sistema debe seguir para proteger una funcionalidad frente a posibles ataques o abusos.
19. La autenticación **Multifactor** (MFA) combina dos o más factores de verificación para aumentar significativamente la seguridad del acceso.
20. El ciclo de vida de desarrollo seguro (**SDLC**) integra actividades y controles de seguridad en cada fase del proceso de construcción del software.

---

## Sección B: Relacionar Conceptos

| Concepto | Definición Correspondiente |
| :--- | :--- |
| **1. Amenaza** | s) Evento o circunstancia con potencial de causar daño a un activo. |
| **2. Vulnerabilidad** | j) Debilidad en un sistema que puede ser aprovechada por un atacante. |
| **3. Riesgo** | m) Combinación de probabilidad de ataque e impacto sobre los activos. |
| **4. Firewall** | f) Mecanismo que filtra el tráfico de red según reglas de seguridad predefinidas. |
| **5. IDS** | h) Sistema que detecta actividad sospechosa en la red y genera alertas. |
| **6. IPS** | k) Sistema que detecta Y bloquea activamente el tráfico malicioso en la red. |
| **7. OWASP** | e) Fundación que publica el Top 10 de vulnerabilidades web más críticas. |
| **8. Hash** | n) Función que transforma datos en una cadena de longitud fija e Irreversible. |
| **9. Cifrado** | i) Proceso de transformar datos legibles en un formato ilegible mediante una clave. |
| **10. MFA** | q) Uso de dos o mas factores para verificar la identidad de un usuario. |
| **11. Autenticación** | b) Proceso de verificar que un usuario es quien dice ser. |
| **12. Autorización** | p) Mecanismo que define qué puede hacer un usuario ya autenticado. |
| **13. Activo** | d) Recurso de valor para la organización: datos, hardware, software o servicios. |
| **14. Control de seguridad** | r) Medida implementada para reducir la probabilidad o impacto de una amenaza. |
| **15. Ataque** | g) Acción deliberada que explota una vulnerabilidad para comprometer la seguridad. |
| **16. Ingeniería social** | l) Técnica que manipula a personas para revelar información confidencial. |
| **17. Malware** | a) Software malicioso diseñado para dañar, robar o comprometer sistemas. |
| **18. SQL Injection** | t) Ataque que inyecta sentencias SQL en formularios para manipular la base de datos. |
| **19. XSS** | c) Técnica que inserta código malicioso en páginas web para ejecutarse en el navegador del visitante. |
| **20. Modelado de amenazas** | o) Técnica sistemática para identificar amenazas en un sistema antes de construirlo. |

---

## Sección C: Completar el Código (Java)

### Ejercicio 1: Validar longitud mínima de contraseña
```java
if (password.length() < 8) { ... }
```

### Ejercicio 2: Verificar si un carácter es dígito
```java
if (Character.isDigit(c) == true) { ... }
```

### Ejercicio 3: Verificar si un carácter es mayúscula
```java
if (Character.isUpperCase(c) == true) { ... }
```

### Ejercicio 4: Complejidad robusta de contraseña
```java
if (password.length() >= 8 && password.matches(".*[0-9].*") && 
password.matches(".*[A-Z].*") && password.matches(".*[@#$%^&+=].*"))
```

### Ejercicio 5: Validación de Email con Expresión Regular
```java
String regex = "^[\\w._%+-]+@[\\w.-]+\\.[a-zA-Z]{2,}$";
if (email.matches(regex)) { ... }
```

### Ejercicio 6: Limpieza y validación de usuario alfanumérico
```java
String cleanUser = username.trim();
if (cleanUser.matches("^[a-zA-Z0-9]{5,12}$")) { ... }
```

### Ejercicio 7: Sanitización básica contra XSS
```java
String safe = input.replace("<", "&lt;").replace(">", 
"&gt;").replace("\"", "&quot;").replace("'", "&#x27;");
```

### Ejercicio 8: Control de flujo seguro por Roles
```java
switch(rol) {
 case "ADMIN": ... break;
 default: ...
}
```

### Ejercicio 9: Control de intentos fallidos
```java
if (intentos >= 3 && user.equals(lockedUser)) { return true; }
```

### Ejercicio 10: Validación de dominio institucional
```java
if (email.contains("@autonoma.edu.pe") && !email.equals("")) { ... }
```

### Ejercicio 11: Validación robusta de campos vacíos
```java
if (input.isEmpty()) { ... } else if (!input.matches("[a-zA-Z]+")) { ... }
```

### Ejercicio 12: Cambio de clave forzando que no sea igual a la anterior
```java
if (!nuevaClave.equals(anterior) && nuevaClave.length() >= 8) { ... }
```

### Ejercicio 13: Captura de excepción en conversión de ID numérico
```java
try {
 int id = Integer.parseInt(input);
 if (id <= 0) throw new Exception();
} catch (NumberFormatException e) { ... }
```

### Ejercicio 14: Validación de rango de edad segura
```java
if (edad < 18 || edad > 100) { System.out.println("Edad fuera de rango permitido"); }
```

### Ejercicio 15: Validación de credenciales con mensaje seguro y ambiguo
```java
if (!isValidUser || !isValidPassword) { throw new SecurityException("Credenciales inválidas"); }
```

---

## Sección D: Análisis de Código

### Fragmento 1: Contraseña en texto plano hardcoded
* **Problema:** Credenciales fijas en el código fuente.
* **Riesgo:** Exposición total de accesos si el código es visible o descompilado.
* **Corrección:** Externalizar credenciales en variables de entorno o almacén de secretos.

### Fragmento 2: Validación de entrada (Whitelisting)
* **Problema:** Estructuralmente seguro. Aplica lista blanca y remueve espacios.
* **Riesgo:** Bajo. Mitiga inyecciones básicas.
* **Mejora:** Agregar límite de tamaño antes de evaluar regex para evitar ataques ReDoS (*Regular Expression DoS*).

### Fragmento 3: Inyección de parámetros sin sanitizar
* **Problema:** Uso directo de entradas del usuario en lógica crítica.
* **Riesgo:** Inyección de comandos, SQLi o XSS dependiendo de dónde se use.
* **Corrección:** Aplicar validación estricta con expresiones regulares antes de procesar.

### Fragmento 4: Control de acceso por rol en sesión
* **Problema:** Seguro si el rol viene de una fuente inmutable del servidor.