# Basic example of clearing and drawing pixels on a ST7565 graphic LCD display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# Modified: Christopher W Hafey, wa1tnr - February 2018
# License: Public Domain

# Import all board pins.
import board
import busio
import digitalio
import time

# Import the ST7565 module.
import adafruit_st7565

# Setup the port pins
data = board.MOSI
clk  = board.SCK

backlight = digitalio.DigitalInOut(board.A4) # optional - do not distribute
a0        = digitalio.DigitalInOut(board.D9)
rst       = digitalio.DigitalInOut(board.D6)
cs        = digitalio.DigitalInOut(board.D5)

backlight.switch_to_output(value=True,  drive_mode=digitalio.DriveMode.PUSH_PULL) # optional

a0.switch_to_output(value       =False, drive_mode=digitalio.DriveMode.PUSH_PULL)
rst.switch_to_output(value      =True,  drive_mode=digitalio.DriveMode.PUSH_PULL)
cs.switch_to_output(value       =True,  drive_mode=digitalio.DriveMode.PUSH_PULL)

# Create the SPI interface.
spi = busio.SPI(clk, MOSI=data)

# Create the ST7565 gLCD class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_st7565.ST7565_SPI(128, 64, spi, a0, rst, cs, external_vcc=False, baudrate=2000000, polarity=0, phase=0)

display.fill(1)

# display.show()

# Set a pixel in the origin 0,0 position.
# display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
# display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
# display.pixel(127, 31, 1)
# display.show()

def char_out():
    global cmd, mbytes
    for p in range(0,6):
        cmd = mbytes[p]
        display.write_data_out(cmd)

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

def disp_text_geom():
    global cmd
    column =  32 # must be zero or a multiple of 16
    icol   = column + 16
    cursor_right = (icol // 16) - 1
    cmd = (0x10 | cursor_right) ; display.write_cmd(cmd) # upper x positional byte
    cmd = (0x00 | 3)    ; display.write_cmd(cmd) # lower x positional byte - fine tuning
    cmd = (0xb0 | 0)    ; display.write_cmd(cmd) # only  y positional byte - page 0 is middle row
    cmd = 0xe0          ; display.write_cmd(cmd)
    # write data here

def draw_solid_bar(): # fill all pixels in 8 consecutive rows to form a black bar
    mbytes = bytearray(b'\x10\x01\xb2\xe0') # 7
    for p in range(0,4):
        cmd = mbytes[p]
        display.write_cmd(cmd)
    # these are not understood correctly, yet:
    display.fill(0xff)
    display.show()

def all_pixels_off():
    global cmd
    for i in range(0,8):
        cmd = (0xb0 | i) ; display.write_cmd(cmd)
        cmd = (0x10 | 0) ; display.write_cmd(cmd)
        cmd = (0x00 | 0) ; display.write_cmd(cmd)
        cmd = 0xe0       ; display.write_cmd(cmd)
        for j in range(0,129):
            cmd = (0x00)
            display.write_data_out(cmd)

def cmd_out8():
    global cmd, mbytes
    for p in range(0,8):
        cmd = mbytes[p]
        display.write_cmd(cmd)

def init_display():
    global cmd, mbytes
    cs.value  = 0 ;
    rst.value = 0 ; time.sleep(0.2)
    rst.value = 1 ;
    mbytes = bytearray(b'\xa3\x2c\x2e\x2f\x26\xaf\x81\x1d') # 8 bytes
    cmd_out8()
    all_pixels_off()
    disp_text_geom()
    write_short_phrase_to_lcd()

init_display()

