import json
import logging

from core.gpio_handler import GpioHandler
from core.logging_utils import configure_logging
configure_logging()

class GpioDevice:
    def __init__(self, mqtt_client, config):
        self.GPIO = GpioHandler()
        self.mqtt_client = mqtt_client
        self.config = config
        self.setup_gpio()
        self.register_homeassistant()
      
    def setup_gpio(self):
        raise NotImplementedError

    def on_message(self, topic, payload):
        raise NotImplementedError

    def subscribe_to_command_topic(self):
        # Return the command topic from the config
        command_topic = self.config['ha_discovery_payload']['command_topic']
        self.mqtt_client.subscribe(command_topic)        
        logging.debug(f"Subscribed to command topic: {command_topic}")
    
    def register_homeassistant(self):
        discovery_topic = self.config["ha_discovery_topic"]
        discovery_payload = json.dumps(self.config["ha_discovery_payload"])
        self.mqtt_client.publish(discovery_topic, discovery_payload, retain=True)
        logging.debug(f"Registered {self.config['ha_discovery_topic']} to Home Assistant")
    
    def publish_state(self):
        raise NotImplementedError
    
    def cleanup(self):
        self.GPIO.cleanup()