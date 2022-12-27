
import serial
import time
# ser = serial.Serial('COM3', 9600,
#                     bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
# # skip first line, since it could be incomplete
# ser.readline()
SERIAL_PORT = 'COM3'
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)


def getTime(string, format, returnFormat):
    return time.strftime(returnFormat,
                         time.strptime(string, format))  # Convert date and time to a nice printable format


def getLatLng(latString, lngString):
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
    return lat, lng


def printRMC(lines):
    global counter
    print("----Welcome to Raspberry PI NAVIC Tracking System By Abhinaba----")
    print("========================================GIRMC========================================")
    # print(lines, '\n')
    print("Fix taken at:", getTime(lines[1] + lines[9], "%H%M%S.%f%d%m%y", "%a %b %d %H:%M:%S %Y"), "UTC")
    print("Status (A=OK,V=KO):", lines[2])
    latlng = getLatLng(lines[3], lines[5])
    print("Lat,Long: ", latlng[0], lines[4], ", ", latlng[1], lines[6], sep='')
    print("Speed (knots):", lines[7])
    print("Track angle (deg):", lines[8])
    print("Magnetic variation: ", lines[10], end='')
    if len(
            lines) == 13:  # The returned string will be either 12 or 13 - it will return 13 if NMEA standard used is above 2.3
        print(lines[11])
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[12].partition("*")[0])
    else:
        print(lines[11].partition("*")[0])

    counter += 1
    if counter == 10:  # Generate HTML every 10s
        counter = 0
        print(latlng)
    return


def printGGA(lines):
    print("========================================GIGGA========================================")
    # print(lines, '\n')
    print("Fix taken at:", getTime(lines[1], "%H%M%S.%f", "%H:%M:%S"), "UTC")
    latlng = getLatLng(lines[2], lines[4])
    print("Lat,Long: ", latlng[0], lines[3], ", ", latlng[1], lines[5], sep='')
    print("Fix quality (0 = invalid, 1 = fix, 2..8):", lines[6])
    print("Satellites:", lines[7].lstrip("0"))
    print("Horizontal dilution:", lines[8])
    print("Altitude: ", lines[9], lines[10], sep="")
    print("Height of geoid: ", lines[11], lines[12], sep="")
    print("Time in seconds since last DGPS update:", lines[13])
    print("DGPS station ID number:", lines[14].partition("*")[0])
    return


def printGSA(lines):
    print("========================================GIGSA========================================")
    # print(lines, '\n')

    print("Selection of 2D or 3D fix (A=Auto,M=Manual):", lines[1])
    print("3D fix (1=No fix,2=2D fix, 3=3D fix):", lines[2])
    print("PRNs of satellites used for fix:", end='')
    for i in range(0, 12):
        prn = lines[3 + i].lstrip("0")
        if prn:
            print(" ", prn, end='')
    print("\nPDOP", lines[15])
    print("HDOP", lines[16])
    print("VDOP", lines[17].partition("*")[0])
    return


def printGSV(lines):
    if lines[2] == '1':  # First sentence
        print("========================================GIGSV========================================")
    else:
        print("===================================================================================")
    # print(lines, '\n')

    print("Number of sentences:", lines[1])
    print("Sentence:", lines[2])
    print("Satellites in view:", lines[3].lstrip("0"))
    for i in range(0, int(len(lines) / 4) - 1):
        print("Satellite PRN:", lines[4 + i * 4].lstrip("0"))
        print("Elevation (deg):", lines[5 + i * 4].lstrip("0"))
        print("Azimuth (deg):", lines[6 + i * 4].lstrip("0"))
        print("SNR (higher is better):", lines[7 + i * 4].partition("*")[0])
    return


def printGLL(lines):
    print("========================================GIGLL========================================")
    # print(lines, '\n')

    latlng = getLatLng(lines[1], lines[3])
    print("Lat,Long: ", latlng[0], lines[2], ", ", latlng[1], lines[4], sep='')
    print("Fix taken at:", getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")
    print("Status (A=OK,V=KO):", lines[6])
    if lines[7].partition("*")[0]:  # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[7].partition("*")[0])
    return

#done
def printVTG(lines):
    print("========================================GIVTG========================================")
    # print(lines, '\n')

    print("True Track made good (deg):", lines[1], lines[2])
    print("Magnetic track made good (deg):", lines[3], lines[4])
    print("Ground speed (knots):", lines[5], lines[6])
    print("Ground speed (km/h):", lines[7], lines[8].partition("*")[0])
    if lines[9].partition("*")[0]:  # Extra field since NMEA standard 2.3
        print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):", lines[9].partition("*")[0])
    return


# ------new add of PINSF-------#

def printNSF(lines):
    print("========================================PIRNSF========================================")
    print("Satellite data received from ID:",lines[1] ,    "STATUS : online")

    print("Dataframe received:", lines[2])
    if lines[8] == '55':
        print("Message frame received: 55", lines[3],lines[4],lines[5],lines[6])
    else:
        print("Alert and warning received: 45", lines[3], lines[4],lines[5],lines[6])
        print(" Decode message from Subframe 1:", lines[7],lines[8],lines[9],lines[10],lines[11],lines[12],lines[13],lines[14],lines[15],lines[16],lines[17],lines[18],lines[19],lines[20],lines[21],lines[22],lines[23],lines[24],lines[25],lines[26],lines[27],lines[28],lines[29],lines[30],lines[31],lines[32],lines[33])
        print("Decode messages from Subframe 2:", lines[34],lines[35],lines[36],lines[37],lines[38])
    return

    # -----String decode---------#


def checksum(line):
    checkString = line.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)

    try:  # Just to make sure
        inputChecksum = int(checkString[2].rstrip(), 16)
    except:
        print("Error in string")
        return False

    if checksum == inputChecksum:
        return True
    else:
        print("=====================================================================================")
        print("===================================Checksum error!===================================")
        print("=====================================================================================")
        print(hex(checksum), "!=", hex(inputChecksum))
        return False


while 1:
    reading = ser.readline()
    # print(reading[0:6]) # to identify the format
    # if checksum(reading):
    if reading[0:6] == b"GIRMC" or reading[0:6] == b"GPRMC":
        printRMC(reading)
        pass
    elif reading[0:6] == b"GIGGA" or reading[0:6] == b"GPGGA":
        printGGA(reading)
        pass
    elif reading[0:6] == b"GPGSA":
        printGSA(reading)
        pass
    elif reading[0:6] == b"GPGSV":
        printGSV(reading)
        pass
    elif reading[0:6] == b"GPGLL":
        printGLL(reading)
        pass
    elif reading[0:6] == b"GPVTG":
        printVTG(reading)
    elif reading[0:6] == b"PIRNSF":
        printNSF(reading)
        pass


