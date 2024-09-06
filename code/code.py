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

# premenne
doba_polievania = 5
cas_kontroly = 0.1
dry_val = 45

#polievanie premenne
malo = 0.35
polovica = 0.56
akurat = 0.7
full = 0.85
error = 1.5


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
display = SH1106(display_bus, width=WIDTH, height=HEIGHT)
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
        text_area.text = "soil:{0} Motor on\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
        display.refresh()        
        #time.sleep(doba_polievania)

    else:
        print('moturek off')
        moturek.value = False
        text_area.text = "soil:{0}\nhladina:{1}\nteplota:{2}\nvlhkost:{3}".format(moisture_level*(120/100),voltage_hladina_vody_value, temperature, humidity)
        display.refresh()        
        
    time.sleep(cas_kontroly)
