import struct

#findes ved at tage en måling på sit batteri, kaldet U
#U*1023/adc_val = u_num
u_num = 15.86271255060729
def calculate_voltage(byte_from_adc):
    value = struct.unpack('>h', byte_from_adc)[0] >> 2

    voltage = (value * u_num) / 1023.0
    
    battery_percentage = voltage * 100 - 320
    
    print("ADC Value: {}".format(value))
    print("Voltage: {:.2f} V".format(voltage))
    print("Battery Percentage: {:.2f}%".format(battery_percentage))
    return battery_percentage
