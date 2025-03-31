import paho.mqtt.client as mqtt
#import gpiozero as gpio
from gpiozero.pins.factory import RPiGPIOFactory
from gpiozero import LED
import json
import time
import glob
#import os

id = "88617db2-7ed3-4245-ab3b-a5ef8a0f2a1e"
client_name = id +"_temperature_client"
client_telemetry_topic = id + "/telemetry"

#set up mqtt
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect("test.mosquitto.org")
mqtt_client.loop_start()
print("MQTT connected")

#set up hardware
factory = RPiGPIOFactory()
red = LED(17, pin_factory = factory)
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

#main loop
try:
	while True:
		temperature = read_temp()

		if temperature is not None:
			telemetry = json.dumps({"temperature" : temperature})
			print("sending telemetry:", telemetry)
			mqtt_client.publish(client_telemetry_topic, telemetry)
			#led on/off
			if temperature > 25:
				red.on()
			else:
				red.off()
		time.sleep(3)
except KeyboardInterrupt:
	print("exiting")
finally:
	red.off()


#read, publish and control

