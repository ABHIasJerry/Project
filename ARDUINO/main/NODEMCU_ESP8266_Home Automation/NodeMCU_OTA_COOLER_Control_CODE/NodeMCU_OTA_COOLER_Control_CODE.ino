
/************AI_ENABLED AIR COOLER*******************/
/* Developed by : Abhinaba  Ghosh                   */
/* Dated        : April 19 , 2021                   */
/* APP          : BLYNK_iOS_Platform                */
/* WIFI HOST    : GOOGLE                            */
/* BLYNK_API    : h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5  */
/* OTA SUPPORT  : ENABLED                           */
/****************************************************/

/***********DEFINES*************************/
#define BLYNK_PRINT Serial
#define DHTTYPE DHT22
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SimpleTimer.h>
#include <SPI.h>
#include <DHT.h>

/**************PIN DECLARATION***************/
#define RELAY        D1
#define DHTPIN       D4
#define BUZZER       D5
#define A_level      A0
#define IN1          D7
#define IN2          D8
#define D_level      D4

/***************ASSIGNMENTS*****************/
DHT dht(DHTPIN, DHT22);
SimpleTimer timer;
int WATER_LEVEL;
int Water_level_read;
int toggleState_R  = 1; //Define integer to remember the toggle state for relay 
int toggleState_PI = 1; //Define integer to remember the toggle state for pump inlet
int toggleState_PO = 0; //Define integer to remember the toggle state for pump outlet

WidgetTerminal terminal(V10);
WidgetLED LIVE_Status(V5);
WidgetLED WiFi_Status(V4);
#define VPIN_RELAY V2
#define VPIN_PUMP_IN V1
WidgetLED IN (V15);
#define VPIN_PUMP_OUT V0
WidgetLED OUT (V16);
//boolean RelayState = false;
boolean PUMP_IN_State = false;
boolean PUMP_OUT_State = false;

/**************BLYNK SETUP******************/
int wifiFlag = 0;

#define AUTH "h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5"                   
#define WIFI_SSID "GOOGLE"             
#define WIFI_PASS "44ffba6d"         

/*************WIFI Connection***************/

void checkBlynkStatus() { // called every 3 seconds by SimpleTimer

  bool isconnected = Blynk.connected();
  if (isconnected == false) {
    wifiFlag = 1;
    WiFi_Status.off(); //Turn off WiFi LED
  }
  if (isconnected == true) {
    wifiFlag = 0;
    WiFi_Status.on(); //Turn on WiFi LED
  }
}

/*************INNITIALIZE*******************/
void setup()
{
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  timer.setInterval(3000L, checkBlynkStatus); // check if Blynk server is connected every 3 seconds
  Blynk.config(AUTH);
  Serial.begin(9600);
  dht.begin();
  pinMode(D1, OUTPUT);
  pinMode(D3, INPUT);
  pinMode(D5, OUTPUT);
  pinMode(D4, INPUT);
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(D1, toggleState_R);
  digitalRead(D7, toggleState_PI);
  digitalRead(D8, toggleState_PO);
  
  timer.setInterval(1000L, sendSensor);
}

/*****************Relay Control*************/
void relayOnOff()
if(toggleState_R == 1){
              digitalWrite(D1, LOW); // turn on relay 1
              toggleState_R = 0;
              Serial.println("Cooler ON");
              }
             else{
              digitalWrite(D1, HIGH); // turn off relay 1
              toggleState_R = 1;
              Serial.println("Cooler OFF");
              }
             delay(100);

void with_internet(){
    //Manual Switch Control
    while (digitalRead(D1) == LOW){
      delay(200);
      relayOnOff(1); 
      Blynk.virtualWrite(VPIN_RELAY, toggleState_R);   // Update Button Widget  
    }

void without_internet(){
    //Manual Switch Control
    while (digitalRead(D1) == LOW){
      delay(200);
      relayOnOff(1);      
    } 
BLYNK_CONNECTED() {
  // Request the latest state from the server
Blynk.syncVirtual(VPIN_RELAY);}	

BLYNK_WRITE(VPIN_RELAY) {
  toggleState_R = param.asInt();
  digitalWrite(D1, toggleState_R);
}

/*****************MAIN**********************/
void sendSensor()
{
  /*********DHT Processing**************/
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t))
  {
    Serial.println("No data available from DHT.");
	LIVE_Status.off();
    return;
  }
  Blynk.virtualWrite(V6, t);
  Blynk.virtualWrite(V7, h);
  LIVE_Status.on();
  /**********WATER LEVEL PROCESSING**********/
  boolean isPressed = (digitalRead(VPIN_PUMP_IN) == LOW);
  boolean isPressed = (digitalRead(VPIN_PUMP_OUT) == LOW);
  WATER_LEVEL      = analogRead(A_level);
  Water_level_read = digitalRead(D_level);

  if (WATER_LEVEL > 600 && Water_level_read = toggleState_PI && isPressed != PUMP_IN_State)
  {
    if (isPressed)
    {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      IN.on();
      OUT.off();
        Blynk.virtualWrite((V11, A_level);
    }
    PUMP_IN_State = isPressed;
  }
  else
  {
    if ( WATER_LEVEL <= 300 && Water_level_read = toggleState_PO && isPressed != PUMP_OUT_State)
    {
      if (isPressed)
      {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        OUT.on();
        IN.off();
          Blynk.virtualWrite((V11, A_level);
      }
      PUMP_OUT_State = isPressed;
    }
    else
    {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      IN.off();
      OUT.off();
    }
  }

}

void loop()
/* {
  boolean isPressed = (digitalRead(RELAY) == LOW);
  if (isPressed != RelayState)
  {
    if (isPressed)
    {
      digitalWrite(D1, HIGH);
    }
    else
    {
      digitalWrite(D1, LOW);
    }
    RelayState = isPressed;
  } */
  if (Wifi.status() != WL_CONNECTED)
  { BLYNK_WRITE(V10)
    terminal.clear();
    terminal.print(F("WIFI Connection : SUCCESS"));
    terminal.println();
    terminal.print(F("FETCH Data : Beginning..."));
    terminal.flush();
  }
  else
  {
	terminal.clear();
	terminal.print(F("WIFI Connection : FAILED"));
    terminal.flush();	
  }
  Blynk.run();
  timer.run();
  if (wifiFlag == 0)
    with_internet();
  else
    without_internet();
}
