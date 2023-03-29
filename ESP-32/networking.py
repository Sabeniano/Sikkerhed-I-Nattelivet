import network
from credentials import credentials

# WiFi connection information
WIFI_SSID = credentials["ssid"]
WIFI_PASSWORD = credentials["password"]

def connect_to_wifi():
    # Create a WLAN interface
    wlan = network.WLAN(network.STA_IF)

    # Activate the WLAN interface
    wlan.active(True)

    # Connect to the network
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for the connection to be established
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected to WiFi network.")

    # Print the network configuration
    print("Network configuration:", wlan.ifconfig())
    return wlan