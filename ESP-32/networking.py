import network
from time import sleep
from credentials import credentials

# WiFi information
WIFI_SSID = credentials["ssid"]
WIFI_PASSWORD = credentials["password"]

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    
    if (wlan.isconnected()):
        wlan.disconnect()
    
    wlan.active(True)
    
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not wlan.isconnected():
        sleep(1)
    print("Connected to WiFi network.")
    print("Network configuration:", wlan.ifconfig())
    return wlan
