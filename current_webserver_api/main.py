from machine import Pin
from html import get_root_html, get_sidebar
from microserver import MicroPyServer

led = Pin(2, Pin.OUT)


def get_script():
    f = open('script.txt')
    html = f.read()
    f.close()
    return html


def root(self, request):
    html = get_root_html('Starting')
    html += '<div style="width:20%;" id="debug">' + str(request) + '</div>'
    html += get_script()
    server.send(html)


def get_devices():
    devices = ['_ldr', 'led_controls']
    return devices


def setup_sidebar(self, request):
    devices = get_devices()
    sidebar = get_sidebar(devices)
    server.send(sidebar + self.html_str)


def action(self, request):

    message = ''
    led_on = str(request).find('led=on') != -1
    led_off = str(request).find('led=off') != -1
    if led_on:
        message = 'ON'
        led.value(1)
    if led_off:
        message = 'OFF'
        led.value(0)

    server.send(str(message))


def led_controls(self, request):

    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    html = """<h1>ESP Web Server</h1> 
  <p>GPIO state: <strong id='gpio_state'>""" + gpio_state + """</strong></p><p><a href="#1" onclick="action('/action?led=on', 'gpio_state');"><button class="button">ON</button></a></p>
  <p><a href="#1" onclick="action('/action?led=off', 'gpio_state');"><button class="button button2">OFF</button></a></p>"""
    server.send(html)


server = MicroPyServer()
server.add_route("/", root)

server.add_route("/action", action)
server.add_route("/led_controls", led_controls)
server.add_route("/sidebar", setup_sidebar)

server.start()
