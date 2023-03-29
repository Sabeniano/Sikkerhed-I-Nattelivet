from time import sleep
from umqtt.simple import MQTTClient
from credentials import credentials

# Connect to MQTT server
def mqtt_client():
    CLIENT_ID = credentials["productid"]
    SERVER = credentials["raspserver"]
    PORT = credentials["port"]
    
    mqtt_client = MQTTClient(CLIENT_ID, SERVER, PORT)
    mqtt_client.connect()
    print("Connected to MQTT server.")
    return mqtt_client

# Check MQTT connection status and reconnect
def check_mqtt_connection(client):
    if not client.check_msg():
        try:
            client.disconnect()
            client.connect()
            print('MQTT reconnected')
        except:
            print('MQTT reconnect failed')
            # Do something else if reconnection fails

