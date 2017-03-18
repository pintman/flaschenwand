"""Small example OSC server
"""
import argparse
import flaschenwand
import pythonosc.dispatcher
import pythonosc.osc_server

class OSCServer:
    def __init__(self, ip="0.0.0.0", port=5555):
        self.note_color = { 0:"red", 1:"green", 2:"blue"}
        self.fw = flaschenwand.Flaschenwand()
        self.colors = [0,0,0]

        disp = pythonosc.dispatcher.Dispatcher()
        disp.map("/noteon/0/", self.handle_color)

        server = pythonosc.osc_server.ThreadingOSCUDPServer((ip, port), disp)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    def handle_color(self, msg, note, val):
        # val in [0,128], therefore take the double 
        self.colors[note] = 2 * val
        self.fw.set_all_pixels_rgb(*self.colors)
        self.fw.show()
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5555, help="The port to listen on")
    args = parser.parse_args()

    OSCServer(ip=args.ip, port=args.port)
