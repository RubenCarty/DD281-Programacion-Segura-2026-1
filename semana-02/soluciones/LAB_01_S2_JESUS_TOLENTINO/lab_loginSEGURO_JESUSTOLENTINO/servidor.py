#!/usr/bin/env python3
import io
import datetime
import ipaddress
import os
import runpy
import ssl
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_DIR = os.path.join(BASE_DIR, "www")
CERT_FILE = os.path.join(BASE_DIR, "certs", "server.crt")
KEY_FILE = os.path.join(BASE_DIR, "certs", "server.key")
PUERTO = 8443


def generar_certificado_local():
    """Genera un par certificado/clave local cuando server.key no fue entregado."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    os.makedirs(os.path.dirname(CERT_FILE), exist_ok=True)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    nombre = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "PE"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Lima"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Lima"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Universidad Autonoma"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ]
    )
    ahora = datetime.datetime.now(datetime.timezone.utc)
    certificado = (
        x509.CertificateBuilder()
        .subject_name(nombre)
        .issuer_name(nombre)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(ahora - datetime.timedelta(minutes=1))
        .not_valid_after(ahora + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    with open(KEY_FILE, "wb") as archivo:
        archivo.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )
    with open(CERT_FILE, "wb") as archivo:
        archivo.write(certificado.public_bytes(serialization.Encoding.PEM))
    print("Certificado y clave local generados en certs/.")


class Handler(BaseHTTPRequestHandler):
    def security_headers(self):
        self.send_header("Strict-Transport-Security", "max-age=31536000")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            path = "/login.html"
        if path == "/login.html":
            with open(os.path.join(WWW_DIR, "login.html"), "rb") as archivo:
                data = archivo.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.security_headers()
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/cgi-bin/login_seguro.py":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        old_env = {
            key: os.environ.get(key)
            for key in ("REQUEST_METHOD", "REMOTE_ADDR", "CGI_BODY")
        }
        os.environ.update(
            {
                "REQUEST_METHOD": "POST",
                "REMOTE_ADDR": self.client_address[0],
                "CGI_BODY": body,
            }
        )
        output = io.StringIO()
        try:
            with redirect_stdout(output):
                runpy.run_path(
                    os.path.join(BASE_DIR, "cgi-bin", "login_seguro.py"),
                    run_name="__main__",
                )
        except SystemExit:
            pass
        finally:
            for key, value in old_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        raw = output.getvalue()
        header_text, _, html_body = raw.partition("\n\n")
        self.send_response(200)
        for line in header_text.splitlines():
            if ":" in line:
                name, value = line.split(":", 1)
                self.send_header(name.strip(), value.strip())
        self.end_headers()
        self.wfile.write(html_body.encode("utf-8"))

    def log_message(self, fmt, *args):
        print(f"[SERVIDOR] {self.address_string()} - {fmt % args}")


def iniciar_servidor():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        generar_certificado_local()
    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.minimum_version = ssl.TLSVersion.TLSv1_2
    contexto.load_cert_chain(CERT_FILE, KEY_FILE)
    servidor = ThreadingHTTPServer(("localhost", PUERTO), Handler)
    servidor.socket = contexto.wrap_socket(servidor.socket, server_side=True)
    print(f"Servidor HTTPS: https://localhost:{PUERTO}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()
