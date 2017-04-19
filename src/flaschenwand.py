import math
import time 
import threading
import neopixel
import colorsys


class Flaschenwand:
    """This class is an abstraction to the neopixel rbg-strip.

    It converts a strip of LEDs into a two-dimensional plane of
    pixels. Each LED is accessible via two coordinates x and y. We
    assume the origin (0,0) to be at lower bottom like in mathematical
    kartesian coordinate systems.

     
    y ^
     3| P(2,3)
     2|
     1|  Q(3,1)
      +------> x
       123


    Each color component (red, green, blue and white) should be a value 
    0-255 where 0 is the lowest intensity and 255 is the highest intensity.

    """
    
    def __init__(self, width=8, height=6, pin=18, ignoring_nums=[24]):
        """Initialize the falschenwand. 

        Ignoring nums is a list of led numbers that should be ignored.

        """
        self.width = width
        self.height = height
        self.ignoring_nums = ignoring_nums

        self.strip = neopixel.Adafruit_NeoPixel(width*height+len(ignoring_nums), pin)
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
        x, y = self.width-1, 0
        num = 0

        while len(self.coords_index) < self.width * self.height:            
            if num in self.ignoring_nums:
                num += 1
                continue

            self.coords_index[(x, y)] = num

            # update pixel number
            num += 1

            # update x,y coordinates
            x, y = self._next_pixel(x, y)
            
        # TODO (0,0) not correctly mapped

    def _next_pixel(self, x, y):
        """Overwrite this method to arrange the LEDs in the display to your
        needs. During initialization this method is called to get the
        next pixel in the strip when at coordinate (x,y). The method
        hat to return a tuple (x', y') with the next coordinates. The
        first point is at the bottom right.

       The default implementation goes like this

         2        <---  <---
         1        v  ^  v  ^ 
         0      <--  <---  ^
            0  1  2  3  4  5 ...
        """
        xneu, yneu = x, y

        if x % 2 == 0:
            # moving v
            if y - 1 >= 0:
                yneu = y - 1
            else:
                xneu = x - 1
        else:
            # moving ^
            if y + 1 < self.height:
                yneu = y + 1
            else:
                xneu = x - 1 

        return xneu, yneu

    def set_pixel(self, x, y, col):
        """Set the pixel at the given position to the neopixel color."""
        self.strip.setPixelColor(self.coords_index[(x, y)], col)

    def get_pixel(self, x, y):
        """Request the color for the pixel at (x,y)."""
        return self.strip.getPixelColor(self.coords_index[(x, y)])

    def set_pixel_rgb(self, x, y, r, g, b, white=0):
        """Set the pixel at the given position to the given color value."""
        self.set_pixel(x, y, neopixel.Color(r, g, b, white))

    def set_all_pixels_rgb(self, r, g, b, white=0):
        """Set the color of all pixels to the specified color."""
        for x in range(self.width):
            for y in range(self.height):
                self.set_pixel_rgb(x, y, r, g, b, white)

    def set_brightness(self, brightness):
        """Set the brightness of all pixels. Use a value between 0 and 255."""
        self.strip.setBrightness(brightness)

    def show(self):
        """Update the display and show the current state."""
        self.strip.show()

    def on_display(self, x, y):
        """Check whether a given coordinate is on the display."""
        return 0 <= x < self.width and 0 <= y < self.height


