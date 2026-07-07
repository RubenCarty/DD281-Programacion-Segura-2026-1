# Laboratorio en Casa — Semana 6
## Programación Segura DD281 | Universidad Autónoma del Perú

**Alumno:** Omar Rivera Castillo  
**Código de alumno:** 2221895826  
**Tema:** Gestión de Sesiones, XSS e IDOR  

---

## Estructura del entregable

```
semana-06/lab-casa/
├── app_vulnerable.py       # Código original sin modificar (análisis de vulnerabilidades)
├── app_segura.py           # Implementación segura con los 11 TODOs completados y comentados
├── reflexion.md            # Reflexión técnico-legal (Tarea 2.3) — mínimo 200 palabras
├── README.md               # Este archivo
└── evidencias/
    ├── tarea1_2_xss_vulnerable.txt     # Demostración XSS en app vulnerable
    ├── tarea1_3_idor_vulnerable.txt    # Demostración IDOR en app vulnerable
    ├── tarea2_2_xss_rechazado.txt      # XSS rechazado en app segura
    └── tarea2_2_idor_rechazado.txt     # IDOR rechazado en app segura
```

## Cómo ejecutar

```bash
pip install flask

# App vulnerable (Parte 1)
python app_vulnerable.py      # corre en http://localhost:5001

# App segura (Parte 2)
python app_segura.py          # corre en http://localhost:5002
```

## Resumen de vulnerabilidades corregidas

| TODO | Vulnerabilidad | OWASP 2021 |
|------|---------------|------------|
| 1 | Clave secreta débil y hardcodeada | A02 - Cryptographic Failures |
| 2 | Cookies sin HttpOnly/Secure/SameSite | A07 - Auth Failures |
| 3 | Falta validación de entrada (username) | A03 - Injection |
| 4 | SQL Injection por concatenación | A03 - Injection |
| 5 | Session Fixation | A07 - Auth Failures |
| 6 | Sin límite de longitud en comentarios | A03 - Injection |
| 7 | SQL Injection en INSERT | A03 - Injection |
| 8 | XSS Almacenado por falta de escape HTML | A03 - Injection |
| 9 | IDOR sin control de acceso a documentos | A01 - Broken Access Control |
| 10 | Information Disclosure en errores | A01 - Broken Access Control |
| 11 | Falta Content-Security-Policy header | A05 - Security Misconfiguration |
