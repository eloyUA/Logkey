from evdev import InputDevice, categorize, ecodes
from collections import Counter
from pathlib import Path

RUTA_FICHERO = "~/.keycounter/log.txt"
FREC_GUARDADO = 50
contador = Counter()

def guardar_frecuencias(path) -> None:
    # Cuando termines, guarda el resultado en un fichero:
    # (este bloque se ejecutaría si haces un mecanismo para romper el loop)
    with open(path, 'w') as f:
        for tecla, cantidad in contador.most_common():
            f.write(f"{tecla}: {cantidad}\n")

def leer_frecuencias(path) -> Counter:
    try:
        carpeta = path.parent
        carpeta.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    except Exception as e:
        print(e)
    
    with open(path, "r", encoding="utf-8") as f:
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
    path = Path(RUTA_FICHERO).expanduser()
    leer_frecuencias(path)
    dev = InputDevice('/dev/input/event4')

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
                    guardar_frecuencias(path)
