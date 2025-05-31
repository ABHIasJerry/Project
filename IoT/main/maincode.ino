/* Author: Abhinaba Ghosh     Date: 20-05-2025   Revision: v1.0   Time: 02:49AM */

/* MAIN CPU code
   Design Flow -> BME680/MPU6050/VL53LOX/SDcard/RTC/NEO-6M-GPS  -> data -> ESP32 -> TX -> PicoW
*/

/* --- PIN Configurations ---
    Name          Pin
   ------        ------
   SCL            GPIO22
   SDA            GPIO 21
   TX             GPIO16
   RX             GPIO17
   ESP-TX1        GPIO10
   ESP-RX1        GPIO9
   MISO           GPIO19
   MOSI           GPIO23
   SCK            GPIO18
   SS             GPIO5
   Analog         GPIO0  -> Sharp AQI
   Analog         GPIO2   -> battery monitor
   Digital        GPIO36
   Power,REF_3V3  3.3 V
   Ground         GND
   CurrentPin     GPIO4
   UVOUT          GPIO15
*/

// Include
#include <SD.h>
#include <SPI.h>
#include <Wire.h>
#include "RTClib.h"
#include <TinyGPSPlus.h>
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include "Adafruit_VL53L0X.h"

// Definations
#define GPS_BAUDRATE 9600  // The default baudrate of NEO-6M is 9600
#define SEALEVELPRESSURE_HPA (1013.25)
#define PIN_SPI_CS 5 // The ESP32 pin GPIO5

// Declarations
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
Adafruit_BME680 bme;
TinyGPSPlus gps;
RTC_DS1307 rtc;
File myFile;

// Pin declarations
int measurePin = 0;  // connect dust sensor to Analog GPIO0 [pin 25]
int ledPower = 36;  // connect to led driver pin of dust sensor to GPIO5 [Digital pin 29]
//int TX = 16; // connect Tx of the ESP with GPS module
//int RX = 17; // connect Rx of the ESP with GPS module
int scl = 22;
int sda = 21;
int miso = 19;
int mosi = 23;
int ss = 5;
int sck = 18;
int ESP_Tx = 10;
int ESP_Rx = 9;
int UVOUT = 15; //Output from the sensor
int currentpin = 4; // current sensing module pin
int analogPin = 2; // Use any ADC pin 

// Global variables initialization
//FLOAT
float latitude = 0.0;
float longitude = 0.0;
float altitude = 0.0;
float speed = 0.0;
float temperature = 0.0;
float pressure = 0.0;
float humidity = 0.0;
float gas = 0.0;
float sea_altitude = 0.0;
float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;
float ppm = 0;
float voltage = 0;
float ppm_real = 0;
float tof_distance = 0.0;
float load_current = 0.0;
float uv_index = 0.0;
float r1 = 6800.0;
float r2 = 12000.0;
//INT
int year = 0;
int month = 0;
int day = 0;
int hour = 0;
int minute = 0;
int second = 0;
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9860;
int batt = 0;
int counter = 0;
//CHAR
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
char buffer[1000]; // Create a buffer to hold the formatted string
//STRING
String result = "";
//const String latitude = " ";
//const String longitude = " ";
const String date_separator = "-";
const String time_separator = ":";
const String formattedTime = "";
const String dateformat = "";
const String utctime = "";
const String status = "OK";
const String sep = ";";
// Constant INT/16
const int MPU_ADDR = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

// Battery voltage function
float battery_read()
{
    //read battery voltage per %
    long sum = 0;                  // sum of samples taken
    float voltage = 0.0;           // calculated voltage
    float output = 0.0;            // output value
    const float battery_max = 3.7; // maximum voltage of battery
    const float battery_min = 3.3; // minimum voltage of battery before shutdown

    float R1 = 100000.0; // resistance of R1 (100K)
    float R2 = 10000.0;  // resistance of R2 (10K)

    for (int i = 0; i < 500; i++)
    {
        int analogValue = analogRead(analogPin);
        sum += analogValue;
        delay(500);
    }
    // calculate the voltage
    voltage = sum / (float)500;
    voltage = (voltage * 1.1) / 4096.0; // for internal 1.1v reference
    // use it with divider circuit 
    // voltage = voltage / (R2/(R1+R2));
    // round value by two DP
    voltage = roundf(voltage * 100) / 100;
    Serial.print("voltage: ");
    Serial.println(voltage, 2);
    output = ((voltage - battery_min) / (battery_max - battery_min)) * 100;
    if (output < 100)
        return output;
    else
        return 100.0f;
}

