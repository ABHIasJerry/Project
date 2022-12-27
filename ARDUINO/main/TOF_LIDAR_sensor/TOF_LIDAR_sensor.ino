/*
  VL53L0X Distance Sensor
  modified on 26 oct 2020
  by Amir Mohammad Shojaee @ Electropeak
  Home

  Based on Adafruit Example
*/

#include "Adafruit_VL53L0X.h"
 
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
 
void setup() {
  Serial.begin(115200);
 
  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
 
  Serial.println(" VL53L0X calibrating......");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power 
  Serial.println(F("VL53L0X TOF LiDAR Range Finder\n\n")); 
}
 
 
void loop() {
  VL53L0X_RangingMeasurementData_t measure;
 
  //Serial.print("Reading a measurement... ");
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
 
  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
    Serial.print("Distance (cm): "); Serial.println((measure.RangeMilliMeter - 25) * 0.1); 
    Serial.print("\n Distance (ft): "); Serial.print((measure.RangeMilliMeter - 25) * 0.00328084);
  } else {
    Serial.println("Distance (cm | ft): Un-detectable ");
  }
 
  delay(500);
}
