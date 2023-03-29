from machine import UART
from micropy.micropyGPS import MicropyGPS
from time import sleep

# denne variabel opdateres til at holde gps data
gps_data = None
# instans af gps klassen opdateres her
gps = None

def get_gps_data():
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    global gps
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        if buf:
            for char in buf:
                gps.update(chr(char)) # Note the conversion to to chr, UART outputs ints normally
        
        #different gps methods that can be used:
        
        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites:', gps.satellites_in_use)
        #print('Altitude:', gps.altitude)
        #print('Latitude:', gps.latitude_string()
        #print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)
        #print('Compas direction: ', gps.compass_direction())
        
        formattedLat = gps.latitude_string()    
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]

        #print(gps.speed_string())
        
        #gps_ada = +formattedLat+","+formattedLon+
        gps_data = formattedLat+","+formattedLon
        gps_in_use = gps.satellites_in_use
        
        ##funktion til at sende
        if formattedLat != "0.0" and formattedLon != "0.0":
            print('Satellites:', gps_in_use)
            print("From gps_location, is not 0 {}".format(gps_data))
            return gps_data
            
        if formattedLat == "0.0" and formattedLon == "0.0":
            print('Satellites:', gps_in_use)
            print("From gps_location, is 0 {}".format(gps_data))
            return gps_data
        sleep(0.1)