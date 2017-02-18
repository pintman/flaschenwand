"""Inspired by oldschool plasma demos.

https://www.youtube.com/watch?v=QcyuYvyvOEI&t=3073s

Implementation details can be found here: http://www.bidouille.org/prog/plasma

"""

import flaschenwand
import time
import math

# Width and height of the display
WIDTH = flaschenwand.DEFAULT_WIDTH
HEIGHT = flaschenwand.DEFAULT_HEIGHT


def main():
    fw = flaschenwand.Flaschenwand(WIDTH, HEIGHT)

    while True:
        current = time.time()

        for x in range(WIDTH):
            for y in range(HEIGHT):
                v = math.sin(x*10.0 + current)
                # -1 < sin() < +1
                # therfore correct the value and bring into range [0, 1]
                v = (v+1.0) / 2.0
                fw.set_pixel_rgb(x, y, 0, 0, 0, white=int(v*255))

        fw.show()
    

if __name__ == "__main__":
    main()
