import json
import time
import paho.mqtt.client as mqtt

id = "88617db2-7ed3-4245-ab3b-a5ef8a0f2a1e"
server_command_topic = id + "/commands"

def handle_telemetry(client, userdata, message):
	try:
		payload = json.loads(message.payload.decode())
		temperature = payload.get("temperature")

		if temperature is not None:
			print(f"Received temperature: {temperature} C")

			# LED should be ON if temperature > 25
			led_status = temperature > 25
			command = {"led_on": led_status}

			print(f"Sending command: {command}")

			result = mqtt_client.publish(server_command_topic, json.dumps(command))

			# Confirm successful publishing
			if result.rc == mqtt.MQTT_ERR_SUCCESS:
				print(f"Command sent successfully: {command}")
			else:
				print(f"Failed to publish command. MQTT error code: {result.rc}")

	except json.JSONDecodeError:
		print("Error decoding telemetry message.")

# Set up MQTT connection
mqtt_client = mqtt.Client(id + "_temperature_server")
mqtt_client.connect("test.mosquitto.org")

# Subscribe and listen for temperature telemetry
mqtt_client.on_message = handle_telemetry
mqtt_client.subscribe(id + "/telemetry")
mqtt_client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    print("?? Stopping server")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
