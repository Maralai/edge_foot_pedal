import json
import logging
import os

from config.humidity import HumiditySensor
from config.temperature import TemperatureSensor
from core.logging_utils import configure_logging

configure_logging()

class DeviceManager:
    def __init__(self, mqtt_client, config_path="./config/mqtt_topics.json"):
        self.mqtt_client = mqtt_client
        self.configs = []
        self.devices = []
        self.config_path = config_path
        self.load_configurations()

    def load_configurations(self):
        try:
            with open(self.config_path, "r") as jsonfile:
                self.configs = json.load(jsonfile)
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_path} not found.")
            self.configs = []
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {self.config_path}.")
            self.configs = []
        except Exception as e:
            logging.error(f"Unexpected error loading configurations: {e}")
            self.configs = []

        self.initialize_devices()

    def initialize_devices(self):
        for config_group in self.configs:
            for config in config_group['entities']:
                if config['type'] == 'temperature_sensor':
                    self._init_temperature_sensor(config)
                elif config['type'] == 'humidity_sensor':
                    self._init_humidity_sensor(config)

    def _init_temperature_sensor(self, config):
        temp_sensor_config = self._replace_placeholders(config)
        temp_sensor = TemperatureSensor(self.mqtt_client, temp_sensor_config)
        self.devices.append(temp_sensor)

    def _init_humidity_sensor(self, config):
        humidity_sensor_config = self._replace_placeholders(config)
        humidity_sensor = HumiditySensor(self.mqtt_client, humidity_sensor_config)
        self.devices.append(humidity_sensor)

    def _replace_placeholders(self, config, color=None):
        # Replace placeholders in the config
        device_id = os.environ.get('DEVICE_ID', 'na')
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self._replace_placeholders(value)
        elif isinstance(config, list):
            config = [self._replace_placeholders(item) for item in config]
        elif isinstance(config, str):
            config = config.replace('{device_id}', device_id)
        return config

    def on_message(self, topic, payload):
        for device in self.devices:
            device.on_message(topic, payload)

    def publish_states(self):
        for device in self.devices:
            device.publish_state()

    def cleanup(self):
        for device in self.devices:
            device.cleanup()  # Assuming each device has a cleanup method
