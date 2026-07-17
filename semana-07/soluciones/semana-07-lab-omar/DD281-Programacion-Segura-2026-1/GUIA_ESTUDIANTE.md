# 📚 GUÍA COMPLETA DEL ESTUDIANTE
# DD281 — Programación Segura | GitHub Workflow

> Sigue esta guía paso a paso para subir tus actividades semanales. Si tienes dudas, abre un Issue usando la plantilla de pregunta académica.

---

## ÍNDICE

1. [Configuración inicial (solo una vez)](#1-configuración-inicial-solo-una-vez)
2. [Hacer Fork del repositorio del curso](#2-hacer-fork-del-repositorio-del-curso)
3. [Clonar tu Fork a tu computadora](#3-clonar-tu-fork-a-tu-computadora)
4. [Flujo de trabajo semanal](#4-flujo-de-trabajo-semanal)
5. [Crear y enviar tu Pull Request](#5-crear-y-enviar-tu-pull-request)
6. [Actualizar tu Fork cuando el docente sube material nuevo](#6-actualizar-tu-fork-cuando-el-docente-sube-material-nuevo)
7. [Buenas prácticas y errores comunes](#7-buenas-prácticas-y-errores-comunes)
8. [Preguntas frecuentes](#8-preguntas-frecuentes)

---

## 1. CONFIGURACIÓN INICIAL (solo una vez)

### Instalar Git

- **Windows:** Descarga desde https://git-scm.com/download/win
- **macOS:** Abre Terminal y escribe `git --version` (se instalará automáticamente)
- **Linux:** `sudo apt install git` o `sudo dnf install git`

Verifica que está instalado:
```bash
git --version
# Debe mostrar: git version 2.x.x
```

### Crear cuenta en GitHub

1. Ve a **https://github.com**
2. Clic en **"Sign up"**
3. Usa tu email universitario si puedes (da acceso a GitHub Education con beneficios gratuitos)
4. Elige un nombre de usuario profesional (ej: `jlopez-dev`, `mgarcia-uap`)

### Configurar Git con tu identidad

Abre Terminal (Mac/Linux) o Git Bash (Windows) y escribe:

```bash
git config --global user.name "Tu Nombre Completo"
# ↑ Reemplaza con TU nombre real

git config --global user.email "tu_email@universidad.edu.pe"
# ↑ Usa el mismo email de tu cuenta GitHub

git config --global init.defaultBranch main
# ↑ Configuración estándar — rama principal se llama "main"
```

---

## 2. HACER FORK DEL REPOSITORIO DEL CURSO

**Fork** = Crear una copia personal del repositorio del docente en TU cuenta GitHub.

> Solo haces esto UNA VEZ al inicio del curso. El mismo Fork lo usas las 8 semanas.

### Pasos:

1. Ve al repositorio del curso:
   `https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1`

2. Clic en el botón **"Fork"** (esquina superior derecha)

3. En la pantalla que aparece:
   - **Owner:** Tu cuenta de GitHub (selecciónala)
   - **Repository name:** Déjalo igual (`DD281-Programacion-Segura-2026-1`)
   - Clic en **"Create fork"**

4. GitHub te redirige a TU copia del repo:
   `https://github.com/TU_USUARIO/DD281-Programacion-Segura-2026-1`

---

## 3. CLONAR TU FORK A TU COMPUTADORA

```bash
# 1. Navega a donde quieres guardar el repo
cd ~/Documentos
# ↑ Puedes usar cualquier carpeta de tu computadora

# 2. Clonar TU fork (no el del docente)
git clone https://github.com/TU_USUARIO/DD281-Programacion-Segura-2026-1.git
# ↑ Reemplaza TU_USUARIO con tu nombre de usuario GitHub
# ↑ Esto descarga todos los archivos a tu computadora

# 3. Entrar al directorio
cd DD281-Programacion-Segura-2026-1

# 4. Conectar con el repo original del docente (upstream)
git remote add upstream https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git
# ↑ "upstream" = el repositorio original del docente
# ↑ Esto te permite descargar material nuevo cuando el docente lo suba

# 5. Verifica la configuración
git remote -v
# Debe mostrar:
# origin    https://github.com/TU_USUARIO/DD281-Programacion-Segura-2026-1.git (fetch)
# origin    https://github.com/TU_USUARIO/DD281-Programacion-Segura-2026-1.git (push)
# upstream  https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git (fetch)
# upstream  https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git (push)
```

---

## 4. FLUJO DE TRABAJO SEMANAL

### PASO A — Actualizar tu Fork con el material nuevo del docente

Antes de empezar cada semana, trae el material nuevo:

```bash
# 1. Traer cambios del repo del docente
git fetch upstream
# ↑ Descarga los cambios del upstream (docente) sin aplicarlos todavía

# 2. Asegúrate de estar en main
git checkout main
# ↑ Cambia a la rama principal

# 3. Aplicar los cambios del docente a tu rama main
git merge upstream/main
# ↑ Fusiona el material nuevo del docente en tu copia local

# 4. Subir la actualización a tu Fork en GitHub
git push origin main
# ↑ Sincroniza tu Fork en GitHub con los cambios del docente
```

Ahora verás el material nuevo (guía de trabajo, laboratorio) en tu repo.

### PASO B — Crear tu carpeta de trabajo

Cada semana debes trabajar en TU carpeta personal:

```bash
# Crear tu carpeta dentro de soluciones de la semana actual
mkdir -p semana-02/soluciones/APELLIDO_NOMBRE
# ↑ Reemplaza APELLIDO_NOMBRE con tu apellido y nombre
# ↑ Ejemplo: GARCIA_JUAN o LOPEZ_MARIA
# ↑ Usa MAYÚSCULAS y guiones bajos, sin espacios ni tildes

# Ejemplo correcto: QUISPE_CARLOS
# Ejemplo incorrecto: carlos quispe, CarlosQuispe, carlos_q
```

### PASO C — Completar el trabajo de la semana

Dentro de tu carpeta (`semana-02/soluciones/APELLIDO_NOMBRE/`), coloca:

```
APELLIDO_NOMBRE/
├── guia_trabajo_s02.md      ← Guía de trabajo completada
├── laboratorio/
│   ├── login_seguro.py      ← Código del laboratorio
│   ├── setup_db.py
│   ├── servidor.py
│   ├── login.html
│   └── capturas/           ← Screenshots de tus pruebas
│       ├── prueba_login_exitoso.png
│       ├── prueba_sql_injection.png
│       └── auth.log
└── reflexion_s02.md         ← (Opcional) Tu análisis personal
```

> **IMPORTANTE:** No subas archivos sensibles:
> - NO subir `server.key` (clave privada SSL)
> - NO subir `.env` o archivos con contraseñas reales
> - NO subir `*.db` si tiene datos personales

### PASO D — Registrar tus cambios en Git

```bash
# 1. Verificar qué archivos nuevos tienes
git status
# ↑ Verás tus archivos en rojo (no registrados aún)

# 2. Agregar TUS archivos (solo los tuyos)
git add semana-02/soluciones/GARCIA_JUAN/
# ↑ Reemplaza con tu carpeta

# 3. Verificar que se agregaron correctamente
git status
# ↑ Ahora deben aparecer en verde

# 4. Crear el commit con un mensaje descriptivo
git commit -m "feat(s02): completa guia de trabajo y laboratorio login seguro - GARCIA JUAN"
# ↑ El mensaje sigue este formato:
#   feat(sXX): descripción - APELLIDO NOMBRE

# 5. Subir al tu Fork en GitHub
git push origin main
# ↑ Esto sube tu trabajo a tu repositorio en github.com
```

---

## 5. CREAR Y ENVIAR TU PULL REQUEST

**Pull Request (PR)** = Solicitar al docente que revise e incorpore tu trabajo al repo oficial.

> Debes hacer UN PR por semana.

### Pasos para crear el PR:

1. Ve a TU fork en GitHub:
   `https://github.com/TU_USUARIO/DD281-Programacion-Segura-2026-1`

2. GitHub mostrará un banner amarillo: **"Compare & pull request"** → Clic ahí
   - Si no aparece: clic en **"Pull requests"** → **"New pull request"**

3. Verifica que la dirección es correcta:
   - **base repository:** `RubenCarty/DD281-Programacion-Segura-2026-1` → `main`
   - **head repository:** `TU_USUARIO/DD281-Programacion-Segura-2026-1` → `main`

4. **Completa el formulario del PR** (usa la plantilla que aparece automáticamente):

```markdown
## Información del Estudiante
- **Nombre:** Juan García López
- **Semana:** 02
- **Tema:** Especificación Formal de Seguridad y Login Seguro

## ¿Qué entrego?
- [x] Guía de trabajo completada (Secciones A-F)
- [x] Laboratorio: login seguro con bcrypt
- [x] Capturas de pantalla de las 6 pruebas
- [x] Reflexión personal

## Dificultades encontradas
Tuve dificultad configurando SSL con OpenSSL en Windows. Usé WSL2 para solucionarlo.

## Preguntas para el docente
¿El rate limiting en Flask funciona igual que en CGI puro?
```

5. Clic en **"Create pull request"**

### Verificar que tu PR fue enviado

- Ve a: `https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1/pulls`
- Debes ver tu PR listado ahí

---

## 6. ACTUALIZAR TU FORK CUANDO EL DOCENTE SUBE MATERIAL NUEVO

El docente sube material nuevo cada semana. Para obtenerlo:

```bash
# Opción A — Desde la línea de comandos
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Opción B — Desde GitHub.com (más fácil)
# 1. Ve a tu fork en GitHub
# 2. Clic en "Sync fork" (botón gris)
# 3. Clic en "Update branch"
# 4. Luego en tu computadora: git pull origin main
```

---

## 7. BUENAS PRÁCTICAS Y ERRORES COMUNES

### Buenas prácticas

| Haz esto | No hagas esto |
|---|---|
| Commits pequeños y frecuentes | Un solo commit al final con todo |
| Mensajes de commit descriptivos | `git commit -m "actualización"` |
| Trabajar en TU carpeta únicamente | Modificar archivos de otros estudiantes |
| Verificar `git status` antes de commit | Hacer commit sin revisar qué se sube |
| Abrir el PR antes del cierre de semana | Esperar al último día |
| Completar el formulario del PR | Dejar el PR en blanco o con "..." |

### Errores comunes y soluciones

**Error: "Your branch is behind 'origin/main'"**
```bash
git pull origin main
# Sincroniza tu rama local con tu fork remoto
```

**Error: "Nothing to commit"**
```bash
git status
# Revisa si los archivos están en la carpeta correcta
ls semana-02/soluciones/TU_APELLIDO_NOMBRE/
```

**Error: Subiste un archivo que no debías (ej: una clave)**
```bash
git rm --cached server.key
echo "server.key" >> .gitignore
git commit -m "fix: elimina archivo sensible del tracking"
git push origin main
```

**Error: Conflicto al hacer merge**
```bash
# 1. Git te dice qué archivos tienen conflicto
git status
# 2. Abre esos archivos, busca los marcadores:
# <<<<<<< HEAD
# (tu versión)
# =======
# (versión del upstream)
# >>>>>>> upstream/main
# 3. Edita el archivo dejando solo lo correcto
# 4. git add archivo_resuelto.md
# 5. git commit -m "fix: resuelve conflicto en semana-01"
```

---

## 8. PREGUNTAS FRECUENTES

**¿Puedo hacer más de un commit por semana?**
Sí, es lo recomendado. Haz commit cada vez que avances algo importante.

**¿El PR tiene fecha límite?**
El docente indica la fecha de cierre cada semana. Generalmente es el viernes antes de las 23:59.

**¿Puedo actualizar mi PR después de enviarlo?**
Sí. Si el docente pide cambios o tú encuentras un error, solo haz los cambios, commit y push. El PR se actualiza automáticamente.

**¿Qué pasa si no hago el PR?**
No tendrás evidencia de entrega para esa semana. El repositorio es la evidencia oficial. Si no aparece tu PR, no hay entrega.

**¿Puedo ver el trabajo de otros estudiantes?**
Sí, el repositorio es público y puedes ver los PRs de tus compañeros. Puedes aprender de ellos, pero cada entrega debe ser tuya.

**¿Puedo usar el material de compañeros como referencia?**
Puedes revisar enfoques, pero el código que subes debe ser desarrollado y entendido por ti. La evaluación incluye defender tu código.

**¿Dónde pido ayuda técnica?**
Abre un Issue en el repositorio del curso:
`https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1/issues/new/choose`
Usa la plantilla "Pregunta Académica".

---

## RESUMEN VISUAL — LO QUE HACES CADA SEMANA

```
INICIO DE SEMANA:
git fetch upstream → git merge upstream/main → git push origin main
     ↑                       ↑                        ↑
Traer material          Aplicarlo local           Actualizar tu
del docente                                          fork GitHub

DURANTE LA SEMANA:
Trabajar en tu carpeta → git add → git commit → git push origin main

CIERRE DE SEMANA:
Abrir Pull Request en GitHub → Completar el formulario → Crear PR

DESPUÉS:
Esperar revisión del docente → Aplicar correcciones si las hay
```

---

## ESTRUCTURA DE TU ENTREGA SEMANAL

```
semana-XX/
└── soluciones/
    └── APELLIDO_NOMBRE/       ← TU CARPETA PERSONAL
        ├── guia_trabajo_sXX.md
        ├── laboratorio/
        │   ├── [tus archivos de código]
        │   └── capturas/
        └── reflexion_sXX.md   (opcional pero valorado)
```

---

*Guía Estudiante — DD281 Programación Segura | Universidad Autónoma del Perú | 2026-1*
