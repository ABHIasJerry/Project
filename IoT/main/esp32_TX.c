#include <ArduinoJson.h>
#include <HardwareSerial.h>

HardwareSerial SerialPort(2); // use UART2
StaticJsonDocument<1000> doc; 

int rpm = 900;
int Measured_Height= 2;
int speed = 5;

void setup()
{
  Serial.begin( 9600 ); 
  SerialPort.begin(115200, SERIAL_8N1, 16, 17); // TX=16 (yellow)   RX=17 (purple)
}

void create_JSON_buffer(int rpm, int Measured_Height, int speed)
{
  Serial.println("... sending data to Pico W UART0");
  // JSON structure
  doc["RPM"] = rpm;
  doc["Height"] = Measured_Height;
  doc["Speed"] = speed;
  serializeJsonPretty(doc, Serial);
  Serial.println(","); 
 
  // Serialize JSON to a string
  String jsonString;
  serializeJson(doc, jsonString);
  // Send JSON data over Serial
  SerialPort.println(jsonString + ",");

  Serial.println("... sending complete successfully !"); 
  delay(1000);
}

void loop(){ create_JSON_buffer(rpm,Measured_Height,speed); }