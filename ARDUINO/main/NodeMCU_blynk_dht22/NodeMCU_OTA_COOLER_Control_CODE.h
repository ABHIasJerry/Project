
/************AI_ENABLED AIR COOLER*******************/
/* Developed by : Abhinaba  Ghosh                   */                              
/* Dated        : April 14 , 2021                   */
/* APP          : BLYNK_iOS_Platform                */
/* WIFI HOST    : SKYNET_GLOBAL                     */
/* BLYNK_API    : h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5  */
/* OTA SUPPORT  : ENABLED                           */
/****************************************************/

/***********DEFINES*************************/
#define BLYNK_PRINT SERIAL
#define DHTTYPE DHT22
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <DHT.h>


/**************PIN DECLARATION***************/
#define Relay        D1
#define DHTPIN       D3
#define BUZZER       D5
#define LED_BUILTIN   2
#define A_level      A0
#define IN1          D7
#define IN2          D8
#define D_level      D4

/***************ASSIGNMENTS*****************/
DHT dht(DHTPIN, DHT22);
BlynkTimer timer;
Blynk.VirtualWrite(V6, t);
Blynk.VirtualWrite(V7, h);
int WATER_LEVEL;
int Water_level_read;
WidgetTerminal terminal(V10);
BLYNK_WRITE(V10)
WidgetLED WifiStatus(V5);
WidgetBUTTON RELAY(V2);
WidgetBUTTON PUMP_IN(V1);
WidgetLED IN(V15);
WidgetBUTTON PUMP_OUT(V0);
WidgetLED OUT(V16);
boolean RelayState = false;
boolean PUMP_IN_State = false;
boolean PUMP_OUT_State = false;

/**************BLYNK SETUP******************/
char auth[] = "h_mNkQ0f42IBmM8OIkFN6sUO6nKD3DG5";
char ssid[] = "SKYNET_GLOBAL" ;
char pass[] = "44ffba6d" ;
WidgetTerminal terminal(V10);
/*************INNITIALIZE*******************/
void setup()
{
	Serial.begin(115200);
	Blynk.begin(auth, ssid, pass);
	pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
	Blynk.VirtualWrite(V5, LOW);
	BLYNK_WRITE(V10)
	terminal.clear();
    delay(10);
	while (Blynk.status() != WL_CONNECTED) 
     {
            delay(500);
            digitalWrite(LED_BUILTIN, HIGH);
			Blynk.VirtualWrite(V5, HIGH);
			terminal.flush();
     }
	dht.begin();
	pinMode(D1 INPUT);
	pinMode(D3 INPUT);
	pinMode(D5 OUTPUT);
	pinMode(D4 INPUT);
	pinMode(D7 OUTPUT);
	pinMode(D8 OUTPUT);
	pinMode(A0 INPUT);
	
	timer.setInterval(1000L, sendSensor);
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
                      return;
                 }
    Blynk.VirtualWrite(V6, t);
    Blynk.VirtualWrite(V7, h);
    
	   /**********WATER LEVEL PROCESSING**********/
	boolean isPressed = (digitalRead(PUMP_IN) == LOW);
	boolean isPressed = (digitalRead(PUMP_OUT) == LOW);
	WATER_LEVEL      = analogRead(A_level);
	Water_level_read = digitalRead(D_level);
	
	if (WATER_LEVEL > 600 && Water_level_read = 1 && isPressed != PUMP_IN_State)
	{
		if (isPressed)
		{
		digitalWrite(IN1, HIGH);
		digitalWrite(IN2, LOW);
		IN.on();
		OUT.off();
		Blynk.VirtualWrite(V11, A_level);
		}
		PUMP_IN_State = isPressed;
	}
	else
	{
		if ( WATER_LEVEL <= 300 && Water_level_read = 0 && isPressed != PUMP_OUT_State)
		{
		if (isPressed)
		{	
		 digitalWrite(IN1, LOW);
		 digitalWrite(IN2, HIGH);
		 OUT.on();
		 IN.off();
		 Blynk.VirtualWrite(V11, A_level);
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
{
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
    }
	
	Blynk.run();
    timer.run();
}