//Arduino Uno; SDA = A4, SCL = A5
// reference: https://www.instructables.com/TCA9548A-I2C-Multiplexer-Module-With-Arduino-and-N/
#include "Wire.h"
#include <U8glib.h>
#define MUX_Address 0x70 // TCA9548A Encoders address

char tmp_string[8];  // Temp string to convert numeric values to string before print to OLED display
U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_FAST);  // Fast I2C / TWI
//U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NONE|U8G_I2C_OPT_DEV_0);  // I2C / TWI

// Initialize I2C buses using TCA9548A I2C Multiplexer
void tcaselect(uint8_t i2c_bus) {
    if (i2c_bus > 7) return;
    Wire.beginTransmission(MUX_Address);
    Wire.write(1 << i2c_bus);
    Wire.endTransmission(); 
}

void setup(){
    DisplayInit(); // Initialize the displays 
}

// Initialize the displays 
void DisplayInit(){
    for (int i = 0; i < 7; i++) {
      tcaselect(i);   // Loop through each connected displays on the I2C buses  
      u8g.firstPage();
      do {
        u8g.begin();  // Initialize display
       } while( u8g.nextPage() );
    }
}


void loop(){
    for (int i = 0; i < 7; i++) {
      tcaselect(i);
      get_val = tcaselect(i);
      u8g.firstPage();
      do {
        /******** Display Something *********/
        u8g.setFont(u8g_font_ncenB10);
        //u8g.drawStr(0, 13, "Connected to:");
        u8g.drawStr(0, 13, get_val);
        itoa(i, tmp_string, 10);  
        u8g.setFont(u8g_font_ncenB18);
        u8g.drawStr(25, 50, tmp_string);
        /************************************/
      } while( u8g.nextPage() );
      delay(50);
    }
    delay(500);
}
