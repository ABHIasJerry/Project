#=====================================================================================#
#============================NMEA PARSER @ ABHINABA===================================#
#=====================================================================================#

import serial
import winsound
import time
import os
import sys
import re
logfile = r"D:\EMBEDDED LATEST PROJECT BACKUP\GIT Platform\Project\Embedded_Python\main\nmea_log.txt"
BLUE = "\033[94m{}\033[00m"
SERIAL_PORT = 'COM6'
SERIAL_RATE = 9600


# Main Code
def main():
    os.remove(logfile)
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)  # To indicate start of Program
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    capture_log()  # to log reading
    print("----Welcome to GPS/GNSS/GLONASS/NavIC Tracking System By @Abhinaba Ghosh [© 2022-23]----")
    while True:
        reading = ser.readline()
        # print(reading[0:6]) # to identify the format
        # print(reading)
        checksum(reading)  # to check the checksum
        if reading[0:6] == b"$GIGSV":
            printGSV(reading)
            # print(reading)
        elif reading[0:6] == b"$GIGLL":
            printGLL(reading)
            # print(reading)
        # elif reading[0:6] == b"$GIGSA":
        #     printGSA(reading)
        #     # print(reading)
        elif reading[0:6] == b"$GIRMC":
            printRMC(reading)
            # print(reading)
        elif reading[0:6] == b"$GIGGA":
            printGGA(reading)
            # print(reading)
        # elif reading[0:6] == b"$GIVTG":
        #     printVTG(reading)
        #     # print(reading)
        elif reading[0:6] == b"$PIRNSF":
            printNSF(reading)
            # print(reading)
        else:
            pass


# Function to Get Lat & Long with UTC
def getTime(string, format, returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format))  # Convert date and time to a nice printable format


def getLatLng(latString, lngString):
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
    return lat, lng
####################################################################


