import time
import board
import busio
import adafruit_sht31d

# Create I2C bus
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)

# Create sensor instance
sensor = adafruit_sht31d.SHT31D(i2c)

# Main loop to read temperature and humidity
while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity

    print(f"Temperature: {temperature:.2f} C")
    print(f"Humidity: {humidity:.2f} %")

    time.sleep(0.1)  # Delay for 2 seconds

