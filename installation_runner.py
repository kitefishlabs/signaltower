#!/usr/bin/env python3

import time
from neopixel import *
# import argparse

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# LED strip configuration:
LED_COUNT = 16      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LED_COUNT = 180

# Define functions which animate LEDs in various ways.


def test_pattern(heartbeat=50):
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    time.sleep(2)
    """Wipe white across display a pixel at a time."""
    for i in range(LED_COUNT):
        strip.setPixelColor(i, (255, 255, 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(LED_COUNT):
        strip.setPixelColor(i, (0, 0, 0))
        strip.show()
        time.sleep(wait_ms/1000.0)
