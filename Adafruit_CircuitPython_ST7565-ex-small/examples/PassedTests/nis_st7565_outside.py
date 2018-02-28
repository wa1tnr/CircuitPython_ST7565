
# Sun Feb 25 03:11:22 UTC 2018

import busio
import board
import digitalio
import time

print("standalone ST7565 program - no driver required."), print("  VERSION 0.0.2b");

backlight = digitalio.DigitalInOut(board.A4)

sid  = digitalio.DigitalInOut(board.MOSI)
sclk = digitalio.DigitalInOut(board.SCK)
a0   = digitalio.DigitalInOut(board.D9)
rst  = digitalio.DigitalInOut(board.D6)
cs   = digitalio.DigitalInOut(board.D5)

backlight.switch_to_output(value=True, drive_mode=digitalio.DriveMode.PUSH_PULL)

sclk.switch_to_output(value=True, drive_mode=digitalio.DriveMode.PUSH_PULL)
sid.switch_to_output(value =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
rst.switch_to_output(value =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
a0.switch_to_output(value  =False, drive_mode=digitalio.DriveMode.PUSH_PULL)
cs.switch_to_output(value  =True, drive_mode=digitalio.DriveMode.PUSH_PULL)


global cmd
cmd = 0

def spiwrite():
    global cmd
    for i in range (7,-1,-1):
        sclk.value = 0
        if (cmd & (1 << ((i)))):
            sid.value = 1
        else:
            sid.value = 0
        sclk.value = 1


def write_cmd():
    global cmd
    a0.value = 0
    spiwrite()

def write_data():
    global cmd
    a0.value = 1
    spiwrite()


def all_pixels_off():
    global cmd
    for i in range(0,8):
        cmd = (0xb0 | i) ; write_cmd()
        cmd = (0x10 | 0) ; write_cmd()
        cmd = (0x00 | 0) ; write_cmd()
        cmd = 0xe0       ; write_cmd()
        for j in range(0,129):
            cmd = (0x00)
            write_data()


def all_pixels_on():
    global cmd
    for i in range(0,8):
        cmd = (0xb0 | i) ; write_cmd()
        cmd = (0x10 | 0) ; write_cmd()
        cmd = (0x00 | 0) ; write_cmd()
        cmd = 0xe0       ; write_cmd()
        for j in range(0,129):
            cmd = (0xff)
            write_data()


def disp_text_geom():
    global cmd
    column =  32 # must be zero or a multiple of 16
    icol   = column + 16
    cursor_right = (icol // 16) - 1
    cmd = (0x10 | cursor_right) ; write_cmd() # upper x positional byte
    cmd = (0x00 | 3)    ; write_cmd() # lower x positional byte - fine tuning
    cmd = (0xb0 | 0)    ; write_cmd() # only  y positional byte - page 0 is middle row
    cmd = 0xe0          ; write_cmd()
    # write data here


def char_out():
    global cmd, muta_bytes
    for p in range(0,6):
        cmd = muta_bytes[p] # own research and experience
        write_data() # assumes preconditions


def write_short_phrase_to_lcd():
    global muta_bytes
    muta_bytes = bytearray(b'\xfc\x02\x1c\x02\xfc\x00') # W - deshipu driver leads this idea
    char_out()
    muta_bytes = bytearray(b'\x10\x10\x10\x10\x10\x00') # dash
    char_out()
    muta_bytes = bytearray(b'\xc0\x80\xfe\x80\xc0\x00') # T
    char_out()
    muta_bytes = bytearray(b'\xfe\x20\x10\x08\xfe\x00') # N
    char_out()
    muta_bytes = bytearray(b'\x00\x42\xfe\x02\x00\x00') # 1
    char_out()
    muta_bytes = bytearray(b'\xfe\x90\x98\x94\x62\x00') # R
    char_out()
    muta_bytes = bytearray(b'\x3e\x48\x88\x48\x3e\x00') # A
    char_out()
    muta_bytes = bytearray(b'\x82\x84\x88\x90\xe0\x00') # 7
    char_out()


def cmd_out8():
    global cmd, muta_bytes
    for p in range(0,8):
        cmd = muta_bytes[p]
        write_cmd()

def init_display():
    global cmd, muta_bytes

    cs.value  = 0 ;
    rst.value = 0 ; time.sleep(0.2)
    rst.value = 1 ;
    muta_bytes = bytearray(b'\xa3\x2c\x2e\x2f\x26\xaf\x81\x1d') # 8 bytes
    cmd_out8()

    all_pixels_off()
    disp_text_geom()
    write_short_phrase_to_lcd()


init_display()

