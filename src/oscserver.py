"""Small example OSC server.

Demo-Video under https://youtu.be/yzpNVKG0z_oo

Configuration

colors

r          g         b
|          |         |
|          |         |
|          |         |
/noteon/0  /noteon/0 /noteon/0/
note 0     note 1    note 2

frequencies

r          g         b
|          |         |
|          |         |
|          |         |
/noteon/1  /noteon/1 /noteon/1
note 0     note 1    note 2

buttons

#[shutdown] /noteon/9/

"""
import argparse
import flaschenwand
import pythonosc.dispatcher
import pythonosc.osc_server
import os
import math


class OSCServer:
    def __init__(self, ip="0.0.0.0", port=5555):
        # mapping noted to colors
        self.note_color = { 0:"red", 1:"green", 2:"blue"}

        disp = pythonosc.dispatcher.Dispatcher()
        # TODO handle in config file
        disp.map("/noteon/0/", self._handle_colors_rgb)
        disp.map("/noteon/1/", self._handle_freq)
        disp.map("/noteon/9/", self._handle_shutdown)

        server = pythonosc.osc_server.ThreadingOSCUDPServer((ip, port), disp)

        print("Serving on {}".format(server.server_address))

        self.worker = flaschenwand.FlaschenwandWorker()
        self.worker.start()
        self.worker.scroll("osc")
        server.serve_forever()

    def _handle_colors_rgb(self, _msg, note, val):
        """Accept a note in [0,2] and value to be uses as color value for red,
        green or blue.
        """
        if note in self.note_color:
            # val in [0,128], therefore take the double
            color = self.note_color[note]
            self.worker.colors[color] = 2 * val

    def _handle_freq(self, msg, note, val):
        if note in self.note_color:
            color = self.note_color[note]
            self.worker.freqs[color] = val
            
    def _handle_shutdown(self, _msg, _note, _val):
        if note == 0:
            self.worker.scroll("bye")
            os.system("shutdown -h now")




class PixelValue:
    def rgb_at(self, x,y, clock_time):
        raise NotImplementedError()

class ConstantPixelColor(PixelValue):
    def __init__(self, color):
        self.color = color
    
    def rgb_at(self, x,y, _clock_time):
        return self.color

class FrequencyPixelColor(PixelValue):
    def __init__(self):
        self.freqs = {"red":4, "green":4, "blue":4}

    def rgb_at(self, x, y, clock_time):
        r = self.sine_norm(self.freqs["red"], clock_time, x)
        g = self.sine_norm(self.freqs["green"], clock_time, x)
        b = self.sine_norm(self.freqs["blue"], clock_time, x)

        return r, g, b

    def sine_norm(self, freq, phase, t):
        """Return a sine value for frequency f, pahse ph at time t. Norm the result into 
        range [0,255].
        """
        # does not work with pi instead of 3
        #v = math.sin(2.0 * math.pi * self.freq * x + clock_time)
        v = math.sin(2*3*freq*t + phase)
        # -1 <= sin() <= +1, correct value, bring into range [0, 1]
        v = (v+1.0) / 2.0        
        return int(v*255)
    
"""
class Signal(threading.Thread):
    def __init__(self, min_val, max_val):
        self.range = (min_val, max_val)
    def run(self):
        while True:
            
        pass
    def __call__(self):
        return None

class Color(Signal):
    def __init__(self, 
"""            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5555, help="The port to listen on")
    args = parser.parse_args()

    OSCServer(ip=args.ip, port=args.port)
