import neopixel


class Flaschenwand:
    def __init__(self, width=6, height=8, pin=18):
        self.width = width
        self.height = height

        self.strip = neopixel.Adafruit_NeoPixel(width*height, pin)
        self.strip.begin()

        self.coords_index = dict()
        self._init_coords()

    def _init_coords(self):
        """Init coordinates to map (x,y) to number of pixel in strip.

        >>> f = Flaschenwand(3,2)
        >>> f.coords_index
        {(0, 1): 5, (2, 0): 2, (0, 0): 0, (1, 0): 1, (1, 1): 4, (2, 1): 3}
        >>> f.coords_index[(0,0)]
        0
        >>> f.coords_index[(2,0)]
        2
        >>> f.coords_index[(2,1)]
        3
        >>> f.coords_index[(0,1)]
        5
        """
        x = 0
        y = 0
        num = 0

        while num < self.width * self.height:
            self.coords_index[(x, y)] = num

            # update pixel number
            num += 1

            # update x,y coordinates
            # 2    -> -> -> ...
            # 1  ^ <- <- <-
            # 0    -> -> -> ^
            if y % 2 == 0:
                # moving  ->
                if x + 1 < self.width:
                    x += 1
                else:
                    y += 1
            else:
                # moving  <-
                if x - 1 >= 0:
                    x -= 1
                else:
                    y += 1

    def set_pixel(self, x, y, col):
        """Set the pixel at the given position to the neopixel color."""
        self.strip.setPixelColor(self.coords_index[(x, y)], col)

    def get_pixel(self, x, y):
        """Request the color for the pixel at (x,y)."""
        return self.strip.getPixelColor(self.coords_index[(x, y)])

    def set_pixel_rgb(self, x, y, r, g, b, white=0):
        """Set the pixel at the given position to the given color value."""
        self.set_pixel(x, y, neopixel.Color(r, g, b, white))

    def set_brightness(self, brightness):
        """Set the brightness of all pixels. Use a value between 0 and 255."""
        self.strip.setBrightness(brightness)

    def show(self):
        """Update the display and show the current state."""
        self.strip.show()

