import logging
from device_manager import DeviceManager
from core.mqtt_client import MqttClientWrapper
from core.logging_utils import configure_logging

configure_logging()

class Worker:
    def __init__(self):
        self.mqtt = MqttClientWrapper()
        self.device_manager = DeviceManager(self.mqtt.client)
        self.setup_mqtt_callbacks()

    def setup_mqtt_callbacks(self):
        self.mqtt.client.on_message = self.on_message        
        self.mqtt.client.subscribe("homeassistant/status")
        # Override other MQTT callbacks here

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            topic = message.topic
            if topic == "homeassistant/status" and payload == "online":
                # Home Assistant has restarted, re-publish sensor states here
                logging.info(f"Home Assistant is online. Republishing device states.")
                self.device_manager.publish_states()
            else:
                # Forward the message to all devices
                self.device_manager.on_message(topic, payload)
        except Exception as e:
            logging.error(f"Error in on_message: {e}", exc_info=True)

    def run(self):
        try:
            self.mqtt.loop_forever()
        except KeyboardInterrupt:
            logging.info("Exiting gracefully")
        finally:
            self.device_manager.cleanup()
            self.mqtt.loop_stop()
            self.mqtt.disconnect()

if __name__ == "__main__":
    worker = Worker()
    worker.run()
