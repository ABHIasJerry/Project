/* ------------------------- LINKS --------------------------------
To learn codes for ESP32 :  https://esp32io.com/esp32-tutorials [.]
Github link : https://github.com/yash-sanghvi/ESP32/tree/master [.]
I2C links : https://www.chippiko.com/list-of-device-i2c-address [.]
https://randomnerdtutorials.com/esp-now-auto-pairing-esp32-esp8266/
https://www.prisma.io/dataguide/mongodb/setting-up-a-local-mongodb-database
/* ----------------------------------------------------------------

/* -------- MCU MAC Addresses ---------------------
RPI [Pi-W] -> MAC ID: 28:cd:c1:07:a7:4c      [WiFi]
ESP [8266] -> MAC ID: 98:CD:AC:28:81:DD   [NodeMCU]
ESP [32S ] -> MAC ID: 0c:b8:15:d7:f5:a8      [WiFi]
           -> MAC ID: 0C:B8:15:D7:F5:AA [Bluetooth]
/* ------------------------------------------------

/* ------- Sensor I2C Addresses -------------------
BME680           -> 0X77                        [\]
MPU6050          -> 0x68                        [\]
OLED 1306 [1.3"] -> 0x3C                        [\]
OLED 1306 [0.9"] -> 0x3D                        [\]
OLED 1306 [9.0"] -> 0x..                        [\]
VL53L0X          -> 0x29                        [\]
RTC              -> 0x68                        [\]
16X2 LCD         -> 0x27                        [\]
TCA9548A         -> 0x74                        [\]
/* ------------------------------------------------

/* ---------- Static IP Address Pool --------------
IP 01: 192.168.0.105                            [?]
IP 01: 192.168.0.106                            [?]
IP 01: 192.168.0.107                            [?]
/* ------------------------------------------------

/* -------------------- HC 05 ----------------------
HC05 [01]   -> Dev Name: IOT-SLAVE-0A  PIN: 1234 [/]
HC05 [02]   -> Dev Name: IOT-SLAVE-0B  PIN: 0000 [|]
HC05 [03]   -> Dev Name: IOT-SLAVE-0C  PIN: 9889 [\]
/* -------------------------------------------------

/* -------------- WebPage Data Format --------------
<Head1> IoT Weather-Station RealTime Monitor </Head1>

<head2> --- GPS DataFrame --- <head2>

        <p> Lat: xxx [N] </p>
        <p> Long: xxx [S] </p>
        <p> Altitude: xxx [m] </p>
        <p> Timestamp: xx:xx:xx [UTC] </p>
        <p> Date: xx/xx/xx </p>

<head2> --- BME DataFrame --- <head2>

        <p> Temperature: xxx [*C] </p>
        <p> Pressure: xxx [hPa] </p>
        <p> Humidity: xxx [%] </p>
        <p> Gas: xxx [KOhms] </p>
        <p> Sea Altitude: xxx [m @ sea-level] </p>

<head2> --- AQI DataFrame --- <head2>

        <p> Voltage: xxx [V] </p>
        <p> Dust Density: xxx [mg x m3] </p>
        <p> PPM: xxx [ppm] </p>

<head2> --- TOF DataFrame --- <head2>

        <p> Lidar Distance: xxx [m] </p>

<head2> --- MPU6050 DataFrame --- <head2>

        <p> Acceleration X-axis: xxx  </p>
        <p> Acceleration Y-axis: xxx  </p>
        <p> Acceleration Z-axis: xxx  </p>
        <p> Gyroscope X-axis: xxx  </p>
        <p> Gyroscope Y-axis: xxx  </p>
        <p> Gyroscope Z-axis: xxx  </p>

<head2> --- UV DataFrame --- <head2>

        <p> UV-Index: xxx [mW/cm^2] </p>

<head2> --- ESP32 DataFrame --- <head2>

        <p> Battery: xxx [%] </p>
        <p> Load Current: xxx [mA] </p>
        <p> IP Address: 192:168:1:xxx </p>
        <p> Status: Ok </p>

<Footer> @AG.All Rights Reserved [2025-2026] </Footer>
/* -------------------------------------------------

cmd: start backend/ESP32_CPU/Docs/esp32_live_monitor_index.html