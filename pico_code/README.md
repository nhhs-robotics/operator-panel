# Prototype Code for Draft 1

* Need to download the Adafruit hid library and copy into the lib/ dir on the Pico
* Components: 
    * Arcade button
        * Wired to GP15 as a pullup 
        * LED requires 5V; not wired up to the Pico
    * Slider
        * Wired to A2
        * Requires analog
    * Analog joystick
        * Wired to A0 and A1
        * It's sending data, but the data is not scaled/zeroed correctly yet
    * Toggle switch
        * Wired to GP14 as a pullup

