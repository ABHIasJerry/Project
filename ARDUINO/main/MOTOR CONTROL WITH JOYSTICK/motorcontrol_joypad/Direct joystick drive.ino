#define joystick     A1
#define pwm1          9
#define pwm2         10
int idle;
  
int motor_control;
/* Turn LED On/Off using ARDUINO & Bluetooth Module 1 = ON ; 0 = OFF */
/* BLUETOOTH NAME: SKYNET-BLE    ;  PASSWORD: 9674215408            */

int Relay = 7;
String R_On = "1";
String R_OFF = "0";
String inputString="";
char removeChar;


void setup() {
  pinMode(pwm1,   OUTPUT);
  pinMode(pwm2,   OUTPUT);
  pinMode(Relay, OUTPUT);
 pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}
 
void loop() {
  
  motor_control = analogRead(joystick);
  motor_control >>= 1;
  if(motor_control>160 && motor_control<200)
  {
    idle = motor_control;
  }
  Serial.println(motor_control);
  if(motor_control >idle){
    digitalWrite(pwm2, 0);
    digitalWrite(pwm1, 1);
    Serial.println("fwd ==drive");
    Serial.println(motor_control - idle-1);
    
  }
  else
    if(motor_control < idle){
      digitalWrite(pwm1, 0);
      digitalWrite(pwm2, 1);
      Serial.println("bwd ==drive");
      Serial.println(idle - motor_control);
     
    }
    else{
      digitalWrite(pwm1, 0);
      digitalWrite(pwm2, 0);
    }


     
      
}
