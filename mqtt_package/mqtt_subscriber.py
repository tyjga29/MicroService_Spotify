import paho.mqtt.client as mqtt
import json
import yaml
import os

from spotify_package.spotify_controller import use_events_for_music, spotify_choose_uri

dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(dir_path, 'mqtt_resources.yaml')
with open(yaml_path, 'r') as f:
    data = yaml.safe_load(f)
    mqtt_data = data["mqtt_resources"]

broker_address = mqtt_data["BROKER_ADDRESS"]
topics = [mqtt_data["TOPIC_CALENDAR"], mqtt_data["TOPIC_DIRECT"]]
broker_port = mqtt_data["BROKER_PORT"]

class MQTTSubscriber:
    def __init__(self):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.username_pw_set("pda_user", "pda_password")
        self.events = []

        # Set up the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in topics:
                client.subscribe(topic)
        else:
            print("Connection failed with code", rc)

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic '{message.topic}': {payload}")
            
        try:
            
            

            if (message.topic == topics[0]):
                message_data = json.loads(payload)
                received_events = message_data.get("events", [])
                print(received_events)
                use_events_for_music(received_events)
            elif (message.topic == topics[1]):
                received_event = payload
                print(received_event)
                spotify_choose_uri(received_event)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def subscribe(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
