# Semana 07 — DevSecOps: CI/CD Seguro + SAST + Secrets Management

## Tema
Integración de seguridad en el pipeline de desarrollo: análisis estático (SAST con bandit/semgrep), gestión de secretos (variables de entorno, Vault), seguridad en contenedores Docker, revisión de dependencias (pip-audit, SBOM) y CI/CD seguro con GitHub Actions.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **configurar un pipeline CI/CD que incluya checks de seguridad automáticos** (SAST, análisis de dependencias, secrets scanning) y aplicar buenas prácticas de gestión de secretos en aplicaciones Python.

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Análisis de un pipeline CI/CD + identificación de riesgos |
| [Laboratorio](laboratorio/) | GitHub Actions workflow con bandit + pip-audit + secrets scan |
| [Material](material/) | Diapositivas y referencias |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-07/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s07.md` — Guía completada
- `laboratorio/`
  - `.github/workflows/security-check.yml` — Tu pipeline de seguridad
  - `requirements.txt` — Dependencias del proyecto
  - `scan_results/` — Reportes de bandit y pip-audit
  - `secrets_config.md` — Diseño de gestión de secretos
  - `capturas/` — Pipeline corriendo en GitHub Actions

## Conceptos clave evaluados
- SAST vs DAST vs IAST: diferencias y cuándo aplicar cada uno
- Por qué NO commitear `.env` con credenciales
- Cómo usar GitHub Secrets para variables de entorno sensibles
- Dockerfile seguro: usuario no-root, imagen base mínima, multi-stage
- Supply chain attacks: ¿qué es el SBOM?

## Referencias clave
- Bandit (SAST Python): https://bandit.readthedocs.io/
- pip-audit: https://pypi.org/project/pip-audit/
- GitHub Actions Security: https://docs.github.com/en/actions/security-guides
- OWASP DevSecOps Guideline: https://owasp.org/www-project-devsecops-guideline/
