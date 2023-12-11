import paho.mqtt.client as mqtt
import logging
import os

from core.logging_utils import configure_logging
configure_logging()

class MqttClientWrapper:
    def __init__(self, client_id=None, server=None, port=1883, username=None, password=None):
        self.client_id = client_id or f"mqtt-client-{os.environ.get('DEVICE_ID', 'default')}"
        self.server = server or os.environ.get('MQTT_SERVER')
        self.port = port
        self.username = username or os.environ.get('MQTT_USERNAME')
        self.password = password or os.environ.get('MQTT_PASSWORD')
        logging.info(f"Initializing MQTT client with client_id: {self.client_id}")
        self.client = mqtt.Client(client_id=self.client_id)
        self.setup_client()

    def setup_client(self):
        logging.debug(f"Setting up MQTT client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.server, self.port, 60)
        except Exception as e:
            logging.error(f"Error connecting to MQTT server: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Connected to MQTT server with result code {rc}")
        # You can subscribe to topics here if there are any generic subscriptions

    def on_disconnect(self, client, userdata, rc):
        logging.info(f"Disconnected from MQTT server with result code {rc}")

    def on_message(self, client, userdata, message):
        # Default message handler, can be overridden by setting client.on_message to another function
        logging.info(f"Message received: {message.payload} on topic {message.topic}")

    def subscribe(self, topic):
        self.client.subscribe(topic)
        logging.info(f"Subscribed to topic: {topic}")

    def publish(self, topic, payload, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain)

    def loop_forever(self):
        self.client.loop_forever()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