# Frame Processors
def printGLL(lines):
    print("========================================GIGLL========================================")
    lines = str(lines)
    format = lines.split(",")
    latlng = getLatLng(format[1], format[3])
    print("Lat,Long: ", latlng[0], format[2], ", ", latlng[1], format[4], sep='')
    print("Fix taken at:", getTime(format[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")
    print("Status (A=OK,V=NOT OK):", format[6])
    if format[7].partition("*")[0]:  # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid, L= Looking):", lines[7].partition("*")[0])
    print("===================================GIGLL EOF========================================")
    return


def printGGA(lines):
    print("========================================GIGGA========================================")
    lines = str(lines)
    format = lines.split(",")
    print("Fix taken at:", getTime(format[1], "%H%M%S.%f", "%H:%M:%S"), "UTC")
    latlng = getLatLng(format[2], format[4])
    print("Lat,Long: ", latlng[0], format[3], ", ", latlng[1], format[5], sep='')
    print("Fix quality (0 = invalid, 1 = fix, 2..8):", lines[6])
    print("Satellites:", format[7].lstrip("0"))
    print("Horizontal dilution:", format[8])
    print("Altitude: ", format[9], format[10], sep="")
    print("Height of geoid: ", format[11], format[12], sep="")
    print("Time in seconds since last DGPS update:", format[13])
    print("DGPS station ID number:", format[14].partition("*")[0])
    print("=====================================GIGGA EOF========================================")
    return


def printRMC(lines):
    print("========================================GIRMC========================================")
    lines = str(lines)
    format = lines.split(",")
    print("Fix taken at:", getTime(format[1] + format[9], "%H%M%S.%f%d%m%y", "%a %b %d %H:%M:%S %Y"), "UTC")
    print("Status (A=OK,V=KO):", format[2])
    latlng = getLatLng(format[3], format[5])
    print("Lat,Long: ", latlng[0], format[4], ", ", latlng[1], format[6], sep='')
    print("Speed (knots):", format[7])
    print("Track angle (deg):", format[8])
    print("Magnetic variation: ", format[10], end='')
    if len(format) == 13:  # The returned string will be either 12 or 13 - it will return 13 if NMEA standard used is above 2.3
        print(format[11])
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", format[12].partition("*")[0])
    else:
        print(format[11].partition("*")[0])
    print("====================================GIRMC EOF========================================")
    return


def printGSA(lines):
    print("========================================GIGSA========================================")
    lines = str(lines)
    format = lines.split(",")
    print("Selection of 2D or 3D fix (A=Auto,M=Manual):", format[1])
    print("3D fix (1=No fix,2=2D fix, 3=3D fix):", format[2])
    print("PRNs of satellites used for fix:", end='')
    for i in range(0, 12):
        prn = format[3 + i].lstrip("0")
        if prn:
            print(" ", prn, end='')
    print("\nPDOP", format[15])
    print("\nHDOP", format[16])
    print("\nVDOP", format[17].partition("*")[0])
    print("====================================GIGSA EOF========================================")
    return


def printGSV(lines):
    print("========================================GIGSV========================================")
    lines = str(lines)
    format = lines.split(",")
    print("Satellite total no of messages(1-9):", format[1])
    print("Satellite message number:", format[2])
    print("Satellites in view:", format[3])
    print("Satellite PRN:", format[4])
    print("Elevation (in deg):", format[5] + "°")
    print("Azimuth (deg):", format[6])
    print("SNR (C/No) 00-99dB:", format[7], "dB")
    print("====================================GIGSV EOF========================================")


def printVTG(lines):
    print("========================================GIVTG========================================")
    lines = str(lines)
    format = lines.split(",")
    print("True Track made good (deg):", format[1], format[2])
    print("Magnetic track made good (deg):", format[3], format[4])
    print("Ground speed (knots):", format[5], format[6])
    print("Ground speed (km/h):", format[7], format[8].partition("*")[0])
    if lines[9].partition("*")[0]:  # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", format[9].partition("*")[0])
    print("=====================================GIVTG EOF========================================")
    return


def printNSF(lines):
    print("========================================PIRNSF========================================")
    lines = str(lines)
    format = lines.split(",")
    print("Satellite data received from ID:", format[1],  "STATUS : online")
    print("Dataframe received:", format[2])
    if format[8] == '55':
        print("Message frame received: 55", format[3], format[4], format[5], format[6])
    else:
        print("Alert and warning received: 45", format[3], format[4],format[5],format[6])
        print(" Decode message from Subframe 1:", format[7],format[8],format[9],format[10],format[11],
              format[12],format[13],format[14],format[15],format[16],format[17],format[18],format[19],
              format[20],format[21],format[22],format[23],format[24],format[25],format[26],format[27],
              format[28],format[29],format[30],format[31],format[32],format[33])
        print("Decode messages from Subframe 2:", format[34],format[35],format[36],format[37],format[38])
    print("=====================================PIRNSF EOF========================================")
    return


# -----String decode---------#
# Checksum
def checksum(line):
    line = str(line)
    checkString = line.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)
    try:
        inputChecksum = int(checkString[2].rstrip(), 16)
    except:
        print("Checksum Error Detected")
        return False
    if checksum == inputChecksum:
        print("===================================Checksum OK!===================================")
        return True
    else:
        print("=====================================================================================")
        print("===================================Checksum error!===================================")
        print("=====================================================================================")
        print(hex(checksum), "!=", hex(inputChecksum))
        return False


# AUTO-LOG
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout

    def write(self, message):
        filename = logfile
        with open(filename, 'a', encoding='utf-8') as self.log:
            self.log.write(message)
        self.terminal.write(message)

    def flush(self):
        pass


def capture_log():
    Blue = "\033[94m{}\033[00m"
    print('[LOGGER]:', Blue.format('ACTIVE'))
    sys.stdout = Logger()


# RUNNER
if __name__ == "__main__":
    main()



