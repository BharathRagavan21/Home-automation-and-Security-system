import RPi.GPIO as GPIO
import time

led = 16

# Set up GPIO pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

def ldr_automation(ldrval, ldr_status):
    try:
        

        # Check conditions for alerts
        if not ldr_status:
            ldr_alert = "Lights Off"
        else:
            ldr_alert = "Lights On"

        if ldrval > 150 and not ldr_status:
            GPIO.output(led, GPIO.HIGH)
            ldr_alert = "Lights On"
            ldr_status = True
            
        elif ldrval < 150 and ldr_status:
            GPIO.output(led, GPIO.LOW)
            ldr_alert = "Lights Off"
            ldr_status = False
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        #GPIO.output(led, GPIO.LOW)

    print("IDR:", ldrval)
    print("Status:", ldr_alert)
    return ldr_status


