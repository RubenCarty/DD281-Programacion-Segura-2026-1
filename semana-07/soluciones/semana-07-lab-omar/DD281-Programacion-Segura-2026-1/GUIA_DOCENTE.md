# 👨‍🏫 GUÍA COMPLETA DEL DOCENTE
# DD281 — Programación Segura | GitHub Workflow

> **Solo para el docente (RubenCarty).** Esta guía cubre desde la creación del repositorio hasta la revisión de PRs semanal, con todos los comandos Git explicados línea por línea.

---

## ÍNDICE

1. [Crear los repositorios en GitHub](#1-crear-los-repositorios-en-github)
2. [Configurar tu entorno local](#2-configurar-tu-entorno-local)
3. [Clonar y configurar el repo localmente](#3-clonar-y-configurar-el-repo-localmente)
4. [Flujo semanal del docente](#4-flujo-semanal-del-docente)
5. [Comandos para actualizar el repo remoto](#5-comandos-para-actualizar-el-repo-remoto)
6. [Revisar y aprobar PRs de estudiantes](#6-revisar-y-aprobar-prs-de-estudiantes)
7. [Comandos Git de emergencia](#7-comandos-git-de-emergencia)
8. [Buenas prácticas de gestión del repo](#8-buenas-prácticas-de-gestión-del-repo)

---

## 1. CREAR LOS REPOSITORIOS EN GITHUB

### PASO A — Crear el repositorio principal del curso

1. Ve a **github.com** → Inicia sesión como `RubenCarty`
2. Clic en **"+"** (esquina superior derecha) → **"New repository"**
3. Configura así:

| Campo | Valor |
|---|---|
| **Repository name** | `DD281-Programacion-Segura-2026-1` |
| **Description** | `Curso de Programación Segura DD281 — Universidad Autónoma del Perú 2026-1` |
| **Visibility** | **Public** ✅ (para que los estudiantes puedan hacer fork) |
| **Add a README file** | ✅ (marcar) |
| **Add .gitignore** | Python (seleccionar) |
| **Choose a license** | MIT License |

4. Clic en **"Create repository"**

### PASO B — Crear los 5 repositorios de proyectos

Repite el proceso para cada uno (los 5 deben ser **Public**):

```
PS-P1-SecureAuth-Platform
PS-P2-SecureBank-API
PS-P3-HealthPortal-Secure
PS-P4-SecureVoting-System
PS-P5-PenTest-Toolkit
```

### PASO C — Configurar protección de la rama main

Para el repo principal (y cada proyecto):
1. Ve al repo → **Settings** → **Branches**
2. Clic en **"Add branch protection rule"**
3. Branch name pattern: `main`
4. Activa:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals** → 1
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**
   - ✅ **Require status checks to pass before merging** (si tienes CI)
5. Clic **"Create"**

> **¿Por qué proteger main?** Evita que alguien (accidentalmente o no) haga push directo al repo oficial. Todos los cambios pasan por PR → tú los revisas → tú los apruebas.

---

## 2. CONFIGURAR TU ENTORNO LOCAL

### Verificar que tienes Git instalado

```bash
git --version
# Debe mostrar: git version 2.x.x
```

### Configurar tu identidad Git (solo la primera vez)

```bash
git config --global user.name "Ruben Quispe Llacctarimay"
# ↑ Establece tu nombre para todos los commits de tu máquina

git config --global user.email "rubencarty4@gmail.com"
# ↑ Establece tu email (debe coincidir con tu cuenta GitHub)

git config --global core.editor "code"
# ↑ Usa VS Code como editor por defecto (opcional)

git config --global init.defaultBranch main
# ↑ Asegura que la rama inicial siempre se llame "main" (estándar actual)
```

### Verificar la configuración

```bash
git config --global --list
# Muestra todos los valores configurados globalmente
# Debes ver: user.name, user.email, etc.
```

### Autenticación con GitHub (recomendado: Personal Access Token)

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Clic **"Generate new token (classic)"**
3. Nombre: `DD281-MacBook-2026`
4. Expiration: 90 days
5. Permisos: ✅ `repo` (completo) + ✅ `workflow`
6. Clic **"Generate token"** → **Copia el token** (solo se muestra una vez)

Cuando Git pida contraseña, usa el token como password.

---

## 3. CLONAR Y CONFIGURAR EL REPO LOCALMENTE

### Clonar el repositorio principal

```bash
# 1. Navega al directorio donde quieres tener el repo
cd ~/Documents/Universidad/DD281
# ↑ Puedes elegir cualquier ruta — este es solo un ejemplo

# 2. Clonar el repositorio desde GitHub
git clone https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git
# ↑ Descarga todos los archivos del repo remoto a tu máquina local
# ↑ Crea una carpeta con el nombre del repo automáticamente

# 3. Entrar al directorio del proyecto
cd DD281-Programacion-Segura-2026-1
# ↑ Ahora estás DENTRO del repositorio local

# 4. Verificar que la conexión remota está correcta
git remote -v
# ↑ Muestra los repositorios remotos configurados
# Debe mostrar:
# origin  https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git (fetch)
# origin  https://github.com/RubenCarty/DD281-Programacion-Segura-2026-1.git (push)
```

### Copiar los materiales que ya tienes localmente al repo

```bash
# Copia los archivos de tu carpeta de Drive al repo clonado
cp -r "/Users/rubenquispellacctarimay/My Drive/U. Autónoma 2026-1/Programación Segura/S2/"* \
      ./semana-02/
# ↑ Copia el contenido de la S2 que ya preparaste al repositorio local

# Verifica qué archivos se copiaron
ls semana-02/
```

---

## 4. FLUJO SEMANAL DEL DOCENTE

### Antes de cada semana — Subir el material de la semana

```bash
# PASO 1: Actualizar tu repo local con lo que hay en GitHub
# (por si hiciste algún cambio desde GitHub.com)
git pull origin main
# ↑ "pull" = traer (jalar) cambios del remoto al local
# ↑ "origin" = nombre del repositorio remoto (por defecto)
# ↑ "main" = rama principal

# PASO 2: Verificar el estado actual del repo
git status
# ↑ Muestra qué archivos han cambiado, cuáles están listos para commit
# Verde = listos para commit (staged)
# Rojo = modificados pero NO preparados para commit (unstaged)

# PASO 3: Agregar los archivos de la nueva semana
# Opción A: Agregar todos los archivos de una semana específica
git add semana-03/
# ↑ Prepara (stage) todos los archivos dentro de semana-03/

# Opción B: Agregar un archivo específico
git add semana-03/guia-trabajo/GT_S03_ValidacionEntrada.md
# ↑ Solo prepara ese archivo específico

# Opción C: Agregar TODOS los cambios (úsalo con cuidado)
git add .
# ↑ El punto (.) significa "todo en el directorio actual y subcarpetas"

# PASO 4: Verificar qué se va a incluir en el commit
git status
# ↑ Los archivos en verde (staged) son los que irán en el próximo commit

# PASO 5: Crear el commit con un mensaje descriptivo
git commit -m "feat(s03): agrega guía de trabajo y laboratorio de validación de entrada"
# ↑ "commit" = guarda una "foto" del estado actual con un mensaje
# ↑ Convención de mensajes:
#    feat(sXX): nueva funcionalidad / nuevo material
#    fix(sXX):  corrección de un error en el material
#    docs(sXX): actualización de documentación
#    chore:     tareas de mantenimiento (actualizar .gitignore, etc.)

# PASO 6: Subir al repositorio remoto en GitHub
git push origin main
# ↑ "push" = enviar (empujar) tus commits locales al repo remoto
# ↑ "origin" = el repositorio remoto
# ↑ "main" = la rama que subes
# Después de esto, los cambios son visibles en github.com
```

### Resumen del flujo semanal (memorízalo)

```
pull → edit files → add → commit → push
  ↑          ↑       ↑       ↑       ↑
Traer    Trabajar  Staging Guardar  Subir
cambios  localmente         snapshot  a GitHub
```

---

## 5. COMANDOS PARA ACTUALIZAR EL REPO REMOTO

### Comandos esenciales explicados

```bash
# ─── VER EL ESTADO ────────────────────────────────────────────────
git status
# ¿Para qué? Ver qué archivos cambiaron y cuáles están staged.
# Úsalo SIEMPRE antes de hacer add y commit.

git log --oneline -10
# ¿Para qué? Ver los últimos 10 commits con su ID corto y mensaje.
# Útil para saber dónde estás y qué se hizo recientemente.

git diff
# ¿Para qué? Ver exactamente qué líneas cambiaron en los archivos unstaged.
# Líneas con + = agregadas (verde), con - = eliminadas (rojo).

# ─── PREPARAR CAMBIOS ─────────────────────────────────────────────
git add archivo.md
# ¿Para qué? Agregar un archivo específico al área de staging.

git add carpeta/
# ¿Para qué? Agregar todos los archivos dentro de una carpeta.

git add .
# ¿Para qué? Agregar TODOS los archivos modificados.
# ⚠️ Úsalo con cuidado — verifica git status antes.

git reset HEAD archivo.md
# ¿Para qué? SACAR un archivo del área de staging (deshacer git add).
# No elimina los cambios, solo los quita del próximo commit.

# ─── GUARDAR Y SUBIR ──────────────────────────────────────────────
git commit -m "mensaje descriptivo"
# ¿Para qué? Crear un snapshot permanente de los archivos staged.
# El mensaje debe explicar QUÉ y POR QUÉ (no "actualización").

git push origin main
# ¿Para qué? Enviar todos los commits locales nuevos al repo de GitHub.
# Requiere conexión a internet y autenticación.

git pull origin main
# ¿Para qué? Traer todos los commits nuevos del repo remoto al local.
# Úsalo al inicio de cada sesión de trabajo para estar actualizado.

# ─── RAMAS (para trabajo avanzado) ───────────────────────────────
git checkout -b semana-04-material
# ¿Para qué? Crear una nueva rama y cambiarte a ella.
# Útil cuando quieres preparar material sin afectar main todavía.

git checkout main
# ¿Para qué? Volver a la rama principal.

git merge semana-04-material
# ¿Para qué? Fusionar la rama de trabajo a la rama actual (main).
# Solo después de que el material esté completo.

git branch -d semana-04-material
# ¿Para qué? Eliminar la rama local que ya fue fusionada.

# ─── ETIQUETAS (para marcar entregas) ────────────────────────────
git tag -a v1.0-semana01 -m "Material completo de la Semana 1"
# ¿Para qué? Marcar un punto específico del historial con un nombre.
# Útil para marcar cierre de cada semana.

git push origin --tags
# ¿Para qué? Subir las etiquetas al repositorio remoto.
```

### Flujo completo de actualización semanal (copiar y adaptar)

```bash
# === INICIO DE SEMANA: Preparar material nuevo ===

# 1. Asegúrate de estar en la rama main y actualizado
git checkout main
git pull origin main

# 2. Crea y coloca los archivos de la nueva semana en la carpeta correcta
# (usa tu editor o copia desde tu Drive)

# 3. Verifica qué cambió
git status

# 4. Revisa el contenido de lo que vas a subir
git diff

# 5. Agrega los archivos de la semana
git add semana-04/

# 6. Confirma qué se va a commitear
git status

# 7. Crea el commit
git commit -m "feat(s04): agrega guia de trabajo, laboratorio y material semana 4 - sesiones seguras"

# 8. Sube al remoto
git push origin main

# 9. Verifica en GitHub que los archivos aparezcan
# → github.com/RubenCarty/DD281-Programacion-Segura-2026-1

# === CIERRE DE SEMANA: Etiquetar ===
git tag -a v1.0-s04-publicada -m "Semana 4 publicada - Gestión de Sesiones"
git push origin --tags
```

---

## 6. REVISAR Y APROBAR PRs DE ESTUDIANTES

### ¿Cómo funciona el flujo Fork + PR?

```
Repo del docente (original)         Repo del estudiante (fork)
github.com/RubenCarty/DD281-...     github.com/EstudianteX/DD281-...
         │                                     │
         │ ── fork ──────────────────────────► │
         │                                     │
         │                                estudiante trabaja
         │                                sube sus cambios
         │                                abre un PR
         │ ◄─── Pull Request ──────────────────│
         │                                     │
    Docente revisa, comenta y aprueba (o rechaza)
         │
    merge (fusiona) la solución
```

### Pasos para revisar un PR

**Desde GitHub.com (método visual):**

1. Ve a tu repo → pestaña **"Pull requests"**
2. Verás la lista de PRs pendientes de los estudiantes
3. Clic en un PR → verás:
   - **Archivos cambiados** (qué subió el estudiante)
   - **Commits** (historial de cambios)
   - **Conversation** (para comentar)

4. Para comentar líneas específicas:
   - Pestaña **"Files changed"**
   - Hover sobre una línea → clic en el `+`
   - Escribe tu comentario técnico
   - Clic **"Start a review"**

5. Para aprobar y fusionar:
   - Clic **"Review changes"** → **"Approve"** → **"Submit review"**
   - Clic **"Merge pull request"** → **"Confirm merge"**

6. Para rechazar (solicitar correcciones):
   - Clic **"Review changes"** → **"Request changes"** → escribe qué falta → **"Submit review"**
   - El estudiante verá los comentarios y debe corregir

**Desde la línea de comandos (para revisión profunda):**

```bash
# Ver todos los PRs abiertos (requiere GitHub CLI: gh)
gh pr list

# Descargar el código del PR #5 para revisarlo localmente
gh pr checkout 5
# ↑ Descarga la rama del PR en tu máquina para probarla

# Ver el diff del PR #5
gh pr diff 5

# Aprobar el PR #5 con comentario
gh pr review 5 --approve --body "Excelente implementación. bcrypt correcto, SQL Injection prevenido con PreparedStatement."

# Solicitar cambios en el PR #5
gh pr review 5 --request-changes --body "Falta el rate limiting en el endpoint de login. Ver comentarios en línea."

# Fusionar el PR #5
gh pr merge 5 --squash --message "merge(s02): solución de QUISPE_CARLOS - login seguro S2"
```

### Checklist de revisión de PR semanal

Para cada PR de estudiante, verifica:

```markdown
## Checklist de revisión — PR S02

### Estructura
- [ ] El PR tiene descripción completa (no está vacía)
- [ ] Los archivos están en la carpeta correcta: semana-02/soluciones/APELLIDO_NOMBRE/
- [ ] No incluye archivos sensibles (.env, *.key, tokens)
- [ ] Incluye todos los entregables requeridos

### Contenido técnico — Semana 2
- [ ] La guía de trabajo está completada (Secciones A-F)
- [ ] El laboratorio tiene el código de login implementado
- [ ] El certificado SSL fue generado (evidencia)
- [ ] Usa bcrypt (no MD5, SHA-1 ni texto plano)
- [ ] Usa PreparedStatement (no concatenación en SQL)
- [ ] El login usa POST (no GET)
- [ ] Incluye capturas de pantalla o screenshots de pruebas
- [ ] Incluye el archivo auth.log con evidencia de pruebas

### Código
- [ ] No tiene contraseñas hardcodeadas
- [ ] No sube server.key (clave privada SSL)
- [ ] El código es funcional (al menos parcialmente)
- [ ] Hay comentarios explicativos en el código
```

---

## 7. COMANDOS GIT DE EMERGENCIA

```bash
# ── DESHACER EL ÚLTIMO COMMIT (sin perder los cambios) ────────────
git reset --soft HEAD~1
# ¿Cuándo? Si cometiste un error en el mensaje del commit o
# añadiste archivos incorrectos. Los cambios vuelven a "staged".

# ── DESHACER CAMBIOS EN UN ARCHIVO (volver al último commit) ──────
git checkout -- archivo.md
# ¿Cuándo? Si modificaste un archivo y quieres descartar esos cambios.
# ⚠️ Esta acción es irreversible — los cambios se pierden.

# ── VER HISTORIAL COMPLETO CON GRÁFICO DE RAMAS ───────────────────
git log --oneline --graph --all
# ¿Cuándo? Para visualizar el historial y las ramas visualmente.

# ── GUARDAR CAMBIOS TEMPORALMENTE (sin commitear) ─────────────────
git stash
# ¿Cuándo? Necesitas hacer git pull pero tienes cambios a medio hacer.
# Los cambios se guardan temporalmente.

git stash pop
# ¿Cuándo? Para recuperar los cambios guardados con stash.

# ── RESOLVER CONFLICTOS ───────────────────────────────────────────
# Cuando git pull dice "CONFLICT":
# 1. Abre el archivo con conflicto (tiene marcadores <<<, ===, >>>)
# 2. Edita el archivo dejando solo la versión correcta
# 3. git add archivo.md
# 4. git commit -m "fix: resuelve conflicto en semana-03/README.md"

# ── ELIMINAR ARCHIVO DEL TRACKING (sin borrarlo del disco) ────────
git rm --cached server.key
# ¿Cuándo? Subiste accidentalmente un archivo que no deberías
# (como una clave privada). Esto lo quita del repositorio.
echo "server.key" >> .gitignore
git commit -m "chore: elimina clave privada del tracking"

# ── FORZAR ACTUALIZACIÓN (úsalo solo en emergencias) ─────────────
git push origin main --force
# ⚠️ PELIGROSO: Sobrescribe el historial remoto.
# Solo si el repo es tuyo y nadie más ha hecho fetch del commit incorrecto.
```

---

## 8. BUENAS PRÁCTICAS DE GESTIÓN DEL REPO

### .gitignore recomendado para el curso

El archivo `.gitignore` ya viene configurado. Asegúrate de que incluya:

```gitignore
# Claves SSL y certificados privados
*.key
*.pem
*.p12
*.pfx

# Variables de entorno y secrets
.env
.env.*
secrets.json
config.local.*

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
venv/
.venv/

# Bases de datos locales
*.db
*.sqlite
*.sqlite3

# IDEs
.vscode/
.idea/
*.swp

# macOS
.DS_Store
Thumbs.db

# Logs (excepto auth.log de laboratorio cuando se requiera)
*.log
!semana-*/laboratorio/ejemplos/auth.log

# Jupyter
.ipynb_checkpoints/
```

### Calendario de revisión de PRs recomendado

| Día | Acción |
|---|---|
| **Lunes** (inicio de semana) | Publicar material de la semana (`git push`) |
| **Viernes** (cierre de entrega) | Los estudiantes deben tener su PR abierto |
| **Sábado-Domingo** | Revisar y comentar PRs |
| **Lunes siguiente** | Abrir nuevos PRs (correcciones) o aprobar |

### Labels de GitHub para clasificar PRs

Crea estos labels en GitHub.com (Settings → Labels):

| Label | Color | Uso |
|---|---|---|
| `semana-01` a `semana-08` | Azul | Identifica la semana |
| `aprobado` | Verde | PR revisado y aprobado |
| `necesita-correccion` | Rojo | Hay errores que corregir |
| `pendiente-revision` | Amarillo | En cola de revisión |
| `incompleto` | Naranja | Falta contenido requerido |
| `excelente` | Morado | Trabajo destacado |

---

## RESUMEN VISUAL — FLUJO COMPLETO DOCENTE

```
INICIO DE SEMANA:
git pull → copiar material → git add → git commit → git push
                                                        ↓
                                              Estudiantes ven el material

DURANTE LA SEMANA:
Estudiantes hacen Fork → trabajan → PR

FIN DE SEMANA (revisión):
gh pr list → revisar cada PR → comentar → aprobar/rechazar

CIERRE SEMANA:
git tag → git push --tags
```

---

*Guía Docente — DD281 Programación Segura | Universidad Autónoma del Perú | 2026-1*
