import requests
from twilio.rest import Client
import RPi.GPIO as GPIO
import time

buzzer = 17
led = 27

# Set up GPIO pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)

def smart_parking(distance, car_parked_alert):
    try:
        phone_numbers = [" "]



        # Initialize Twilio client
        twilio_account_sid = " "
        twilio_auth_token = " "
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        # Check conditions for alerts
        car_parked = "Parked"

        if distance < 200:
            GPIO.output(buzzer, GPIO.HIGH)
            GPIO.output(led, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(buzzer, GPIO.LOW)
            GPIO.output(led, GPIO.LOW)
            car_parked = "Parked"
            # Send SMS notification
            if  not car_parked_alert:
                sms_body = "*** Welcome Home! ***"
                twilio_client.messages.create(
                    to=phone_numbers,  # Replace with your mobile numbers
                    from_="+12184534999",  # Your Twilio phone number
                    body=sms_body
                )
                car_parked_alert = True
                
                
        elif distance == 201 and car_parked_alert:
            GPIO.output(buzzer, GPIO.LOW)
            GPIO.output(led, GPIO.LOW)
            car_parked = "Not Parked"
            # Send SMS notification
            sms_body = "*** Have a Safe Journey! ***"
            twilio_client.messages.create(
                to=phone_numbers,  # Replace with your mobile numbers
                from_=" ",  # Your Twilio phone number
                body=sms_body
            )
            car_parked_alert = False
            
    except KeyboardInterrupt:
        GPIO.cleanup()

    print("Distance:", distance)
    print("Status:", car_parked)
    return car_parked_alert
