import network
from time import sleep
from credentials import credentials

# WiFi connection information
WIFI_SSID = credentials["ssid"]
WIFI_PASSWORD = credentials["password"]

def connect_to_wifi():
    # Create a WLAN interface
    wlan = network.WLAN(network.STA_IF)
    
    #Fixer WiFi OS fejl!
    if (wlan.isconnected()):
        wlan.disconnect()
    
    # Activate the WLAN interface
    wlan.active(True)
    
    # Connect to the network
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Wait for the connection to be established
    while not wlan.isconnected():
        sleep(1)
    print("Connected to WiFi network.")
    # Print the network configuration
    print("Network configuration:", wlan.ifconfig())
    return wlan