"""Small example OSC server
"""
import argparse
import flaschenwand

from pythonosc import dispatcher
from pythonosc import osc_server

note_color = { 0:"red", 1:"green", 2:"blue"}

fw = flaschenwand.Flaschenwand()
colors = [0,0,0]

def print_color(msg, note, val):
    global fw, colors
    # print("msg", msg, "note", note, "val", val, ":", note_color[note])

    # val in [0,128], therefore take the double 
    colors[note] = 2 * val
    fw.set_all_pixels_rgb(*colors)
    fw.show()
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5555, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #dispatcher.set_default_handler(print)
    dispatcher.map("/noteon/0/", print_color)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
