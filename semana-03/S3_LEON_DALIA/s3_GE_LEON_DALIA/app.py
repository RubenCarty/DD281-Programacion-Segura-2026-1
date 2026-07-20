app.config.update(
    SESSION_COOKIE_HTTPONLY = True,   # protege contra XSS
    SESSION_COOKIE_SECURE   = False,  # True en producción con HTTPS
    SESSION_COOKIE_SAMESITE = 'Strict' # evita CSRF
)
