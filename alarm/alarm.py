from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import network, usocket, utime, ntptime

# user data
ssid = "your_wifi_ssid"
pw = "your_wifi_pw"

pic_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Wheelock_mt2.jpg/675px-Wheelock_mt2.jpg"
web_query_delay = 600000
timezone_hour = 0  # timezone offset (hours)
alarm = [7, 30, 0]  # alarm[hour, minute, enabled(1=True)]

oled = SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))
buzzer = Pin(14, Pin.OUT)
buzzer.off
shake_sensor = Pin(12, Pin.IN, Pin.PULL_UP)

# connect to wifi
print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)
while not wifi.isconnected():
    pass
print("Connected.")

# setup web server
s = usocket.socket()
s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
s.bind(("", 80))  # listen port 80
s.setblocking(False)  # set to non-blocking mode
s.settimeout(1)
s.listen(1)  # allow 1 client
print("Web server is now online at", ssid, "IP:", wifi.ifconfig()[0])


# webpage to be sent to user
def webpage(data):
    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<head>"
    html += "<title>MicroPython Alarm Clock</title>"
    html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    html += "<link rel=\"icon\" href=\"#\">"
    html += "<style>body {background-color: Moccasin;} h1 {color: SaddleBrown;} h2 {color: Olive;} </style>"
    html += "</head>"
    html += "<body><center>"
    html += "<h1>MicroPython Alarm Clock</h1>"
    html += "<h2>When the hell would you sir like to wake up?</h2>"
    html += "<p><img src=\"" + pic_url + "\" width=300px></p>"
    html += "<form methon=\"GET\" action=\"\">"
    html += "<p>Set at (hour/minute) "
    html += "<input type=\"text\" name=\"hour\" size=\"2\" maxlength=\"2\" value=\"" + str(data[0]) + "\">"
    html += " : <input type=\"text\" name=\"minute\" size=\"2\" maxlength=\"2\" value=\"" + str(data[1]) + "\">"
    html += "</p><p>Enable: <select name=\"enable\">"
    if data[2] == 1:
        html += "<option value=\"0\">No</option>"
        html += "<option value=\"1\" selected>Yes</option>"
    else:
        html += "<option value=\"0\" selected>No</option>"
        html += "<option value=\"1\">Yes</option>"
    html += "</select></p>"
    html += "<p><input type=\"submit\" value=\"Update\"></p>"
    html += "</form>"
    html += "<p><input type=\"button\" value=\"Refresh\" onclick=\"window.location.href=''\"></p>"
    html += "</center></body>"
    html += "</html>"
    return html


update_time = utime.ticks_ms() - web_query_delay
clients = []

while True:

    try:
        # listen to new clients
        client, addr = s.accept()
        print("New client connected, IP:", addr)
        clients.append(client)
    except:
        pass  # no clients to connect now

    # if there are clients connected:
    for client in clients:

        try:
            # get HTTP response
            request = client.recv(1024)
            request_text = str(request.decode("utf-8"))
            para_pos = request_text.find("/?")

            # extract GET parameters and set the alarm
            if para_pos > 0:
                para_str = request_text[para_pos + 2:(request_text.find("HTTP/") - 1)]
                para_array = para_str.split('&')

                for i in range(len(para_array)):
                    para_array[i] = (para_array[i])[para_array[i].find('=') + 1:]

                for i in range(3):
                    if para_array[i].isdigit():
                        alarm[i] = int(para_array[i])
                    else:
                        print("!!! Alarm time set error !!!")

                print("Alarm has been set to", str(alarm[0]) + ":" + str(alarm[1]))
                if alarm[2] == 1:
                    print("Alarm enabled")
                else:
                    print("Alarm disabled")

            # send web page to user
            response = webpage(alarm)
            print("Sending web page...")
            client.send("HTTP/1.1 200 OK\n")
            client.send("Content-Type: text/html; charset=utf-8\n")
            client.send("Connection: close\n\n")
            client.send(response)
            client.close()
            clients.remove(client)
            print("Client connection ended.")

        except:
            pass

    # update web clock time
    if utime.ticks_ms() - update_time >= web_query_delay:

        try:
            # update system time from NTP server
            ntptime.settime()
            print("NTP server query successful.")
            print("System time updated:", utime.localtime())
            update_time = utime.ticks_ms()

        except:
            print("NTP server query failed.")

    # display time and alarm status
    local_time_sec = utime.time() + timezone_hour * 3600
    local_time = utime.localtime(local_time_sec)
    time_str = "Alarm: {3:02d}:{4:02d}:{5:02d}".format(*local_time)
    alarm_str = "Time:  {0:02d}:{1:02d}".format(*alarm)
    alarm_str += " [O]" if alarm[2] == 1 else " [X]"

    oled.fill(0)
    oled.text(alarm_str, 0, 8)
    oled.text(time_str, 0, 24)
    oled.text(wifi.ifconfig()[0], 0, 48)
    oled.show()

    # trigger alarm
    if alarm[2] == 1 and alarm[0] == local_time[3] and alarm[1] == local_time[4]:

        print("!!! Alarm triggered !! Shake to turn off !!!")
        buzzer.on()

        # turn off alarm if user shake the vibration switch
        if shake_sensor.value() == 1:
            alarm[2] = 0
            buzzer.off()
            print("Alarm turned off.")