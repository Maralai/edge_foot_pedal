import os

class GpioHandler:
    def __init__(self):
        platform = os.getenv('PLATFORM').lower()
        
        if platform == 'jetson':
            import Jetson.GPIO as GPIO
        elif platform == 'rpi':
            import RPi.GPIO as GPIO
        else:
            raise Exception(f"Unknown platform: {platform}")
        
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BOARD)

        # Add commonly used constants for easier access
        self.HIGH = self.GPIO.HIGH
        self.LOW = self.GPIO.LOW
        self.IN = self.GPIO.IN
        self.OUT = self.GPIO.OUT

    def setup(self, pin, mode):
        self.GPIO.setup(pin, mode)

    def output(self, pin, state):
        self.GPIO.output(pin, state)

    def input(self, pin):
        return self.GPIO.input(pin)
    
    def add_event_detect(self, pin, edge, callback, bouncetime):
        return self.GPIO.add_event_detect(pin, edge, callback=callback, bouncetime=bouncetime)

    def cleanup(self):
        self.GPIO.cleanup()
