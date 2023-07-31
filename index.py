from spam import Spam
import time
spam = Spam('Diablo IV')
spam.start()

try:
    now = time.time()
    while True:
        if time.time() - now > 10:
            spam.stop()
except KeyboardInterrupt:
    spam.stop()
    print("Exiting...")