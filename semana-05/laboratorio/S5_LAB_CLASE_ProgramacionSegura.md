# LABORATORIO DE CLASE — SEMANA 5
# PROGRAMACIÓN SEGURA — DD281
# Universidad Autónoma del Perú

```
Nombre: _________________________________ Código: ______________
Fecha: _________________________

TEMA: Identificación y remediación de SQL Injection en código real
TIEMPO: 35 minutos | Bajo supervisión del docente
```

---

## SOFTWARE (disponible en el aula)

Solo se necesita:
- **Navegador web** → https://replit.com (sin instalar nada)
- O **Python 3 + terminal** si el aula tiene computadoras con Python instalado

**Acceso en 2 minutos:**
1. Ir a https://replit.com
2. Crear cuenta gratuita (o usar cuenta existente)
3. New Repl → Python → nombrar "Lab5_SQLi_[TuApellido]"
4. Pegar el código base y ejecutar

---

## ACTIVIDAD: "Auditoría Express de Código"

El equipo de TI de MediSalud S.A. detectó actividad sospechosa en sus logs. Te contratan como auditor de seguridad junior y te entregan 3 fragmentos de código para revisar. Tienes 35 minutos.

### CÓDIGO BASE (pegar en Replit o archivo local):

```python
#!/usr/bin/env python3
"""
LAB CLASE S5 — MediSalud S.A. — Auditoría de Código
Nombre del estudiante: ___________________
Fecha: ___________________
"""

# ═══════════════════════════════════════════════════
# FRAGMENTO 1 — Sistema de búsqueda de pacientes
# ═══════════════════════════════════════════════════

def buscar_paciente_INSEGURO(nombre_paciente: str) -> str:
    """Versión INSEGURA — para análisis."""
    # Simula la consulta SQL que se ejecutaría en BD real
    query = f"SELECT * FROM pacientes WHERE nombre LIKE '%{nombre_paciente}%'"
    return f"[Ejecutando]: {query}"

def buscar_paciente_SEGURO(nombre_paciente: str) -> str:
    """
    ▶ TODO 1: Implementar versión segura.
    Usa consulta parametrizada y valida el input.
    La consulta parametrizada se vería así:
    query = "SELECT * FROM pacientes WHERE nombre LIKE ?"
    valor = (f"%{nombre_paciente}%",)
    """
    # Validación del input
    if not nombre_paciente or len(nombre_paciente) > 100:
        return "Error: nombre inválido"
    
    # ▶ COMPLETA AQUÍ: escribe la consulta parametrizada
    query_segura = "???"  # Reemplazar con la consulta correcta
    valor = ("???",)       # Reemplazar con el valor parametrizado
    
    # Simula la ejecución (en lab real usaríamos cursor.execute(query_segura, valor))
    return f"[Ejecutando de forma segura]: {query_segura} con valor={valor}"


# ═══════════════════════════════════════════════════
# FRAGMENTO 2 — Login del personal médico
# ═══════════════════════════════════════════════════

def login_personal_INSEGURO(usuario: str, password: str) -> dict:
    """Versión INSEGURA — para análisis."""
    query = "SELECT id, nombre, especialidad FROM medicos WHERE usuario='" + usuario + "' AND password='" + password + "'"
    
    # Simula la ejecución (en lab real: cursor.execute(query))
    print(f"  SQL generado: {query}")
    
    # Simula resultado (asume que el payload admin'-- devuelve resultado)
    if "OR '1'='1" in query or "--" in query:
        return {"acceso": True, "usuario": "BYPASS_EXITOSO", "via": "SQL_INJECTION"}
    return {"acceso": False}

def login_personal_SEGURO(usuario: str, password: str) -> dict:
    """
    ▶ TODO 2: Implementar versión segura.
    1. Validar que usuario solo tenga caracteres alfanuméricos y .
    2. Usar prepared statement
    3. Devolver mensaje genérico si falla (no revelar cuál campo falló)
    """
    import re
    
    # ▶ COMPLETA: validación del usuario
    if not re.match(r'???', usuario):  # Regex que permita solo letras, números y punto
        return {"acceso": False, "mensaje": "Datos inválidos"}
    
    # Simula la consulta parametrizada
    query_segura = "SELECT id, nombre, especialidad FROM medicos WHERE usuario=? AND password=?"
    print(f"  SQL parametrizado: {query_segura}")
    print(f"  Parámetros: ({repr(usuario)}, [PROTEGIDO])")
    
    # Simula verificación (siempre falla en el lab porque no tenemos BD real)
    return {"acceso": False, "mensaje": "Credenciales inválidas"}  # Mensaje genérico


# ═══════════════════════════════════════════════════
# FRAGMENTO 3 — Endpoint de diagnóstico del servidor
# ═══════════════════════════════════════════════════

def diagnostico_servidor_INSEGURO(ip_host: str) -> str:
    """Versión INSEGURA — para análisis."""
    import subprocess
    # VULNERABILIDAD: shell=True + concatenación = Command Injection
    cmd = f"ping -c 2 {ip_host}"
    resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return resultado.stdout

def diagnostico_servidor_SEGURO(ip_host: str) -> str:
    """
    ▶ TODO 3: Implementar versión segura.
    1. Validar que ip_host sea una IP válida con ipaddress.ip_address()
    2. Usar subprocess con LISTA de argumentos (sin shell=True)
    3. Rechazar IPs privadas
    """
    import subprocess
    import ipaddress
    
    try:
        # ▶ COMPLETA: validar la IP
        ip = ipaddress.ip_address("???")  # Pasar ip_host aquí
        
        # ▶ COMPLETA: rechazar IPs privadas/loopback
        if ip.is_private:  # Añadir también is_loopback
            return "Error: IP no permitida"
        
        # ▶ COMPLETA: subprocess con lista (SIN shell=True)
        resultado = subprocess.run(
            ["ping", "-c", "2", "???"],  # Pasar str(ip) aquí
            capture_output=True, text=True, timeout=5
        )
        return resultado.stdout
        
    except ValueError:
        return "Error: IP inválida"


# ═══════════════════════════════════════════════════
# PRUEBAS — Ejecuta esto para verificar tu trabajo
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("AUDITORÍA DE SEGURIDAD — MediSalud S.A.")
    print("=" * 60)
    
    # ─── FRAGMENTO 1: Búsqueda de pacientes ───
    print("\n▌ FRAGMENTO 1 — Búsqueda de pacientes")
    print("\n  [INSEGURO] Búsqueda normal:")
    print(" ", buscar_paciente_INSEGURO("Garcia"))
    
    print("\n  [INSEGURO] Con SQL Injection:")
    payload_sqli = "' UNION SELECT usuario, password, NULL FROM medicos--"
    print(" ", buscar_paciente_INSEGURO(payload_sqli))
    
    print("\n  [SEGURO] Misma búsqueda normal:")
    print(" ", buscar_paciente_SEGURO("Garcia"))
    
    print("\n  [SEGURO] Intento de SQL Injection (debe ser bloqueado):")
    print(" ", buscar_paciente_SEGURO(payload_sqli))
    
    # ─── FRAGMENTO 2: Login del personal ───
    print("\n" + "=" * 60)
    print("▌ FRAGMENTO 2 — Login del personal médico")
    print("\n  [INSEGURO] Login normal:")
    print(" ", login_personal_INSEGURO("dr.garcia", "clave123"))
    
    print("\n  [INSEGURO] Con SQL Injection:")
    print(" ", login_personal_INSEGURO("admin'--", "cualquiercosa"))
    
    print("\n  [SEGURO] Intento de bypass (debe ser rechazado):")
    print(" ", login_personal_SEGURO("admin'--", "cualquiercosa"))
    
    # ─── FRAGMENTO 3: Diagnóstico ───
    print("\n" + "=" * 60)
    print("▌ FRAGMENTO 3 — Diagnóstico del servidor")
    print("\n  [INSEGURO - SOLO MOSTRAR, NO EJECUTAR EN CLASE]")
    print("  Payload: '127.0.0.1; ls -la' ejecutaría comandos del SO")
    
    print("\n  [SEGURO] IP válida pública:")
    print(" ", diagnostico_servidor_SEGURO("8.8.8.8"))
    
    print("\n  [SEGURO] IP privada (debe rechazarse):")
    print(" ", diagnostico_servidor_SEGURO("192.168.1.1"))
    
    print("\n  [SEGURO] Command injection (debe rechazarse):")
    print(" ", diagnostico_servidor_SEGURO("8.8.8.8; ls -la"))
    
    # ─── PREGUNTA FINAL ───
    print("\n" + "=" * 60)
    print("▌ PREGUNTA DE ANÁLISIS FINAL")
    print("""
    Responde directamente en este archivo (agrega un comentario al final):
    
    1. ¿Cuál de los 3 fragmentos tiene la vulnerabilidad más peligrosa? ¿Por qué?
    
    2. ¿Qué tienen en común las 3 vulnerabilidades a nivel de causa raíz?
    
    3. ¿Cómo verificarías que la versión SEGURA realmente funciona 
       (qué pruebas harías)?
    """)

# ═══════════════════════════════════════════════════
# TUS RESPUESTAS (agrega aquí):
# ═══════════════════════════════════════════════════
"""
1. El fragmento más peligroso es: _______________
   Porque: _______________

2. Lo que tienen en común es: _______________

3. Las pruebas que haría son: _______________
"""
```

