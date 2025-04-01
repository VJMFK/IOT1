import paho.mqtt.client as mqtt
import json
import time

id = "88617db2-7ed3-4245-ab3d-a5ef8a0f2a1e"
#adding part4
server_command_topic = id +"/commands"

def handle_telemetry(client, userdata, message):
	try:
		payload = json.loads(message.payload.decode())
		command = {"led_on":payload["temperature"] > 25}
		print("sending message: ", command)
		mqtt_client.publish(server_command_topic, json.dumps(command))
		print("message recieved: ", payload)
	except json.JSONDecodeError:
		print("error decoding telemetry.")
#connect to broker
mqtt_client = mqtt.Client(id + "_temperature_server")
mqtt_client.connect("test.mosquitto.org")
#handle subscribing
mqtt_client.on_message = handle_telemetry
mqtt_client.loop_start()
mqtt_client.subscribe(id + "/telemetry")


try:
	while True:
		time.sleep(2)
except KeyboardInterrupt:
	print("stop server")
	mqtt_client.loop_stop()
	mqtt_client.disconnect()

