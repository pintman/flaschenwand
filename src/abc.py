import flaschenwand
import time

f = flaschenwand.Flaschenwand()
fo = flaschenwand.Font()

fo.show(f, "a")
f.show()
time.sleep(1)

fo.show(f, "b")
f.show()
time.sleep(1)

fo.show("c")
f.show()
