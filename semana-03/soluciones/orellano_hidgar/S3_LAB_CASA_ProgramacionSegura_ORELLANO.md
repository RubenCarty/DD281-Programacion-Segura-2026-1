# S3 - LABORATORIO EN CASA
## Sistema de Sesiones Seguras con RBAC en Flask

| Campo | Detalle |
|---|---|
| **Curso** | Programacion Segura (DD281) - Semana 3 |
| **Nombre del estudiante** | Hidgar Orellano Huerta |
| **Codigo** | 2221892872 |
| **Seccion** | 6 |
| **Fecha de entrega** | 21/06/2026 |
| **Modalidad** | Individual |

---

## Objetivo del laboratorio

Implementar un sistema Flask con gestion de sesiones seguras, RBAC con tres roles, prevencion de Session Fixation, logout completo y auditoria basica de sesiones activas.

---

## Estructura entregada

```text
semana-03/soluciones/orellano_hidgar/
├── S3_GUIA_ESTUDIANTE_ProgramacionSegura_ORELLANO.md
├── S3_LAB_CASA_ProgramacionSegura_ORELLANO.md
├── laboratorio/
│   ├── app.py
│   ├── requirements.txt
│   ├── respuestas.md
│   └── templates/
│       ├── login.html
│       ├── dashboard.html
│       ├── admin.html
│       └── error.html
└── capturas/
    └── README.md
```

---

## Como ejecutar el laboratorio

Entrar a la carpeta del laboratorio:

```bash
cd semana-03/soluciones/orellano_hidgar/laboratorio
```

Crear un entorno virtual, instalar Flask y ejecutar:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir en el navegador:

```text
http://localhost:5000
```

---

## Usuarios de prueba

| Rol | Usuario | Contrasena |
|---|---|---|
| admin | admin@test.com | Admin2026! |
| supervisor | supervisor@test.com | Super2026! |
| usuario | usuario@test.com | Usuario2026! |

---

## Funcionalidades implementadas

- Cookie de sesion con `HttpOnly=True`.
- Cookie con `SameSite=Lax`.
- `SESSION_COOKIE_SECURE=False` en local, con comentario indicando `True` para produccion con HTTPS.
- `session.clear()` antes de asignar identidad en login para prevenir Session Fixation.
- Logout con `session.clear()` y eliminacion de cookie en cliente.
- Decorador `require_role(*roles)` para RBAC.
- Rutas protegidas por rol:
  - `/mi-perfil`: admin, supervisor y usuario.
  - `/reportes`: admin y supervisor.
  - `/admin/panel`: solo admin.
  - `/admin/sesiones-activas`: solo admin.
- Ruta educativa `/demo/fixation`.
- Auditoria basica de sesiones activas con hash de session ID, usuario, IP, login y ultimo acceso.

---

## Pruebas realizadas

Las pruebas funcionales se documentan en:

```text
laboratorio/respuestas.md
```

Resultados ejecutados:

```text
sin_login_dashboard 302 /login
login_usuario 302 /dashboard
usuario_reportes 403
usuario_admin 403
supervisor_reportes 200
supervisor_admin 403
admin_panel 200
admin_sesiones 200
demo_fixation 200
```

---

## Evidencias

La carpeta `capturas/` queda preparada para agregar screenshots si el docente los solicita. El archivo `capturas/README.md` indica que capturas tomar: cookie en DevTools, rutas con 403/200 y demo de Session Fixation.
