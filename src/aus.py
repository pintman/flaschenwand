#!/usr/bin/env python3

import neopixel
import os 

# pin in BCM order
pin = 18

if "LED_COUNT" in os.environ:
    leds = os.environ["LED_COUNT"]
else:
    leds = 50

strip = neopixel.Adafruit_NeoPixel(leds, pin)
strip.begin()

for i in range(leds):
    strip.setPixelColorRGB(i, 0,0,0)

strip.show()

