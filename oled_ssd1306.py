from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Pillow or PIL.
ssd1306_address = 0x3c
rotation = 1 # 0 is no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3 represents 270° rotation

serial = i2c(port=1, address=ssd1306_address)
device = ssd1306(serial, rotate=rotation)

# device.display()
print(device.size)
print(device.width, device.height)
print(device.bounding_box)

with canvas(device) as draw: # draw is PIL.ImageDraw object
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello World", fill="white")

time.sleep(1)


with canvas(device, dither=True) as draw:
    draw.rectangle((10, 10, 30, 30), outline="white", fill="red")

time.sleep(1)


# Box and text rendered in portrait mode
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="white")
time.sleep(1)




