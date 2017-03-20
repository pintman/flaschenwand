"""Small example OSC server.

Demo-Video under https://youtu.be/yzpNVKG0z_oo
"""
import argparse
import flaschenwand
import pythonosc.dispatcher
import pythonosc.osc_server
import os
import threading
import time
import math


class OSCServer:
    def __init__(self, ip="0.0.0.0", port=5555):
        # mapping noted to colors
        self.note_color = { 0:"red", 1:"green", 2:"blue"}

        disp = pythonosc.dispatcher.Dispatcher()
        disp.map("/noteon/0/", self._handle_colors_rgb)
        disp.map("/noteon/1/", self._handle_freq)
        disp.map("/noteon/9/", self._handle_shutdown)

        server = pythonosc.osc_server.ThreadingOSCUDPServer((ip, port), disp)

        print("Serving on {}".format(server.server_address))

        self.worker = FlaschenwandWorker()
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
        #print("shutdown received.", note, val)
        self.worker.scroll("bye")
        os.system("shutdown -h now")


class FlaschenwandWorker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pause = False
        self.fw = flaschenwand.Flaschenwand()
        self.colors = {"red":127, "green":127, "blue":127}
        self.freqs = {"red":4, "green":4, "blue":4}

    def run(self):
        print("worker started")
        current = 0
        while True:
            if self.pause:
                continue
            current += 0.1
            #current = time.time()
            for x in range(self.fw.width):
                for y in range(self.fw.height):
                    r,g,b = self._rgb_at(x,y, current)                    
                    self.fw.set_pixel_rgb(x, y, r,g,b)

            self.fw.show()            
            print(self.colors, self.freqs)
            time.sleep(0.1)

    def sine_norm(self, f, ph, t):
        """Return a sine value for frquency f, pahse ph at time t. Norm the result into 
        range [0,255].
        """
        # does not work with pi instead of 3
        v = math.sin(2*3*f*t + ph)
        # -1 <= sin() <= +1, correct value, bring into range [0, 1]
        v = (v+1.0) / 2.0        
        return int(v*255)
            
    def _rgb_at(self, x, y, clock_time):
        #v = math.sin(2.0 * math.pi * self.freq * x + clock_time)
        r = self.sine_norm(self.freqs["red"], clock_time, x)
        g = self.sine_norm(self.freqs["green"], clock_time, x)
        b = self.sine_norm(self.freqs["blue"], clock_time, x)

        return r, g, b

    def scroll(self, text):
        self.pause = True
        fnt = flaschenwand.Font()
        fnt.scroll_text(self.fw, text)
        self.pause = False
            

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