class Font:
    """A set of character that be displayed on a Flaschenwand."""
    def __init__(self):
        self.char_pixel = dict()

        # Character can as well be represented in integer form
        # For instance for character 'a':
        # >>> 0b111101111101
        # 3965
        # >>> "{0:b}".format(3965)
        # '111101111101'
        #
        self.char_pixel[" "] = [[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]]
        self.char_pixel["a"] = [[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                                [1, 0, 1]]
        self.char_pixel["b"] = [[1, 1, 0],
                                [1, 1, 0],
                                [1, 0, 1],
                                [1, 1, 1]]
        self.char_pixel["c"] = [[1, 1, 1],
                                [1, 0, 0],
                                [1, 0, 0],
                                [1, 1, 1]]
        self.char_pixel["d"] = [[1, 1, 0],
                                [1, 0, 1],
                                [1, 0, 1],
                                [1, 1, 0]]
        self.char_pixel["e"] = [[1, 1, 1],
                                [1, 1, 0],
                                [1, 0, 0],
                                [1, 1, 1]]
        self.char_pixel["f"] = [[1, 1, 1],
                                [1, 1, 0],
                                [1, 0, 0],
                                [1, 0, 0]]
        self.char_pixel["g"] = [[1, 1, 1],
                                [1, 0, 0],
                                [1, 0, 1],
                                [1, 1, 1]]
        self.char_pixel["h"] = [[1, 0, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                                [1, 0, 1]]
        self.char_pixel["i"] = [[1, 1, 1],
                                [0, 1, 0],
                                [0, 1, 0],
                                [1, 1, 1]]
        self.char_pixel["j"] = [[1, 1, 1],
                                [0, 1, 0],
                                [0, 1, 0],
                                [1, 1, 0]]
        self.char_pixel["k"] = [[1, 0, 1],
                                [1, 1, 0],
                                [1, 0, 1],
                                [1, 0, 1]]
        self.char_pixel["l"] = [[1, 0, 0],
                                [1, 0, 0],
                                [1, 0, 0],
                                [1, 1, 1]]
        self.char_pixel["m"] = [[1, 1, 1],
                                [1, 1, 1],
                                [1, 0, 1],
                                [1, 0, 1]]
        self.char_pixel["n"] = [[1, 1, 0],
                                [1, 0, 1],
                                [1, 0, 1],
                                [1, 0, 1]]
        self.char_pixel["o"] = [[0, 1, 1],
                                [1, 0, 1],
                                [1, 0, 1],
                                [1, 1, 0]]
        self.char_pixel["p"] = [[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                                [1, 0, 0]]
        self.char_pixel["q"] = [[0, 1, 0],
                                [1, 0, 1],
                                [1, 1, 0],
                                [0, 1, 1]]
        self.char_pixel["r"] = [[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 0],
                                [1, 0, 1]]
        self.char_pixel["s"] = [[0, 1, 1],
                                [1, 0, 0],
                                [0, 0, 1],
                                [1, 1, 0]]
        self.char_pixel["t"] = [[1, 1, 1],
                                [0, 1, 0],
                                [0, 1, 0],
                                [0, 1, 0]]
        self.char_pixel["u"] = [[1, 0, 1],
                                [1, 0, 1],
                                [1, 0, 1],
                                [0, 1, 1]]
        self.char_pixel["v"] = [[1, 0, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                                [0, 1, 0]]
        self.char_pixel["w"] = [[1, 0, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                                [1, 1, 1]]
        self.char_pixel["x"] = [[1, 0, 1],
                                [0, 1, 0],
                                [1, 0, 1],
                                [1, 0, 1]]
        self.char_pixel["y"] = [[1, 0, 1],
                                [1, 1, 1],
                                [0, 0, 1],
                                [1, 1, 1]]
        self.char_pixel["z"] = [[1, 1, 1],
                                [0, 0, 1],
                                [1, 0, 0],
                                [1, 1, 1]]
        # TODO add numbers

    def pixels(self, char):
        return self.char_pixel[char]

    def set_char(self, flaschenwand, char, x=0, y=0):
        """Display the given character in the given color on a Flaschenwand."""
        pixels = self.pixels(char)

        for yy in range(len(pixels)):
            for xx in range(len(pixels[yy])):
                if pixels[yy][xx] == 1:
                    v = 255
                else:
                    v = 0

                if flaschenwand.on_display(x+xx, flaschenwand.height-1-y-yy):
                    # turn y-axis upside-down
                    flaschenwand.set_pixel_rgb(x+xx, flaschenwand.height-1-y-yy,
                                               v, v, v)

    def scroll_text(self, flaschenwand, text, wait_time=0.2):
        """Scroll the given text on the given flaschenwand. wait_time controls
        the speed of scrollin: it's the number of seconds to wait
        before advancing the display.
        """
        # create dictionary to hold character and x-position to be displayed.
        chars_pos = []
        pos = 4
        for c in text:
            chars_pos += [_DisplayItem(c, pos)]
            pos += 4

        flaschenwand.set_all_pixels_rgb(0, 0, 0)

        for i in range(len(chars_pos)*4+flaschenwand.width):
            flaschenwand.set_all_pixels_rgb(0, 0, 0)

            for item in chars_pos:
                self.set_char(flaschenwand, item.char, item.pos)
                # scroll left
                item.pos -= 1
        
            flaschenwand.show()
    
            time.sleep(wait_time)


class _DisplayItem:
    def __init__(self, char, pos):
        self.char = char
        self.pos = pos


class FlaschenwandWorker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pause = False
        self.fw = Flaschenwand()
        self.colors = {"red": 127, "green": 127, "blue": 127}
        self.freqs = {"red": 4, "green": 4, "blue": 4}
        self.progs = [FlaschenwandProgramm(self.colors, self.freqs),
                      PlasmaRotating(self.colors, self.freqs)]

    def run(self):
        print("worker started")
        current_time = 0
        while True:
            if self.pause:
                continue
            current_time += 0.1
            # current = time.time()
            prog = self.progs[0]
            prog.colors, prog.freqs = self.colors, self.freqs
            for x in range(self.fw.width):
                for y in range(self.fw.height):
                    r, g, b = prog.rgb_at(x, y, current_time)
                    self.fw.set_pixel_rgb(x, y, r, g, b)

            self.fw.show()
            # print(self.colors, self.freqs)
            time.sleep(0.1)

    def scroll(self, text):
        self.pause = True
        fnt = Font()
        fnt.scroll_text(self.fw, text, wait_time=0.1)
        self.pause = False

    def next_program(self):
        self.progs = self.progs[1:] + [self.progs[0]]
        print("using program", self.progs[0])
        

class FlaschenwandProgramm:
    def __init__(self, rgb_colors, rgb_frequencies):
        self.colors = rgb_colors
        self.freqs = rgb_frequencies
    
    def sine_norm(self, freq, phase, t):
        """Return a sine value for frquency f, phase ph at time t. Norm the
        result into range [0,255].
        """
        # does not work with pi instead of 3
        # v = math.sin(2.0 * math.pi * self.freq * x + clock_time)
        v = math.sin(2*3*freq*t + phase)
        # -1 <= sin() <= +1, correct value, bring into range [0, 1]
        v = (v+1.0) / 2.0        
        return int(v*255)

    def rgb_at(self, x, y, clock_time):
        r = self.sine_norm(self.freqs["red"], clock_time, x)
        g = self.sine_norm(self.freqs["green"], clock_time, x)
        b = self.sine_norm(self.freqs["blue"], clock_time, x)

        # weight colors
        r *= self.colors["red"] / 255
        g *= self.colors["green"] / 255
        b *= self.colors["blue"] / 255

        return int(r), int(g), int(b)
        
class PlasmaRotating(FlaschenwandProgramm):
    def __init__(self, rgb_colors, rgb_frequencies):
        super().__init__(rgb_colors, rgb_frequencies)
        print("colors", self.colors)

    def rgb_at(self, x, y, clock_time):
        v = math.sin(1*(0.5*x*math.sin(clock_time/2) + 0.5*y*math.cos(clock_time/3)) + clock_time)
        v = (v+1.0) / 2.0
        r, g, b = colorsys.hsv_to_rgb(v, 1, v)

        r *= 255
        g *= 255
        b *= 255
        """
        r = self.sine_norm(self.freqs["red"], clock_time, x)
        g = self.sine_norm(self.freqs["green"], clock_time, x)
        b = self.sine_norm(self.freqs["blue"], clock_time, x)
        """
        
        # weight colors
        r *= self.colors["red"] / 255
        g *= self.colors["green"] / 255
        b *= self.colors["blue"] / 255

        return int(r), int(g), int(b)
