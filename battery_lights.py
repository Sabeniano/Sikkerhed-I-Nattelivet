def led_percentage(ledgreen, ledred, percentage):
    if percentage > 21:
        ledred.off()
        ledgreen.on()
    if percentage < 20:
        ledred.on()
        ledgreen.off()
        