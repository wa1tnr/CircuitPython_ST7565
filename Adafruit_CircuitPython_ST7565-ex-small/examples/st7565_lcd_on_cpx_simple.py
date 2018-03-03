# Basic example of clearing and drawing pixels on a ST7565 graphic LCD display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# Modified: Christopher W Hafey, wa1tnr - February/March 2018
# License: Public Domain

print("  r019a0  ")

"""

We are on
   Adafruit CircuitPython 2.2.3 on 2018-02-05; Adafruit CircuitPlayground Express with samd21g18

pins ref:
https://github.com/adafruit/circuitpython/blob/master/ports/atmel-samd/boards/circuitplayground_express/pins.c#L6

    A1 SCK  PA05  D6
    A3 MOSI PA07  D10

siddacious: You should also be able to do
SCK=A3 
MOSI=A2 or

SCK = A1
MOSI = A3
nis: Okay because they're the same SERCOM0.x group.
siddacious: Yea, SCK can be on pad 1 or 3, MOSI on pad 0,2,3


PA05       PA06       PA07
A1         A2         A3
D6         D9         D10
SERCOM0.1  SERCOM0.2  SERCOM0.3
SCK        MOSI       MOSI
                      SCK

TESTED GOOD:

  MOSI A3 and SCK A1
  MOSI A2 and SCK A3 (nice, as physically paired closely)

FAILED:
  MOSI A2 and SCK A1


"""

# Import all board pins.
import board
import busio
import digitalio
import time

# Import the ST7565 module.
import adafruit_st7565

"""
PA05      PA06        PA07
A1          A2          A3
D6          D9         D10
"""

# Setup the port pins
# data = board.A3  #  make connection  at  pin A3 for CPX   MOSI   A3 MOSI PA07  D10
# clk  = board.A1  #  make connection  at  pin A1 for CPX   SCK    A1 SCK  PA05  D6

data = board.A2    #  make connection  at  pin A2 for CPX   MOSI   A2 MOSI PA06  D9
clk  = board.A3    #  make connection  at  pin A3 for CPX   SCK    A3 SCK  PA07  D10

a0        = digitalio.DigitalInOut(board.A7)
rst       = digitalio.DigitalInOut(board.A5)
cs        = digitalio.DigitalInOut(board.A4)

"""
wiring summary

  1 /CS  BROWN    mcu-A4     cs   = digitalio.DigitalInOut(board.A4)
  2 /RST RED      mcu-A5     rst  = digitalio.DigitalInOut(board.A5)
  3 AO   ORANGE   mcu-A7     a0   = digitalio.DigitalInOut(board.A7)
  4 SCLK YELLOW   mcu-A3     clk  = board.A3 #  make connection  at  pin A3 for CPX
  5 SID  GREEN    mcu-A2     data = board.A2 #  make connection  at  pin A2 for CPX
  6 VDD  BLUE     mcu-3.3
  7 GND  VIOLET   mcu-GND
"""

a0.switch_to_output(value       =False, drive_mode=digitalio.DriveMode.PUSH_PULL)
rst.switch_to_output(value      =True,  drive_mode=digitalio.DriveMode.PUSH_PULL)
cs.switch_to_output(value       =True,  drive_mode=digitalio.DriveMode.PUSH_PULL)

# Create the SPI interface.
spi = busio.SPI(clk, MOSI=data)

# Create the ST7565 gLCD class.
display = adafruit_st7565.ST7565_SPI(128, 64, spi, a0, rst, cs, external_vcc=False, baudrate=2000000, polarity=0, phase=0)


# char_out()
# write an array of 6 bytes to the display, left to right,
# to form the glyph of a text character.  Includes inter-
# character padding (of one pixel).

def char_out():
    global cmd, mbytes
    for p in range(0,6):
        cmd = mbytes[p]
        display.write_data_out(cmd)


# write_short_phrase_to_lcd()
# sequentially specify an array of six bytes, called mbytes,
# and write them to the LCD using char_out().  Iterate to
# spell a common word (in a human language, such as English)
# on the graphic display.

def write_short_phrase_to_lcd():
    global mbytes
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A  idea to use bytearray from deshipu's code
    char_out()
    mbytes = bytearray(b'\xfe\x82\x82\x82\x7c\x00')  # D 
    char_out()
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A
    char_out()
    mbytes = bytearray(b'\xfe\x90\x90\x90\x80\x00')  # F
    char_out()
    mbytes = bytearray(b'\xfe\x90\x98\x94\x62\x00')  # R
    char_out()
    mbytes = bytearray(b'\xfc\x02\x02\x02\xfc\x00')  # U
    char_out()
    mbytes = bytearray(b'\x00\x82\xfe\x82\x00\x00')  # I
    char_out()
    mbytes = bytearray(b'\xc0\x80\xfe\x80\xc0\x00')  # T
    char_out()


