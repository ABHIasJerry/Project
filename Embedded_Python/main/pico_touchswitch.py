from machine import Pin
import time

touch = Pin(18,Pin.IN,Pin.PULL_DOWN)   # Pin 24 of Pico
led = Pin(25,Pin.OUT)                  # On-board LED
red = Pin(11,Pin.OUT)
amber = Pin(12,Pin.OUT)
green = Pin(13,Pin.OUT)
onboard_temp_sensor = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
    amber.value(0)
    red.value(0)
    green.value(0)
    reading = onboard_temp_sensor.read_u16() * conversion_factor
    device_temperature = 27 - (reading - 0.706) / 0.001721
    if touch.value():
        print("Touch Detected")
        led.toggle()
        amber.value(1)
        red.toggle()
        print("Device Temperature:", device_temperature, "*C")
        time.sleep(0.5)