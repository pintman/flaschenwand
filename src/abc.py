import flaschenwand
import time

fw = flaschenwand.Flaschenwand()
fnt = flaschenwand.Font()

for c in "abcdefghijklmnopqrstuvwxyz":
    fnt.set_char(fw, c)
    fw.show()
    time.sleep(1)

