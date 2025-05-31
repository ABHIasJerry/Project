# UART Communication Example with Raspberry Pi Pico W

# import
import machine, utime
from machine import Pin

# Initialize the onboard LED (GPIO 2)
led = Pin("LED", Pin.OUT)

# Define UART pins | # UART0, GP0 -> (TX)(yellow)   & GP1 -> (RX)(purple)
uart = machine.UART(0, baudrate=115200, bits=8, parity=None, stop=1, tx=0, rx=1, timeout=300)

# Define UART pins | # UART1, GP4 -> (TX)(orange)   & GP5 -> (RX)(gray)
uart1 = machine.UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=4, rx=5, timeout=300)  

# Count buffer data
counter = int(0)
status = False
received_data = " "
readable_data = " "
while True:

    # Receive data
    if uart.any():
        led.on()
        received_data = uart.read()
        print("UART data counter -> ", counter)
        print(f"Received UART1 data ::  [{received_data}] ")
        counter += 1
        status = True
        led.off()

    # Decode bytes to a readable string (UTF-8 or other encoding)
    if status:
        readable_data = received_data.decode('utf-8').strip()
        print(f"Received UART1 readable data ::  [{readable_data}] \n")
        status = False
        
    # Send data
    uart1.write(readable_data)
        
    utime.sleep(1)

