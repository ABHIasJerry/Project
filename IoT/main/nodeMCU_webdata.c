

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);   // Default UART0 // TX=1 (gray)   RX=3 (orange)
  while (!Serial){;}
  digitalWrite(LED_BUILTIN, LOW); 
}

void loop()
  { 
  // Read from SerialPort and write to Serial
  if (Serial.available() > 0) 
  {
  String uartData = "";
  while (Serial.available() > 0) {char receivedChar = Serial.read(); uartData += receivedChar;} 
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  Serial.println(uartData); delay(100);}
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(1000);
  }