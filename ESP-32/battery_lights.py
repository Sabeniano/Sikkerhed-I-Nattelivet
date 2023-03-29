def led_percentage(ledgreen, ledred, percentage):
    #TODO: Real ifs
    if percentage > 80:
        print("From test1 {}".format(percentage))
        ledred.off()
        ledgreen.off()
    if percentage < 100:
        ledgreen.value(0)
        ledred.value(1) 
        print("From test2 {}".format(percentage))
        