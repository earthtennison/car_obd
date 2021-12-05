import board
import busio
import adafruit_ssd1306
import digitalio
from PIL import Image, ImageDraw, ImageFont

class OLED:
    
    def __init__(self, width=128, height=64, addr=0x3c, font_path="font/Minicradft.ttf"):
        i2c = busio.I2C(board.SCL, board.SDA)

        # initialize oled
        # enable i2c fist, then
        # find address using $i2cconnect 1
        reset_pin = None # any pin!
        oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=addr) # 128 width x 64 height
        
        # Clear display
        oled.fill(0)
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (oled.width, oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white background
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        
        self.oled = oled
        self.image = image
        self.draw = draw
        self.display()
        self.font_path = font_path
        
    def write(self, text, size=15):
        # Draw a white background
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        
        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        font = ImageFont.truetype('Minecraft.ttf', 20)
        # Draw Some Text
        (font_width, font_height) = font.getsize(text)
        self.draw.text((self.oled.width//2 - font_width//2, self.oled.height//2 - font_height//2),
                  text, font=font, fill=0)
        self.display()

    def write_gauge(self, title, value, unit):
        # Draw a white background
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        
        font = ImageFont.truetype(self.font_path, 15)
        self.draw.text((5,5), title, font=font, fill=0)
        
        font = ImageFont.truetype(self.font_path, 40)
        (font_width, font_height) = font.getsize(value)
        self.draw.text((self.oled.width//2 - font_width//2, self.oled.height//2 - font_height//2),
                       value, font=font, fill=0)
        
        font = ImageFont.truetype(self.font_path, 15)
        self.draw.text((self.oled.width//2 + font_width//2 + 5, self.oled.height//2 + font_height//2),
                       unit, font=font, fill=0)
        self.display()
        
        
    def display(self):
        # Display image
        self.oled.image(self.image)
        self.oled.show()
        
    def clear(self):
        # Clear display
        self.oled.fill(0)
        self.oled.show()

if __name__ == "__main__":
    o = OLED()
    #o.write("rpm\n20")
    o.write_gauge("traveled", "20", "km")
