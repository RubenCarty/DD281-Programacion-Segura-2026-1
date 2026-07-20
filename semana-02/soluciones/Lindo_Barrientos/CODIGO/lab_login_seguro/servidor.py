#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# servidor.py — Servidor HTTPS con soporte CGI para el laboratorio
# ══════════════════════════════════════════════════════════════════
import ssl
import http.server
import os
import sys

# Directorios del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_DIR  = os.path.join(BASE_DIR, "www")

# Cambiar al directorio www para servir archivos estáticos
os.chdir(BASE_DIR)

# Configuración del servidor
PUERTO    = 8443
CERT_FILE = os.path.join(BASE_DIR, "certs", "server.crt")
KEY_FILE  = os.path.join(BASE_DIR, "certs", "server.key")
CGI_DIR   = os.path.join(BASE_DIR, "cgi-bin")

class MiHandler(http.server.CGIHTTPRequestHandler):
    """Handler personalizado para servir CGI y archivos estáticos."""

    # Directorio de scripts CGI
    cgi_directories = ["/cgi-bin"]

    def translate_path(self, path):
        """Redirige / a /login.html y sirve estáticos desde www/."""
        if path == "/":
            path = "/login.html"

        # Si es CGI, usar la ruta base
        if path.startswith("/cgi-bin/"):
            return os.path.join(BASE_DIR, path[1:])

        # Archivos estáticos desde www/
        return os.path.join(WWW_DIR, path.lstrip("/"))

    def log_message(self, format, *args):
        """Personaliza el log del servidor."""
        print(f"[SERVIDOR] {self.address_string()} - {format % args}")

def iniciar_servidor():
    # Verificar que existen los certificados
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("ERROR: No se encontraron los certificados SSL.")
        print(f"  Buscando: {CERT_FILE}")
        print(f"  Buscando: {KEY_FILE}")
        print("\nEjecuta primero los comandos OpenSSL de la Parte 1.2")
        sys.exit(1)

    # Crear contexto SSL
    contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Cargar certificado y clave privada
    contexto_ssl.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Opciones de seguridad del contexto SSL
    contexto_ssl.minimum_version = ssl.TLSVersion.TLSv1_2   # TLS 1.2 mínimo
    contexto_ssl.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:!aNULL')

    # Crear servidor HTTP
    servidor = http.server.HTTPServer(('localhost', PUERTO), MiHandler)

    # Envolver con SSL
    servidor.socket = contexto_ssl.wrap_socket(
        servidor.socket, 
        server_side=True
    )

    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║           SERVIDOR HTTPS INICIADO — LABORATORIO S2              ║
╠══════════════════════════════════════════════════════════════════╣
║  URL:          https://localhost:{PUERTO}                          ║
║  CGI:          https://localhost:{PUERTO}/cgi-bin/               ║
║  Certificado:  {CERT_FILE[-40:]:40}  ║
║  TLS mínimo:   TLS 1.2                                          ║
╠══════════════════════════════════════════════════════════════════╣
║  ⚠️  El navegador mostrará alerta de certificado autofirmado.   ║
║     Acepta la excepción de seguridad para continuar.            ║
╠══════════════════════════════════════════════════════════════════╣
║  Ctrl+C para detener el servidor                                ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()
