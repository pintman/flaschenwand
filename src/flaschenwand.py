# import neopixel


class Flaschenwand:
    def __init__(self, width=6, height=8, pin=18, ):
        self.width = width
        self.height = height

        # self.strip = neopixel.Adafruit_NeoPixel(width*height, pin)
        self.coords = dict()
        self._init_coords()

    def _init_coords(self):
        """Init coordinates to map (x,y) to number of pixel in strip.

        >>> f = Flaschenwand(3,2)
        >>> f.coords
        {(0, 1): 5, (2, 0): 2, (0, 0): 0, (1, 0): 1, (1, 1): 4, (2, 1): 3}
        >>> f.coords[(0,0)]
        0
        >>> f.coords[(2,0)]
        2
        >>> f.coords[(2,1)]
        3
        >>> f.coords[(0,1)]
        5
        """
        x = 0
        y = 0
        num = 0

        while num < self.width * self.height:
            self.coords[(x,y)] = num

            # update pixel number
            num += 1

            # update x,y coordinates
            # 2   .-> -> -> ...
            # 1  ^ <- <- <-.
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

if __name__ == "__main__":
    f = Flaschenwand(3,2)
