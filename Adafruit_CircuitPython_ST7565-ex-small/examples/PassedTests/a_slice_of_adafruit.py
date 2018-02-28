# example on a ST7565 graphic LCD display.
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
display = adafruit_st7565.ST7565_SPI(128, 64, spi, a0, rst, cs, external_vcc=False,                     polarity=0, phase=0)


def char_out():
    global cmd, mbytes
    for p in range(0,16):
        cmd = mbytes[p]
        display.write_data_out(cmd)

def char6_out():
    global cmd, mbytes
    for p in range(0,6):
        cmd = mbytes[p]
        display.write_data_out(cmd)


def write_adafruit_logo_out():
    global mbytes
    mbytes = bytearray(b'\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x0F\x07\x07') ; char_out()
    mbytes = bytearray(b'\x07\x3F\xFF\xFF\xFF\xFF\xFF\xFE\xFF\xFF\xFF\xFF\xFF\x3E\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0F\x3F') ; char_out()
    mbytes = bytearray(b'\x70\x60\x60\x60\x60\x30\x7F\x3F\x00\x00\x1F\x3F\x70\x60\x60\x60') ; char_out()
    mbytes = bytearray(b'\x60\x39\xFF\xFF\x00\x06\x1F\x39\x60\x60\x60\x60\x30\x3F\x7F\x00') ; char_out()
    mbytes = bytearray(b'\x00\x60\xFF\xFF\x60\x60\x00\x7F\x7F\x70\x60\x60\x40\x00\x7F\x7F') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x7F\x7F\x00\x00\x00\x7F\x7F\x00\x00\x60\xFF\xFF') ; char_out()
    mbytes = bytearray(b'\x60\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()

    mbytes = bytearray(b'\x00\x07\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xFE\xFE\xFE\xFC\xF8') ; char_out()
    mbytes = bytearray(b'\xF8\xF0\xFE\xFF\xFF\xFF\x7F\x3F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x1F') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF') ; char_out()
    mbytes = bytearray(b'\xFF\x00\x00\x00\xFF\xFF\xE0\xC0\xC0\xC0\xFF\x7F\x00\x00\x1E\x7F') ; char_out()
    mbytes = bytearray(b'\xE1\xC0\xC0\xC0\xC0\x61\xFF\xFF\x00\x00\xFE\xFF\x01\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\xFF\xFF\x00\x00\x21\xF9\xF8\xDC\xCC\xCF\x07\x00\xC0\xFF\xFF\xC0') ; char_out()
    mbytes = bytearray(b'\x80\x00\xFF\xFF\xC0\xC0\x80\x00\x00\xFF\xFF\x00\x00\x1F\x7F\xF9') ; char_out()
    mbytes = bytearray(b'\xC8\xC8\xC8\xC8\x79\x39\x00\x00\x71\xF9\xD8\xCC\xCE\x47\x03\x00') ; char_out()






def write_short_phrase_to_lcd():
    global mbytes
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A  idea to use bytearray from deshipu's code
    char6_out()
    mbytes = bytearray(b'\xfe\x82\x82\x82\x7c\x00')  # D 
    char6_out()
    mbytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00')  # A
    char6_out()
    mbytes = bytearray(b'\xfe\x90\x90\x90\x80\x00')  # F
    char6_out()
    mbytes = bytearray(b'\xfe\x90\x98\x94\x62\x00')  # R
    char6_out()
    mbytes = bytearray(b'\xfc\x02\x02\x02\xfc\x00')  # U
    char6_out()
    mbytes = bytearray(b'\x00\x82\xfe\x82\x00\x00')  # I
    char6_out()
    mbytes = bytearray(b'\xc0\x80\xfe\x80\xc0\x00')  # T
    char6_out()


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

def all_pixels_on():
    global cmd
    for i in range(0,8):
        cmd = (0xb0 | i) ; display.write_cmd(cmd)
        cmd = (0x10 | 0) ; display.write_cmd(cmd)
        cmd = (0x00 | 0) ; display.write_cmd(cmd)
        cmd = 0xe0       ; display.write_cmd(cmd)
        for j in range(0,129):
            cmd = (0xff)
            display.write_data_out(cmd)

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


def disp_logo_geom():
    global cmd
    column =  0 # must be zero or a multiple of 16
    icol   = column + 16
    cursor_right = (icol // 16) - 1
    cmd = (0x10 | 0)    ; display.write_cmd(cmd) # upper x positional byte
    cmd = (0x00 | 0)    ; display.write_cmd(cmd) # lower x positional byte - fine tuning
    cmd = (0xb0 | 0)    ; display.write_cmd(cmd) # only  y positional byte - page 0 is middle row
    cmd = 0xe0          ; display.write_cmd(cmd)
    # write data here

def cmd_out8():
    global cmd, mbytes
    for p in range(0,8):
        cmd = mbytes[p]
        display.write_cmd(cmd)

def init_lcd():
    global cmd, mbytes
    cs.value  = 0 ;
    rst.value = 0 ; time.sleep(0.2)
    rst.value = 1 ;
    # mbytes = bytearray(b'\xa3\x2c\x2e\x2f\x26\xaf\x81\x1d') # 8 bytes
    # cmd_out8()
    display.init_display()
    all_pixels_off()
    disp_logo_geom()
    write_adafruit_logo_out()

def nexifi():
    write_short_phrase_to_lcd()
    all_pixels_off()
    disp_text_geom()
    disp_logo_geom()
    adafruit_logo_out()
    # all_pixels_off()

def appendii():
    time.sleep(8.1)
    all_pixels_on()
    time.sleep(8.1)
    all_pixels_off()
    disp_text_geom()
    write_short_phrase_to_lcd()

init_lcd()

# time.sleep(8.1)
