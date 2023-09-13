import serial
import requests
import weather as wa
import gas as ga
import parking as car
import flame as fa
import ir_module as ir
import ldr_module as ldr
import soil as mo
import RPi.GPIO as GPIO
import time 
# Set the serial port and baud rate (adjust as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600)

# ThingSpeak API key
THINGSPEAK_API_KEY = " "

# ThingSpeak update URL
THINGSPEAK_UPDATE_URL = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"

# Read and upload sensor data
def main():
    temperature_alert_sent = False
    humidity_alert_sent = False
    gas_alert_sent = False
    car_parked_alert = True
    flame_alert_sent = False
    ir_status = False
    ldr_status = False
    soil_alert_sent = False
    try:
        while True:
            line = ser.readline().decode().strip()
            if line.startswith("Humidity:"):
                humidity = float(line.split(":")[1])
                temperature = float(ser.readline().decode().strip().split(":")[1])
                
                gas_value = int(ser.readline().decode().strip().split(":")[1])
                ir_value = int(ser.readline().decode().strip().split(":")[1])
                fire_value = int(ser.readline().decode().strip().split(":")[1])
                ldr_value = int(ser.readline().decode().strip().split(":")[1])
                soil_moisture = int(ser.readline().decode().strip().split(":")[1])
                ultrasonic_distance = float(ser.readline().decode().strip().split(":")[1])
                if ultrasonic_distance > 200:
                    ultrasonic_distance = 201
                
                
                temperature_alert_sent,humidity_alert_sent = wa.weather_api(temperature,humidity,temperature_alert_sent,humidity_alert_sent)
                gas_alert_sent = ga.gas_api(gas_value,gas_alert_sent)
                car_parked_alert = car.smart_parking(ultrasonic_distance,car_parked_alert)
                flame_alert_sent = fa.flame_api(fire_value,flame_alert_sent)
                ir_status = ir.light_automation(ir_value, ir_status)
                ldr_status = ldr.ldr_automation(ldr_value, ldr_status)
                soil_alert_sent = mo.moisture(soil_moisture, soil_alert_sent)
                
                print("\n\n")
                time.sleep(10)                
                payload = {
                    "field1": humidity,
                    "field2": temperature,
                    "field3": gas_value,
                    "field4": ir_value,
                    "field5": fire_value,
                    "field6": ldr_value,
                    "field7": soil_moisture,
                    "field8": ultrasonic_distance
                }
                
                response = requests.get(THINGSPEAK_UPDATE_URL, params=payload)
                
                if response.status_code == 200:
                    print("Data uploaded to ThingSpeak")
                else:
                    print("Error uploading data to ThingSpeak")
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()


