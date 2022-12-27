# Complete project details at https://RandomNerdTutorials.com
from machine import Pin
import network

def web_page():
    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    html = """ your code  """
    return html

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        if led_on == 6:
            print('LED ON')
            led.value(1)
        if led_off == 6:
            print('LED OFF')
            led.value(0)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()