#!/usr/bin/env python3
import http.server
import socketserver
import os
import urllib.parse
import sqlite3
import bcrypt
import html

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

class LoginHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/login.html':
            self.serve_login_page()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/login':
            self.process_login()
    
    def serve_login_page(self):
        html_content = open('login.html').read()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def process_login(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(data)
        usuario = params.get('usuario', [''])[0]
        password = params.get('password', [''])[0]
        
        conn = sqlite3.connect('../db/usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, hash_password, rol FROM usuarios WHERE usuario = ?", (usuario,))
        fila = cursor.fetchone()
        conn.close()
        
        if fila and bcrypt.checkpw(password.encode(), fila[1].encode()):
            resultado = f"<h1>✅ Bienvenido {html.escape(usuario)}</h1><p>Rol: {fila[2]}</p>"
        else:
            resultado = "<h1>❌ Credenciales incorrectas</h1>"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(resultado.encode())
    
    def log_message(self, format, *args):
        pass

print("Servidor en http://localhost:8000")
socketserver.TCPServer(("", PORT), LoginHandler).serve_forever()
