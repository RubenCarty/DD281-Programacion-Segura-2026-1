# EVALUACIÓN PARCIAL — PROGRAMACIÓN SEGURA DD281
## Universidad Autónoma del Perú · Semestre 2026-1

---

```
┌────────────────────────────────────────────────────────────────────────┐
│          EVALUACIÓN PARCIAL — PROGRAMACIÓN SEGURA DD281                │
│             INGENIERÍA DE SISTEMAS COMPUTACIONALES                     │
│                        SEMESTRE 2026-1                                 │
├────────────────────────────────────────┬───────────────────────────────┤
│ CÓDIGO DEL ESTUDIANTE: ____________    │ NÚMERO DE CLASE: __________   │
│ APELLIDOS Y NOMBRES: _______________   │ FECHA: ____________________   │
│ DOCENTE: Mg. Ruben Quispe Llacctarimay │ Duración: 300 min (5 horas)  │
└────────────────────────────────────────┴───────────────────────────────┘
```

---

## CONTEXTO DEL PROYECTO

**UQ AI SOLUTION COMPANY** es una empresa peruana emergente especializada en Inteligencia Artificial que ofrece tres líneas de servicio:

| División | Servicios |
|---|---|
| **UQ AI Solutions** | Agentes IA, chatbots empresariales, automatización, soluciones para MYPES, asistentes para salud y educación, Big Data, Programación Segura, DevSecOps |
| **UQ AI Academy** | Cursos de IA, Machine Learning, RAG, LLM, agentes inteligentes, programación segura, big data, cloud computing |
| **UQ AI Lab** | Prototipos, demos, investigación aplicada, proyectos con estudiantes, comunidad de IA |

