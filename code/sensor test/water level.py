import board
import analogio
import time
from digitalio import DigitalInOut, Direction, Pull



analog_out = analogio.AnalogIn(board.A0)


#5 je ešte ok hodnota. pod 5 je málo vody :))#

def ldr_value(x):
    # toto dava take ok hodnoty, ale preratavam to * 100 aby to d8valo kind of od 1 do 100 values
    x = x / 65535
    x = x*100
    return x

while True:
        
    print('analog output 17 = {0}'.format(ldr_value(analog_out.value)))

    time.sleep(0.1)
    


