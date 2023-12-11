import json
import logging
import os
from config.switch_sensor import SwitchSensor
from core.logging_utils import configure_logging

configure_logging()

class DeviceManager:
    def __init__(self, mqtt_client, config_path="./config/_topics.json"):
        self.mqtt_client = mqtt_client
        self.configs = []
        self.switch_sensors = []
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

        self.initialize_switch_sensors()

    def _replace_placeholders(self, config):
        device_id = os.environ.get('DEVICE_ID','na')
        platform = os.environ.get('PLATFORM','na')
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self._replace_placeholders(value)
        elif isinstance(config, list):
            config = [self._replace_placeholders(item) for item in config]
        elif isinstance(config, str):
            config = config.replace('{device_id}', device_id)
            config = config.replace('{platform}', platform)
        return config

    def initialize_switch_sensors(self):
        for config in self.configs:
            updated_config = self._replace_placeholders(config)
            switch_sensor = SwitchSensor(self.mqtt_client, updated_config)
            self.switch_sensors.append(switch_sensor)

    def on_message(self, topic, payload):
        for sensor in self.switch_sensors:
            sensor.on_message(topic, payload)

    def publish_states(self):
        for sensor in self.switch_sensors:
            sensor.publish_state()

    def cleanup(self):
        for sensor in self.switch_sensors:
            sensor.cleanup()  # Assuming each sensor has a cleanup method