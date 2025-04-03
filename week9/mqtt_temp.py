import paho.mqtt.client as mqtt
import gpiozero as gpio
from gpiozero import LED
import json
import time
import glob
#import os

id = "88617db2-7ed3-4245-ab3b-a5ef8a0f2a1e"
client_name = id +"_temperature_client"
client_telemetry_topic = id + "/telemetry"
client_command_topic = id + "/commands" #part4

#set up mqtt
mqtt_client = mqtt.Client(client_name)
#mqtt_client.connect("test.mosquitto.org")
#mqtt_client.loop_start()
print("MQTT connected")

#set up hardware
#factory = RPiGPIOFactory()
red =gpio.LED(17)
red.off()

#still part2 reading temperature
def read_temp():
	try:
		base_dir = "/sys/bus/w1/devices/"
		device_folder = glob.glob(base_dir + "28*")
		if not device_folder:
			raise FileNotFoundError("no db18b20 sensor found")
		device_file = device_folder[0] + "/w1_slave" 
		with open(device_file, "r") as f:
			lines = f.readlines()
		if "YES" in lines[0]:
			#extract value
			temp_string = lines[1].split("t=")[-1]
			temp_c = float(temp_string) / 1000.0
			return round(temp_c, 2)
		else:
			return None
	except Exception as e:
		print(f"error reading temperature:{e}")
		return None
		
		
#handle incoming commands
def handle_command(client, userdata, message):
	try:
		payload = json.loads(message.payload.decode())
		print(f"Received command payload: {payload}")  # Debugging output

		# Ensure led_on is correctly processed
		if not payload.get("led_on", False):  
			red.on()
			print("LED OFF ") #circuit is inverted? weird
		else:
			red.off()
			print("LED ON ")
	except json.JSONDecodeError:
		print("Error decoding command message")
        
        
#subscribe
mqtt_client.connect("test.mosquitto.org")
mqtt_client.subscribe(client_command_topic)
mqtt_client.on_message = handle_command

mqtt_client.loop_start()


#main loop
try:
	while True:
		temperature = read_temp()

		if temperature is not None:
			telemetry = json.dumps({"temperature" : temperature})
			print(f"sending telemetry:", telemetry)
			mqtt_client.publish(client_telemetry_topic, telemetry)

		time.sleep(3)
except KeyboardInterrupt:
	print("exiting")
finally:
	mqtt_client.loop_stop()
	mqtt_client.disconnect()
	red.off()
	print("cleaning up")



