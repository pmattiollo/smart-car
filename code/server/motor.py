import time
from pca9685 import PCA9685


def duty_range(duty1, duty2, duty3, duty4):
    clamp = lambda value: max(-4095, min(value, 4095))
    return clamp(duty1), clamp(duty2), clamp(duty3), clamp(duty4)


class Motor:
    def init(self):
        if self.initialized == True:
            return
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.set_pwm_freq(50)
        self.initialized = True

    def left_upper_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(0, 0)
            self.pwm.set_motor_pwm(1, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(1, 0)
            self.pwm.set_motor_pwm(0, abs(duty))
        else:
            self.pwm.set_motor_pwm(0, 4095)
            self.pwm.set_motor_pwm(1, 4095)

    def left_lower_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(3, 0)
            self.pwm.set_motor_pwm(2, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(2, 0)
            self.pwm.set_motor_pwm(3, abs(duty))
        else:
            self.pwm.set_motor_pwm(2, 4095)
            self.pwm.set_motor_pwm(3, 4095)

    def right_upper_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(6, 0)
            self.pwm.set_motor_pwm(7, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(7, 0)
            self.pwm.set_motor_pwm(6, abs(duty))
        else:
            self.pwm.set_motor_pwm(6, 4095)
            self.pwm.set_motor_pwm(7, 4095)

    def right_lower_wheel(self, duty):
        if duty > 0:
            self.pwm.set_motor_pwm(4, 0)
            self.pwm.set_motor_pwm(5, duty)
        elif duty < 0:
            self.pwm.set_motor_pwm(5, 0)
            self.pwm.set_motor_pwm(4, abs(duty))
        else:
            self.pwm.set_motor_pwm(4, 4095)
            self.pwm.set_motor_pwm(5, 4095)

    def set_speed(self, duty1, duty2, duty3, duty4):
        self.init()
        duty1, duty2, duty3, duty4 = duty_range(duty1, duty2, duty3, duty4)
        self.left_upper_wheel(-duty1)
        self.left_lower_wheel(-duty2)
        self.right_upper_wheel(-duty3)
        self.right_lower_wheel(-duty4)

    def loop(self):
        self.set_speed(2000, 2000, 2000, 2000)  # Forward
        time.sleep(3)
        self.set_speed(-2000, -2000, -2000, -2000)  # Back
        time.sleep(3)
        self.set_speed(-500, -500, 2000, 2000)  # Left
        time.sleep(3)
        self.set_speed(2000, 2000, -500, -500)  # Right
        time.sleep(3)
        self.set_speed(0, 0, 0, 0)  # Stop

    def destroy(self):
        self.set_speed(0, 0, 0, 0)


def main():
    motor = Motor()
    try:
        motor.loop()
    except KeyboardInterrupt:
        motor.destroy()


if __name__ == '__main__':
    main()
