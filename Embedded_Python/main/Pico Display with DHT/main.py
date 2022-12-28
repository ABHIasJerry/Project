from machine import Pin, I2C
from SSD1306 import SSD1306_I2C
import utime as time
from dht import DHT11, InvalidChecksum

WIDTH = 128  # oled display width
HEIGHT = 64  # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)  # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : " + hex(i2c.scan()[0]).upper())  # Display device address
print("I2C Configuration: " + str(i2c))  # Display I2C config

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)  # Init oled display

while True:
    time.sleep(1)
    pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t = (sensor.temperature)
    h = (sensor.humidity)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    # Clear the oled display in case it has junk on it.
    oled.fill(0)

    # Add some text
    oled.text("Temp: ", 10, 10)
    oled.text(str(sensor.temperature), 50, 10)
    oled.text("*C", 90, 10)

    oled.text("Humi: ", 10, 30)
    oled.text(str(sensor.humidity), 50, 30)
    oled.text("%", 90, 30)

    time.sleep(1)
    oled.show()