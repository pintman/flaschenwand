"""
Some tests for correct connection
"""

import flaschenwand
import time
import math
import colorsys

def main():
    fw = flaschenwand.Flaschenwand()

    while True:
        current = time.time()

        for r,g,b in [(1,1,1), (1,0,0), (0,1,0), (0,0,1)]:
            
            for y in range(fw.height):
                for x in range(fw.width):
                    fw.set_all_pixels_rgb(0,0,0)
                    fw.set_pixel_rgb(x, y, int(r*255), int(g*255), int(b*255))
                    fw.show()
                    time.sleep(0.2)
    

if __name__ == "__main__":
    main()
