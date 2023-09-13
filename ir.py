import RPi.GPIO as GPIO
import time

led = 22

# Set up GPIO pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

def light_automation(irval, ir_status):
    try:
        

        # Check conditions for alerts
        if not ir_status:
            ir_alert = "Lights Off"
        else:
            ir_alert = "Lights On"

        if irval == 0 and not ir_status:
            GPIO.output(led, GPIO.HIGH)
            ir_alert = "Lights On"
            ir_status = True
            
        elif irval == 0 and ir_status:
            GPIO.output(led, GPIO.LOW)
            ir_alert = "Lights Off"
            ir_status = False
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        #GPIO.output(led, GPIO.LOW)

    print("IR:", irval)
    print("Status:", ir_alert)
    return ir_status

