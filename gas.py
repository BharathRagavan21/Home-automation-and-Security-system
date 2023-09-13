import serial
import requests
from twilio.rest import Client
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
buzzer = 17
motor_enable_pin = 18  # Connect to the ENA pin on the L298N
motor_input1 = 23      # Connect to the IN1 pin on the L298N
motor_input2 = 24      # Connect to the IN2 pin on the L298N

# Set up GPIO pins as outputs
GPIO.setup(motor_enable_pin, GPIO.OUT)
GPIO.setup(motor_input1, GPIO.OUT)
GPIO.setup(motor_input2, GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

motor_pwm = GPIO.PWM(motor_enable_pin, 100)

def gas_api(gasval,gas_alert_sent):
        
        try:
            phone_numbers = [" "]



            # Initialize Twilio client
            twilio_account_sid = ""
            twilio_auth_token = " "
            twilio_client = Client(twilio_account_sid, twilio_auth_token)

            

            # Check conditions for alerts
            gas_alert = "Normal"
            
            if gasval > 420:
                GPIO.output(motor_input1, GPIO.HIGH)
                GPIO.output(motor_input2, GPIO.LOW)
                motor_pwm.start(50)
                if not gas_alert_sent:
                    gas_alert = "High Gas Leakage Alert"
                    # Send SMS notification with weather details
                    sms_body = (
                        f"*** High Gas Leakage Alert! ***\n"
                        f"\tGas Level is above 400.\n\n"
                        f"\tSensor Data:\n"
                        f"\t\tGas Level: {gasval}.\n"  # Corrected format
                        f"\t\tPlease check imediately"
                    )
                    twilio_client.messages.create(
                        to=phone_numbers,  # Replace with your mobile number
                        from_=" ",  # Your Twilio phone number
                        body=sms_body
                    )
                    gas_alert_sent = True
                    GPIO.output(buzzer, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(buzzer, GPIO.LOW)
            
            
            else:
                GPIO.output(motor_input1, GPIO.LOW)
                GPIO.output(motor_input2, GPIO.LOW)
                motor_pwm.stop()
                gas_alert_sent = False
            
        except KeyboardInterrupt:
            # Clean up GPIO configuration on program exit
            GPIO.output(motor_input1, GPIO.LOW)
            GPIO.output(motor_input2, GPIO.LOW)
            motor_pwm.stop()
            GPIO.output(buzzer, GPIO.LOW)
            GPIO.cleanup()    
        
        print("Gas Level:", gasval)
        return gas_alert_sent