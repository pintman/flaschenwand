import flaschenwand
import time
import colorsys

def main():
    fw = flaschenwand.Flaschenwand()
    hue = 0

    while True:
        if hue > 1:
            hue = 0
        else:
            hue += 0.001

        for x in range(fw.width):
            for y in range(fw.height):                
                # transform from hsv to rgb: cycle through colors.
                r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
                fw.set_pixel_rgb(x, y, int(r*255), int(g*255), int(b*255))

        fw.show()
        time.sleep(0.3)
    

if __name__ == "__main__":
    main()
