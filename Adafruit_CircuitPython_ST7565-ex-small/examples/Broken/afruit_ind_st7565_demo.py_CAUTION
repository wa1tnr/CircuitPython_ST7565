import board
import busio
import digitalio
import time

import adafruit_st7565

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
spi = busio.SPI(clk, MOSI=data)
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

def disp_logo_geom(page):
    global cmd
    column =  0 # must be zero or a multiple of 16
    icol   = column + 16
    cursor_right = (icol // 16) - 1
    cmd = (0x10 | 0)    ; display.write_cmd(cmd) # upper x positional byte
    cmd = (0x00 | 0)    ; display.write_cmd(cmd) # lower x positional byte - fine tuning
    cmd = (0xb0 | page)    ; display.write_cmd(cmd) # only  y positional byte - page 0 is middle row
    cmd = 0xe0          ; display.write_cmd(cmd)
    # write data here

def write_adafruit_logo_out(): # 32107654 page order
    global mbytes

    page = 2 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x03\x07\x0F\x1F\x1F\x3F\x3F\x3F\x3F\x07\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x7F\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x1F\x3F\x70\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x06\x00\x00\x00\x03\x03') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()

    page = 1 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x1F\x0F\x07\x07') ; char_out()
    mbytes = bytearray(b'\x07\x3F\xFF\xFF\xFF\xFF\xFF\xFE\xFF\xFF\xFF\xFF\xFF\x3E\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0F\x3F') ; char_out()
    mbytes = bytearray(b'\x70\x60\x60\x60\x60\x30\x7F\x3F\x00\x00\x1F\x3F\x70\x60\x60\x60') ; char_out()
    mbytes = bytearray(b'\x60\x39\xFF\xFF\x00\x06\x1F\x39\x60\x60\x60\x60\x30\x3F\x7F\x00') ; char_out()
    mbytes = bytearray(b'\x00\x60\xFF\xFF\x60\x60\x00\x7F\x7F\x70\x60\x60\x40\x00\x7F\x7F') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x7F\x7F\x00\x00\x00\x7F\x7F\x00\x00\x60\xFF\xFF') ; char_out()
    mbytes = bytearray(b'\x60\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()

    page = 0 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x80\xF8\xFC\xFE\xFE\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xEF\xE7\xE7\xE3') ; char_out()
    mbytes = bytearray(b'\xF3\xF9\xFF\xFF\xFF\xF7\x07\x1F\xFF\xFF\xFF\xFF\xFF\xFF\x7F\xFF') ; char_out()
    mbytes = bytearray(b'\x7F\x7F\x7F\x7F\x7F\x7F\x3F\x3F\x1F\x0F\x07\x03\x00\x00\x00\xC0') ; char_out()
    mbytes = bytearray(b'\xE0\x60\x20\x20\x60\xE0\xE0\xE0\x00\x00\x80\xC0\xE0\x60\x20\x60') ; char_out()
    mbytes = bytearray(b'\x60\xE0\xE0\xE0\x00\x00\x80\xC0\x60\x60\x20\x60\x60\xE0\xE0\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\xE0\xE0\x00\x00\x00\xE0\xE0\x00\x00\x00\x00\x00\x80\xE0') ; char_out()
    mbytes = bytearray(b'\x60\x60\x60\x60\xE0\x80\x00\x00\x00\xE0\xE0\x00\x00\x00\xE0\xE0') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()

    page = 7 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x00\x00\x00\x03\x07\x1F\x9F\xFF\xFF\xFF\xFF\xFF\xFF\xFD\xF1\xE3') ; char_out()
    mbytes = bytearray(b'\xE3\xCF\xFF\xFF\xFF\xFF\xF0\xFC\x7F\x3F\x3F\x3F\x3F\x7F\xFF\xFF') ; char_out()
    mbytes = bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xFC\xF0\xE0\x80\x00\x00\x00\x0C') ; char_out()
    mbytes = bytearray(b'\x1C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x7F\x7F\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x07\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1C\x0C\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()

    page = 6 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x00\x07\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xFE\xFE\xFE\xFC\xF8') ; char_out()
    mbytes = bytearray(b'\xF8\xF0\xFE\xFF\xFF\xFF\x7F\x3F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x1F') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF') ; char_out()
    mbytes = bytearray(b'\xFF\x00\x00\x00\xFF\xFF\xE0\xC0\xC0\xC0\xFF\x7F\x00\x00\x1E\x7F') ; char_out()
    mbytes = bytearray(b'\xE1\xC0\xC0\xC0\xC0\x61\xFF\xFF\x00\x00\xFE\xFF\x01\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\xFF\xFF\x00\x00\x21\xF9\xF8\xDC\xCC\xCF\x07\x00\xC0\xFF\xFF\xC0') ; char_out()
    mbytes = bytearray(b'\x80\x00\xFF\xFF\xC0\xC0\x80\x00\x00\xFF\xFF\x00\x00\x1F\x7F\xF9') ; char_out()
    mbytes = bytearray(b'\xC8\xC8\xC8\xC8\x79\x39\x00\x00\x71\xF9\xD8\xCC\xCE\x47\x03\x00') ; char_out()

    page = 5 ; disp_logo_geom(page)
    mbytes = bytearray(b'\x00\x00\x00\x00\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x80\xC0\xE0\xF0\xF8\xF8\xFC\xFC\xFC\xFC\xF8\xF0\xC0') ; char_out()
    mbytes = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0') ; char_out()
    mbytes = bytearray(b'\xC0\x00\x00\x00\xC0\xC0\x00\x00\x00\x00\xC0\xC0\x00\x00\x00\x80') ; char_out()
    mbytes = bytearray(b'\xC0\xC0\xC0\xC0\xC0\x80\xC0\xC0\x00\x00\x00\x80\xC0\xC0\xC0\xC0') ; char_out()
    mbytes = bytearray(b'\xC0\x80\x00\x00\x80\xC0\xC0\xC0\xC0\xC0\x00\x00\x00\xC0\xC0\x00') ; char_out()
    mbytes = bytearray(b'\x00\x00\xC0\x80\x00\x00\x00\x00\x00\xC0\xC0\x00\x00\x00\x80\xC0') ; char_out()
    mbytes = bytearray(b'\xC0\xC0\xC0\xC0\x80\x80\x00\x00\x80\xC0\xC0\xC0\xC0\x80\x00\x00') ; char_out()



def write_row():
    global cmd, page
    cmd = (0x10 | 0) ; display.write_cmd(cmd)
    cmd = (0x00 | 0) ; display.write_cmd(cmd)
    cmd = (0xb0 | page) ; display.write_cmd(cmd)
    cmd = 0xe0       ; display.write_cmd(cmd)
    for j in range(0,129):
        cmd = (0x00)
        display.write_data_out(cmd)

def all_pixels_off():
    global page
    for page in range(3,-1,-1):
        write_row()
    for page in range(7,3,-1):
        write_row()

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
    display.init_display()
    all_pixels_off()
    write_adafruit_logo_out()

def nopeis():
    time.sleep(8.2)

init_lcd()

# time.sleep(8.1)
"""
ST7565 LCD library!  ST7565.cpp

Copyright (C) 2010 Limor Fried, Adafruit Industries

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

some of this code was written by <cstone@pobox.com> originally; it is in the public domain.
"""

