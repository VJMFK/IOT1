import paho.mqtt.client as mqtt
import json

id = "88617db2-7ed3-4245-ab3d-a5ef8a0f2a1e"

def handle_telemetry(client, userdata, message):
	payload = json.loads(message.payload.decode())
	print("message recieved: ", payload)
mqtt_client = mqtt.Client(id + "temperature_server")
mqtt_client.connect("test.mosquitto.org")
mqtt_client.subscribe(id + "/telemetry")
mqtt_client.on_message = handle_telemetry
mqtt_client.loop_start()
while True:
	pass


