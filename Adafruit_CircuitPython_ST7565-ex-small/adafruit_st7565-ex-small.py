# The MIT License (MIT)
#
# Copyright (c) 2017 Michael McWethy
#
# portions Copyright (c) 2018 Christopher W Hafey, wa1tnr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_st7565-ex-small`
====================================================

MicroPython ST7565 graphic LCD driver, SPI interface

From: adafruit_ssd1306.py, with similar intellectual property details.

* Author(s): Tony DiCola, Michael McWethy.  Contributions: Christopher W Hafey, wa1tnr
"""

import time
import framebuf

from adafruit_bus_device import spi_device
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_fictional_ST7565.git"

#pylint: disable-msg=bad-whitespace
# register definitions
SET_VOLUME_FIRST        = const(0x81)  # enhance gLCD contrast
SET_VOLUME_SECOND       = const(0x00)  # contrast, follow-on value
                                       # ex. 0x81, then 0x00 | (0x1d & 0x3f)
CMD_RMW                 = const(0xE0)
CMD_RMW_CLEAR           = const(0xEE)
CMD_INTERNAL_RESET      = const(0xE2)


# Early versions of the present program will kludge hexadecimal values
# directly into the code, and will not use these constants.

CMD_NOP                 = const(0xE3)
CMD_TEST                = const(0xF0)
#pylint: enable-msg=bad-whitespace


class _ST7565: # was: _ST7565nis
    """Base class for ST7565 display driver"""
    #pylint: disable-msg=too-many-arguments
    #pylint: disable-msg=too-many-instance-attributes
    def __init__(self, framebuffer, width, height, external_vcc, reset):
        self.framebuf = framebuffer
        self.fill = self.framebuf.fill
        self.pixel = self.framebuf.pixel
        self.line = self.framebuf.line
        self.text = self.framebuf.text
        self.scroll = self.framebuf.scroll
        self.blit = self.framebuf.blit
        self.vline = self.framebuf.vline
        self.hline = self.framebuf.hline
        self.fill_rect = self.framebuf.fill_rect
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        # reset may be None if not needed
        self.reset_pin = reset
        if self.reset_pin:
            self.reset_pin.switch_to_output(value=0)
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations of the upstream program (I2C
        # needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        """Base class to initialize display"""
        for cmd in ( 0xa3, 0x2c, 0x2e, 0x2f, 0x26, 0xaf, 0x81, 0x1d):
            self.write_cmd(cmd)

        # for cmd in ( 0x10, 0x00, 0xb0, 0xe0):
        #    self.write_cmd(cmd)

















        # self.fill(0)
        # self.show()

    def poweroff(self):
        franz = 0 # noop


    def contrast(self, contrast):
        franz = 0 # noop



    def invert(self, invert):
        franz = 0 # noop


    def write_framebuf(self):
        """Derived class must implement this"""
        raise NotImplementedError

    def write_cmd(self, cmd):
        """Derived class must implement this"""
        raise NotImplementedError

    def poweron(self): # L140 old
        "Reset device and turn on the display."
        if self.reset_pin:
            self.reset_pin.value = 1
            time.sleep(0.001)
            self.reset_pin.value = 0
            time.sleep(0.010)
            self.reset_pin.value = 1
            time.sleep(0.010)
        # self.write_cmd(SET_DISP | 0x01)

    def show(self):
        """Update the display"""
        xpos0 = 0
        xpos1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            xpos0 += 32
            xpos1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(xpos0)
        self.write_cmd(xpos1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()








































#pylint: disable-msg=too-many-arguments
class ST7565_SPI(_ST7565):
    """
    SPI class for ST7565

    :param width: the width of the physical screen in pixels,
    :param height: the height of the physical screen in pixels,
    :param spi: the SPI peripheral to use,
    :param a0: Register Select - the data/command pin to use (often labeled "D/C" but is a0 here),
    :param reset: the reset pin to use - aka /RST - active LOW,
    :param cs: the chip-select pin to use (sometimes labeled "SS" but is /cs here).
    """
    def __init__(self, width, height, spi, a0, reset, cs, *,
                 external_vcc=False, baudrate=8000000, polarity=0, phase=0):
        self.rate = 10 * 1024 * 1024
        a0.switch_to_output(value=0)
        self.spi_device = spi_device.SPIDevice(spi, cs, baudrate=baudrate,
                                               polarity=polarity, phase=phase)
        self.a0_pin = a0
        self.buffer = bytearray((height // 8) * width)
        framebuffer = framebuf.FrameBuffer1(self.buffer, width, height)
        super().__init__(framebuffer, width, height, external_vcc, reset)

    def write_cmd(self, cmd):
        """Send a command to the SPI device"""
        self.a0_pin.value = 0
        with self.spi_device as spi:
            spi.write(bytearray([cmd]))

    def write_framebuf(self):
        """write to the frame buffer via SPI"""
        self.a0_pin.value = 1
        with self.spi_device as spi:
            spi.write(self.buffer)

    def write_data_out(self, cmd): # not found in SSD1306 driver
        """write data out via SPI"""
        self.a0_pin.value = 1
        with self.spi_device as spi:
            spi.write(bytearray([cmd])) # useful alternate means to deliver data

# Line 247
