# Semana 04 — Gestión de Sesiones Seguras + Control de Acceso

## Tema
Gestión segura de sesiones HTTP: tokens, cookies seguras (HttpOnly, SameSite, Secure), expiración, invalidación. Control de Acceso basado en Roles (RBAC) y prevención de escalada de privilegios.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **implementar sesiones seguras resistentes a session hijacking y fixation**, y diseñar un esquema RBAC que aplique el principio de mínimo privilegio en una aplicación web.

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Diseño de RBAC + análisis de vulnerabilidades de sesión |
| [Laboratorio](laboratorio/) | Implementación de sesiones seguras con Flask/CGI |
| [Material](material/) | Diapositivas y referencias |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-04/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s04.md` — Guía completada
- `laboratorio/` — Implementación de sesiones seguras
- `rbac_design.md` — Diseño de roles y permisos para tu proyecto
- `capturas/` — Evidencia de pruebas

## Conceptos clave evaluados
- Session ID: longitud, aleatoriedad, regeneración post-login
- Cookie attributes: HttpOnly, SameSite=Strict, Secure, Max-Age
- RBAC vs ABAC
- Escalada de privilegios horizontal vs vertical
- OWASP A01:2021 Broken Access Control

## Referencias clave
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP Access Control Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html