//Takes an average of readings on a given pin
//Returns the average
int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 
  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
  return(runningValue);
}
 
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


void setup() {
  Serial.begin(9600);   // serial print Fn
  Serial1.begin(9600, SERIAL_8N1, ESP_Tx, ESP_Rx); // Initialize UART1 on custom pins (e.g., TX = ESP_Tx, RX = ESP_Rx)
  Serial2.begin(GPS_BAUDRATE, SERIAL_8N1, 16, 17);
  Wire.begin(sda, scl, 100000); // SDA, SCL, Clock Speed
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // Set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Wire.beginTransmission(MPU_ADDR);
  pinMode(ledPower, OUTPUT);
  pinMode(UVOUT, INPUT);
  pinMode(analogPin, INPUT);
  pinMode(currentpin, INPUT);

  while (!Serial);
    Serial.println("Initialising Sensor(s) Data processing by ESP-Controller.....");

  if (!bme.begin()) { Serial.println(F("Could not find a valid BME680 sensor, check wiring!")); while (1);}

    // Set up oversampling and filter initialization
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320*C for 150 ms

  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));}

  if (!SD.exists("/IoT_WeatherStationData.txt")) {
    Serial.println(F("File [IoT_WeatherStationData.txt] doesn't exist. Creating file..."));
    myFile = SD.open("/IoT_WeatherStationData.txt", FILE_WRITE);
    myFile.close();}
  // recheck if file is created or not
  if (SD.exists("/IoT_WeatherStationData.txt")) {
    Serial.println(F("Required file exists on SD Card."));}
  else{
    Serial.println(F("File doesn't exist on SD Card."));}

  sprintf(buffer, 
              formattedTime, sep,
              latitude, sep,
              longitude, sep,
              altitude, sep,
              speed, sep,
              dateformat, sep,
              utctime, sep,
              temperature, sep,
              pressure, sep,
              humidity, sep,
              gas, sep,
              sea_altitude, sep,
              calcVoltage, sep,
              dustDensity, sep,
              ppm_real, sep,
              tof_distance, sep,
              AcX, sep,
              AcY, sep,
              AcZ, sep,
              GyX, sep,
              GyY, sep,
              GyZ, sep,
              uv_index, sep,
              load_current, sep,
              batt, sep,
              status);

  }


  // main function
  void loop() {

    // ---- RTC ++++
    DateTime now = rtc.now();
    String yearStr = String(now.year(), DEC);
    String monthStr = (now.month() < 10 ? "0" : "") + String(now.month(), DEC);
    String dayStr = (now.day() < 10 ? "0" : "") + String(now.day(), DEC);
    String hourStr = (now.hour() < 10 ? "0" : "") + String(now.hour(), DEC); 
    String minuteStr = (now.minute() < 10 ? "0" : "") + String(now.minute(), DEC);
    String secondStr = (now.second() < 10 ? "0" : "") + String(now.second(), DEC);
    String dayOfWeek = daysOfTheWeek[now.dayOfTheWeek()];
    String formattedTime = dayOfWeek + ", " + yearStr + "-" + monthStr + "-" + dayStr + " " + hourStr + ":" + minuteStr + ":" + secondStr;
    // ---- RTC ----

    // ---- GPS ++++
    if (Serial2.available() > 0) {
      if (gps.encode(Serial2.read())) {
        
        if (gps.location.isValid()) { latitude = gps.location.lat(); longitude = gps.location.lng(); 
        } else {latitude = 0.0; longitude = 0.0;}
        
        if (gps.altitude.isValid()) { altitude = gps.altitude.meters(); 
        } else {altitude = 0.0;}

        if (gps.speed.isValid()) { speed = gps.speed.kmph(); 
        } else {speed = 0.0;}

        if (gps.date.isValid() && gps.time.isValid()) {
          year = gps.date.year();
          month = gps.date.month();
          day = gps.date.day();
          hour = gps.time.hour();
          minute = gps.time.minute();
          second = gps.time.second();

        } else { year = 0; month = 0; day = 0; hour = 0; minute = 0; second = 0;}
      }
    }
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println("No GPS data received: check wiring");}
    // ---- GPS ----

    // ---- BME680 ++++
    unsigned long endTime = bme.beginReading();   // Tell BME680 to begin measurement.
    delay(50);
    if (!bme.endReading()) { Serial.println("Failed to BME680 sensor reading."); return;
    } else { temperature = bme.temperature; pressure = bme.pressure / 100.0; humidity = bme.humidity; 
             gas = bme.gas_resistance / 1000.0; sea_altitude = bme.readAltitude(SEALEVELPRESSURE_HPA);
             // *C | hPa | % | KOhms | m @ sea-level
            }
    // ---- BME680 ----


    // ---- MPU6050 ++++
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B); // Starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(true);
    Wire.requestFrom(MPU_ADDR, 14, true); // Request a total of 14 registers

    AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    // ---- MPU6050 ----


    // ---- TOF ++++
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
    if (measure.RangeStatus != 4) { tof_distance = measure.RangeMilliMeter; 
      } else { tof_distance = 0.0; } // phase failures have incorrect data
    // ---- TOF ----


    // ---- SHARP AQI ++++
    digitalWrite(ledPower, LOW);  // power ON the LED
    delayMicroseconds(samplingTime);
    voMeasured = analogRead(measurePin);  // read the dust value
    ppm = ppm + voMeasured;
    delayMicroseconds(deltaTime);
    digitalWrite(ledPower, HIGH);  // turn the LED off
    delayMicroseconds(sleepTime);
  
    // calcVoltage = voMeasured * (5.0 / 1024.0); // 0 - 5V mapped to 0 - 1023 integer values for arduino
    calcVoltage = (voMeasured / 1023.0) * 5.0; // 0 - 3.3V mapped to 0 - 1023 integer values for esp's
    dustDensity = 170 * calcVoltage - 0.1;
    ppm_real = (calcVoltage-0.0356)*120000;  
  
    if (ppm_real < 0)
        ppm_real = 0;  
    // Serial.print(calcVoltage,3) [V]; Serial.print(dustDensity) [mg x m3]; Serial.print(ppm_real,3) [ppm];
    // ---- SHARP AQI ----

    // ---- UV Sensor ++++
    int uvLevel = averageAnalogRead(UVOUT);
    //int refLevel = averageAnalogRead(REF_3V3);
    int refLevel = 3;
    //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
    float outputVoltage = 3.3 / refLevel * uvLevel;
    float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
    uv_index = uvIntensity;
    //Serial.println("output: "); Serial.print(refLevel);
    //Serial.print("ML8511 output: "); Serial.print(uvLevel);
    //Serial.print(" / ML8511 voltage: "); Serial.print(outputVoltage);
    //Serial.print(" / UV Ray Intensity (mW/cm^2): "); Serial.print(uvIntensity);
    // ---- UV Sensor ----

    // ---- BATT % ++++
    batt = battery_read();
    // Serial.println("Battery Level: ");
    // Serial.println(battery_read(), 2);
    // ---- BATT % ----

    // ---- current A ++++
    int adc = analogRead(currentpin);
    float adc_voltage = adc * (3.3 / 4096.0);
    float current_voltage = (adc_voltage * (r1+r2)/r2);
    float current = (current_voltage - 2.5) / 0.100;
    // Serial.print("Current Value: ");  Serial.println(current);
    load_current = current;
    // ---- current A ----

    // create the data buffer
    dateformat = day + date_separator + month + date_separator + year;
    utctime = hour + time_separator + minute + time_separator + second;

    //Serial.println(buffer);

  // Write data on SD card
  if (myFile) {
    myFile.println(buffer); // write data
    myFile.print("\n"); // separator
    myFile.close();
  } else { Serial.print("SD Card: Issue encountered while attempting to open the file esp32.txt"); }

  // Transfer data over serial bus from esp32 over TX
    Serial1.println(buffer);
    Serial1.print("\n");


// End of Loop
delay(5000);
}