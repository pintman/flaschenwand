#!/usr/bin/env python3

import flaschenwand
import sys

if __name__ == "__main__":
    text = " ".join(sys.argv[1:])
    print("Displaying on Falschenwand:", text)
    fw = flaschenwand.Flaschenwand()
    fnt = flaschenwand.Font()
    fnt.scroll_text(fw, text)
