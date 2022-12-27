
/************AI_ENABLED AIR COOLER*******************/
/* Developed by : Abhinaba  Ghosh                   */
/* Dated        : April 14 , 2021                   */
/* APP          : BLYNK_iOS_Platform                */
/* WIFI HOST    : SKYNET_GLOBAL                     */
/* BLYNK_API    : h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5  */
/* OTA SUPPORT  : ENABLED                           */
/****************************************************/

#define BLYNK_PRINT Serial    // Comment this out to disable prints and save space
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SimpleTimer.h>
#include <DHT.h>


// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5"; //Enter the Auth code which was send by Blink

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "GOOGLE";  //Enter your WIFI Name
char pass[] = "44ffba6d";  //Enter your WIFI Password

#define DHTPIN 2          // Digital pin 4
WidgetLED LIVE_Status(V5);
WidgetTerminal terminal(V10);
#define DHTTYPE DHT22   // DHT 22, AM2302, AM2321

DHT dht(DHTPIN, DHTTYPE);
SimpleTimer timer;


// This function sends Arduino's up time every second to Virtual Pin (5).
// In the app, Widget's reading frequency should be set to PUSH. This means
// that you define how often to send data to Blynk App.
void sendSensor()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit
  
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    LIVE_Status.off();
    return;
  }
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  Blynk.virtualWrite(V7, h);  //V5 is for Humidity
  Blynk.virtualWrite(V6, t);  //V6 is for Temperature
  LIVE_Status.on();
}

void setup()
{
  Serial.begin(9600); // See the connection status in Serial Monitor
  Blynk.begin(auth, ssid, pass);
  terminal.clear();
    terminal.print(F("WIFI Connection : SUCCESS"));
    terminal.println();
    delay(100);
    terminal.print(F("FETCH Data : Beginning..."));
    terminal.flush();
  dht.begin();

  // Setup a function to be called every second
  timer.setInterval(1000L, sendSensor);
}

void loop()
{
  Blynk.run(); // Initiates Blynk
  timer.run(); // Initiates SimpleTimer
}
