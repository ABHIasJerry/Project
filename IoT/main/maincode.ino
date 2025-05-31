/* Author: Abhinaba Ghosh     Date: 25-05-2025   Revision: v1.0   Time: 02:49AM */

/* MAIN CPU code -> Design Flow -> BME680/MPU6050/VL53LOX/RTC/NEO-6M-GPS/UV-sensor/Current-sensor -> data -> ESP32 -> TX -> PicoW (SDcard + MongoDB + Webpage) */

/* --- PIN Configurations ---
          Name              Pin
        ---------------------------  
        | SCL            | GPIO22
        | SDA            | GPIO 21
        | TX             | GPIO16
        | RX             | GPIO17
        | ESP-TX1        | GPIO10
        | ESP-RX1        | GPIO9
        | MISO           | GPIO19
        | MOSI           | GPIO23
        | SCK            | GPIO18
        | SS/CS          | GPIO5
        | Analog         | GPIO0   -> Sharp AQI
        | Analog         | GPIO2   -> battery monitor
        | Digital        | GPIO36
        | Power,REF_3V3  | 3.3 V
        | Ground         | GND
        | CurrentPin     | GPIO4
        | UVOUT          | GPIO15
        -------------------------
*/

// Include
#include <SD.h>
#include <SPI.h>
#include <Wire.h>
#include "RTClib.h"
#include <Arduino.h>
#include <TinyGPSPlus.h>
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include "Adafruit_VL53L0X.h"

// Definations
#define GPS_BAUDRATE 9600  // The default baudrate of NEO-6M is 9600
#define SEALEVELPRESSURE_HPA (1013.25)  // Correction

// Pin Declarations
#define PIN_SPI_CS 5    // The ESP32 pin GPIO5
#define measurePin 0    // connect dust sensor to Analog GPIO0 [pin 25]
#define ledPower 36     // connect to led driver pin of dust sensor to GPIO5 [Digital pin 29]
#define scl 22          // I2C data capture
#define sda 21          // I2C data capture
#define miso 19         // SPI data transfer
#define mosi 23         // SPI data transfer
#define ss 5            // SPI data transfer
#define sck 18          // SPI data transfer
#define GPS_TX 16       // connect Tx of the ESP with GPS module
#define GPS_RX 17       // connect Rx of the ESP with GPS module
#define ESP_Tx 10       // UART0-TX data transfer to PicoW
#define ESP_Rx 9        // UART0-RX data transfer to PicoW
#define UVOUT 15        // Output from the sensor
#define currentpin 4    // current sensing module pin
#define analogPin 2     // Use any ADC pin 

// Declarations
StaticJsonDocument<1000> doc;
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
Adafruit_BME680 bme;
TinyGPSPlus gps;
RTC_DS1307 rtc;
File myFile;

// Global variables initialization
//FLOAT
float altitude,speed;
float temperature,pressure,humidity,gas,sea_altitude;
float voMeasured,calcVoltage,dustDensity,ppm;
float voltage,ppm_real,tof_distance,load_current,uv_index;
float r1 = 6800.0; float r2 = 12000.0;

//INT
int year,month,day,hour,minute,deltaTime,batt,counter,second,samplingTime;
int sleepTime = 9860; int satellites; int process_counter = 0;

//CHAR
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

//STRING
String latitude;
String longitude;
String date_separator = "-";
String time_separator = ":";
String dateformat;
String utctime;
String jsonString;
String status = "OK";

// Constant String/INT/int16
const String formattedTime = "";
const int MPU_ADDR = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

// Size_t
size_t freeHeap;
size_t minFreeHeap; 
size_t maxAllocHeap; 

// Dependent Functions
int averageAnalogRead(int pinToRead) {
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 
  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
  return(runningValue);}

float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;}


/* Sensor Functions */
// ---- UV ++++
void uv_sensor_process() {
    int uvLevel = averageAnalogRead(UVOUT);
    //int refLevel = averageAnalogRead(REF_3V3);
    int refLevel = 3;
    //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
    float outputVoltage = 3.3 / refLevel * uvLevel;
    float uvIntensity = mapFloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
    uv_index = uvIntensity;
    //Serial.println("output: "); Serial.print(refLevel);
    //Serial.print("ML8511 output: "); Serial.print(uvLevel);
    //Serial.print(" / ML8511 voltage: "); Serial.print(outputVoltage);
    //Serial.print(" / UV Ray Intensity (mW/cm^2): "); Serial.print(uvIntensity);
    }

