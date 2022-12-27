//Libs for espnow and wifi
#include <esp_now.h>
#include <WiFi.h>

//Channel used in the connection
#define CHANNEL 1

//Gpios that we are going to read (digitalRead) and send to the Slaves
//It's important that the Slave source code has this same array
//with the same gpios in the same order
uint8_t gpios[] = {23, 2};

//In the setup function we'll calculate the gpio count and put in this variable,
//so we don't need to change this variable everytime we change
//the gpios array total size, everything will be calculated automatically
//on setup function
int gpioCount;

//Slaves Mac Addresses that will receive data from the Master
//If you want to send data to all Slaves, use only the broadcast address {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}
//If you want to send data to specific Slaves, put their Mac Addresses separeted with comma (use WiFi.macAddress())
//to find out the Mac Address of the ESPs while in STATION MODE)
uint8_t macSlaves[][6] = {
  //To send to specific Slaves
  //{0x24, 0x0A, 0xC4, 0x0E, 0x3F, 0xD1}, {0x24, 0x0A, 0xC4, 0x0E, 0x4E, 0xC3}
  //Or to send to all Slaves
  {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}
};