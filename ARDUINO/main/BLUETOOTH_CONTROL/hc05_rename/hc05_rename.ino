#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11);   // RX | TX

void setup() 
{
  pinMode(9, OUTPUT);    // this pin will pull the HC-05 
                         //  pin 34 (KEY pin) HIGH to switch                            module to AT mode

  digitalWrite(9, HIGH); 
  Serial.begin(9600);
  Serial.println("Enter AT commands:");
  BTSerial.begin(38400);  // HC-05 default speed in AT 
                          // command mode
}

void loop()
{
  // Keep reading from HC-05 and send to Arduino 
  // Serial Monitor
  if (BTSerial.available())
    Serial.write(BTSerial.read());

  // Keep reading from Arduino Serial Monitor 
  //  and send to HC-05
  if (Serial.available())
    BTSerial.write(Serial.read());
}
