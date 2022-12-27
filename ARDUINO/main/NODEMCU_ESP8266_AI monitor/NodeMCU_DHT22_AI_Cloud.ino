

//DHT22 Project
//Channel ID: 1135938
//Author: mwa0000019434212
//Access: Private
//Temperature and humidity reading data from NodeMcu
// Read API Key : FUA6POMOXNHNEGIT

#include <DHT.h>  // Including library for dht
#include <ESP8266WiFi.h> 
String apiKey = "89DBU5AZH68H4BUG";     //  Enter your Write API key from ThingSpeak

const char *ssid =  "SKYNET_GLOBAL";     // replace with your wifi ssid and wpa2 key
const char *pass =  "44ffba6d";
const char* server = "api.thingspeak.com";

#define DHTPIN 0          //pin where the dht22 is connected
#define LED_BUILTIN 2
 
DHT dht(DHTPIN, DHT22);

WiFiClient client;
 
void setup() 
{
       pinMode(LED_BUILTIN, OUTPUT);
       digitalWrite(LED_BUILTIN, LOW);
       Serial.begin(115200);
       delay(10);
       dht.begin();
 
       Serial.println("*******************");
     delay(200);
     Serial.println("\n WELCOME! Mr. ABHINABA. AUTHORIZATION GRANTED... ");
     delay(500);
     Serial.println("\n INNITIALIZING SKYNET NETWORK ");
     Serial.println("*******************");
       Serial.println(ssid);
 
 
       WiFi.begin(ssid, pass);
 
      while (WiFi.status() != WL_CONNECTED) 
     {
            
            delay(500);
            digitalWrite(LED_BUILTIN, HIGH);
            Serial.print(".");
     }
      Serial.println("");
      Serial.println("SECURED NETWORK ESTABLISHED....ENCRYPTING DATAFLOW");
      Serial.println("IP Tracking : ");
      Serial.println(WiFi.localIP());  // Print the IP address
 
}
 
void loop() 
{
  
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      
              if (isnan(h) || isnan(t)) 
                 {
                     Serial.println("No data available from sensors.");
                      return;
                 }

                         if (client.connect(server,80))   //   "184.106.153.149" or api.thingspeak.com
                      {  
                            
                             String postStr = apiKey;
                             postStr +="&field1=";
                             postStr += String(t);
                             postStr +="&field2=";
                             postStr += String(h);
                             postStr += "\r\n\r\n";
 
                             client.print("POST /update HTTP/1.1\n");
                             client.print("Host: api.thingspeak.com\n");
                             client.print("Connection: close\n");
                             client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n");
                             client.print("Content-Type: application/x-www-form-urlencoded\n");
                             client.print("Content-Length: ");
                             client.print(postStr.length());
                             client.print("\n\n");
                             client.print(postStr);
 
                             Serial.print("Ambient Temperature: ");
                             Serial.print(t);
                             Serial.print(" °C ");
               Serial.print("\n Ambient Humidity: ");
                             Serial.print(h);
               Serial.print(" %");
               Serial.print("\n Wind Speed: ");
               Serial.print(" UNDETECTED");
                             Serial.println("\n --> *Uploading dataframe to Cloud Database....*");
                        }
          client.stop();
 
          Serial.println("updating data from AI cloud...");
  
    delay(10000);
}
