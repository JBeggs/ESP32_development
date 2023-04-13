from machine import Pin

from microserver import MicroPyServer
from html import get_html, get_sidebar
# from dht import DHT22


# def _ldr():
#     ldr = Pin(26, Pin.IN)
#     if ldr.value():
#         result = 'Detected'
#     else:
#         result = 'ALL CLEAR'
#     print(result)
#     return result


# def _dht22():
#     # DHT11 and DHT22 library
#     # https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/dht.html
#
#     # functions related to the board - http://docs.micropython.org/en/latest/esp8266/library/machine.html
#     import machine
#
#     d = DHT22(machine.Pin(25))
#     # Ask for data
#     d.measure()
#     print(dir(d))
#     print((d.__dict__))
#     result = str(d.temperature()) + ' : '
#     print(result)
#     result += str(d.humidity())
#     print(result)
#     return result


def root(request):
    html = get_html('Starting again 23')
    server.send(html)


def get_devices():
    devices = ['_ldr']
    return devices


def setup_sidebar():
    devices = get_devices()
    sidebar = get_sidebar(devices)
    return sidebar


server = MicroPyServer()
''' add route '''
server.add_route("/", root)

server.add_route("/nav", setup_sidebar)

server.start()
