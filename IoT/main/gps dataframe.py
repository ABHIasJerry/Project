# import serial
# import time
# serialPort = serial.Serial(port="COM3", baudrate=9600,
#                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
#
# serialString = ""                           # Used to hold data coming over UART
#
#
# while 1:
#     # Wait until there is data waiting in the serial buffer
#     if serialPort.in_waiting > 0:
#         # Read data out of the buffer until a carriage return / new line is found
#         serialString = serialPort.readline()
#         print(serialString.decode('utf-8'))
#         # serialPort.write(b"Thank you for sending data \r\n")


