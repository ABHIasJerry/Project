/*-----------------------------------------------------------------------------------------------------------------------------------------------------------------
 * @target:      Arduino UNO R3
 * @purpose:     RC drone remote controller
 * @file:        Analog Joystick data processing to convert into PWM signals for NodeMCU to read. 
 * @author:      Abhinaba Ghosh
 * @date:        22/07/2022
 * @time:        01:30:54 AM IST
 * @memory size: 39% of program storage on UNO [12616 bytes], 26% of dynamic memory [537 bytes], Max 2048 bytes.
 * @peripherals: 2 Analog Joystick, 1 Piezo Buzzer, 1 LED PCB, 1 OLED display(U8GLIB_SSD1306_128X64)
 * @Pins Used:   [Analog]-> A1,A2,A3,A4   [SDA/SCL]-> A4,A5  [PWM]-> 3,5,6,9  [Digital]-> 7,11  [Power]-> 5V, 3.3V  [Gnd]-> --
 * @Validation:  Done 
 * @Copyright:   Abhinaba,2022-23. All Rights Reserved.Strictly personal
 * @version:     1.0.3
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------*/

// Declare Analog/Digital Pins
int throttle = A0;
int steer = A1;
int pitch = A2;
int rotate = A3;
const int buzzer = 11; //[buzzer (-) to gnd and (+) to pin 11]
int remote_led = 7;  //remote led panel

//Include the graphics library.
#include "U8glib.h" 

//Initialize display.
U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NONE | U8G_I2C_OPT_DEV_0);

// Initialize variables to defaults
int throttle_pos = 0;
int steer_pos = 0;
int pitch_pos = 0;
int rotate_pos = 0;

// Initialize mapping variables to PWM
int map_throttle = 0;
int map_steer = 0;
int map_pitch = 0;
int map_rotate = 0;

//Initialize Analog Readings
void setup()
{
  Serial.begin(9600);
  pinMode(3,OUTPUT); // PWM Throttle
  pinMode(5,OUTPUT); // PWM Steer
  pinMode(6,OUTPUT); // PWM Pitch/Yaw
  pinMode(9,OUTPUT); // PWM Rotate
  pinMode(remote_led, OUTPUT);// LED PCB
  pinMode(throttle,INPUT); // Analog Throttle
  pinMode(steer,INPUT); // Analog Steer
  pinMode(pitch,INPUT); // Analog Pitch/Yaw
  pinMode(rotate,INPUT);  // Analog Rotate
  
  // Buzzer sequence to begin data-transfer
  tone(buzzer, 500); // Send 0.5KHz sound signal...
  delay(100);        // ...for 0.1 sec
  noTone(buzzer);     // Stop sound...
  delay(500);        // ...for 0.5 sec
  tone(buzzer, 1000); // Send 1KHz sound signal...
  delay(100);        // ...for 1 sec
  noTone(buzzer);     // Stop sound...
  delay(500);        // ...for 0.5 sec
  tone(buzzer, 2000); // Send 2KHz sound signal...
  delay(100);        // ...for 1 sec
  noTone(buzzer);     // Stop sound...
  delay(500);        // ...for 0.5 sec
  tone(buzzer, 3000); // Send 3KHz sound signal...
  delay(500);        // ...for 0.5 sec
  noTone(buzzer);     // Stop sound...

  //Set font for OLED
    u8g.setFont(u8g_font_unifont);
}

// OLED Data display
void draw(void)
{
    //Write text. (x, y, text)
    u8g.drawStr(20, 40, "REMOTE READY");
}

//Create loop sequence
void loop()
{
  // Indicates Remote is ready
  digitalWrite(remote_led, HIGH); // LED Turns ON.
  // Displays welcome screen in OLED
  u8g.firstPage();
    do {
        draw();
    } while (u8g.nextPage());
  // Analog readings
  throttle_pos = analogRead(throttle);
  steer_pos = analogRead(steer);
  pitch_pos = analogRead(pitch);
  rotate_pos = analogRead(rotate);
  // Data mapping 
  map_throttle = map(throttle_pos,0,1024,0,255);
  map_steer = map(steer_pos, 0, 1024, 0, 255);
  map_pitch = map(pitch_pos, 0, 1024, 0, 255);
  map_rotate = map(rotate_pos, 0, 1024, 0, 255);
  //Write PWM Data
      analogWrite(3,map_throttle);
      analogWrite(5,map_steer);
      analogWrite(6,map_pitch);
      analogWrite(9,map_rotate);
  //Print Values
  Serial.print("--START BUFFER [");
  Serial.print("THROTTLE: ");
  Serial.print(map_throttle);
  Serial.print(" | STEER: ");
  Serial.print(map_steer);
  Serial.print(" | PITCH: ");
  Serial.print(map_pitch);
  Serial.print(" | ROTATE: ");
  Serial.print(map_rotate);
  Serial.print("] --END BUFFER");
  Serial.println(" ");
  //delay(100);  // to use for data-sync if required.
}

// END
