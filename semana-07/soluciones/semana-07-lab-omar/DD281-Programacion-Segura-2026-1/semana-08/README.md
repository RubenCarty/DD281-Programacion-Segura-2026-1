# Semana 08 — Auditoría de Seguridad + OWASP Testing + Presentación Final

## Tema
Auditoría de seguridad web con OWASP Testing Guide v4.2: reconocimiento, análisis de superficie de ataque, testing de autenticación, autorización, gestión de sesiones y criptografía. Presentación y defensa del proyecto final.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **realizar una auditoría de seguridad básica** de una aplicación web siguiendo la metodología OWASP Testing Guide, documentar hallazgos con severidad CVSS, y presentar el proyecto grupal del curso.

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Metodología de auditoría + plantilla de reporte |
| [Laboratorio](laboratorio/) | Auditoría de la aplicación desarrollada en las semanas previas |
| [Material](material/) | Diapositivas, rúbrica de evaluación final |

## Entrega del estudiante (ENTREGA FINAL)

Sube tu trabajo en:
```
semana-08/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s08.md` — Guía completada
- `reporte_auditoria.md` — Reporte de auditoría de seguridad con:
  - Metodología usada
  - Vulnerabilidades encontradas (con severidad CVSS)
  - Evidencias (capturas)
  - Recomendaciones
- `reflexion_curso.md` — Reflexión de aprendizaje del curso completo
- `capturas/` — Evidencia de las pruebas de auditoría

## Presentación del Proyecto Grupal

Cada grupo presenta su proyecto en la sesión final (15 min + 5 min preguntas):

| Ítem | Peso |
|---|---|
| Funcionalidad implementada | 30% |
| Controles de seguridad aplicados | 30% |
| Calidad del código y documentación | 20% |
| Presentación y defensa | 20% |

## Conceptos clave evaluados
- OWASP Testing Guide v4.2 — Fases de una auditoría
- CVSS v3.1: Base Score, Vector String, severidad
- Diferencia entre vulnerability assessment y penetration testing
- Informe ejecutivo vs informe técnico de seguridad
- Lecciones aprendidas del curso: de código inseguro a código seguro

## Referencias clave
- OWASP Testing Guide v4.2: https://owasp.org/www-project-web-security-testing-guide/
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1
- OWASP ZAP (DAST): https://www.zaproxy.org/
- Nikto web scanner: https://cirt.net/Nikto2

---

> **Nota:** Esta es la entrega final del curso. El PR de la semana 08 debe estar abierto antes del inicio de la sesión final.
