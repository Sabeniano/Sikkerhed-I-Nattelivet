import usocket
from time import sleep
from umqtt.simple import MQTTClient
from credentials import credentials

CLIENT_ID = credentials["productid"]
SERVER = credentials["raspserver"]
PORT = credentials["port"]

# Connect to MQTT server
def connect_mqtt_client():
    mqtt_client = MQTTClient(CLIENT_ID, SERVER, PORT)
    
    try:
        mqtt_client.connect()
    except OSError as e:
        if "Name or service not known" in str(e):
            print('Error connecting to MQTT broker: hostname could not be resolved')
        else:
            print('Error connecting to MQTT broker:', e)
        return False
        
    print("Connected to MQTT server.")
    return mqtt_client

# Check MQTT connection status and reconnect
def check_mqtt_connection(mqtt_client):
    try:
        mqtt_client.ping()
    except:
        try:
            mqtt_client.disconnect()
            mqtt_client.connect()
            print('MQTT reconnected')
        except Exception as e:
            print('MQTT reconnect failed:', e)
            # Do something else if reconnection fails

