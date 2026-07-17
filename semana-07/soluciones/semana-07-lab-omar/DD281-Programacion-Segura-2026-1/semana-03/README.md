# Semana 03 — Validación de Entrada + Prevención de Inyección

## Tema
Validación y sanitización de entradas, prevención de SQL Injection (PreparedStatements, ORM), Cross-Site Scripting (XSS), CSRF y otras formas de inyección (LDAP, XML, Command Injection).

## Competencia de la semana
Al finalizar, el estudiante será capaz de **identificar y corregir vulnerabilidades de inyección** en código Python/SQL, aplicando validación de entradas en capas (cliente + servidor) y usando herramientas como bandit y sqlmap (en entorno controlado).

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Análisis de código vulnerable + corrección |
| [Laboratorio](laboratorio/) | Sistema de búsqueda con y sin SQL Injection + XSS demo |
| [Material](material/) | Diapositivas y referencias |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-03/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s03.md` — Guía completada
- `laboratorio/` — Versión segura de los ejercicios de inyección
- `capturas/` — Demostración del ataque y la defensa

## Conceptos clave evaluados
- Diferencia entre validación y sanitización
- PreparedStatements con `?` vs concatenación con f-strings
- Stored XSS vs Reflected XSS vs DOM-based XSS
- CSRF token: dónde se genera, dónde se valida
- OWASP A03:2021 Injection

## Referencias clave
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP XSS Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- Bandit (Python SAST): https://bandit.readthedocs.io/
