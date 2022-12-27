/*-----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * @target:      NodeMCU ESP8266 0.9
 * @purpose:     RC drone remote controller
 * @file:        Reading Analog Joystick data converted into PWM signals from Arduino UNO. 
 * @author:      Abhinaba Ghosh
 * @date:        22/07/2022
 * @time:        01:30:54 AM IST
 * @memory size: 271120 bytes (199027 compressed) at 0x00000000 in 17.7 seconds (effective 122.6 kbit/s)...
 * @peripherals: 6 channels used
 * @Pins Used:   [PWM]-> D0,D3,D4,D5,D6,D7  [Power]-> 5V, 3.3V  [Gnd]-> --
 * @Validation:  Done 
 * @Copyright:   Abhinaba,2022-23. All Rights Reserved.Strictly personal
 * @version:     1.0.3
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------*/

// declare channels
double channel_1;
double channel_2;
double channel_3;
double channel_4;
//int channel_5;
//int channel_6;

// Declare Digital pins
int THROTTLE_FW_BW = D5;
int STEER_L_R = D3;
int PITCH_YAW = D4;
int ROTATE_L_R = D7;
//int NAV_LIGHTS = D5;
//int BEACON = D0;
int SPEED = D6;

// Initialize inputs
void setup(){
  pinMode(THROTTLE_FW_BW, INPUT);
  pinMode(STEER_L_R, INPUT);
  pinMode(PITCH_YAW, INPUT);
  pinMode(ROTATE_L_R, INPUT);
  pinMode(SPEED, OUTPUT);
  // outlines
//  pinMode(NAV_LIGHTS, INPUT_PULLUP);
//  pinMode(BEACON, INPUT_PULLUP);
  Serial.begin(9600);

}

void loop(){
  channel_1 = pulseIn(THROTTLE_FW_BW, HIGH);
  channel_2 = pulseIn(STEER_L_R, HIGH);
  channel_3 = pulseIn(PITCH_YAW, HIGH);
  channel_4 = pulseIn(ROTATE_L_R, HIGH);
  analogWrite(SPEED, channel_1);
  // outlines
//  channel_5 = digitalRead(NAV_LIGHTS);
//  channel_6 = digitalRead(BEACON);
  // TERMINAL VIEW
  Serial.print("Throttle [Forward/Backward]: ");
  Serial.print(channel_1);Serial.print(" ");
  Serial.print("Steer [Left/Right]: ");
  Serial.print(channel_2);Serial.print(" ");
  Serial.print("Pitch/Yaw: ");
  Serial.print(channel_3);Serial.print(" ");
  Serial.print("Rotate [Left/Right]: ");
  Serial.print(channel_4);
  // Buttons
//  if (channel_5 == LOW){
//    Serial.println("Navigation Lights: ");
//    Serial.print("PRESSED");Serial.print(" ");}
//    else{
//      Serial.println("Navigation Lights: ");
//      Serial.print("--");Serial.print(" ");
//    }
//   if (channel_6 == LOW){
//    Serial.print("Beacons: ");
//    Serial.print("PRESSED");Serial.print(" ");}
//    else{
//      Serial.print("Beacons: ");
//    Serial.print("--");Serial.print(" ");
//    }
  Serial.println(" ");

}

// END
