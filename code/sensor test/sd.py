import board
import busio
import digitalio
import adafruit_sdcard
import storage

# Initialize SPI bus and pins
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP21)  # Chip select pin (pin 7)

# Initialize SD card object
sdcard = adafruit_sdcard.SDCard(spi, cs)

# Mount the SD card
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create a file and write data to it
with open("/sd/kokos.txt", "w") as file:
    file.write("U stink")

# Read data from the file
with open("/sd/kokos.txt", "r") as file:
    data = file.read()
    print(data)



