#!/usr/bin/env python3

import flaschenwand
import time

f = flaschenwand.Flaschenwand()

for i in range(255):
    f.set_all_pixels_rgb(0, i, 0)    
    f.show()
    time.sleep(0.01)
    
