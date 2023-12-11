import json
import threading
import time
import os
import logging

from core.gpio_device import GpioDevice
from core.logging_utils import configure_logging
configure_logging()

class TemperatureSensor(GpioDevice):
    def __init__(self, mqtt_client, config):
        super().__init__(mqtt_client, config)

    def setup_gpio(self):
        return True
    
    def on_message(self, topic, payload):
        return True
    
    def cleantup(self):
        return True