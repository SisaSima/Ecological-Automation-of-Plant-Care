import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_sh1106 import SH1106
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import time
import board


#btn = DigitalInOut(board.GP16)
#btn.direction = Direction.INPUT
#btn.pull = Pull.UP

# Release any resources currently in use for the displays
displayio.release_displays()

# Define the I2C pins
sda_pin = board.GP0
scl_pin = board.GP1

# Initialize the I2C bus
i2c = busio.I2C(scl=scl_pin, sda=sda_pin)

# Create the SSD1306 OLED display object
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 130
HEIGHT = 70

# Create the SSD1306 display object
display = SH1106(display_bus, width=WIDTH, height=HEIGHT)
display.auto_refresh = False

# Create a display context for drawing
splash = displayio.Group()
display.show(splash)

# Draw a label
text = ""
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=2, y=10)
splash.append(text_area)
# Keep the display updated




# Initialize the analog pin for the soil moisture sensor
soil_moisture_pin = AnalogIn(board.A1)

def get_voltage(pin):
    # Convert the analog pin value (0-65535) to a voltage (0-3.3V)
    return (pin.value * 3.3) / 65536
    
def get_moisture_level(voltage):
    # Convert the voltage to a moisture level percentage
    # This is a rough conversion, adjust based on your sensor's specifications
    return 100-(voltage / 3.3)*100
    #return voltage/3.3


while True:
   # Read the voltage from the soil moisture sensor
    voltage = get_voltage(soil_moisture_pin)
    
    # Calculate the moisture level percentage
    moisture_level = get_moisture_level(voltage)
    
    # Print the values
    #print("Soil Moisture Voltage: {:.2f} V".format(voltage))
    print("Soil Moisture Level: {:.2f}%".format(moisture_level*(120/100)))
    
    print()
    
    text_area.text = "{0}".format(moisture_level*(120/100))
    display.refresh()
    
    time.sleep(0.1)

    # Wait for a second before reading again



