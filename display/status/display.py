import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class display(object):
    def __init__(self):
        self.screen = None

        self.width = 128
        self.height = 64
        self.i2cAddr = 0x3C

        self.initialize()

        self.titleFont = self.getFont(12)
        self.infoFont = self.getFont(14)

    def initialize(self):
        # Use for I2C.
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, self.i2c, addr=self.i2cAddr)

        self.clearScreen()
    
    # Clear display.
    def clearScreen(self):
        self.oled.fill(0)
        self.oled.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

    def getFont(self, fontSize):
        # REF: https://www.programcreek.com/python/example/68996/PIL.ImageFont.load_default
        try:
            # For Linux
            font = ImageFont.truetype("DejaVuSans.ttf", fontSize)
        except Exception:
            print("Pi Status ->\t{0}".format("No font DejaVuSans; use default instead"), flush=True)
            # For others
            font = ImageFont.load_default()
        
        return font

    def getTimeString(self):
        s = time.localtime()
        t = time.strftime("%Y-%m-%d %H:%M:%S", s)

        return t
    
    def updateDisplay(self, title, valueTitle, valueText, value, centerTitle=False):
        t = self.getTimeString()
        print("Pi Status Update ->\t{0}\t{1}\t{2}\t{3}\t{4:.0f}".format(t, title, valueTitle, valueText, value), flush=True)
        # Clear the screen
        self.clearScreen()

        # Show Title
        x = 0
        if centerTitle:
            (font_width, font_height) = self.titleFont.getsize(title)
            x = self.oled.width // 2 - font_width // 2
        self.draw.text(
            (x, 0),
            title,
            font=self.titleFont,
            fill=255,
        )

        # Draw line
        self.draw.line([(0, 15), (self.oled.width, 15)], fill=255, width=0)

        # Display Text
        (font_width, font_height) = self.infoFont.getsize(valueTitle)
        self.draw.text(
            (self.oled.width // 2 - font_width // 2, 16),
            valueTitle,
            font=self.infoFont,
            fill=255,
        )

        # Display Text
        (font_width, font_height) = self.infoFont.getsize(valueText)
        self.draw.text(
            (self.oled.width // 2 - font_width // 2, 32),
            valueText,
            font=self.infoFont,
            fill=255,
        )

        # Display Value
        if value >= 0:
            x = (self.oled.width - 100) // 2
            for i in range(10):
                if i < value:
                    self.draw.rectangle((x, 50, x+6, 63), outline=255, fill=255)
                else:
                    # self.draw.line([(x, 63), (x+6, 63)], fill=255, width=1)
                    self.draw.rectangle((x, 50, x+6, 63), outline=255, fill=0)
                
                x += 10

        # Display image
        self.oled.image(self.image)
        self.oled.show()