/*
  Modified by Abhinaba according to small display resolution.
  The purpose of this program is to test and demonstrate the display performance of the 128 x 64 display

  Code will be used to display a bar graph from measured input voltage .
  Pin connections
  Arduino   device
  A0    Voltage read (5K pot across +5, and ground)
  A4    SDA (if no SDA pin)
  A5    SCL (if not SCL pin)
  SDA   SDA
  SLC   SLC
*/

#include <SPI.h>
#include <Wire.h>

#include <Adafruit_SSD1306.h>

#define OLED_RESET 4
# define ADJ_PIN A0
Adafruit_SSD1306 Display(OLED_RESET);

int r = 0;
int i = 0;

void setup()   {


  Display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)

  // i'll follow the license agreement and display the Adafruit logo
  // and since they were nice enough to supply the libraries
  Display.clearDisplay();
  Display.display();
  delay (1000);

  DrawTitles();

}


void loop() {

  // get some dummy data to display


  // r = rand() / 220;
  r = analogRead(ADJ_PIN);
  r = r / 7.98;

  Display.setTextSize(1);
  // note set the background color or the old text will still display
  Display.setTextColor(WHITE, BLACK);
  Display.setCursor(20, 17);
  Display.println(Format(r * 7.99 / 204.6, 3, 2));
  Display.setCursor(55, 17);
  Display.println("volts/sec");

  //draw the bar graph
  Display.fillRect(r, 27, 10 - r, 10, BLACK);
  Display.fillRect(3, 27, r, 10, WHITE);

  for (i = 1; i < 13; i++) {
    Display.fillRect(i * 10, 25, 2, 10, BLACK);
  }

  // now that the display is build, display it...
  Display.display();


}


void DrawTitles(void) {

  Display.setTextSize(1);
  Display.setTextColor(WHITE);
  Display.setCursor(10, 0);
  Display.println("-- MULTIMETER --");

  Display.setTextSize(1);
  Display.setTextColor(WHITE);
  Display.setCursor(0, 8);
  Display.println("Measured Volts [ DC ]");
  //Display.println("Random number");
  Display.display();

}


String Format(double val, int dec, int dig ) {

  // this is my simple way of formatting a number
  // data = Format(number, digits, decimals) when needed

  int addpad = 0;
  char sbuf[20];
  String fdata = (dtostrf(val, dec, dig, sbuf));
  int slen = fdata.length();
  for ( addpad = 1; addpad <= dec + dig - slen; addpad++) {
    fdata = " " + fdata;
  }
  return (fdata);

}
