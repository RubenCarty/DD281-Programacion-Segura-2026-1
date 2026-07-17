"""
app_double_submit.py — Implementación del patrón Double Submit Cookie
Tarea 3.1 — Programación Segura DD281 — Semana 7

CONCEPTO:
El servidor genera un token aleatorio y lo envía en DOS lugares:
  1. Una cookie (HttpOnly=False, para que el JS del cliente pueda leerla)
  2. En el body JSON de la respuesta (el cliente JS lo guarda y lo reenvía en POSTs)

Al recibir el POST, el servidor compara ambos. Un atacante puede forzar un POST
(CSRF), pero NO puede leer el valor de la cookie de otro dominio (Same-Origin Policy),
por lo tanto no puede incluir el token correcto en el body → el ataque falla.
"""

from flask import Flask, request, session, jsonify, make_response
import secrets

app = Flask(__name__)
# La SECRET_KEY se genera aleatoriamente en cada arranque (solo para demo)
app.secret_key = secrets.token_hex(32)


@app.route('/obtener-token-ds')
def obtener_token():
    """
    Genera el token y lo envía tanto en cookie como en el body.
    El cliente debe guardar el valor del body y enviarlo en futuros POSTs.
    """
    token = secrets.token_hex(32)
    response = make_response(jsonify({"csrf_ds_token": token}))

    # Enviar el token en una cookie (HttpOnly=False para que JS pueda leerla)
    # NOTA: HttpOnly=False es INTENCIONAL aquí. El JS legítimo de la app necesita
    # leer este valor para incluirlo en el body del formulario. Esta es la diferencia
    # con la cookie de sesión (que sí debe ser HttpOnly=True).
    response.set_cookie(
        'csrf_ds_token',
        token,
        httponly=False,   # El JS del cliente necesita leer esta cookie
        secure=True,
        samesite='Strict'
    )
    return response


@app.route('/comprar-v2', methods=['POST'])
def comprar_v2():
    """
    Valida el Double Submit Cookie antes de procesar la compra.
    """
    # El token viene en la cookie Y en el body del formulario
    token_cookie = request.cookies.get('csrf_ds_token')
    token_body = request.form.get('csrf_token')

    # ─────────────────────────────────────────────────────────────────────────
    # TODO: Implementar la verificación del Double Submit Cookie
    #
    # Caso 1: token_cookie es None
    #   El usuario nunca llamó a GET /obtener-token-ds, por lo tanto la cookie
    #   no existe. Sin token de referencia en el servidor, no hay forma de
    #   verificar nada → rechazar con 403.
    #
    # Caso 2: token_body es None
    #   El formulario no incluyó el campo csrf_token. Esto ocurre si:
    #   a) El cliente legítimo tiene un bug (olvidó incluirlo)
    #   b) Es un ataque CSRF — el atacante no pudo leer la cookie (Same-Origin Policy)
    #   En ambos casos → rechazar con 403.
    #
    # Caso 3: Comparación con secrets.compare_digest()
    #   Se usa compare_digest() en vez de == para prevenir timing attacks:
    #   Con ==, Python puede devolver False más rápido si los primeros caracteres
    #   ya no coinciden. Un atacante que mide el tiempo de respuesta puede
    #   deducir cuántos caracteres del token ya adivinó correctamente.
    #   compare_digest() siempre tarda el mismo tiempo sin importar cuántos
    #   caracteres coincidan, eliminando esta vulnerabilidad de canal lateral.
    # ─────────────────────────────────────────────────────────────────────────

    # Caso 1: cookie no existe
    if not token_cookie:
        return jsonify({
            "error": "CSRF token cookie ausente. Llama primero a GET /obtener-token-ds"
        }), 403

    # Caso 2: token no incluido en el body
    if not token_body:
        return jsonify({
            "error": "CSRF token ausente en el body del formulario"
        }), 403

    # Caso 3: comparación segura contra timing attacks
    # secrets.compare_digest() requiere que ambas cadenas sean del mismo tipo (str o bytes)
    if not secrets.compare_digest(token_cookie, token_body):
        return jsonify({
            "error": "CSRF token inválido: cookie y body no coinciden"
        }), 403

    # Si los tokens son válidos, procesar la compra
    producto = request.form.get('producto', '')
    monto = request.form.get('monto', 0)
    return jsonify({"comprado": producto, "monto": monto, "estado": "compra exitosa"})


"""
RESPUESTAS A LAS PREGUNTAS DE LA TAREA 3.1
============================================

PREGUNTA 1: ¿Por qué el atacante no puede replicar el ataque aunque sepa el nombre de la cookie?

El atacante puede saber que la cookie se llama 'csrf_ds_token', pero no puede LEER su valor
desde evil.com. La Same-Origin Policy del navegador impide que un script en evil.com acceda
a cookies o respuestas de otro dominio (localhost:5004). El atacante puede forzar al navegador
a ENVIAR la cookie en el POST (eso lo hace el navegador automáticamente), pero ese valor
en la cookie debe coincidir con lo que el atacante incluye en el BODY del formulario.
Como no puede leer la cookie, no sabe qué poner en el body → el compare_digest falla → 403.

PREGUNTA 2: ¿Cuándo es el Double Submit Cookie MENOS seguro que el token en sesión?

El Double Submit Cookie es vulnerable si el atacante puede ESCRIBIR cookies en subdominios
del sitio víctima. Por ejemplo, si tiendaapp.com tiene un subdominio comprometido como
blog.tiendaapp.com, un script malicioso en ese subdominio puede sobreescribir la cookie
'csrf_ds_token' para el dominio .tiendaapp.com con un valor que el atacante conoce.
Luego, desde evil.com, el formulario CSRF incluye ese valor conocido en el body → los
tokens coinciden → el ataque funciona.
El token en sesión es más robusto porque se almacena en el servidor (no en el cliente),
por lo que nunca puede ser sobreescrito por un subdominio comprometido.
Este ataque se conoce como "Cookie Tossing" o "Cookie Injection via Subdomain".

PREGUNTA 3: ¿Por qué se usa secrets.compare_digest() en vez de == para comparar tokens?

El operador == realiza una comparación de "cortocircuito": tan pronto como encuentra un
carácter que no coincide, devuelve False. Esto significa que comparar un token completamente
erróneo tarda MENOS tiempo que comparar uno que difiere solo en el último carácter.

Un atacante sofisticado puede medir estos tiempos de respuesta (timing attack / side-channel
attack) con miles de intentos y deducir, carácter a carácter, cuántos ya adivinó
correctamente, reduciendo el espacio de búsqueda de 2^256 a solo 64*256 intentos.

secrets.compare_digest() usa una comparación de tiempo constante: siempre compara TODOS los
caracteres sin importar si encuentra una diferencia temprana. Esto hace que el tiempo de
respuesta sea idéntico independientemente de cuántos caracteres coincidan, eliminando el
canal lateral de tiempo.
"""

if __name__ == '__main__':
    app.run(debug=False, port=5005)
