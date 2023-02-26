from rainbowio import colorwheel
import neopixel
import time
import random

import array

num_pixels = 30

def rainbow_cycle(pixels,wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def neopix_twinkle_test(pixels,wait):
    is_lit = [False for i in range(num_pixels)]

    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)

    for i in range(num_pixels):
        pix = random.randint(0,num_pixels-1)
        while (is_lit[pix]):
            pix = random.randint(0,num_pixels-1)
        pixels[pix] = (red,green,blue)
        is_lit[pix] = True
        pixels.show()
        time.sleep(wait)

def neopix_test(pixels,wait):

    for i in range(num_pixels):
        #pixels[round(random(num_pixels))] = (10,0,0)
        #random.randint(1,num_pixels)
        pixels[num_pixels-(i+1)] = (255,0,10)
        pixels.show()
        time.sleep(wait)
    for i in range(num_pixels):
        pixels[i] = (20,10,255)
        pixels.show()
        time.sleep(wait)

