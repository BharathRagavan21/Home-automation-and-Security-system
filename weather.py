import serial
import requests
from twilio.rest import Client


def weather_api(temperature,humidity,temperature_alert_sent,humidity_alert_sent):
        
        phone_numbers = [" "]

        # Initialize Twilio client
        twilio_account_sid = " "
        twilio_auth_token = " "
        twilio_client = Client(twilio_account_sid, twilio_auth_token)
    
        # Get live weather data from OpenWeatherMap API
        weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={OPENWEATHERMAP_CITY}&appid={OPENWEATHERMAP_API_KEY}")
        weather_data = weather_response.json()
        current_weather = weather_data["weather"][0]["description"]
        temperature_celsius = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius

        # Check conditions for alerts
        temperature_alert = "Normal"
        humidity_alert = "Normal"
        
        if float(temperature) > 26:
            if not temperature_alert_sent:
                temperature_alert = "High Temperature Alert"
                # Send SMS notification with weather details
                sms_body = (
                    f"*** High Temperature Alert! ***\n"
                    f"\tTemperature is above 26°C.\n\n"
                    f"\tSensor Data:\n"
                    f"\t\tTemperature: {float(temperature):.2f} °C.\n"  # Corrected format
                    f"\t\tHumidity: {humidity} .\n\n"
                    f"\tNote Current Details:\n"
                    f"\t\tTemperature: {temperature_celsius:.2f} °C.\n"
                    f"\t\tWeather: {current_weather}."
                )
                twilio_client.messages.create(
                    to=phone_numbers,  # Replace with your mobile number
                    from_=" ",  # Your Twilio phone number
                    body=sms_body
                )
                temperature_alert_sent = True
        
        else:
            temperature_alert_sent = False
            
        if float(humidity) > 50:
            if not humidity_alert_sent:
                humidity_alert = "High Humidity Alert"
                # Send SMS notification with weather details
                sms_body = (
                    f"*** High Humidity Alert! ***\n"
                    f"\tHumidity is above 50.\n\n"
                    f"\tSensor Data:\n"
                    f"\t\tTemperature: {float(temperature):.2f} °C.\n"
                    f"\t\tHumidity: {humidity}.\n\n"  # Corrected format
                    f"\tNote Current Details:\n"
                    f"\t\tTemperature: {temperature_celsius:.2f} °C.\n"
                    f"\t\tWeather: {current_weather}."
                )
                twilio_client.messages.create(
                    to=phone_numbers,  # Replace with your mobile number
                    from_=" ",  # Your Twilio phone number
                    body=sms_body
                )
                humidity_alert_sent = True
        else:
            humidity_alert_sent = False

        print("Humidity:", humidity, "%")
        print("Temperature:", temperature, "°C")
        print("Current Weather:", current_weather)
        print("Temperature Celsius:", temperature_celsius, "°C")
        print("Temperature Alert:", temperature_alert)
        print("Humidity Alert:", humidity_alert)
        return temperature_alert_sent,humidity_alert_sent