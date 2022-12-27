/* Turn LED On/Off using ARDUINO & Bluetooth Module 1 = ON ; 0 = OFF */
/* BLUETOOTH NAME: SKYNET-BLE    ;  PASSWORD: 9674215408            */

int Relay = 7;
String R_On = "1";
String R_OFF = "0";
String inputString="";
char removeChar;

void setup()                  
{
 Serial.begin(9600);
 pinMode(Relay, OUTPUT);
 pinMode(LED_BUILTIN, OUTPUT);
}
void loop()
{
  if(Serial.available()){
  while(Serial.available())
    {
      // reading the input
      char inputChar = (char)Serial.read();
      // Appending Char to Form String of Characters.
      inputString += inputChar;       
    }
    Serial.println(inputString);
    while (Serial.available() > 0) 
    {
      // clearing serial buffer if any.
      removeChar = Serial.read() ;
    }     
    if(inputString == R_On){
      // Setting Relay To ON.
     digitalWrite(Relay, HIGH);
     digitalWrite(LED_BUILTIN, HIGH);
     Serial.println(' The Device is ON ');
    }
    else if(inputString == R_OFF){
      // Setting Relay To OFF.
      digitalWrite(Relay, LOW);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println(' The Device is OFF ');
    }
    // Setting inputString to OFF.
    inputString = "";

  }

}
