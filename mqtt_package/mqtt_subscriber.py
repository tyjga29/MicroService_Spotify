import paho.mqtt.client as mqtt
import json
import yaml
import os

from spotify_package.spotify_controller import use_events_for_music

dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
with open(yaml_path, 'r') as f:
    data = yaml.safe_load(f)
    mqtt_data = data["mqtt_resources"]

broker_address = mqtt_data["BROKER_ADDRESS"]
broker_port = mqtt_data["BROKER_PORT"]
topic = mqtt_data["TOPIC"]

class MQTTSubscriber:
    def __init__(self):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.events = []

        # Set up the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(self.topic)
        else:
            print("Connection failed with code", rc)

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic '{message.topic}': {payload}")

        try:
            message_data = json.loads(payload)
            received_events = message_data.get("events", [])
            print(received_events)
            use_events_for_music(received_events)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def subscribe(self):
        self.topic = topic
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
