import flaschenwand
import time

f = flaschenwand.Flaschenwand()
fo = flaschenwand.Font()

for c in "abcdefghijklmnopqrstuvwxyz":
    fo.set_char(f, c)
    f.show()
    time.sleep(1)

