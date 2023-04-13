import network
import time

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('New Home', '1223334444')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)

print('Connection successful')
print(sta_if.ifconfig())
