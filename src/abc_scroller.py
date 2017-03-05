import flaschenwand
import time

class DisplayItem:
    def __init__(self, char, pos):
        self.char = char
        self.pos = pos

fw = flaschenwand.Flaschenwand()
fnt = flaschenwand.Font()

# Each character is 3 pixels width + 1 pixel space
chars = "hallo welt "

# create dictionary to hold character and x-position to be displayed.
chars_pos = []
pos = 4
for c in chars:
    chars_pos += [DisplayItem(c, pos)]
    pos += 4

fw.set_all_pixels_rgb(0,0,0)

for i in range(len(chars_pos)*4):
    fw.set_all_pixels_rgb(0,0,0)    

    for item in chars_pos:
        fnt.set_char(fw, item.char, item.pos)
        # scroll left
        item.pos -= 1
        
    fw.show()
    
    time.sleep(0.2)
    
