import RPi.GPIO as GPIO

class Infrared:
    def __init__(self):
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def get_value(self):
        lmr = 0x00
        if GPIO.input(self.IR01):
            lmr = (lmr | 4)
        if GPIO.input(self.IR02):
            lmr = (lmr | 2)
        if GPIO.input(self.IR03):
            lmr = (lmr | 1)

        return lmr