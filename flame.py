import serial
import requests
from twilio.rest import Client
import RPi.GPIO as GPIO
import time

buzzer = 17

GPIO.setmode(GPIO.BCM)

# Set up GPIO pins as outputs

GPIO.setup(buzzer,GPIO.OUT)


def flame_api(flameval,flame_alert_sent):
        
        try:
            phone_numbers = [""]



            # Initialize Twilio client
            twilio_account_sid = " "
            twilio_auth_token = " "
            twilio_client = Client(twilio_account_sid, twilio_auth_token)

            

            # Check conditions for alerts
            flame_alert = "Normal"
            
            if flameval == 0:
                if not flame_alert_sent:
                    flame_alert = "High Flame Alert"
                    # Send SMS notification with weather details
                    sms_body = (
                        f"*** High Flame Alert! ***\n"
                        f"\tFlame Detected \n"  # Corrected format
                        f"\t\tPlease check imediately"
                    )
                    twilio_client.messages.create(
                        to=phone_numbers,  # Replace with your mobile number
                        from_=" ",  # Your Twilio phone number
                        body=sms_body
                    )
                    flame_alert_sent = True
                    GPIO.output(buzzer, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(buzzer, GPIO.LOW)
            
            
            else:
                flame_alert = "Normal"
                flame_alert_sent = False
            
        except KeyboardInterrupt:
            # Clean up GPIO configuration on program exit
            GPIO.output(buzzer, GPIO.LOW)
            GPIO.cleanup()    
        
        print("Flame Level:", flameval)
        print("Flame Status:", flame_alert)
        return flame_alert_sent


