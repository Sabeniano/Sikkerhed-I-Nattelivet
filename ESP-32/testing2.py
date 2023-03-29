from umqtt.simple import MQTTClient
from networking import network_connection

def main(server="giant-monkey-39.telebit.io"):
    c = MQTTClient("umqtt_client", server, 20190)
    c.connect()
    c.publish(b"test", b"hello")
    c.disconnect()
    
while True:
    network_connection()
    main()