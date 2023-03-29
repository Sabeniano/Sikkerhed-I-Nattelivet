import struct

    ##https://www.w3schools.com/python/gloss_python_bitwise_operators.asp
    # unpack() # tager en bytestring og konvertere det til en tuple af værdier baseret på '>h'
    # >h       # 'h' specificerer, at dataen er en 2-byte (16-bit) signed integer.
    # [0]      # [0] i slutningen af struct.unpack() metoden tilgår den første (og eneste) værdi i tuplen. 
    # >>       # [0] tuple værdien "shiftes" 2 bits til højre med >> operator for at opnå den 10-bit ADC-værdi.
    #
    # De to bytes som bliver send til data
    # udpakkes som en stor-endian 16-bit signed integer
    # og derefter konverteres til en 10-bit signed integer
    # ved at shiftet værdien 2 bits til højre.

u_num = 16.49418502202643
def calculate_voltage(byte_from_adc):
    ##https://www.w3schools.com/python/gloss_python_bitwise_operators.asp
    value = struct.unpack('>h', byte_from_adc)[0] >> 2

    voltage = (value * u_num) / 1023.0
    
    battery_percentage = voltage * 100 - 320
    
    print("ADC Value: {}".format(value))
    print("Voltage: {:.2f} V".format(voltage))
    print("Battery Percentage: {:.2f}%".format(battery_percentage))

    return battery_percentage