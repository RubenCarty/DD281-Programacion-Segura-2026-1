# Semana 05 — Criptografía Aplicada

## Tema
Criptografía simétrica (AES-256), asimétrica (RSA, ECC), funciones hash (SHA-256, SHA-3), firmas digitales, gestión de claves y PKI. Aplicación práctica en Python con la biblioteca `cryptography`.

## Competencia de la semana
Al finalizar, el estudiante será capaz de **seleccionar el algoritmo criptográfico adecuado para cada caso de uso** (cifrado en tránsito, en reposo, autenticación, integridad) y **implementarlo correctamente** evitando los errores criptográficos más comunes (OWASP A02).

## Contenido disponible

| Recurso | Descripción |
|---|---|
| [Guía de Trabajo](guia-trabajo/) | Selección de algoritmos + análisis de implementaciones inseguras |
| [Laboratorio](laboratorio/) | Cifrado AES-GCM, RSA, HMAC y gestión de claves en Python |
| [Material](material/) | Diapositivas y referencias |

## Entrega del estudiante

Sube tu trabajo en:
```
semana-05/soluciones/APELLIDO_NOMBRE/
```

Incluye:
- `guia_trabajo_s05.md` — Guía completada
- `laboratorio/`
  - `cifrado_simetrico.py` — AES-256-GCM
  - `cifrado_asimetrico.py` — RSA / ECC
  - `firmas_digitales.py` — Firma + verificación
  - `capturas/` — Evidencia de ejecución

## Conceptos clave evaluados
- AES-GCM vs AES-CBC: ¿cuál proporciona autenticación integrada?
- ¿Por qué no usar ECB mode?
- RSA vs ECC: ventajas en dispositivos IoT/mobile
- HMAC vs hash simple para integridad
- Gestión de claves: ¿dónde NO guardarlas?
- OWASP A02:2021 Cryptographic Failures

## Advertencia
No subas claves privadas RSA al repositorio. Genera claves nuevas solo para demostración y elimínalas.

## Referencias clave
- Python cryptography library: https://cryptography.io/en/latest/
- NIST Approved Algorithms: https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program
- Cryptopals Challenges (práctica): https://cryptopals.com/
