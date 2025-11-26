from evdev import InputDevice, categorize, ecodes
from collections import Counter

RUTA_FICHERO = '/home/eloy348/Programas/Logkey/conteo_teclas.txt'
FREC_GUARDADO = 50
contador = Counter()

def guardar_frecuencias() -> None:
    # Cuando termines, guarda el resultado en un fichero:
    # (este bloque se ejecutaría si haces un mecanismo para romper el loop)
    with open(RUTA_FICHERO, 'w') as f:
        for tecla, cantidad in contador.most_common():
            f.write(f"{tecla}: {cantidad}\n")

def leer_frecuencias() -> Counter:
    with open(RUTA_FICHERO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue  # saltar líneas vacías

            if ":" not in linea:
                continue  # saltar líneas inválidas

            palabra, valor = linea.split(":", 1)
            palabra = palabra.strip()
            valor = valor.strip()

            try:
                valor = int(valor)
            except ValueError:
                continue  # si el valor no es entero, se ignora

            contador[palabra] = valor

if __name__ == '__main__':
    leer_frecuencias()
    dev = InputDevice('/dev/input/event0')

    print('Registrando letras, pulsa Ctrl+C para terminar.')
    cont_presiones = 0
    for evento in dev.read_loop():
        if evento.type == ecodes.EV_KEY:
            key = categorize(evento)
            # Solo cuando se presiona (value = 1)
            if key.keystate == key.key_down:
                keyname = key.keycode
                contador[keyname] += 1
                cont_presiones += 1
                if cont_presiones % FREC_GUARDADO == 0:
                    guardar_frecuencias()
