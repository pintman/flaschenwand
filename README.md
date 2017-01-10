Falschenwand
============

Das Projekt wurde inspiriert durch die Matewand des 32C3.

http://matelight.rocks/


Material
========

MicroPython Smart Holiday Lights
https://learn.adafruit.com/micropython-smart-holiday-lights

Adafruit NeoPixel Digital RGB LED Strip - Black 60 LED - BLACK
https://www.adafruit.com/products/1461

Medium 16x32 RGB LED matrix panel
https://www.adafruit.com/products/420

12mm Diffused Thin Digital RGB LED Pixels (Strand of 25) - WS2801
https://www.adafruit.com/products/322
25 Pixel als "Lichterkette"

Im Adafruit Shop leider recht hohe Versandkosten >20€.

Lichterkette mit steuerbaren LEDs (43€)
http://www.exp-tech.de/12mm-diffused-flat-digital-rgb-led-pixels-strand-of-25-ws2801

bei Ebay
http://www.ebay.de/sch/i.html?_odkw=adafruit&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xdiffused+rgb+led.TRS0&_nkw=diffused+rgb+led&_sacat=0

bei Amazon
https://www.amazon.de/WS2811-Pixels-digital-Addressable-String/dp/B00MXW054Y/ref=sr_1_4?s=kitchen&ie=UTF8&qid=1483302387&sr=1-4&keywords=WS2801


Bauteile
========

WS2812B mit dem Controller WS2811 scheinen eine gute Lösung zu sein.

Level-Shifter: 3V -> 5V
https://www.adafruit.com/products/1787
https://cdn-shop.adafruit.com/datasheets/74AHC125.pdf


Händler
=======

Sparkfun: https://www.sparkfun.com/
Versandkosten ~ 8,50€ - 2.6 Wochen Lieferzeit

Lieferanten
http://www.mikrocontroller.net/articles/Hauptseite
http://www.mikrocontroller.net/articles/Elektronikversender

Elektronik Wunderland (Bochum)
http://www.elektronik-wunderland.de/


Anleitung
=========

http://www.aoakley.com/articles/2015-11-18-raspberry-pi-christmas-led-matrix.php
https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all

Lib für den Pi
https://github.com/jgarff/rpi_ws281x

git clone https://github.com/jgarff/rpi_ws281x.git
