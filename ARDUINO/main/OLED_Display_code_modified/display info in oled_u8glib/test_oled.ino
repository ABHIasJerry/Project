#include "U8glib.h"

U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NONE|U8G_I2C_OPT_DEV_0);  // I2C / TWI

void draw(void) {
  // graphic commands to redraw the complete screen should be placed here 
  //u8g.setFont(u8g_font_unifont);
  //u8g.setFont(u8g_font_helvB24);
  u8g.setFont(u8g_font_6x10);
  u8g.drawStr( 5, 10, "T: 29 C");
  u8g.drawStr( 70, 10, "H: 96 %");
  u8g.drawStr( 5, 25, "TIME: 10:21 PM");
  u8g.drawStr( 5, 40, "LAT : 22°32'59.99 N ");
  u8g.drawStr( 5, 57, "LONG : 88°19'60.00 E");
}

void setup(void) {
  // flip screen, if required
  // u8g.setRot180();
 
  // set SPI backup if required
  //u8g.setHardwareBackup(u8g_backup_avr_spi);

  // assign default color value
  if ( u8g.getMode() == U8G_MODE_R3G3B2 ) {
    u8g.setColorIndex(255);     // white
  }
  else if ( u8g.getMode() == U8G_MODE_GRAY2BIT ) {
    u8g.setColorIndex(3);         // max intensity
  }
  else if ( u8g.getMode() == U8G_MODE_BW ) {
    u8g.setColorIndex(1);         // pixel on
  }
  else if ( u8g.getMode() == U8G_MODE_HICOLOR ) {
    u8g.setHiColorByRGB(255,255,255);
  }
}

void loop(void) {
  // picture loop
  u8g.firstPage(); 
  do {
    draw();
  } while( u8g.nextPage() );
 
  // rebuild the picture after some delay
  delay(50);
}
