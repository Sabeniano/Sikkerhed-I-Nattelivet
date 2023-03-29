import _thread
import network
import gps
import utime
import mqtt_communication
from time import sleep
from credentials import credentials
from networking import connect_to_wifi
from machine import ADC, Pin, I2C, SoftI2C
from battery_lights import led_percentage
from bytes_to_voltage import calculate_voltage
from testing import test_byte


# Define a debounce time in milliseconds
debounce = 50

# Define a variable to store the last time the button was pressed
last_pressed_time = 0

## Pin objekter
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
green_led = Pin(32, Pin.OUT)
red_led = Pin(33, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)



## MCP3021 I2C addresse
address = 0x49 #73

## Slukker LED
red_led.off()
green_led.off()

## Delte variabler, til thread lock
gps_pos_recent = None
send_data_flag = False


## Lavet er _thread lock objekt, som vi bruger så vi kan sende data mellem threads,
## som sørger for at ingen andre threads kan bruge den delte variable før den bliver frigjort
lock = _thread.allocate_lock()

wlan = connect_to_wifi()
mqtt_client = mqtt_communication.mqtt_client()

PRODUCT_ID = credentials["productid"]

# GPS thread function
def gps_thread(sleep_timer):
    global gps_pos_recent
    while True:
        gps_data = gps.get_gps_data()
        with lock:
            gps_pos_recent = gps_data
        sleep(sleep_timer)

# Send data thread function
def send_data_thread(sleep_timer):
    global gps_pos_recent, send_data_flag
    while True:
        if send_data_flag:
            with lock:
                data = gps_pos_recent
            if data is not None and len(data) > 7:
                mqtt_client.publish('gps_data_topic',PRODUCT_ID +' '+ data)
                print("Data sent successfully")
                #TODO VIBRATION IF STATEMENT HVIS DATA IKKE ER SENDT
                #if
                #print("Failed to send data")
            else:
                #TODO VIBRATION
                print("No signal from GPS")
            send_data_flag = False
        sleep(sleep_timer)

def button_pressed(pin):
    global last_pressed_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_pressed_time) > DEBOUNCE_MS:
        last_pressed_time = current_time

def main_loop():
    global send_data_flag
    while True:
        data = i2c.readfrom(address, 2)
        
        #network
        if not wlan.isconnected():
            connect_to_wifi()
        #mqtt_client
        if mqtt_client.sock is None:
            mqtt_communication.check_mqtt_connection(mqtt_client)
        ## Læser værdi fra ADC med I2C
    
        #battery_percentage = calculate_voltage(data)
        #led_percentage(green_led, red_led, battery_percentage)

        button_pressed = not button.value()  ##Simulate waiting for button press event
        if button_pressed:
            print("button pressed")
            with lock:
                send_data_flag = True
        sleep(1)
    
_thread.start_new_thread(gps_thread, (1,))
_thread.start_new_thread(send_data_thread, (5,))
main_loop()


##Todo:
##knap som sender gps_pos_recent til mqqt raspberrypi
##bedre tjek på if data != "0.0,0.0":
##vibration på if data == "0.0,0.0"(stadig bedre tjek):
##kominber bytes_to_voltage fil med battery_lights


## TODO ESP:
## BEDRE LOGIK PÅ INTERNET OG MQTT CONNECTION


## knap til send gps data
## vibrator hvis gps data ikke sendt
## led batteri
    
## TODO RaspberryPi:
## mqtt broker tjek
## netværk? tjek
## få data fra esp med mqtt broker tjek
## opsæt python til at kigge på mqtt data og derefter brug data
## matplot kort
## sæt latitude og longitude på matplot kort
## data på database
## gem data på database
## sæt ALLE latitude og longitude på matplot kort
## ring til mobil
## login funktion
## session funktion

    

