# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
# from board import SCL, SDA, MOSI, SCK, A4
import board
import busio
import digitalio

# Import the SSD1306 module.
import adafruit_st7565nis

print("feldspar cranshow rotashow CENOPIC")

backlight = digitalio.DigitalInOut(board.A4)

data = board.MOSI   # Pin connected to backpack DAT/data.
clk  = board.SCK    # Pin connected to backpack CLK.

a0   = digitalio.DigitalInOut(board.D9)
rst  = digitalio.DigitalInOut(board.D6)
cs   = digitalio.DigitalInOut(board.D5)

backlight.switch_to_output(value=True, drive_mode=digitalio.DriveMode.PUSH_PULL)

rst.switch_to_output(value =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
a0.switch_to_output(value  =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
cs.switch_to_output(value  =True, drive_mode=digitalio.DriveMode.PUSH_PULL)

spi = busio.SPI(clk, MOSI=data)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_st7565nis.ST7565nis_SPI(128, 64, spi, a0, rst, cs, external_vcc=False, baudrate=2000000, polarity=0, phase=0)


def char_out():
    global cmd, muta_bytes
    for p in range(0,6):
        cmd = muta_bytes[p]
        display.write_datao(cmd)

def write_short_phrase_to_lcd():
    global muta_bytes
    muta_bytes = bytearray(b'\xfc\x02\x1c\x02\xfc\x00') # W - deshipu driver leads this idea
    char_out()
    muta_bytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00') # A
    char_out()
    muta_bytes = bytearray(b'\x00\x42\xfe\x02\x00\x00') # 1
    char_out()
    muta_bytes = bytearray(b'\xc0\x80\xfe\x80\xc0\x00') # T
    char_out()
    muta_bytes = bytearray(b'\xfe\x20\x10\x08\xfe\x00') # N
    char_out()
    muta_bytes = bytearray(b'\xfe\x90\x98\x94\x62\x00') # R
    char_out()
    muta_bytes = bytearray(b'\x10\x10\x10\x10\x10\x00') # dash
    char_out()
    muta_bytes = bytearray(b'\x82\x84\x88\x90\xe0\x00') # 7
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


disp_text_geom()
write_short_phrase_to_lcd()

muta_bytes = bytearray(b'\x10\x03\xb2\xe0') # 7
for p in range(0,4):
    cmd = muta_bytes[p]
    display.write_cmd(cmd)

display.fill(0xff)
display.show()