---

## PUNTOS DE VERIFICACIÓN

**Verificación 1 (10 min):** Ejecuta el código base sin modificar. Debes ver los SQL Injection funcionando en las versiones INSEGURAS. Captura la salida.

**Verificación 2 (20 min):** Completa los 3 TODO. Al ejecutar, las versiones SEGURAS deben:
- Buscar paciente SEGURO: mostrar la consulta parametrizada correcta
- Login SEGURO: rechazar `admin'--` con mensaje genérico
- Diagnóstico SEGURO: rechazar IPs privadas y command injection

**Verificación 3 (30 min):** Las respuestas a las 3 preguntas finales están escritas en el archivo.

---

## ROL DEL DOCENTE DURANTE EL LABORATORIO

### Qué observar mientras circula:
- Estudiantes que ejecutan sin leer: pedirles que lean el comentario de cada función primero
- Estudiantes que copian la versión insegura como solución: señalar la diferencia entre `f"...{variable}"` y `"...?"` con `(variable,)`
- Error más común en TODO 1: escribir `f"...%{nombre}%"` en lugar de `"...?"` con `(f"%{nombre}%",)`

### Preguntas de andamiaje para estudiantes bloqueados:
- "¿Qué diferencia ves entre la consulta con f-string y la consulta con ?"
- "¿El signo ? en SQL significa pregunta o significa placeholder?"
- "Si le paso el valor por separado, ¿puede el atacante 'salirse' del valor y escribir SQL?"

### Señales de que entendió vs no entendió:
- **Entendió:** usa `cursor.execute(query, (valor,))` y explica que el `?` es el placeholder
- **No entendió:** sigue usando f-strings o concatenación en la "versión segura"

### Cierre del laboratorio (5 min):
Pedir a 2-3 voluntarios que muestren su pantalla y lean sus respuestas a las 3 preguntas. El docente corrige en vivo.

---

## ENTREGABLE EN CLASE

El estudiante muestra al docente:
1. La terminal con el output de las 3 verificaciones pasando
2. Las respuestas escritas al final del archivo
3. Responde verbalmente: "¿Por qué el prepared statement previene el SQL Injection?"
