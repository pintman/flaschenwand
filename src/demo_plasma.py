"""Inspired by oldschool plasma demos.

https://www.youtube.com/watch?v=QcyuYvyvOEI&t=3073s

Implementation details can be found here: http://www.bidouille.org/prog/plasma

"""

import flaschenwand
import time
import math
import colorsys

def main():
    fw = flaschenwand.Flaschenwand()

    while True:
        current = time.time()

        for x in range(fw.width):
            for y in range(fw.height):
                v = math.sin(x*25.0 + current)
                # -1 < sin() < +1
                # therfore correct the value and bring into range [0, 1]
                v = (v+1.0) / 2.0
                # transform from hsv to rgb: cycle through colors.
                r, g, b = colorsys.hsv_to_rgb(v, 1, v)
                fw.set_pixel_rgb(x, y, int(r*255), int(g*255), int(b*255))

        fw.show()
    

if __name__ == "__main__":
    main()
