import _thread
import network
import utime
from time import sleep
from credentials import credentials
from networking import connect_to_wifi
from machine import ADC, Pin, I2C, SoftI2C, UART
from battery_lights import led_percentage
from bytes_to_voltage import calculate_voltage
from mqtt_communication import connect_mqtt_client, check_mqtt_connection
from micropy.micropyGPS import MicropyGPS

## Pin objekter
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
green_led = Pin(32, Pin.OUT)
red_led = Pin(33, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)
vib = Pin(19, Pin.OUT, value=0)

## Instans af wlan og mqtt
wlan = connect_to_wifi()
mqtt_client = connect_mqtt_client()

## MCP3021 I2C addresse
address = 0x49 #73

## Slukker LED
red_led.off()
green_led.off()

##_thread lock objekt
lock = _thread.allocate_lock()

## Delte variabler, til thread lock
send_data_flag = False

gps_from_thread = None

## Debounce timer
debounce = 50

## Bliver ikke brugt
last_pressed_time = 0

# Product id på ESP
PRODUCT_ID = credentials["productid"]

def gps_thread(sleep_timer):
    uart = UART(2, baudrate=9600, bits=8, parity=None,
                stop=1, timeout=5000, rxbuf=1024)
    global gps_from_thread
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        if buf:
            for char in buf:
                gps.update(chr(char))
        
        formattedLat = gps.latitude_string()    
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]

        gps_in_use = gps.satellites_in_use

        if formattedLat != "0.0" and formattedLon != "0.0":
            gps_from_thread = formattedLat+","+formattedLon
            print("From gps_thread: {}".format(gps_from_thread))
        sleep(sleep_timer)

# Send data thread function
def send_data_thread(sleep_timer):
    global gps_from_thread, send_data_flag
    while True:
        if send_data_flag:
            with lock:
                data = gps_from_thread
                print(data)
            if data is not None and len(data) > 7:
                mqtt_client.publish('gps_data_topic',PRODUCT_ID +' '+ data)        
                vib.value(0)
                print("Sendt data!")
            else:
                vib.value(1)
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
    
    if not wlan.isconnected():
        connect_to_wifi()
        vib.value(0)
    else:
        vib.value(1)
        
    
    if not mqtt_client:
        return
    
    while True:
        data = i2c.readfrom(address, 2)
        
        if not wlan.isconnected():
            connect_to_wifi()
            vib.value(1)
        else:
            vib.value(0)
        
        if check_mqtt_connection(mqtt_client):
            vib.value(1)
        else:
            vib.value(0)
        
        battery_percentage = calculate_voltage(data)
        led_percentage(green_led, red_led, battery_percentage)

        button_pressed = not button.value() 
        if button_pressed:
            print("button pressed")
            with lock:
                send_data_flag = True
        sleep(1)
    
_thread.start_new_thread(gps_thread, (1,))
_thread.start_new_thread(send_data_thread, (5,))
main_loop()
