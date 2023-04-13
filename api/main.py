from html import web_page
from machine import Pin, PWM
from api import api
import time
try:
    import usocket as socket
except:
    import socket
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# pwm_pin = PWM(Pin(18, mode=Pin.OUT))
pwm_pin = PWM(Pin(18), freq=50)

while True:

    conn, addr = s.accept()
    conn.settimeout(3.0)

    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)

    request = str(request)
    motor_speed = request.find('motor_speed=') > -1


    if motor_speed:

        motor_speed = request.split(' HTTP')[0].split("motor_speed=")[1].replace("'",'')

        pwm_pin.duty(int(motor_speed))

        print('motor_speed = ')   
        print(motor_speed)
        response = str(motor_speed)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        print(response)
        print('closing')
    else:
        response = web_page(pwm_pin)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()