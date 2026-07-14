# Respuestas del Laboratorio S3 - Sesiones Seguras con RBAC en Flask

| Campo | Detalle |
|---|---|
| Estudiante | Hidgar Orellano Huerta |
| Codigo | 2221892872 |
| Seccion | 6 |
| Fecha | 21/06/2026 |

## Parte 1 - Exploracion

**P1.1:** La cookie `session` que aparece en DevTools no muestra el email del usuario directamente. Flask guarda una cookie firmada criptograficamente; contiene datos de sesion serializados y protegidos con la `SECRET_KEY`, pero no debe tratarse como un lugar para guardar informacion sensible en texto claro.

**P1.2:** Si `SESSION_COOKIE_HTTPONLY` cambia a `False`, la cookie deja de estar protegida contra lectura desde JavaScript. En DevTools ya no aparece marcada como HttpOnly, lo que permitiria que un XSS intente leerla con `document.cookie`.

**P1.3:** Al ejecutar `document.cookie`, una cookie con `HttpOnly=True` no se muestra a JavaScript. Esto ocurre porque el navegador impide que scripts del lado cliente lean esa cookie, reduciendo el impacto de ataques XSS orientados al robo de sesiones.

## Parte 2 - Pruebas RBAC ejecutadas

Pruebas realizadas con el cliente de pruebas de Flask sobre `app.py`.

| Prueba | Usuario | Ruta | Resultado esperado | Resultado real |
|---|---|---|---|---|
| 1 | usuario@test.com | `/reportes` | 403 Acceso denegado | 403 Acceso denegado |
| 2 | supervisor@test.com | `/reportes` | 200 OK, muestra reportes | 200 OK |
| 3 | usuario@test.com | `/admin/panel` | 403 Acceso denegado | 403 Acceso denegado |
| 4 | admin@test.com | `/admin/panel` | 200 OK, panel admin | 200 OK |
| 5 | Sin login | `/dashboard` | Redirige a `/login` | 302 Redirect a `/login` |

Resultados adicionales:

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

**Pregunta 2.1:** Si `/admin/panel` verificara el rol con `request.args.get('role') == 'admin'`, el rol dependeria de un valor controlado por el cliente. Un atacante podria entrar a `/admin/panel?role=admin` y saltarse la autorizacion. Por eso el rol se lee desde `session`, que fue asignada por el servidor al autenticar, y se valida con el decorador `require_role`.

**Pregunta 2.2:** El error 403 implementado no muestra stack traces, rutas internas, variables del servidor ni informacion sensible. Solo indica que el acceso fue denegado y que se requiere un rol especifico. En produccion se podria hacer el mensaje aun mas generico para reducir informacion disponible para un atacante.

## Puntos de verificacion Parte 2

- [X] `session.clear()` en el login para prevenir Session Fixation.
- [X] Logout limpia la sesion del servidor/framework y elimina la cookie del cliente.
- [X] `/reportes` retorna 403 para rol `usuario` y 200 para `supervisor`.
- [X] `/admin/panel` retorna 403 para todo rol que no sea `admin`.
- [X] Tabla de pruebas completa con resultados reales.

## Parte 3 - Desafios

**Desafio 3.1 - Simulacion de Session Fixation:** La ruta `/demo/fixation` esta implementada y devuelve el estado de la cookie antes o despues del login. La defensa principal esta en el login: se ejecuta `session.clear()` antes de asignar `user_id`, `user_role` y `user_name`, de modo que datos previos de sesion no se heredan despues de autenticar.

**Observacion:** En la prueba automatica la ruta `/demo/fixation` respondio `200 OK`. Al probar manualmente en navegador, antes del login debe mostrarse sin usuario autenticado, y despues del login debe indicar que ya existe `user_id` en sesion. La sesion fue limpiada antes de asignar la identidad autenticada.

**Desafio 3.2 - Auditoria de sesiones activas:** Se agrego el diccionario `sesiones_auditoria`, el hash del session ID, la IP, hora de login y ultimo acceso. El decorador `require_role` actualiza `last_seen` en cada ruta protegida y `/admin/sesiones-activas` permite revisar esa informacion solo con rol `admin`.

## Reflexion final

El concepto mas dificil de implementar fue entender que la autenticacion y la autorizacion son pasos diferentes. No basta con saber que un usuario inicio sesion; tambien se debe verificar que tenga permiso para cada ruta. El concepto de mayor impacto para el proyecto es RBAC junto con el principio de minimo privilegio, porque evita que usuarios normales accedan a funciones administrativas aunque conozcan la URL. Tambien considero importante `HttpOnly` y `SameSite`, ya que reducen el impacto de XSS y CSRF. En conjunto, estas medidas hacen que la aplicacion no dependa de valores manipulables por el cliente.
