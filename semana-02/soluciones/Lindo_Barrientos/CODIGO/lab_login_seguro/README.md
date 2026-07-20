# README — Cómo ejecutar el laboratorio (Login Seguro S2)

> **Requisito de versión:** usa **Python 3.12** (o 3.11) o **WSL2 (Ubuntu)**.
> Con Python 3.13+ falla en `import cgi` (el módulo fue eliminado).

## 0. Instalar dependencia

```bash
pip install bcrypt
```

## 1. Generar el certificado SSL autofirmado

Desde la carpeta `lab_login_seguro/`:

```bash
# A) Clave privada RSA de 2048 bits
openssl genrsa -out certs/server.key 2048

# B) CSR (no interactivo, con CN=localhost — OBLIGATORIO para el lab)
openssl req -new -key certs/server.key -out certs/server.csr \
  -subj "/C=PE/ST=Lima/L=Lima/O=UnivAutonoma/OU=Ingenieria/CN=localhost"

# C) Autofirmar el certificado (válido 365 días)
openssl x509 -req -days 365 -in certs/server.csr \
  -signkey certs/server.key -out certs/server.crt

# D) (Linux/WSL) proteger la clave privada
chmod 600 certs/server.key
```

## 2. Inicializar la base de datos

```bash
python3 setup_db.py
```

Crea `db/usuarios.db` con 4 usuarios de prueba (hash bcrypt factor 12).

## 3. (Linux/WSL) Dar permisos de ejecución a los CGI

```bash
chmod 755 cgi-bin/login_seguro.py cgi-bin/login_inseguro.py
```

## 4. Iniciar el servidor

```bash
python3 servidor.py
```

Abre el navegador en **https://localhost:8443** y acepta la excepción del certificado autofirmado.

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `juan.garcia` | `MiPassword123!` | estudiante |
| `maria.lopez` | `SecurePass456#` | estudiante |
| `prof.rodriguez` | `DocPass789$` | docente |
| `admin` | `AdminSuper012!` | administrador |

## ⚠️ Antes de subir al repositorio (importante)

NO subas la clave privada ni la BD. Agrega esto a tu `.gitignore`:

```
certs/server.key
certs/server.csr
db/*.db
logs/*.log
```

El entregable incluye `certs/server.crt` (solo el certificado), el código, `logs/auth.log` (de tus pruebas) y el informe. **Nunca `server.key`.**
