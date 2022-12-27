#include <SoftwareSerial.h>
SoftwareSerial gsmSerial(9, 5); // RX, TX
void setup()
{
   gsmSerial.begin(9600); // Setting the baud rate of GSM Module
   Serial.begin(9600); // Setting the baud rate of Serial Monitor (Arduino)
   delay(1000);
   Serial.println("Get GSM Model Data");
}
void loop()
{
   ReadUnreadMessages();
   delay(1000);
}
void ReadUnreadMessages()
{
   Serial.println("GSM model");
   gsmSerial.println("AT+CGMM\r");
   delay(2000);
   Serial.println("GSM Modem IMEI Number");
   gsmSerial.println("AT+CGSN\r");
   delay(2000);
   Serial.println("GSM SIM Identity");
   gsmSerial.println("AT+CCID\r");
   delay(2000);
   Serial.println("GSM SIM Auto detect");
   gsmSerial.println("AT+COPS=0\r");
   delay(2000);
   Serial.println("GSM SIM Network Status");
   gsmSerial.println("AT+CREG\r");
   delay(2000);
   Serial.println("GSM SIM Signal strength");
   gsmSerial.println("AT+CSQ\r");
   delay(2000);
   // Print the response on the Serial Monitor
   while (gsmSerial.available() > 0) {
      Serial.write(gsmSerial.read());
   }
}
