int sensorPin = A0;
int digiPin = 12; 
int sensorValue1; 
int sensorValue2;  
//int limit = 300; 

void setup() {
 Serial.begin(9600);
 //pinMode(13, OUTPUT);
 pinMode(12,  INPUT);
}

void loop() {

 sensorValue1 = analogRead(sensorPin);
 sensorValue2 = digitalRead(digiPin); 
 Serial.println("Analog Value : ");
 Serial.println(sensorValue1);
 delay(1000);
 Serial.println("Digital Value : ");
 Serial.println(sensorValue2);
 delay(1000);
 
// if (sensorValue<250 && 350) {
// digitalWrite(13, HIGH); 
// }
// else {
// digitalWrite(13, LOW); 
// }
 
 //delay(100); 
}
