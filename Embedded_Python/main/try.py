# #!/usr/bin/env python
#
# import re
#
# """ Calculate  the checksum for NMEA sentence
#     from a GPS device. An NMEA sentence comprises
#     a number of comma separated fields followed by
#     a checksum (in hex) after a "*". An example
#     of NMEA sentence with a correct checksum (of
#     0x76) is:
#
#       $GPGSV,3,3,10,26,06,048,,27,50,073,24*74"
# """
#
#
# def checksum(sentence):
#     """ Remove any newlines """
#     if re.search("\n$", sentence):
#         sentence = sentence[:-1]
#
#     nmeadata, cksum = re.split('\*', sentence)
#
#     calc_cksum = 0
#     for s in nmeadata:
#         calc_cksum ^= ord(s)
#
#     """ Return the nmeadata, the checksum from
#         sentence, and the calculated checksum
#     """
#     return nmeadata, '0x' + cksum, hex(calc_cksum)
#
#
# if __name__ == '__main__':
#
#     """ NMEA sentence with checksum error (3rd field
#        should be 10 not 20)
#     """
#     line = "$GPGSV,3,3,10,26,06,048,,27,50,073,24*74\n"
#
#     """ Get NMEA data and checksums """
#
#     data, cksum, calc_cksum = checksum(line)
#
#     """ Verify checksum (will report checksum error) """
#     if cksum != calc_cksum:
#         print("Error in checksum for: %s" % (data))
#         print("Checksums are %s and %s" % (cksum, calc_cksum))

# data = "Lat,Long: 22.4820993N, 88.3440806E"

# Import module
from geopy.geocoders import Nominatim

# # Initialize Nominatim API
# geolocator = Nominatim(user_agent="geoapiExercises")
#
# # Assign Latitude & Longitude
# Latitude = "22.4820993N"
# Latt = len(Latitude)
# Latitude = Latitude[:Latt - 1]
# Longitude = "88.3440806E"
# Longg = len(Longitude)
# Longitude = Longitude[:Longg - 1]
#
# # Displaying Latitude and Longitude
# print("Latitude: ", Latitude)
# print("Longitude: ", Longitude)
#
# # Get location with geocode
# location = geolocator.geocode(Latitude + "," + Longitude)
#
# # Display location
# print("\nLocation of the given Latitude and Longitude:")
# print(location)

############################################################################

# In Range
self.label_21.setText("---")  #in range

# GGL
self.lineEdit.setText("---")  #Lat
self.lineEdit_2.setText("---")  #Long
self.lineEdit_3.setText("---")  #fix
self.lineEdit_4.setText("---")  #status
self.lineEdit_5.setText("---")  #mode

# GGA
self.lineEdit_6.setText("---")  #fix quality
self.lineEdit_7.setText("---")  #satellites
self.lineEdit_8.setText("---")  #dilution
self.lineEdit_9.setText("---")  #alt
self.lineEdit_10.setText("---")  #geoid
self.lineEdit_11setText("---")  #dgps
self.label_19.setText("---")  #update

# RMC
self.lineEdit_12.setText("---")  #speed
self.lineEdit_13.setText("---")  #angle
self.lineEdit_14.setText("---")  #magnetic
self.lineEdit_15.setText("---")  #mode

# GSA
self.lineEdit_16.setText("---")  #2d
self.lineEdit_17.setText("---")  #3d
self.lineEdit_18.setText("---")  #prn
self.lineEdit_19.setText("---")  #pd
self.lineEdit_20.setText("---")  #hd
self.lineEdit_21.setText("---")  #vd

# VTG
self.lineEdit_29.setText("---")  #true
self.lineEdit_30.setText("---")  #mag
self.lineEdit_31.setText("---")  #speed knot
self.lineEdit_32.setText("---")  #speed kmph
self.lineEdit_33.setText("---")  #mode

# GSV
self.lineEdit_22.setText("---")  #total
self.lineEdit_23.setText("---")  #sat msg
self.lineEdit_24.setText("---")  #view
self.lineEdit_25.setText("---")  #prn
self.lineEdit_26.setText("---")  #elevation
self.lineEdit_27.setText("---")  #azimuth
self.lineEdit_28.setText("---")  #srn

#NSF
self.lineEdit_34.setText("---")  #data rx
self.lineEdit_35.setText("---")  #data frame
self.lineEdit_36.setText("---")  #msg frame rx
self.lineEdit_37.setText("---")  #alert
self.lineEdit_38.setText("---")  #sf1
self.lineEdit_39.setText("---")  #sf2

############################################################################################