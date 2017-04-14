import sys
import time
import rtmidi.midiutil as midi
import collections

# taken from
# https://github.com/SpotlightKid/python-rtmidi/blob/master/examples/basic/midiin_callback.py

class MidiInputHandler:
    def __init__(self, port):
        self.port = port
        self.vs = collections.OrderedDict()

    def cls(self):
        print(chr(27) + "[2J")
        
    def __call__(self, event, data=None):
        message, _ = event
        chan, note, val = message

        if chan not in self.vs:
            self.vs[chan] = collections.OrderedDict()
            
        self.vs[chan][note] = val

        self.print_values()

    def note_val_as_string(self, val):
        var = (val//2) * "#"
        return var + " ({})".format(val)
        
    def print_values(self):
        self.cls()
        
        for chan in self.vs:
            print("chan", chan)
            for note in self.vs[chan]:
                print("note", note, "=",
                      self.note_val_as_string(self.vs[chan][note]))
                

if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    print("Give me an input port")
    midi.list_input_ports()
    exit(1)

midiin, port_name = midi.open_midiinput(port)
midiin.set_callback(MidiInputHandler(port_name))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    midiin.close_port()
