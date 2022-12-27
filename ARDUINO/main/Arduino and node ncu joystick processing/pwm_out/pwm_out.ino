double channel_1;

void setup(){
  pinMode(D0, INPUT);
  Serial.begin(9600);
}

void loop(){
  channel_1 = pulseIn(D0, HIGH);
  Serial.println(channel_1);
}
