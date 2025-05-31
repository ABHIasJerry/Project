

from machine import Pin
import network, socket, time, os
from html import create_html_page
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
ssid = os.getenv('SSID')
password = os.getenv('PASSWORD')
ip = os.getenv('IP_ADD')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
print("Connected to Wi-Fi!")
print("IP Address:", wlan.ifconfig()[0])

# HTML content for the webpage
html = create_html_page(dataframe)

# Start a web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print("Web server running on http://{}:80".format(wlan.ifconfig()[0]))

while True:
    try:
        client, addr = server.accept()
        print("Client connected from", addr)
        request = client.recv(1024)
        print("Request:", request)

        # Send HTTP response
        client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        client.send(html)
        client.close()
    except Exception as e:
        print("Error:", e)
        client.close()