La empresa necesita un **sitio web corporativo moderno, seguro y funcional** similar a [deeplearning.ai](https://www.deeplearning.ai/) o [landing.ai](https://landing.ai/). Tu misión es **diseñar, implementar y desplegar** este sitio aplicando los principios de **Programación Segura** vistos en clase.

> **Puedes usar IA Generativa** (Claude, GitHub Copilot, ChatGPT, Gemini) para generar código. Lo que se evalúa es que el código **funcione correctamente**, aplique **seguridad real** y tú puedas **explicar cada parte**.

---

## STACK TECNOLÓGICO OBLIGATORIO

| Capa | Tecnología | Por qué |
|---|---|---|
| **Frontend** | Next.js 14 + TypeScript + Tailwind CSS | Framework React moderno con SSR/SSG |
| **Backend** | Java Spring Boot 3.x + Spring Security | API REST robusta con seguridad integrada |
| **Base de datos** | H2 (en memoria) + JPA/Hibernate | BD embebida, sin instalación adicional |
| **Autenticación** | JWT + bcrypt (BCryptPasswordEncoder) | Programación Segura: hashing + tokens |
| **Deploy Frontend** | Vercel (gratuito) | HTTPS automático, CDN global |
| **Deploy Backend** | Railway.app o Render.com (gratuito) | Hosting Java gratuito |
| **Repositorio** | GitHub | Control de versiones, evidencia de commits |
| **Asistente IA** | Claude / GitHub Copilot / ChatGPT | Acelerar el desarrollo |

---

## DESARROLLO

### PREGUNTA 1 — Sitio Web Frontend: Landing Page UQ AI Solution *(6 puntos)*

Diseña e implementa la **Landing Page** de UQ AI Solution Company usando **Next.js 14 + Tailwind CSS**. La página debe ser moderna, responsiva y contener las siguientes secciones:

**1.1** Sección **Hero** con: nombre de la empresa, tagline ("Inteligencia Artificial para el Perú y el Mundo"), botones CTA ("Explorar Servicios", "Contactar") y una imagen/animación de fondo. *(1 punto)*

**1.2** Sección **UQ AI Solutions**: tres tarjetas de servicio con íconos, título, descripción y al menos 6 servicios visibles (agentes IA, chatbots, automatización, MYPES, salud/educación, Big Data). *(1 punto)*

**1.3** Sección **UQ AI Academy** y **UQ AI Lab**: listado visual de cursos disponibles y proyectos del laboratorio con diseño de tarjetas (cards). *(1 punto)*

**1.4** Sección **Formulario de Contacto** (Lead Form): campos Nombre, Email, Empresa, Teléfono y Mensaje. Al enviar, debe guardar el lead en el backend vía API REST. *(1 punto)*

**1.5** **Navbar responsivo** con logo, menú de navegación (Servicios, Academia, Lab, Contacto, Iniciar Sesión) y versión hamburguesa en mobile. *(1 punto)*

**1.6** **Footer** con información de la empresa, redes sociales (íconos), año, y aviso legal. El diseño general debe ser **comparable visualmente a deeplearning.ai o landing.ai** (profesional, moderno, con paleta de colores coherente). *(1 punto)*

> **Nota:** Enviar evidencia de funcionamiento en formato video mostrando el sitio en desktop y mobile. El link del video debe ser público.

---

### PREGUNTA 2 — Backend Seguro: Spring Boot + H2 + REST API *(5 puntos)*

Diseña e implementa el **backend** de UQ AI Solution usando **Java Spring Boot 3.x** con las siguientes especificaciones:

**2.1** Crear el proyecto Spring Boot con las dependencias: `Spring Web`, `Spring Security`, `Spring Data JPA`, `H2 Database`, `Lombok`, `jjwt` (para JWT). Nombre del proyecto: `T_APELLIDO_NOMBRE_backend`. *(0.5 puntos)*

**2.2** Implementar la entidad **`Usuario`** con los atributos: `id`, `nombre`, `apellidos`, `email`, `password` (hash), `rol` (`ADMIN` o `USER`), `area`. Todos los atributos son obligatorios. La contraseña **NUNCA se almacena en texto plano** — usar `BCryptPasswordEncoder`. *(1 punto)*

**2.3** Implementar la entidad **`Lead`** (contacto del formulario) con: `id`, `nombre`, `email`, `empresa`, `telefono`, `mensaje`, `fechaRegistro`. *(0.5 puntos)*

**2.4** Implementar los endpoints REST **seguros**:

| Método | Endpoint | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/api/auth/register` | Público | Registrar nuevo usuario (hash bcrypt) |
| `POST` | `/api/auth/login` | Público | Login → retorna JWT |
| `GET` | `/api/usuarios` | Solo ADMIN | Listar todos los usuarios |
| `GET` | `/api/usuarios/{id}` | ADMIN o el mismo USER | Ver usuario por ID |
| `POST` | `/api/leads` | Público | Guardar lead del formulario |
| `GET` | `/api/leads` | Solo ADMIN | Listar todos los leads |

*(1.5 puntos)*

**2.5** Configurar **Spring Security** con: CORS para el dominio frontend, CSRF desactivado (se usa JWT stateless), filtro JWT en cada request, y endpoints `/api/auth/**` y `POST /api/leads` públicos. *(1 punto)*

**2.6** Configurar **H2** con consola habilitada en `/h2-console` solo para desarrollo. Nombre de BD: `BD_apellido_nombre_T1`. Verificar con **Postman o curl** que los endpoints funcionen. *(0.5 puntos)*

---

### PREGUNTA 3 — Login Seguro y Panel de Administración *(5 puntos)*

Implementa el sistema de **autenticación y autorización segura** aplicando los conceptos de Programación Segura:

**3.1** Página `/login` en Next.js: formulario con campos Email y Contraseña, validación de campos vacíos en frontend, y llamada al endpoint `POST /api/auth/login`. Aplicar: *(1 punto)*
- No mostrar si el usuario existe o no (mensaje genérico: "Credenciales incorrectas")
- Botón con loading state mientras procesa
- Límite de intentos en frontend (bloquear botón 30s tras 3 fallos)

**3.2** El JWT recibido del backend debe almacenarse en una **cookie HttpOnly** (NO en localStorage) usando la respuesta del servidor. Configurar: `HttpOnly=true`, `Secure=true` (en producción), `SameSite=Strict`. Justifica en comentario de código por qué NO se usa localStorage. *(1 punto)*

**3.3** Implementar **rutas protegidas** en Next.js usando middleware (`middleware.ts`): si el usuario no tiene cookie JWT válida y accede a `/dashboard` o `/admin`, redirigir a `/login`. *(1 punto)*

**3.4** Panel `/dashboard` (solo usuarios autenticados): mostrar nombre del usuario logueado, rol y área. Si el rol es `ADMIN`: mostrar tabla con todos los leads registrados (consumiendo `GET /api/leads` con el JWT en el header `Authorization: Bearer <token>`). Si el rol es `USER`: solo ver su propio perfil. *(1 punto)*

**3.5** Implementar **logout seguro**: al hacer clic en "Cerrar Sesión", eliminar la cookie del servidor (set-cookie con Max-Age=0) Y limpiar cualquier estado local. Redirigir a `/login`. *(1 punto)*

---

### PREGUNTA 4 — Despliegue y Repositorio GitHub *(2 puntos)*

**4.1** Subir el proyecto a **GitHub** con mínimo **3 commits significativos** (no vale un solo commit con todo el código). Los commits deben reflejar el avance: setup inicial → features → deploy. Enviar evidencia de los commits en la nube. *(1 punto)*

**4.2** Desplegar el **frontend en Vercel** (`vercel.com`): conectar el repositorio GitHub, configurar variables de entorno (`NEXT_PUBLIC_API_URL` apuntando al backend desplegado), verificar que el sitio cargue en el dominio `.vercel.app`. Desplegar el **backend en Railway.app o Render.com**. Enviar las URLs públicas. *(1 punto)*

---

### PREGUNTA 5 — Video Evidencia de Funcionamiento *(2 puntos)*

Grabar un **video de máximo 5 minutos** mostrando:
1. El sitio web cargando desde la URL de Vercel (dominio público)
2. El formulario de contacto enviando un lead (verificar en panel admin)
3. Login con usuario ADMIN → acceso al dashboard con tabla de leads
4. Login con usuario USER → solo ve su perfil (RBAC funcionando)
5. Intento de acceder a `/dashboard` sin login → redirige a `/login`
6. Logout → cookie eliminada (mostrar en DevTools > Application > Cookies)

> El link del video debe ser **público** (YouTube no listado, Google Drive o Loom).

*(2 puntos)*

---

## RUBRICA DE CALIFICACIÓN

| ÍTEM | DESCRIPCIÓN | PUNTAJE COMPLETO | PUNTAJE PARCIAL | NO RESPONDE | TOTAL |
|---|---|---|---|---|---|
| **P1** | Landing Page Next.js | 6 | 3 | 0 | **6** |
| **P2** | Backend Spring Boot + H2 | 5 | 2.5 | 0 | **5** |
| **P3** | Login Seguro + JWT + RBAC | 5 | 2.5 | 0 | **5** |
| **P4** | GitHub + Vercel Deploy | 2 | 1 | 0 | **2** |
| **P5** | Video Evidencia | 2 | 1 | 0 | **2** |
| | | | | **SUMA TOTAL** | **20** |

---

## DETALLE DE RUBRICA POR PREGUNTA

### P1 — Landing Page (6 puntos)
| Sub-ítem | 100% | 50% | 0% |
|---|---|---|---|
| 1.1 Hero (1pt) | Hero completo, animación, CTA funcionando | Solo texto, sin diseño | Sin sección |
| 1.2 Services cards (1pt) | 6+ servicios con íconos y descripción | 3-5 servicios o sin íconos | Sin sección |
| 1.3 Academy + Lab (1pt) | Ambas secciones con cards completas | Solo una sección | Sin secciones |
| 1.4 Lead Form (1pt) | Formulario envía datos al backend OK | Formulario sin conexión al backend | Sin formulario |
| 1.5 Navbar responsive (1pt) | Funciona en desktop y mobile | Solo desktop o roto en mobile | Sin navbar |
| 1.6 Footer + diseño (1pt) | Profesional, comparable a deeplearning.ai | Diseño básico/incompleto | Sin footer |

### P2 — Backend (5 puntos)
| Sub-ítem | 100% | 50% | 0% |
|---|---|---|---|
| 2.1 Setup Spring Boot (0.5pt) | Proyecto corre sin errores | Corre con warnings | No compila |
| 2.2 Entidad Usuario + bcrypt (1pt) | Hash bcrypt correcto, nunca texto plano | Hash implementado incorrectamente | Contraseñas en texto plano |
| 2.3 Entidad Lead (0.5pt) | Todos los campos presentes | Faltan campos | Sin entidad |
| 2.4 Endpoints REST (1.5pt) | Todos los 6 endpoints funcionan | 3-5 endpoints funcionan | 0-2 endpoints |
| 2.5 Spring Security + JWT (1pt) | JWT válido, CORS configurado, filtro OK | JWT implementado pero con errores | Sin seguridad |
| 2.6 H2 configurado (0.5pt) | Consola H2 accesible, BD correcta | H2 funciona pero mal configurada | Sin H2 |

### P3 — Login Seguro (5 puntos)
| Sub-ítem | 100% | 50% | 0% |
|---|---|---|---|
| 3.1 Página login (1pt) | Validación, mensaje genérico, loading | Login funciona sin validaciones de seguridad | Sin login |
| 3.2 Cookie HttpOnly (1pt) | JWT en cookie HttpOnly, Secure, SameSite | JWT en localStorage (INSEGURO) | Sin almacenamiento token |
| 3.3 Rutas protegidas (1pt) | Middleware redirige correctamente | Protección parcial o bypasseable | Sin protección |
| 3.4 Dashboard + RBAC (1pt) | Admin ve leads, User ve solo su perfil | Solo un rol implementado | Sin dashboard |
| 3.5 Logout seguro (1pt) | Cookie eliminada en servidor, estado limpio | Solo limpia localStorage/estado local | Sin logout |

---

## GUÍA DE DESARROLLO PASO A PASO

> **Tiempo estimado con IA Generativa: 4.5 — 5.5 horas**

### HORA 1 (0:00 – 1:00) — Setup y Estructura

#### Paso 1: Crear proyecto Next.js
```bash
npx create-next-app@14 uq-ai-frontend \
  --typescript --tailwind --eslint --app --src-dir

cd uq-ai-frontend
npm install axios js-cookie @types/js-cookie lucide-react
npm run dev  # Verificar http://localhost:3000
```

**Prompt para IA (GitHub Copilot / Claude):**
> "Crea la estructura de carpetas para un proyecto Next.js 14 App Router que tiene: landing page, página de login, dashboard protegido, y middleware de autenticación con JWT en cookies HttpOnly."

#### Paso 2: Crear proyecto Spring Boot
1. Ir a [start.spring.io](https://start.spring.io/)
2. Configurar:
   - Project: **Maven**
   - Language: **Java**
   - Spring Boot: **3.2.x**
   - Group: `com.uqai`
   - Artifact: `backend`
   - Name: `T_Apellido_Nombre_backend`
   - Dependencies: **Spring Web**, **Spring Security**, **Spring Data JPA**, **H2 Database**, **Lombok**, **Validation**
3. Descargar y abrir en IntelliJ IDEA o VS Code
4. Agregar en `pom.xml`:
```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.3</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>
```

---

### HORA 2 (1:00 – 2:30) — Backend: API REST + JWT + bcrypt

#### Paso 3: Configurar application.properties
```properties
# application.properties
spring.application.name=uq-ai-backend
server.port=8080

# H2 Database
spring.datasource.url=jdbc:h2:mem:BD_apellido_nombre_T1
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true

# JWT Secret (cambia esto en producción)
jwt.secret=uqAiSolutionSecretKey2026ProgramacionSeguraDD281
jwt.expiration=86400000

# CORS
cors.allowed.origins=http://localhost:3000
```

#### Paso 4: Crear las entidades

**Prompt para IA:**
> "Crea una entidad JPA 'Usuario' con los campos: id (Long auto-generado), nombre (String, NotBlank), apellidos (String, NotBlank), email (String, Email, unique), password (String), rol (enum: ADMIN/USER), area (String). Incluye anotaciones Lombok @Data @Builder @NoArgsConstructor @AllArgsConstructor."

```java
// src/main/java/com/uqai/backend/entity/Usuario.java
@Entity
@Table(name = "usuarios")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Usuario {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    @NotBlank private String nombre;

    @Column(nullable = false)
    @NotBlank private String apellidos;

    @Column(unique = true, nullable = false)
    @Email private String email;

    @Column(nullable = false)
    private String password; // SIEMPRE hash bcrypt, nunca texto plano

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Rol rol; // ADMIN o USER

    @Column(nullable = false)
    @NotBlank private String area;
}
```

```java
// src/main/java/com/uqai/backend/entity/Lead.java
@Entity
@Table(name = "leads")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Lead {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank private String nombre;
    @Email private String email;
    private String empresa;
    private String telefono;
    @Column(length = 1000)
    private String mensaje;
    @CreationTimestamp
    private LocalDateTime fechaRegistro;
}
```

#### Paso 5: Servicio JWT

**Prompt para IA:**
> "Crea un JwtService en Spring Boot que genere y valide tokens JWT usando la librería jjwt 0.12.3. Debe tener métodos: generateToken(String email), extractEmail(String token), isTokenValid(String token, UserDetails userDetails), getExpirationDate(String token)."

```java
@Service
public class JwtService {
    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration}")
    private long expiration;

    public String generateToken(String email) {
        return Jwts.builder()
            .subject(email)
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + expiration))
            .signWith(getSigningKey())
            .compact();
    }

    public String extractEmail(String token) {
        return Jwts.parser().verifyWith(getSigningKey())
            .build().parseSignedClaims(token)
            .getPayload().getSubject();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        return extractEmail(token).equals(userDetails.getUsername())
            && !isTokenExpired(token);
    }

    private boolean isTokenExpired(String token) {
        return Jwts.parser().verifyWith(getSigningKey())
            .build().parseSignedClaims(token)
            .getPayload().getExpiration().before(new Date());
    }

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secretKey.getBytes(StandardCharsets.UTF_8));
    }
}
```

#### Paso 6: Controller de Autenticación

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<UsuarioResponse> register(@Valid @RequestBody RegisterRequest req) {
        return ResponseEntity.ok(authService.register(req));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest req) {
        // SEGURIDAD: mensaje genérico si falla (no revela si el email existe)
        try {
            return ResponseEntity.ok(authService.login(req));
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(new AuthResponse(null, null, "Credenciales incorrectas"));
        }
    }
}
```

**AuthService — aplicar bcrypt:**
```java
@Service @RequiredArgsConstructor
public class AuthService {
    private final UsuarioRepository usuarioRepo;
    private final PasswordEncoder passwordEncoder; // BCryptPasswordEncoder
    private final JwtService jwtService;
    private final AuthenticationManager authManager;

    public UsuarioResponse register(RegisterRequest req) {
        // PROGRAMACIÓN SEGURA: hash de contraseña con bcrypt antes de guardar
        Usuario usuario = Usuario.builder()
            .nombre(req.getNombre())
            .apellidos(req.getApellidos())
            .email(req.getEmail())
            .password(passwordEncoder.encode(req.getPassword())) // bcrypt aquí
            .rol(Rol.USER)
            .area(req.getArea())
            .build();
        return UsuarioResponse.from(usuarioRepo.save(usuario));
    }

    public AuthResponse login(LoginRequest req) {
        authManager.authenticate(
            new UsernamePasswordAuthenticationToken(req.getEmail(), req.getPassword())
        );
        String token = jwtService.generateToken(req.getEmail());
        Usuario u = usuarioRepo.findByEmail(req.getEmail()).orElseThrow();
        return new AuthResponse(token, u.getRol().name(), "OK");
    }
}
```

#### Paso 7: Configuración Spring Security

**Prompt para IA:**
> "Configura Spring Security 6 en Spring Boot 3 para: JWT stateless (sin sesiones), CORS permitiendo http://localhost:3000, endpoints públicos: POST /api/auth/**, POST /api/leads, GET /h2-console/**, endpoint /api/usuarios solo ADMIN, filtro JWT personalizado."

```java
@Configuration @EnableWebSecurity @RequiredArgsConstructor
public class SecurityConfig {
    private final JwtAuthFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable) // JWT es stateless, CSRF no aplica
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/h2-console/**").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/leads").permitAll()
                .requestMatchers("/api/usuarios").hasRole("ADMIN")
                .requestMatchers("/api/leads").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .headers(h -> h.frameOptions(f -> f.disable())) // Para H2 console
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("http://localhost:3000", "https://*.vercel.app"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true); // Para cookies HttpOnly
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12); // 12 rounds = seguro para 2026
    }

    @Bean
    public AuthenticationManager authManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
```

**Probar con curl:**
```bash
# Registrar admin
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","apellidos":"UQ","email":"admin@uqai.pe","password":"Admin2026!","area":"Sistemas"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@uqai.pe","password":"Admin2026!"}'

# Usar el token retornado en el header
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8080/api/usuarios
```

---

### HORA 3 (2:30 – 3:30) — Frontend: Landing Page

#### Paso 8: Estructura de carpetas Next.js
```
src/
├── app/
│   ├── page.tsx              ← Landing page (/)
│   ├── login/page.tsx        ← Página de login
│   ├── dashboard/page.tsx    ← Panel protegido
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── Navbar.tsx
│   ├── Hero.tsx
│   ├── Services.tsx
│   ├── Academy.tsx
│   ├── Lab.tsx
│   ├── ContactForm.tsx
│   └── Footer.tsx
├── lib/
│   └── api.ts                ← Funciones para llamar al backend
└── middleware.ts              ← Protección de rutas
```

#### Paso 9: Landing Page

**Prompt para IA:**
> "Crea un componente Hero.tsx en Next.js 14 con Tailwind CSS para UQ AI Solution Company. Debe tener: fondo oscuro (#0a0a1a) con gradiente azul/morado, título grande 'Inteligencia Artificial para el Perú y el Mundo', subtítulo, dos botones CTA, y una animación CSS de partículas o gradiente. Estilo similar a deeplearning.ai o landing.ai."

**Componente Services.tsx:**
```tsx
// components/Services.tsx
const services = [
  { icon: "🤖", title: "Agentes de IA", desc: "Automatiza procesos con agentes inteligentes" },
  { icon: "💬", title: "Chatbots Empresariales", desc: "Atención al cliente 24/7 con IA" },
  { icon: "⚡", title: "Automatización", desc: "Elimina tareas repetitivas con RPA + IA" },
  { icon: "🏥", title: "Salud & Educación", desc: "Asistentes especializados para tu sector" },
  { icon: "📊", title: "Big Data", desc: "Análisis de datos a escala empresarial" },
  { icon: "🔒", title: "DevSecOps", desc: "Seguridad integrada en cada etapa" },
];

export default function Services() {
  return (
    <section id="servicios" className="py-20 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center text-white mb-4">
          UQ AI Solutions
        </h2>
        <p className="text-gray-400 text-center mb-12">
          Soluciones de IA para empresas de todos los tamaños
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((s, i) => (
            <div key={i} className="bg-gray-800 rounded-xl p-6 hover:bg-gray-700 
                                    transition-all border border-gray-700 hover:border-blue-500">
              <div className="text-4xl mb-3">{s.icon}</div>
              <h3 className="text-xl font-semibold text-white mb-2">{s.title}</h3>
              <p className="text-gray-400">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Formulario de Contacto — envía al backend:**
```tsx
// components/ContactForm.tsx
"use client";
import { useState } from "react";
import axios from "axios";

export default function ContactForm() {
  const [form, setForm] = useState({ nombre:"", email:"", empresa:"", telefono:"", mensaje:"" });
  const [status, setStatus] = useState<"idle"|"loading"|"ok"|"error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/leads`, form);
      setStatus("ok");
      setForm({ nombre:"", email:"", empresa:"", telefono:"", mensaje:"" });
    } catch {
      setStatus("error");
    }
  };

  return (
    <section id="contacto" className="py-20 bg-gray-950">
      <div className="max-w-2xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-white text-center mb-10">
          ¿Listo para usar IA en tu empresa?
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* campos del formulario */}
          <input type="text" placeholder="Nombre completo" required
            value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 
                       focus:border-blue-500 focus:outline-none" />
          <input type="email" placeholder="Email empresarial" required
            value={form.email} onChange={e => setForm({...form, email: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 
                       focus:border-blue-500 focus:outline-none" />
          <input type="text" placeholder="Empresa" 
            value={form.empresa} onChange={e => setForm({...form, empresa: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 
                       focus:border-blue-500 focus:outline-none" />
          <textarea placeholder="¿En qué podemos ayudarte?" rows={4} required
            value={form.mensaje} onChange={e => setForm({...form, mensaje: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 
                       focus:border-blue-500 focus:outline-none resize-none" />
          <button type="submit" disabled={status === "loading"}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg 
                       transition-colors disabled:opacity-50">
            {status === "loading" ? "Enviando..." : "Contactar a UQ AI"}
          </button>
          {status === "ok" && <p className="text-green-400 text-center">✅ Mensaje enviado. Te contactaremos pronto.</p>}
          {status === "error" && <p className="text-red-400 text-center">❌ Error al enviar. Intenta de nuevo.</p>}
        </form>
      </div>
    </section>
  );
}
```

---

### HORA 4 (3:30 – 4:30) — Login Seguro + Dashboard + Cookie HttpOnly

#### Paso 10: Página de Login

**Prompt para IA:**
> "Crea una página de login en Next.js 14 para UQ AI Solution Company. Debe: (1) llamar a POST /api/auth/login, (2) Si el backend retorna 200 con el JWT, hacer POST a /api/auth/set-cookie en Next.js para guardar el token en cookie HttpOnly, (3) mostrar mensaje de error genérico 'Credenciales incorrectas' sin importar si fue email o password, (4) bloquear el botón 30 segundos tras 3 intentos fallidos."

```tsx
// app/login/page.tsx
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [intentosFallidos, setIntentosFallidos] = useState(0);
  const [bloqueadoHasta, setBloqueadoHasta] = useState<number>(0);

  const estaBloqueado = Date.now() < bloqueadoHasta;
  const segundosBloq = Math.ceil((bloqueadoHasta - Date.now()) / 1000);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (estaBloqueado) return;
    setLoading(true);
    setError("");

    try {
      // 1. Pedir token al backend Java
      const { data } = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, form
      );

      // 2. Guardar JWT en cookie HttpOnly (via Route Handler de Next.js)
      // PROGRAMACIÓN SEGURA: JWT en HttpOnly cookie, NO en localStorage
      await axios.post("/api/auth/set-cookie", { token: data.token, rol: data.rol });

      router.push("/dashboard");
    } catch {
      const nuevosIntentos = intentosFallidos + 1;
      setIntentosFallidos(nuevosIntentos);
      // SEGURIDAD: mensaje genérico, no revela qué campo fue incorrecto
      setError("Credenciales incorrectas. Verifica tu email y contraseña.");
      // Bloquear tras 3 intentos
      if (nuevosIntentos >= 3) {
        setBloqueadoHasta(Date.now() + 30000); // 30 segundos
        setError("Demasiados intentos fallidos. Espera 30 segundos.");
        setIntentosFallidos(0);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-800">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white">UQ AI Solution</h1>
          <p className="text-gray-400 mt-2">Panel de Administración</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input type="email" placeholder="Email" required
            value={form.email} onChange={e => setForm({...form, email: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none" />
          <input type="password" placeholder="Contraseña" required
            value={form.password} onChange={e => setForm({...form, password: e.target.value})}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none" />

          {error && <p className="text-red-400 text-sm text-center">{error}</p>}

          <button type="submit"
            disabled={loading || estaBloqueado}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition-colors disabled:opacity-50">
            {loading ? "Verificando..." :
             estaBloqueado ? `Bloqueado (${segundosBloq}s)` : "Iniciar Sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}
```

#### Paso 11: Route Handler para Cookie HttpOnly

```typescript
// app/api/auth/set-cookie/route.ts
// PROGRAMACIÓN SEGURA: el JWT se guarda en cookie HttpOnly desde el servidor
// El cliente JavaScript NUNCA puede leer esta cookie (document.cookie no la ve)
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { token, rol } = await req.json();

  const res = NextResponse.json({ ok: true });

  // Cookie HttpOnly: JavaScript del navegador NO puede leerla
  res.cookies.set("auth_token", token, {
    httpOnly: true,    // SEGURIDAD: JS no puede acceder
    secure: process.env.NODE_ENV === "production", // Solo HTTPS en prod
    sameSite: "strict", // SEGURIDAD: protege contra CSRF
    maxAge: 86400,     // 24 horas
    path: "/",
  });

  res.cookies.set("user_rol", rol, {
    httpOnly: false,   // El rol sí puede ser leído por JS para UI condicional
    sameSite: "strict",
    maxAge: 86400,
    path: "/",
  });

  return res;
}
```

#### Paso 12: Middleware de Rutas Protegidas

```typescript
// middleware.ts (raíz del proyecto)
import { NextRequest, NextResponse } from "next/server";

export function middleware(req: NextRequest) {
  const token = req.cookies.get("auth_token")?.value;
  const { pathname } = req.nextUrl;

  // Rutas que requieren autenticación
  const protectedRoutes = ["/dashboard", "/admin"];
  const isProtected = protectedRoutes.some(route => pathname.startsWith(route));

  if (isProtected && !token) {
    // Redirigir a login si no hay token
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Si ya está logueado e intenta ir a /login, redirigir al dashboard
  if (pathname === "/login" && token) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/admin/:path*", "/login"],
};
```

#### Paso 13: Dashboard con RBAC

```tsx
// app/dashboard/page.tsx
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

async function getLeads(token: string) {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/leads`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return [];
    return res.json();
  } catch { return []; }
}

export default async function DashboardPage() {
  const cookieStore = cookies();
  const token = cookieStore.get("auth_token")?.value;
  const rol   = cookieStore.get("user_rol")?.value;

  if (!token) redirect("/login");

  const leads = rol === "ADMIN" ? await getLeads(token) : [];

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-white">
            Panel UQ AI {rol === "ADMIN" ? "👑 Admin" : "👤 Usuario"}
          </h1>
          <form action="/api/auth/logout" method="POST">
            <button type="submit"
              className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg">
              Cerrar Sesión
            </button>
          </form>
        </div>

        {rol === "ADMIN" && (
          <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
            <div className="p-4 border-b border-gray-800">
              <h2 className="text-xl font-semibold text-white">
                Leads Registrados ({leads.length})
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-gray-300">
                <thead className="bg-gray-800 text-gray-400 uppercase text-xs">
                  <tr>
                    {["Nombre","Email","Empresa","Mensaje","Fecha"].map(h => (
                      <th key={h} className="px-4 py-3 text-left">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {leads.map((lead: any) => (
                    <tr key={lead.id} className="hover:bg-gray-800">
                      <td className="px-4 py-3">{lead.nombre}</td>
                      <td className="px-4 py-3">{lead.email}</td>
                      <td className="px-4 py-3">{lead.empresa || "—"}</td>
                      <td className="px-4 py-3 max-w-xs truncate">{lead.mensaje}</td>
                      <td className="px-4 py-3 text-gray-500">{new Date(lead.fechaRegistro).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {rol !== "ADMIN" && (
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <p className="text-gray-400">
              Bienvenido. Eres usuario con rol <span className="text-blue-400 font-bold">USER</span>.
              Contacta al administrador para ampliar tus permisos.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
```

**Logout Route Handler:**
```typescript
// app/api/auth/logout/route.ts
import { NextResponse } from "next/server";

export async function POST() {
  const res = NextResponse.redirect(new URL("/login", "http://localhost:3000"));
  // SEGURIDAD: eliminar cookie del servidor (Max-Age=0)
  res.cookies.set("auth_token", "", { maxAge: 0, path: "/" });
  res.cookies.set("user_rol", "", { maxAge: 0, path: "/" });
  return res;
}
```

---

### HORA 5 (4:30 – 5:30) — Deploy + GitHub + Video

#### Paso 14: Variables de Entorno

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

**En Vercel (dashboard):**
```
NEXT_PUBLIC_API_URL=https://tu-backend.railway.app
```

#### Paso 15: Deploy en Railway (Backend)
1. Crear cuenta en [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo" → seleccionar el repo del backend
3. Railway detecta automáticamente Spring Boot con Maven
4. Agregar variable de entorno: `PORT=8080`
5. Copiar la URL pública (ej: `https://uq-ai-backend.up.railway.app`)

#### Paso 16: Deploy en Vercel (Frontend)
```bash
# Instalar Vercel CLI
npm install -g vercel

# Desde la carpeta del frontend
vercel

# Responder las preguntas:
# Set up and deploy? → Y
# Which scope? → tu cuenta
# Link to existing project? → N (primero)
# Project name? → uq-ai-frontend
# In which directory is your code? → ./

# Agregar variable de entorno en el dashboard de Vercel:
# NEXT_PUBLIC_API_URL = https://tu-backend.railway.app
```

#### Paso 17: GitHub — Commits Significativos

```bash
# 1er commit: Setup inicial
git init
git add .
git commit -m "feat: inicializar proyecto Next.js + Spring Boot con estructura base"

# 2do commit: Backend API + JWT
git add backend/
git commit -m "feat: implementar API REST Spring Boot con JWT, bcrypt y H2 (OWASP A02/A07)"

# 3er commit: Frontend landing + login seguro
git add frontend/
git commit -m "feat: landing page UQ AI + login seguro con cookie HttpOnly (prog. segura)"

# 4to commit: Deploy
git add .
git commit -m "chore: configurar variables de entorno para deploy Vercel + Railway"

git remote add origin https://github.com/TU_USUARIO/uqai-solution-web.git
git push -u origin main
```

---

## HERRAMIENTAS DE IA RECOMENDADAS PARA DESARROLLO

| Herramienta | Uso Principal | Link |
|---|---|---|
| **GitHub Copilot** | Autocompletar código en VS Code/IntelliJ | github.com/features/copilot |
| **Claude (Anthropic)** | Generar componentes completos, debuggear errores | claude.ai |
| **ChatGPT** | Consultas rápidas, configuraciones | chat.openai.com |
| **v0 by Vercel** | Generar UI React/Tailwind desde descripción | v0.dev |
| **Bolt.new** | Prototipo full-stack en minutos | bolt.new |

### Prompts Útiles para la Evaluación

**Para el Hero:**
> "Crea un componente Hero.tsx con Next.js y Tailwind CSS para una empresa de IA llamada UQ AI Solution Company. Fondo negro con gradiente azul/morado, tipografía grande, 2 botones CTA. Estilo oscuro moderno similar a https://landing.ai"

**Para la configuración Spring Security:**
> "Configura Spring Security 6 para JWT stateless en Spring Boot 3.2. Endpoints públicos: /api/auth/**, POST /api/leads. Endpoint /api/leads GET solo para ADMIN. CORS para http://localhost:3000 y *.vercel.app. Explica cada línea de configuración."

**Para depurar CORS:**
> "Tengo un error CORS en Spring Boot cuando mi frontend Next.js en http://localhost:3000 llama a http://localhost:8080/api/leads. El error es: 'Access to XMLHttpRequest has been blocked by CORS policy'. ¿Cómo soluciono esto sin desactivar toda la seguridad?"

---

## ESTIMACIÓN DE TIEMPO CON IA GENERATIVA

| Tarea | Sin IA | Con IA Generativa |
|---|---|---|
| Setup Next.js + Spring Boot | 30 min | **10 min** |
| Entidades JPA + Repositorios | 45 min | **15 min** |
| JWT Service + Spring Security | 90 min | **30 min** |
| Landing Page (Hero + Services + Academy + Lab) | 120 min | **45 min** |
| Formulario de Contacto + conexión API | 45 min | **15 min** |
| Login Seguro + Cookie HttpOnly | 60 min | **20 min** |
| Middleware + Rutas Protegidas | 30 min | **10 min** |
| Dashboard + RBAC | 45 min | **20 min** |
| Logout Seguro | 20 min | **5 min** |
| Deploy Vercel + Railway | 40 min | **20 min** |
| GitHub + Commits + Video | 30 min | **15 min** |
| **TOTAL** | **~8.5 horas** | **~3.5 – 5 horas** ✅ |

> **Respuesta:** Sí es posible en 5 horas con IA generativa, si el estudiante: (1) conoce los conceptos base, (2) usa GitHub Copilot + Claude para generar código, (3) trabaja en paralelo frontend-backend desde el inicio.

---

## APLICACIÓN DE CONCEPTOS DE PROGRAMACIÓN SEGURA

| Concepto del Silabo | Cómo se aplica en el proyecto |
|---|---|
| **bcrypt (S2)** | `BCryptPasswordEncoder.encode()` en registro de usuario |
| **JWT Stateless** | Token firmado con HS256, sin sesión en servidor |
| **Cookie HttpOnly (S3)** | JWT en cookie HttpOnly: JavaScript NO puede leer con `document.cookie` |
| **Cookie SameSite=Strict (S3)** | Previene CSRF: la cookie no se envía en requests cross-site |
| **HTTPS (S2)** | Vercel proporciona TLS automático (Secure=true en producción) |
| **RBAC (S3)** | `hasRole("ADMIN")` en Spring Security; dashboard diferenciado por rol |
| **SQL Injection Prevention (S2)** | JPA/Hibernate usa queries parametrizadas por defecto |
| **Mensaje genérico de error (S3)** | Login retorna "Credenciales incorrectas" (no revela si email existe) |
| **CORS configurado (S2)** | Solo los dominios del frontend tienen permiso de llamar al backend |
| **Validación de inputs (S2)** | `@NotBlank`, `@Email`, `@Valid` en los DTOs del backend |
| **Rate limiting en frontend** | Bloqueo de 30s tras 3 intentos fallidos en el botón de login |
| **OWASP A01 — Control de Acceso** | Middleware Next.js protege rutas; Spring Security protege endpoints |
| **OWASP A02 — Fallas Criptográficas** | bcrypt rounds=12, JWT con clave secreta fuerte |
| **OWASP A07 — Fallas de Autenticación** | JWT con expiración, logout elimina cookie del servidor |

---

## LINKS Y RECURSOS RECOMENDADOS

### Documentación Oficial
- **Next.js 14 App Router:** https://nextjs.org/docs/app
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Spring Boot:** https://spring.io/projects/spring-boot
- **Spring Security (JWT):** https://docs.spring.io/spring-security/reference/

### Tutoriales Específicos
- Next.js con Auth + Cookie HttpOnly: https://youtu.be/DJvM2lSPn6w
- Spring Boot + JWT + H2 paso a paso: https://youtu.be/BVdQ3iuovg0
- Deploy Spring Boot en Railway: https://docs.railway.app/guides/spring-boot
- Deploy Next.js en Vercel: https://vercel.com/docs/frameworks/nextjs

### Generadores de UI
- **v0.dev** — genera componentes Tailwind desde descripción: https://v0.dev
- **Shadcn/ui** — componentes listos para Next.js: https://ui.shadcn.com

### Sitios de Referencia Visual
- https://www.deeplearning.ai/ — referencia de diseño
- https://landing.ai/ — referencia de diseño

---

## ENTREGABLES

| # | Entregable | Formato |
|---|---|---|
| 1 | URL del sitio desplegado en Vercel | Link público |
| 2 | URL del repositorio GitHub (público) | Link GitHub |
| 3 | Screenshots del panel H2 con datos | Imágenes |
| 4 | Screenshots de Postman mostrando los 6 endpoints | Imágenes |
| 5 | Video de evidencia (máx. 5 min) | YouTube/Drive/Loom público |

---

*Evaluación Parcial — Programación Segura DD281 · Universidad Autónoma del Perú*
*Docente: Mg. Ruben Quispe Llacctarimay · Semestre 2026-1*