// ---- Battery% ++++
float battery_read() {
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
        return 100.0f;}

// ---- RTC ++++
void rtc_time() {
    DateTime now = rtc.now();
    String yearStr = String(now.year(), DEC);
    String monthStr = (now.month() < 10 ? "0" : "") + String(now.month(), DEC);
    String dayStr = (now.day() < 10 ? "0" : "") + String(now.day(), DEC);
    String hourStr = (now.hour() < 10 ? "0" : "") + String(now.hour(), DEC); 
    String minuteStr = (now.minute() < 10 ? "0" : "") + String(now.minute(), DEC);
    String secondStr = (now.second() < 10 ? "0" : "") + String(now.second(), DEC);
    String dayOfWeek = daysOfTheWeek[now.dayOfTheWeek()];
    String formattedTime = dayOfWeek + ", " + yearStr + "-" + monthStr + "-" + dayStr + " " + hourStr + ":" + minuteStr + ":" + secondStr;}

// ---- GPS ++++
void gps_sensor() {
    if (Serial2.available() > 0) {
      if (gps.encode(Serial2.read())) {
        
        if (gps.location.isValid()) { latitude = (gps.location.lat(),6); longitude = (gps.location.lng(),6); 
        } else {latitude = 0.0; longitude = 0.0;}
        
        if (gps.altitude.isValid()) { altitude = gps.altitude.meters(); 
        } else {altitude = 0.0;}

        if (gps.speed.isValid()) { speed = gps.speed.kmph(); 
        } else {speed = 0.0;}

        if (gps.satellites.isValid()) { satellites = gps.satellites.value();
        } else {satellites = 0;}

        if (gps.date.isValid() && gps.time.isValid()) {
          year = gps.date.year();
          month = gps.date.month();
          day = gps.date.day();
          hour = gps.time.hour();
          minute = gps.time.minute();
          second = gps.time.second();

        } else { year = 0000; month = 00; day = 00; hour = 00; minute = 00; second = 00;}
      }
    }
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println("No GPS data received: check wiring");}}

// ---- BME680 ++++
void bme680_sensor() {
    unsigned long endTime = bme.beginReading();   // Tell BME680 to begin measurement.
    delay(50);
    if (!bme.endReading()) { Serial.println("Failed to BME680 sensor reading."); return;
    } else { temperature = bme.temperature; pressure = bme.pressure / 100.0; humidity = bme.humidity; 
             gas = bme.gas_resistance / 1000.0; sea_altitude = bme.readAltitude(SEALEVELPRESSURE_HPA);
             // *C | hPa | % | KOhms | m @ sea-level
            }}

// ---- MPU6050 ++++
void mpu6050_sensor() {
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
}

// ---- TOF ++++
void lidar_sensor() {
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
    if (measure.RangeStatus != 4) { tof_distance = measure.RangeMilliMeter; 
        } else { tof_distance = 0.0; }}// phase failures have incorrect data

// ---- SHARP AQI ++++
void aqi_sensor() {
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
}

// ---- current A ++++
void system_load_measurement() {
    int adc = analogRead(currentpin);
    float adc_voltage = adc * (3.3 / 4096.0);
    float current_voltage = (adc_voltage * (r1+r2)/r2);
    float current = (current_voltage - 2.5) / 0.100;
    // Serial.print("Current Value: ");  Serial.println(current);
    load_current = current;}

// ----- SD Card Write ++++
void write_to_sd_card(String JSON_data) {
  if (myFile) {
    myFile.println(JSON_data); // write data + add the json data variable somehow
    myFile.print(",");
    myFile.print("\n"); // separator
    myFile.close();
  } else { Serial.print("SD Card: Issue encountered while attempting to open the file esp32.txt"); }}

