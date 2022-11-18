from pca9685 import PCA9685


class Servo:
    def init(self):
        if self.initialized == True:
            return
        self.PwmServo = PCA9685(0x40, debug=True)
        self.PwmServo.set_pwm_freq(50)
        self.PwmServo.set_servo_pulse(8, 1500)
        self.PwmServo.set_servo_pulse(9, 1500)
        self.initialized = True

    def set_servo_pwm(self, channel, angle, error=10):
        angle = int(angle)
        if channel == '0':
            self.PwmServo.set_servo_pulse(8, 2500 - int((angle + error) / 0.09))
        elif channel == '1':
            self.PwmServo.set_servo_pulse(9, 500 + int((angle + error) / 0.09))
        elif channel == '2':
            self.PwmServo.set_servo_pulse(10, 500 + int((angle + error) / 0.09))
        elif channel == '3':
            self.PwmServo.set_servo_pulse(11, 500 + int((angle + error) / 0.09))
        elif channel == '4':
            self.PwmServo.set_servo_pulse(12, 500 + int((angle + error) / 0.09))
        elif channel == '5':
            self.PwmServo.set_servo_pulse(13, 500 + int((angle + error) / 0.09))
        elif channel == '6':
            self.PwmServo.set_servo_pulse(14, 500 + int((angle + error) / 0.09))
        elif channel == '7':
            self.PwmServo.set_servo_pulse(15, 500 + int((angle + error) / 0.09))


def main():
    print("Now servos will rotate to 90°.")
    print("If they have already been at 90°, nothing will be observed.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    pwm = Servo()
    while True:
        try:
            pwm.set_servo_pwm('0', 90)
            pwm.set_servo_pwm('1', 90)
        except KeyboardInterrupt:
            print("\nEnd of program")
            break


if __name__ == '__main__':
    main()
