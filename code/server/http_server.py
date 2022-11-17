from logging.config import dictConfig
import time
from flask import Flask, request

from buzzer import Buzzer
from adc import ADC
from ultrasonic import Ultrasonic
from motor import Motor
from servo import Servo

app = Flask(__name__)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s : %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})
def current_milli_time():
    return round(time.time() * 1000)

SENSOR_GET_THREASHOLD_MS = 50
last_sensor = None

motor = Motor()
servo = Servo()
ultrasonic = Ultrasonic()
buzzer = Buzzer()
adc = ADC()
# led = Led()

@app.route("/buzzer", methods=["POST"])
def buzzer():
    global buzzer
    value = request.get_json().get('value')
    if value == None:
        return ('value can not be null', 400)
    app.logger.debug(f'Buzzer request received with value [{value}]')
    buzzer.run(value)
    return ('', 204)


@app.route("/motor", methods=["POST"])
def motor():
    global motor
    req = request.get_json()
    motor_values = {'front_left': req.get('front_left'), 'rear_left': req.get('rear_left'),
                    'front_right': req.get('front_right'), 'rear_right': req.get('rear_right')}
    if motor_values['front_left'] == None:
        return ('front_left can not be null', 400)
    if motor_values['rear_left'] == None:
        return ('rear_left can not be null', 400)
    if motor_values['front_right'] == None:
        return ('front_right can not be null', 400)
    if motor_values['rear_right'] == None:
        return ('rear_right can not be null', 400)
    app.logger.debug(f'Motor request received with value [{motor_values}]')
    motor.set_speed(motor['front_left'], motor['rear_left'],
                    motor['front_right'], motor['rear_right'])
    return ('', 204)


@app.route("/servo", methods=["POST"])
def servo():
    global servo
    req = request.get_json()
    channel = req.get('channel')
    angle = req.get('angle')
    if channel == None:
        return ('channel can not be null', 400)
    if angle == None:
        return ('angle can not be null', 400)
    try:
        int(angle)
        return ('angle should be integer', 400)
    except ValueError:
        pass
    app.logger.debug(
        f'Servo request received with channel [{channel}] and angle [{angle}]')
    servo.set_servo_pwm(channel, angle)
    return ('', 204)


@app.route("/sensors", methods=["GET"])
def sensors():
    global ultrasonic
    global adc
    global last_sensor
    if last_sensor != None and last_sensor[0] > (current_milli_time() - SENSOR_GET_THREASHOLD_MS):
        return last_sensor[1]
    app.logger.debug('Request for reading sensor data')
    ultrasonic_value = ultrasonic.get_distance()
    light1 = adc.recv(0)
    light2 = adc.recv(1)
    power = adc.recv(2) * 3
    sensor_date = {
        'ultrasonic': ultrasonic_value,
        'light1': light1,
        'light2': light2,
        'power': power
    }
    last_sensor = (current_milli_time(), sensor_date)
    return sensor_date
