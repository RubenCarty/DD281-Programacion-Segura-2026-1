# 🔐 DD281 — Programación Segura | Universidad Autónoma del Perú
## Ciclo 2026-1 | Docente: Mg. Ruben Quispe Llacctarimay

[![GitHub](https://img.shields.io/badge/GitHub-RubenCarty-181717?logo=github)](https://github.com/RubenCarty)
[![License](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)
[![Semanas](https://img.shields.io/badge/Semanas-8-blue)]()
[![Estudiantes](https://img.shields.io/badge/Modalidad-Fork%20%2B%20PR-orange)]()

---

## 📋 Descripción del Curso

**Programación Segura (DD281)** es un curso de educación superior enfocado en el diseño, implementación y auditoría de software seguro. Los estudiantes aprenden a construir aplicaciones que resisten los ataques más comunes del mundo real, aplicando estándares internacionales (OWASP, NIST, ISO 27001).

> **Repositorio oficial del curso** — Aquí se publican guías de trabajo, laboratorios y material semanal. Los estudiantes suben sus soluciones mediante **Fork + Pull Request**.

---

## 🗂️ Estructura del Repositorio

```
DD281-Programacion-Segura-2026-1/
│
├── README.md                          ← Este archivo
├── GUIA_DOCENTE.md                    ← Guía completa para el docente
├── GUIA_ESTUDIANTE.md                 ← Guía completa para el estudiante
├── SYLLABUS.md                        ← Sílabo del curso
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md       ← Plantilla de PR para estudiantes
│   ├── ISSUE_TEMPLATE/
│   │   └── pregunta-academica.md     ← Plantilla para preguntas
│   └── workflows/
│       └── validate-structure.yml    ← Validación automática de PR
│
├── semana-01/                         ← Introducción + Modelado de Amenazas
│   ├── README.md
│   ├── guia-trabajo/
│   ├── laboratorio/
│   ├── material/
│   └── soluciones/                   ← Estudiantes suben AQUÍ (APELLIDO_NOMBRE/)
│
├── semana-02/                         ← Especificación Formal + Login Seguro
├── semana-03/                         ← Validación de Entrada + SQL Injection
├── semana-04/                         ← Gestión de Sesiones + Cookies
├── semana-05/                         ← Criptografía Aplicada
├── semana-06/                         ← APIs Seguras + OAuth2 + JWT
├── semana-07/                         ← DevSecOps + CI/CD Seguro
└── semana-08/                         ← Auditoría + OWASP Testing + Entrega Final
```

---

## 📅 Plan de Trabajo Semanal

| Semana | Tema | Competencia |
|:---:|---|---|
| **S01** | Introducción a la Programación Segura + Modelado de Amenazas (STRIDE) | Diseño preventivo |
| **S02** | Especificación Formal de Seguridad + Login Seguro (CGI + SSL) | Autenticación robusta |
| **S03** | Validación de Entrada + Prevención de Inyección (SQL, XSS, CSRF) | Defensa en código |
| **S04** | Gestión de Sesiones Seguras + Cookies + Control de Acceso | RBAC y autorización |
| **S05** | Criptografía Aplicada: Cifrado simétrico, asimétrico, hashing | Datos protegidos |
| **S06** | APIs Seguras: OAuth2, JWT, Rate Limiting, API Gateway | Servicios seguros |
| **S07** | DevSecOps: CI/CD seguro, SAST, DAST, Secrets Management | Pipeline seguro |
| **S08** | Auditoría + OWASP Testing Guide + Presentación Final | Evaluación integral |

---

## 🚀 Inicio Rápido

### Para el Docente
→ Ver [GUIA_DOCENTE.md](GUIA_DOCENTE.md) — Comandos, flujo de trabajo y revisión de PRs.

### Para el Estudiante
→ Ver [GUIA_ESTUDIANTE.md](GUIA_ESTUDIANTE.md) — Fork, clone, trabajo semanal y cómo hacer un PR.

---

## 📁 Proyectos Innovadores del Curso

Los 5 grupos trabajan en repositorios independientes:

| Grupo | Proyecto | Repositorio |
|:---:|---|---|
| G1 | SecureAuth Platform — Autenticación robusta completa | [PS-P1-SecureAuth-Platform](https://github.com/RubenCarty/PS-P1-SecureAuth-Platform) |
| G2 | SecureBank API — API bancaria con seguridad enterprise | [PS-P2-SecureBank-API](https://github.com/RubenCarty/PS-P2-SecureBank-API) |
| G3 | HealthPortal Secure — Portal médico con compliance HIPAA | [PS-P3-HealthPortal-Secure](https://github.com/RubenCarty/PS-P3-HealthPortal-Secure) |
| G4 | SecureVoting System — Sistema de votación con integridad garantizada | [PS-P4-SecureVoting-System](https://github.com/RubenCarty/PS-P4-SecureVoting-System) |
| G5 | PenTest Toolkit — Herramienta de auditoría de seguridad web | [PS-P5-PenTest-Toolkit](https://github.com/RubenCarty/PS-P5-PenTest-Toolkit) |

---

## 📌 Reglas del Repositorio

1. **Cada estudiante trabaja en su propio Fork** — nunca directamente en este repositorio.
2. **Una PR por semana por estudiante** — el PR debe estar abierto antes del cierre de la semana.
3. **Carpeta de solución personal**: `semana-XX/soluciones/APELLIDO_NOMBRE/`
4. **No subir datos sensibles**: claves API, contraseñas, tokens — usar `.gitignore`.
5. **Mensajes de commit descriptivos**: `feat(s02): agrega login seguro con bcrypt`
6. **Las PRs sin descripción serán rechazadas** — usa la plantilla de PR.

---

## 🔗 Recursos del Curso

| Recurso | Link |
|---|---|
| OWASP Top 10 | https://owasp.org/Top10/ |
| NIST Password Guidelines | https://pages.nist.gov/800-63-3/sp800-63b.html |
| OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html |
| Have I Been Pwned | https://haveibeenpwned.com |
| SSL Labs Test | https://www.ssllabs.com/ssltest/ |
| GitHub Docs — Forks | https://docs.github.com/en/get-started/quickstart/fork-a-repo |

---

## 👨‍🏫 Contacto

- **Docente:** Mg. Ruben Quispe Llacctarimay
- **GitHub:** [@RubenCarty](https://github.com/RubenCarty)
- **LinkedIn:** [ruben-quispe-l](https://linkedin.com/in/ruben-quispe-l)
- **Email:** rubencarty4@gmail.com

---

*Universidad Autónoma del Perú — Ingeniería de Sistemas — 2026-1*