// JSON Data-Frame creation
void create_JSON_buffer() {

  dateformat = String(day) + date_separator + String(month) + date_separator + String(year);    // Date Today
  utctime = String(hour) + time_separator + String(minute) + time_separator + String(second);  // UTC Time from GPS
  
  // Frame Start
  doc["Data Counter"] = process_counter; doc["RTC Timestamp"] = formattedTime;
  doc["Lat"] = latitude; doc["Long"] = longitude; doc["Altitude"] = altitude; doc["Speed"] = speed;
  doc["Date"] = dateformat; doc["Satellites"] = satellites; doc["UTC Time"] = utctime;  
  
  doc["Temperature"] = temperature; doc["Pressure"] = pressure; doc["Humidity"] = humidity; doc["Gas"] = gas; doc["Sea Altitude"] = sea_altitude;

  doc["Voltage"] = calcVoltage;  // [v] (round upto 3 decimal places)
  doc["Dust Density"] = dustDensity;  // [mg x m3]
  doc["PPM"] = ppm_real; // [ppm] (round upto 3 decimal places)

  doc["TOF Distance"] = tof_distance; // m

  doc["Acceleration-X"] = AcX; doc["Acceleration-Y"] = AcY; doc["Acceleration-Z"] = AcZ;
  doc["Gyro-X"] = GyX; doc["Gyro-Y"] = GyY; doc["Gyro-Z"] = GyZ;
  
  doc["UV Index"] = uv_index;  // [mW/cm^2]
  
  doc["Current Usage"] = load_current; // [mA]
  doc["Battery"] = round(batt); // [%] (round upto 2 decimal places)
  doc["Memory Usage"] = String("Free Heap: ") + freeHeap + String(" Minimum Free Heap: ") + minFreeHeap + String(" Largest Free Block: ") + maxAllocHeap + String(" [bytes]");
  doc["Status"] = "OK";
  // Frame End

  serializeJsonPretty(doc, Serial);
  serializeJsonPretty(doc, Serial1);  // Transmit data over UART1 to other MCU
  Serial.println(",");
  Serial1.println(","); 
  serializeJson(doc, jsonString);
  write_to_sd_card(jsonString); // Todo : edit this function
  } 
  

// ESP32 System Info
void system_info() {
  freeHeap = ESP.getFreeHeap();  // Get free heap memory
  minFreeHeap = ESP.getMinFreeHeap();  // Get minimum free heap memory since boot
  maxAllocHeap = ESP.getMaxAllocHeap();  // Get largest block of free memory

  // Print memory details
  Serial.println("-------------------------");
  Serial.println("Memory Usage:"); Serial.print("Free Heap: "); Serial.print(freeHeap); Serial.println(" bytes");
  Serial.print("Minimum Free Heap: "); Serial.print(minFreeHeap); Serial.println(" bytes");
  Serial.print("Largest Free Block: "); Serial.print(maxAllocHeap); Serial.println(" bytes");
  Serial.println("-------------------------");}

// Setup MCU
void setup() {
  Serial.begin(115200);   // serial print Fn
  Serial1.begin(9600, SERIAL_8N1, ESP_Tx, ESP_Rx); // Initialize UART1 on custom pins (e.g., TX = ESP_Tx, RX = ESP_Rx)
  Serial2.begin(GPS_BAUDRATE, SERIAL_8N1, GPS_TX, GPS_RX);
  Wire.begin(sda, scl, 100000); // SDA, SCL, Clock Speed
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // Set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Wire.beginTransmission(MPU_ADDR);
  pinMode(ledPower, OUTPUT);
  pinMode(UVOUT, INPUT);
  pinMode(analogPin, INPUT);
  pinMode(currentpin, INPUT);

  while (!Serial); Serial.println("Initialising Sensor(s) Data processing by ESP-Controller.....");
    
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
    Serial.println(F("File doesn't exist on SD Card."));}}

// MAIN Function
void loop() {
    system_info();
    battery_read();
    system_load_measurement();
    rtc_time();
    aqi_sensor();
    gps_sensor();
    bme680_sensor();
    mpu6050_sensor();
    lidar_sensor();
    create_JSON_buffer();  // this also writes data to SD card
    process_counter = process_counter + 1;
    delay(1000);
}
