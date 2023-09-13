import requests
from twilio.rest import Client


def moisture(soilval, soil_alert_sent):
    
        phone_numbers = [" "]

        # Initialize Twilio client
        twilio_account_sid = " "
        twilio_auth_token = " "
        twilio_client = Client(twilio_account_sid, twilio_auth_token)
        
        # Check conditions for alerts
        

        if soilval > 850:
            soil_alert = "Requires Water"
            # Send SMS notification with weather details
            if not soil_alert_sent:
                sms_body = (
                    f"*** Low Moisture Alert! ***\n"
                    f"\tMoisture Below 850.\n\n"
                    f"\tSensor Data:\n"
                    f"\t\tMoisture: {soilval}.\n"  # Corrected format
                    f"\t\tPlease Water your plants."
                )
                twilio_client.messages.create(
                    to=phone_numbers,  # Replace with your mobile number
                    from_=" ",  # Your Twilio phone number
                    body=sms_body
                )
                soil_alert_sent = True
            
        else:
            soil_alert = "No Water Required"
            soil_alert_sent = False
            

        print("Moisture:", soilval)
        print("Status:", soil_alert)
        return soil_alert_sent



