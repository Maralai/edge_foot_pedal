import time
import json
import logging

from core.gpio_device import GpioDevice
from core.logging_utils import configure_logging

configure_logging()

class SwitchSensor(GpioDevice):
    def __init__(self, mqtt_client, switch_config):
        logging.info(f"Initializing Switch")
        self.state = None

        # Setup GPIO
        self.pin = switch_config["switch_logic_pin"]

        super().__init__(mqtt_client, switch_config)        
        self.publish_state()

    def setup_gpio(self):
        """Setup the GPIO pin for the switch sensor."""
        try:
            self.GPIO.setup(self.pin, self.GPIO.IN)
            self.GPIO.add_event_detect(self.pin, self.GPIO.BOTH, callback=self.switch_handler, bouncetime=300)
            self.state = self.GPIO.input(self.pin)
            logging.info(f"GPIO pin {self.pin} setup successfully, initial state: {self.state}")
        except RuntimeError:
            logging.warning(f"GPIO pin {self.pin} already registered, removing event detection and re-registering")
            self.GPIO.remove_event_detect(self.pin)
            self.GPIO.add_event_detect(self.pin, self.GPIO.BOTH, callback=self.switch_handler, bouncetime=300)
        except Exception as e:
            logging.error(f"Error setting up GPIO pin {self.pin}: {e}", exc_info=True)

    def switch_handler(self, channel):
        """Handle switch state changes."""
        time.sleep(.02)
        position_changed = self.GPIO.input(channel)
        if position_changed != self.state:
            self.state = position_changed
            self.publish_state()

    def publish_state(self):
        """Publish the current state of the switch sensor to the MQTT topic."""
        message = "WAITING" if self.state == 1 else "PRESSED"
        state_topic = self.config['ha_discovery_payload']['state_topic']
        self.mqtt_client.publish(state_topic, message, retain=True)
        logging.info(f"Published state {message} to {state_topic}")