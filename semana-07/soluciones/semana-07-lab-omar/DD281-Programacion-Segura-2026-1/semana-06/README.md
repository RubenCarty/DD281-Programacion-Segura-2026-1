# Semana 06 — APIs Seguras: OAuth2 + JWT + Rate Limiting

## Tema
Diseño y seguridad de APIs REST: autenticación con JWT (JSON Web Tokens), autorización con OAuth 2.0, Rate Limiting, API Keys, validación de entrada en APIs y protección contra OWASP API Security Top 10.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **diseñar una API REST segura** con autenticación JWT, autorización OAuth2, rate limiting y validación de payloads, aplicando OWASP API Security Top 10.

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Diseño de arquitectura segura de API + análisis de vulnerabilidades |
| [Laboratorio](laboratorio/) | API Flask con JWT + Rate Limiting + HTTPS |
| [Material](material/) | Diapositivas y referencias |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-06/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s06.md` — Guía completada
- `laboratorio/`
  - `api_segura.py` — API Flask con JWT
  - `auth_server.py` — Servidor de autenticación (o integrado)
  - `test_api.py` — Tests de seguridad
  - `capturas/` — Evidencia con Postman o curl

## Conceptos clave evaluados
- JWT: estructura (header.payload.signature), algoritmo HS256 vs RS256
- ¿Por qué no guardar datos sensibles en el payload JWT?
- OAuth2: flujos (Authorization Code, Client Credentials, Implicit)
- Rate limiting: tokens bucket vs fixed window
- OWASP API Security Top 10: API1 (BOLA), API2 (Broken Auth), API3 (BOPLA)

## Referencias clave
- OWASP API Security Top 10: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- JWT.io (debugger): https://jwt.io/
- PyJWT docs: https://pyjwt.readthedocs.io/
- Flask-Limiter: https://flask-limiter.readthedocs.io/
