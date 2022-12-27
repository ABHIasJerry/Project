
// WATER PUMP controller FW & BW in Y-Axis of joystick //

#define enA 8   // Connect ENA of motordriver to pin 8 of UNO //
int jpin = A1;  // Connect Joystick Yaxis in A1 pin //
int jval;
int IN1 = 9;    // Connect IN1 of motordriver to pin 9 of UNO //
int IN2 = 10;   // Connect IN2 of motordriver to pin 10 of UNO //
int motor_speed;
int speed_pin;
 
void setup() {
  pinMode(enA, OUTPUT);
  pinMode(speed_pin, OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(jpin,INPUT);
  Serial.begin(9600);
}
 
void loop() {
    jval = analogRead(jpin);
    Serial.println(jval);
  if (jval<519)
  {
    digitalWrite(IN1 , LOW);
    digitalWrite(IN2 , HIGH);
    motor_speed = (-255./519.)*jval+255.;
    analogWrite(speed_pin,motor_speed);
    analogWrite(enA, motor_speed);
    Serial.println(speed_pin);
  }
  if (jval>=519)
  {
    digitalWrite(IN1 , HIGH);
    digitalWrite(IN2 , LOW);
    motor_speed = (255./519.)*jval-255.;
    analogWrite(speed_pin,motor_speed);
    analogWrite(enA, motor_speed);
    Serial.println(speed_pin);
    }
  }
