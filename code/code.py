import time
import board
from analogio import AnalogIn
import digitalio
import busio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_sh1106 import SH1106
from digitalio import DigitalInOut, Direction, Pull
import adafruit_sht31d
import adafruit_sdcard
import storage


# premenne
doba_polievania = float(5)
cas_kontroly = 0.1
dry_val = 45
chcena_val = 60 # pozadovana vlhkost
filename = "doba_polievania"
filename2 = "vlhkost"
odmlka_senzoru = 5

   

# výška hladiny premenne
malo = 0.35
polovica = 0.56
akurat = 0.7
full = 0.85
error = 1.5

#SDcard
# Initialize SPI bus and pins
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP21)  # Chip select pin (pin 7)
# Initialize SD card object
sdcard = adafruit_sdcard.SDCard(spi, cs)
# Mount the SD card
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
# Create a file and write data to it

try:
    with open("/sd/{0}.txt".format(filename), "r") as file:
        for line in file:
            pass
        doba_polievania = float(line)
        print(doba_polievania)
except:
    doba_polievania = doba_polievania


"""
THIS WORKS
with open("/sd/{0}.txt".format(filename), "a") as file:
    file.write("\n{0}".format(doba_polievania))
with open("/sd/{0}.txt".format(filename), "r") as file:
    for line in file:
        pass
    doba_polievania = line
    print(doba_polievania)
"""

# SHT30
i2c_sht30 = busio.I2C(scl=board.GP3, sda=board.GP2)
sensor = adafruit_sht31d.SHT31D(i2c_sht30)

# moturek definice
moturek = digitalio.DigitalInOut(board.GP13)
moturek.direction = digitalio.Direction.OUTPUT

# Didplay "Even if a cow walked by udder, if it works, dont touch it"
# Release any resources currently in use for the displays
displayio.release_displays()
sda_pin = board.GP0
scl_pin = board.GP1
i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 130
HEIGHT = 70
display = SH1106(display_bus, width=WIDTH, height=HEIGHT, rotation=180)
display.auto_refresh = False
splash = displayio.Group()
display.show(splash)
# Draw a label
text = ""
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=2, y=10)
splash.append(text_area)

# soil moisture
soil_moisture_pin = AnalogIn(board.A1)
#hladina vody
hladina_vody_pin = AnalogIn(board.A0)
# sprav vo while cykle if hladina vody < x: print('m8lo vody')..atd


def get_voltage(pin):
    # Convert the analog pin value (0-65535) to a voltage (0-3.3V)
    return (pin.value * 3.3) / 65536
def get_moisture_level(voltage):
    # Convert the voltage to a moisture level percentage
    # This is a rough conversion, adjust based on your sensor's specifications
    return 100-(voltage / 3.3)*100
    #return voltage/3.3


while True:
   
### IF DONE: DElETE ###
    #doba_polievania = 1 ### <--THIS ### JUST DELETEIT, lebo ti to kurví program
    
    print(doba_polievania)
    #print(type(doba_polievania))
    
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    print(f"Temperature: {temperature:.2f} C")
    print(f"Humidity: {humidity:.2f} %")
    
# Read the voltage from the soil moisture sensor
    voltage = get_voltage(soil_moisture_pin)
    voltage_hladina_vody = get_voltage(hladina_vody_pin)
    
# hodnoty výšky hladiny vody
    if voltage_hladina_vody <= malo:
        voltage_hladina_vody_value = 'malo'
    if voltage_hladina_vody <= polovica and voltage_hladina_vody >= malo:
        voltage_hladina_vody_value = 'polovica'
    if voltage_hladina_vody <= akurat and voltage_hladina_vody >= polovica:
        voltage_hladina_vody_value = 'akurat'
    if voltage_hladina_vody >= akurat and voltage_hladina_vody <= full:
        voltage_hladina_vody_value = 'full'
    if voltage_hladina_vody >= full:
        voltage_hladina_vody_value = 'error:touching'

# Calculate the moisture level percentage
    moisture_level = get_moisture_level(voltage)
    
    # Print the values
    #print("Soil Moisture Voltage: {:.2f} V".format(voltage))
    print("Soil Moisture Level: {:.2f}%".format(moisture_level*(120/100)))
    
    print()
    
    text_area.text = "soil:{0}\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
    display.refresh()

    if moisture_level*(120/100) <= dry_val:
        print('moturek on')
        moturek.value = True
        time.sleep(doba_polievania)
        moturek.value = False
        time.sleep(odmlka_senzoru)

        # znovu zneram hodnotu na moisture analog pine, aby som zistila novú hodnotu
        voltage = get_voltage(soil_moisture_pin)
        moisture_level = get_moisture_level(voltage)
        with open("/sd/{0}.txt".format(filename2), "a") as file:
            file.write("\n{0}".format(moisture_level*(120/100)))

        #matematicka operacia
        doba_polievania = doba_polievania*(chcena_val/(moisture_level*(120/100)))
        with open("/sd/{0}.txt".format(filename), "a") as file:
            file.write("\n{0}".format(doba_polievania))

        # display refresh
        text_area.text = "soil:{0} Motor on\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
        display.refresh() 
        
        
        text_area.text = "soil:{0} Motor on\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
        display.refresh()        
        #time.sleep(doba_polievania)

    else:
        print('moturek off')
        moturek.value = False
        text_area.text = "soil:{0}\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
        display.refresh()        

# new doba_polievania value check
    try:
        with open("/sd/{0}.txt".format(filename), "r") as file:
            for line in file:
                pass
            doba_polievania = float(line)
            print(doba_polievania)
    except:
        doba_polievania = doba_polievania
     
    time.sleep(cas_kontroly)
