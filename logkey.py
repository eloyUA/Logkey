from evdev import InputDevice, categorize, ecodes
from collections import Counter
from pathlib import Path

FILE_PATH = "~/Logkey/log.txt"
INPUT_DEVICE_PATH = "/dev/input/event0"
SAVE_FREQ = 50

def create_log_file(path: str):
    try:
        dir = path.parent
        dir.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    except Exception as e:
        print(e)

def save_frequencies(path: str, counter: Counter) -> None:
    total = counter.total()
    with open(path, 'w') as f:
        for key, amount in counter.most_common():
            f.write(f"{key}: {amount}, {round((amount/total)*100, 2)}%\n")

def read_frequencies(path: str) -> Counter:
    counter = Counter()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue

            word, values = line.split(":", 1)
            count, _ = values.split(",", 1)
            word = word.strip()
            count = count.strip()

            try:
                count = int(count)
                counter[word] = count
            except ValueError:
                continue
    return counter

if __name__ == '__main__':
    path = Path(FILE_PATH).expanduser()
    dev = InputDevice(INPUT_DEVICE_PATH)

    create_log_file(path)    
    counter = read_frequencies(path)

    print('Registering letters, press Ctrl+C to finish.')
    counter_press = 0
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)
            # Only when the key is pressed (value = 1)
            if key.keystate == key.key_down:
                keyname = key.keycode
                counter[keyname] += 1
                counter_press += 1
                if counter_press % SAVE_FREQ == 0:
                    save_frequencies(path, counter)