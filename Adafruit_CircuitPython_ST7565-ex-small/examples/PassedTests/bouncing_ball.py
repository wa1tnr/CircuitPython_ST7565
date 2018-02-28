import board
import busio
import digitalio
import adafruit_st7565

print("jake calico  feldspar cranshow rotashow CENOPIC")

backlight = digitalio.DigitalInOut(board.A4)
data = board.MOSI   # Pin connected to backpack DAT/data.
clk  = board.SCK    # Pin connected to backpack CLK.
a0   = digitalio.DigitalInOut(board.D9)
rst  = digitalio.DigitalInOut(board.D6)
cs   = digitalio.DigitalInOut(board.D5)
backlight.switch_to_output(value=True, drive_mode=digitalio.DriveMode.PUSH_PULL)
a0.switch_to_output(value  =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
rst.switch_to_output(value =True, drive_mode=digitalio.DriveMode.PUSH_PULL)
cs.switch_to_output(value  =True, drive_mode=digitalio.DriveMode.PUSH_PULL)

# Create the SPI interface.
spi = busio.SPI(clk, MOSI=data)

# Create the ST7565 gLCD class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

display = adafruit_st7565.ST7565_SPI(128, 64, spi, a0, rst, cs, external_vcc=False, baudrate=2000000, polarity=0, phase=0)

# Helper function to draw a circle from a given position with a given radius
# This is an implementation of the midpoint circle algorithm,
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example for details
def draw_circle(xpos0, ypos0, rad, col=1):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)

# initial center of the circle
center_x = 63
center_y = 15
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 8

# start with a blank screen
display.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
display.show()
while True:
    # undraw the previous circle
    draw_circle(center_x, center_y, radius, col=0)

    # if bouncing off right
    if center_x + radius >= display.width:
        # start moving to the left
        x_inc = -1
    # if bouncing off left
    elif center_x - radius < 0:
        # start moving to the right
        x_inc = 1

    # if bouncing off top
    if center_y + radius >= display.height:
        # start moving down
        y_inc = -1
    # if bouncing off bottom
    elif center_y - radius < 0:
        # start moving up
        y_inc = 1

    # go more in the current direction
    center_x += x_inc
    center_y += y_inc

    # draw the new circle
    draw_circle(center_x, center_y, radius)
    # show all the changes we just made
    display.show()


