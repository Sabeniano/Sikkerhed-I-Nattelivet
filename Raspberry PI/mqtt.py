import os
import sqlite3
import paho.mqtt.client as mqtt
from twilio_sms import send_sms

db_path = db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db', 'sinDB.db'))

def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")

    prod_koord = data.split(" ",1)
    lat_long = prod_koord[1].split(",",1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
                INSERT INTO koordinater (bruger_id, latitude, longitude)
                SELECT bruger_id, ?, ?
                FROM bruger
                WHERE produkt = ?
                ''', (lat_long[0], lat_long[1], prod_koord[0]))
    conn.commit()
    conn.close()
    print("record inserted.")
    print(f"Received message: {message.payload.decode()}")
    lokation_url = f'https://young-frog-3.telebit.io/lokation/{lat_long[0]}/{lat_long[1]}'
    send_sms("+4560571314", lokation_url)

def mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("gps_data_topic")
    client.loop_start()
