import flaschenwand
import time

fw = flaschenwand.Flaschenwand()
fnt = flaschenwand.Font()

# Each character is 3 pixels width
chars = "abcdefghijklmnopqrstuvwxyz"

fw.set_all_pixels_rgb(0,0,0)

for c in chars:
    for x in range(fw.width):
        fw.set_all_pixels_rgb(0,0,0)
        fnt.set_char(fw, c, x)
        fw.show()
        time.sleep(0.2)

