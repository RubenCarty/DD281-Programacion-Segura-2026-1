# Semana 02 — Especificación Formal de Seguridad + Login Seguro

## Tema
Especificación formal de seguridad (7 componentes: activos, sujetos, objetos, operaciones, condiciones, mecanismos, respuesta), autenticación segura con bcrypt, SSL/TLS y CGI en Python.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **diseñar una especificación formal de seguridad y construir un sistema de login resistente a SQL Injection, fuerza bruta y timing attacks**, usando bcrypt + HTTPS.

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/S2_GUIA_TRABAJO_ESTUDIANTE.md) | 6 secciones: recuperación S1, diagnóstico, selección múltiple, análisis, colaborativo, metacognición |
| [Laboratorio](laboratorio/S2_LABORATORIO_LOGIN_SEGURO.md) | Implementación completa de login seguro: SSL + bcrypt + CGI |
| [Material](material/) | Sesión completa y diapositivas |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-02/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s02.md` — Guía completada (Secciones A-F)
- `laboratorio/` — Código implementado:
  - `setup_db.py`
  - `login_seguro.py`
  - `servidor.py`
  - `login.html`
  - `capturas/` — Screenshots de las 6 pruebas
  - `auth.log` — Log de autenticación (con datos de prueba, no reales)

> **No subir:** `server.key`, `server.crt` (generarlos localmente), `.db` con datos personales.

## Conceptos clave evaluados

- bcrypt vs MD5/SHA-1: ¿por qué bcrypt es superior?
- PreparedStatement vs f-string en SQL
- Perfect Forward Secrecy (PFS)
- Timing attacks y cómo prevenirlos
- HTTP Security Headers (HSTS, X-Frame-Options)

## Fecha de cierre del PR
**Ver anuncio del docente en clase.**

## Referencias clave
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- NIST SP 800-63B (Password guidelines): https://pages.nist.gov/800-63-3/sp800-63b.html
- bcrypt docs (Python): https://pypi.org/project/bcrypt/
