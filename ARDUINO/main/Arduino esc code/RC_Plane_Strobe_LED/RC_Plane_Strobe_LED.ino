//RC Plane Strobe blinking LED

//#define ledpin 2      // right red led
//#define ledpin2 3     // left green led
//#define ledpin3 4     // left white strobe
//#define ledpin4 5     // right white strobe
#define ledpin5 D8      // left red led
//#define ledpin6 7     // back blue led
int channel;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  pinMode(ledpin, OUTPUT);
//  pinMode(ledpin2, OUTPUT);
//  pinMode(ledpin3, OUTPUT);
//  pinMode(ledpin4, OUTPUT);
  pinMode(ledpin5, OUTPUT);
  //pinMode(ledpin6, OUTPUT);
    
}

void loop() {
  
//channel = pulseIn(9, HIGH);
//
// if (channel > 1800)
// {
//  digitalWrite (ledpin, HIGH);
//  digitalWrite (ledpin2, HIGH);
//  delay(100);
//  digitalWrite (ledpin3, HIGH);
//  digitalWrite (ledpin4, HIGH);
//  delay(50);
//  digitalWrite (ledpin3, LOW);
//  digitalWrite (ledpin4, LOW);
//  delay(50);
//  digitalWrite (ledpin3, HIGH);
//  digitalWrite (ledpin4, HIGH);
//  delay(50);
//  digitalWrite (ledpin3, LOW);
//  digitalWrite (ledpin4, LOW);
//  delay(500);
  digitalWrite (ledpin5, HIGH);
  delay(50);
  digitalWrite (ledpin5, LOW);
  delay(100);
  digitalWrite (ledpin5, HIGH);
  delay(70);
  digitalWrite (ledpin5, LOW);
  delay(1500);
//}
//else {digitalWrite(ledpin, LOW);
//      digitalWrite(ledpin2, LOW);
//}
//
//  Serial.println(channel);

}