# write_inverted_phrase_to_lcd():
# See 'write_short_phrase_to_lcd()' -- same function, but made inverted,
# for a simple visual check (used only during active development) to verify
# that the program was recently updated.

def write_inverted_phrase_to_lcd():

    global mbytes
    mbytes = bytearray(b'\xc0\x80\xfe\x80\xc0\x00')  # T
    char_out() 
    mbytes = bytearray(b'\x00\x82\xfe\x82\x00\x00')  # I
    char_out() 
    mbytes = bytearray(b'\xfc\x02\x02\x02\xfc\x00')  # U
    char_out() 
    mbytes = bytearray(b'\xfe\x90\x98\x94\x62\x00')  # R
    char_out() 
    mbytes = bytearray(b'\xfe\x90\x90\x90\x80\x00')  # F
    char_out() 
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A
    char_out() 
    mbytes = bytearray(b'\xfe\x82\x82\x82\x7c\x00')  # D 
    char_out() 
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A
    char_out()


# disp_text_geom()
# setup positional metrics by commanding the display hardware,
# in preparation for a data stream that will be placed onto
# the display at the locations specified.
def disp_text_geom():
    global cmd
    page = 0 # vary from 0 to 7 - 3 is top row and 4 is bottom row.  0 is middle.
    column =  32 # must be zero or a multiple of 16
    icol   = column + 16
    cursor_right = (icol // 16) - 1
    cmd = (0x10 | cursor_right) ; display.write_cmd(cmd) # upper x positional byte
    cmd = (0x00 | 3)    ; display.write_cmd(cmd) # lower x positional byte - fine tuning
    cmd = (0xb0 | page)    ; display.write_cmd(cmd) # only  y positional byte - page 0 is middle row
    cmd = 0xe0          ; display.write_cmd(cmd)
    # write data here


# send_preamble()
# Unfinished idea -- specify an array of bytes, then write them as
# commands sent to the LCD controller.
#  
# This is an alternate format for sending bytes as commands, and
# is used when no tranforms are required against the data to be
# sent (as when OR'ing data into the byte to be sent).
#  
# Compare with disp_text_geom().

def send_preamble():
    mbytes = bytearray(b'\x12\x03\xb0\xe0')
    for p in range(0,4):
        cmd = mbytes[p]
        display.write_cmd(cmd)
        # write data here

def all_pixels_off():
    global cmd
    for i in range(0,8):
        cmd = (0xb0 | i) ; display.write_cmd(cmd)
        cmd = (0x10 | 0) ; display.write_cmd(cmd)
        cmd = (0x00 | 0) ; display.write_cmd(cmd)
        cmd = 0xe0       ; display.write_cmd(cmd)
        for j in range(0,129):
            cmd = (0x00) # substitute 0xff to turn all pixels on
            display.write_data_out(cmd)


# draw_solid_bar():  POORLY UNDERSTOOD
# Uses the library to do stuff.
# Pages are 8 pixels tall by 128 pixels wide.  When display.fill(1)
# is called, it interacts with the framebuffer, filling locations in
# that framebuffer with a color value (0 or 1; in this case, it's a '1').
# display.show() separately transfers this framebuffer (via SPI) to
# the display hardware (which has its own buffer).

def draw_solid_bar():
    display.fill(1) # default page is top line.  display.fill()
                    # applies to a single page, not the entire LCD
    display.show()


# init_lcd()
# Toggle /RST and call the library's init_display()
# For a finished look, turn off all pixels before
# moving on to the main program.

def init_lcd():
    global cmd, mbytes
    cs.value  = 0 ;
    rst.value = 0 ; time.sleep(0.2)
    rst.value = 1 ;
    display.init_display()
    all_pixels_off()


# Payload.  Show those messages!
def show_messages():
    # send_preamble()
    disp_text_geom()
    write_short_phrase_to_lcd()


# cruft to hang onto when needed:
def leppard():
    write_short_phrase_to_lcd()
    write_inverted_phrase_to_lcd()
    draw_solid_bar()


# - - - -   The Program   - - - -
init_lcd()
show_messages()

