# LABORATORIO EN CLASE — SEMANA 6
## Programación Segura DD281 | Universidad Autónoma del Perú
**Tema:** Gestión de Sesiones, XSS e IDOR  
**Tiempo:** 35 minutos  
**Modalidad:** Individual  
**Plataforma:** Replit (replit.com) o VS Code + Python  
**Puntaje:** 20 puntos (evaluación formativa)

---

## INSTRUCCIONES GENERALES

- Trabaja de forma individual. No compartas código durante la sesión.
- Tienes exactamente 35 minutos para completar los 3 ejercicios.
- Al terminar, sube tu archivo a la tarea del Aula Virtual o comparte el link de Replit con el docente.
- Esta es una evaluación **formativa**: cuenta para tu nota, pero el objetivo principal es que aprendas el proceso de auditoría.

**Si usas Replit:**
1. Ve a [replit.com](https://replit.com) y crea un nuevo Repl de tipo Python.
2. Instala Flask con: `pip install flask`
3. Crea el archivo `auditoria.py` con el código que se te proporciona.

**Si usas VS Code:**
```bash
pip install flask
python auditoria.py
```

---

## ESCENARIO: SaludDigital — Auditoría Express

**Contexto:** SaludDigital es una clínica digital que conecta médicos y pacientes vía web. Su equipo de desarrollo ha publicado los siguientes endpoints en producción hace 2 semanas. Un usuario reportó comportamiento extraño en la búsqueda de pacientes.

**Tu rol:** Eres un consultor de seguridad contratado por 35 minutos para hacer una auditoría rápida. Debes identificar las vulnerabilidades, proponer la corrección del endpoint más crítico, y explicar el impacto legal.

**Código a auditar:**

```python
from flask import Flask, request, session
import sqlite3, html

app = Flask(__name__)
app.secret_key = "sd2024"

@app.route('/buscar-paciente')
def buscar_paciente():
    if not session.get('medico_id'):
        return "No autorizado", 401
    
    nombre = request.args.get('nombre', '')
    conn = sqlite3.connect('clinica.db')
    
    # Buscar paciente
    pacientes = conn.execute(
        f"SELECT id, nombre, diagnostico FROM pacientes WHERE nombre LIKE '%{nombre}%'"
    ).fetchall()
    conn.close()
    
    resultado = "<h2>Resultados:</h2>"
    for p in pacientes:
        resultado += f"<p>ID: {p[0]} — Nombre: {p[1]} — Diagnóstico: {p[2]}</p>"
    
    return f"<html><body>{resultado}</body></html>"

@app.route('/historial/<int:paciente_id>')
def ver_historial(paciente_id):
    if not session.get('medico_id'):
        return "No autorizado", 401
    
    conn = sqlite3.connect('clinica.db')
    historial = conn.execute(
        "SELECT * FROM historiales WHERE paciente_id = ?", (paciente_id,)
    ).fetchall()
    conn.close()
    
    return str(historial)
```

---

## EJERCICIO 1 — Identificación rápida de vulnerabilidades

**Tiempo:** 10 minutos  
**Puntaje:** 5 puntos

Lee el código anterior con atención. Completa la siguiente tabla de auditoría identificando **al menos 3 vulnerabilidades**:

| # | Línea / fragmento de código | Vulnerabilidad | Categoría OWASP 2021 | Riesgo |
|---|---|---|---|---|
| 1 | | | | Alto / Medio / Bajo |
| 2 | | | | Alto / Medio / Bajo |
| 3 | | | | Alto / Medio / Bajo |
| 4 (bonus) | | | | Alto / Medio / Bajo |

**Pistas:**
- ¿Cómo se construye la consulta SQL en `buscar_paciente`? ¿Es seguro?
- ¿Qué pasa con el valor de `nombre` antes de insertarlo en el HTML de respuesta?
- En `ver_historial`, ¿se verifica que el médico en sesión tenga autorización sobre ese `paciente_id` específico?
- ¿Es `"sd2024"` una clave secreta adecuada para producción?

---

## EJERCICIO 2 — Corrección rápida

**Tiempo:** 20 minutos  
**Puntaje:** 10 puntos

### Parte A — Reescribir `buscar_paciente()` de forma segura (7 puntos)

Reescribe **únicamente la función `buscar_paciente()`** de forma segura. Tu versión debe cumplir exactamente estos requisitos:

1. **Consulta parametrizada con LIKE:** El carácter `%` debe ir dentro del valor del parámetro, no en el placeholder SQL.
2. **Validación de longitud:** Rechaza búsquedas de más de 100 caracteres con código HTTP 400.
3. **Escape del output HTML:** Usa `html.escape()` sobre cada valor del paciente antes de incluirlo en la respuesta HTML.
4. **CSP header:** La respuesta debe incluir el header `Content-Security-Policy: default-src 'self'; script-src 'self'`.

**Estructura esperada de tu solución:**

```python
from flask import Flask, request, session, make_response
import sqlite3, html

app = Flask(__name__)
app.secret_key = "sd2024"  # (mantén igual por ahora, lo verás en el Ejercicio 3)

@app.route('/buscar-paciente')
def buscar_paciente():
    if not session.get('medico_id'):
        return "No autorizado", 401
    
    nombre = request.args.get('nombre', '').strip()
    
    # AQUÍ: validar longitud
    
    conn = sqlite3.connect('clinica.db')
    # AQUÍ: consulta parametrizada con LIKE
    conn.close()
    
    resultado = "<h2>Resultados:</h2>"
    for p in pacientes:
        # AQUÍ: escapar nombre y diagnóstico
        resultado += f"<p>ID: {p[0]} — Nombre: {nombre_seguro} — Diagnóstico: {diagnostico_seguro}</p>"
    
    # AQUÍ: crear response con make_response y agregar CSP header
    return response
```

### Parte B — IDOR oculto en `ver_historial()` (3 puntos)

La función `ver_historial()` tiene una vulnerabilidad de IDOR que no es evidente a primera vista.

**Pregunta:** ¿Cuál es el IDOR? El código verifica que el médico esté autenticado, pero ¿verifica que ese médico tenga autorización para ver el historial de **ese paciente específico**?

Escribe la consulta SQL corregida que verifique que el médico en sesión (`session['medico_id']`) tiene relación con el `paciente_id` solicitado. Asume que existe una tabla `citas` con columnas `medico_id` y `paciente_id`.

```python
@app.route('/historial/<int:paciente_id>')
def ver_historial(paciente_id):
    if not session.get('medico_id'):
        return "No autorizado", 401
    
    medico_id = session['medico_id']
    conn = sqlite3.connect('clinica.db')
    
    # ESCRIBE AQUÍ la consulta corregida que verifique la relación médico-paciente
    historial = conn.execute(
        # Tu consulta aquí
    ).fetchall()
    conn.close()
    
    if not historial:
        return "No encontrado", 404  # Mismo mensaje para "no existe" y "no autorizado"
    return str(historial)
```

---

## EJERCICIO 3 — Reflexión breve

**Tiempo:** 5 minutos  
**Puntaje:** 5 puntos

Responde en **3 a 5 oraciones** las siguientes preguntas:

1. En el código de SaludDigital, la columna `diagnostico` se almacena junto con el nombre del paciente y puede ser visible en los resultados de búsqueda. ¿Por qué el diagnóstico médico de un paciente es un tipo de dato que requiere protección especial, más allá de cualquier otro dato personal como el nombre o el correo?

2. ¿Qué ley peruana protege específicamente este tipo de datos? ¿Cómo clasifica esa ley los datos de salud?

3. Si SaludDigital sufriera una brecha y se filtraran diagnósticos de pacientes por la vulnerabilidad SQL Injection que encontraste, ¿qué consecuencias legales podría enfrentar la empresa?

---

## ENTREGA

Al finalizar los 35 minutos, sube al Aula Virtual (tarea "Lab Clase S6") **un solo archivo** llamado `auditoria_[tu_codigo].py` (reemplaza `[tu_codigo]` con tu código de alumno) que contenga:

```python
# NOMBRE COMPLETO: 
# CÓDIGO DE ALUMNO:
# FECHA:

# ============================================================
# EJERCICIO 1 — TABLA DE VULNERABILIDADES
# ============================================================
# Escribe tu tabla como comentarios de Python:
# 1. Línea: ... | Vulnerabilidad: ... | OWASP: ... | Riesgo: ...
# 2. Línea: ... | Vulnerabilidad: ... | OWASP: ... | Riesgo: ...
# 3. Línea: ... | Vulnerabilidad: ... | OWASP: ... | Riesgo: ...

# ============================================================
# EJERCICIO 2A — buscar_paciente() CORREGIDA
# ============================================================
# (Tu función corregida aquí)

# ============================================================
# EJERCICIO 2B — ver_historial() CORREGIDA
# ============================================================
# (Tu función corregida aquí)

# ============================================================
# EJERCICIO 3 — REFLEXIÓN
# ============================================================
# (Tu respuesta como comentarios de Python)
```

---

## CRITERIOS DE EVALUACIÓN

| Ejercicio | Criterio | Puntaje |
|---|---|---|
| Ejercicio 1 | Mínimo 3 vulnerabilidades identificadas con OWASP correcto | 5 pts |
| Ejercicio 2A | Función con consulta parametrizada + escape + CSP | 7 pts |
| Ejercicio 2B | Consulta con JOIN o subconsulta que verifica médico-paciente | 3 pts |
| Ejercicio 3 | Menciona datos sensibles, ley peruana y consecuencias | 5 pts |
| **TOTAL** | | **20 pts** |

**Nota:** No se descuentan puntos por errores de sintaxis menores si la lógica de seguridad es correcta. El objetivo es demostrar que entiendes el principio de la mitigación.
