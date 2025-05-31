
# Link: https://randomnerdtutorials.com/raspberry-pi-pico-microsd-card-micropython/

"""
MicroSD Card Module	         Raspberry Pi Pico
    3V3*	                    3V3(OUT)
    CS	                        GPIO 5
    MOSI (TX)	                GPIO 3
    CLK/SCK	                    GPIO 2
    MISO (RX)	                GPIO 4
    GND	                        GND
"""


from machine import UART, Pin, SPI
import time, sdcard, os

# Constants
SPI_BUS = 0
SCK_PIN = 2
MOSI_PIN = 3
MISO_PIN = 4
CS_PIN = 5
SD_MOUNT_PATH = '/sd'
FILE_PATH = 'sd/esp_buffer_data.txt'

# Initialize UART (UART0 is used here)
# UART0 TX -> GPIO0, RX -> GPIO1
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def sdcard_data_mount(data):
    # Init SPI communication
    spi = SPI(SPI_BUS,sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
    cs = Pin(CS_PIN)
    sd = sdcard.SDCard(spi, cs)
    
    os.mount(sd, SD_MOUNT_PATH)   # Mount microSD card
    # List files on the microSD card
    # print(os.listdir(SD_MOUNT_PATH))
    
    # Create new file on the microSD card
    with open(FILE_PATH, "a") as file:
        # Write to the file
        file.write(data)
        file.write(",")
        file.write("\n")
        
    # Check that the file was created:
    # print(os.listdir(SD_MOUNT_PATH))
    
    # Open the file in reading mode
    # with open(FILE_PATH, "r") as file:
    #     # read the file content
    #     content = file.read()
    #     print("File content:", content)  
    

def get_UART0_data_from_esp32():
    
    try:
        while True:
            if uart.any():  # Check if data is available
                data = uart.read()  # Read the incoming data
                data = data.split("\n")
                if data:
                    print("Received:", data.decode('utf-8'))  # Decode and print the data
                    sdcard_data_mount(data)  # write on SD card
                    dataframe = list(data)
                    # add this to webpage
            time.sleep(0.1)  # Small delay to avoid busy-waiting
    except Exception as e:
        print('An error occurred:', e)


# main code:
if __name__ == "__main__":
    print("UART Initialized. Waiting for data...")
    get_UART0_data_from_esp32()
