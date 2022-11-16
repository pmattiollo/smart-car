#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
from threading import Thread

from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from client_ui import Ui_Client
from mode import MODE
from command import COMMAND, COMMAND_SEPARATOR, COMMAND_TERMINATOR
from thread_utils import *
from video import *
from control import Control

CMD_LED_OFF = COMMAND_SEPARATOR + str(0) + COMMAND_SEPARATOR + str(0) + COMMAND_SEPARATOR + str(
    0) + COMMAND_TERMINATOR


class ClientWindow(QMainWindow, Ui_Client):
    def __init__(self):
        self.led_index = None
        self.streaming_thread = None
        self.receive_thread = None
        super(ClientWindow, self).__init__()
        self.setupUi(self)
        self.target_host = self.IP.text()
        self.video_streaming = None
        self.control = None
        self.servo1 = 90
        self.servo2 = 90
        self.label_FineServo2.setText("0")
        self.label_FineServo1.setText("0")
        self.setMouseTracking(True)
        self.Key_W = False
        self.Key_A = False
        self.Key_S = False
        self.Key_D = False
        self.Key_Space = False
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.progress_Power.setMinimum(0)
        self.progress_Power.setMaximum(100)
        self.label_Servo1.setText('90')
        self.label_Servo2.setText('90')
        self.label_Video.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Servo1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Servo2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.label_FineServo1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_FineServo2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.HSlider_Servo1.setMinimum(0)
        self.HSlider_Servo1.setMaximum(180)
        self.HSlider_Servo1.setSingleStep(1)
        self.HSlider_Servo1.setValue(self.servo1)
        self.HSlider_Servo1.valueChanged.connect(self.change_left_right)

        self.HSlider_FineServo1.setMinimum(-10)
        self.HSlider_FineServo1.setMaximum(10)
        self.HSlider_FineServo1.setSingleStep(1)
        self.HSlider_FineServo1.setValue(0)
        self.HSlider_FineServo1.valueChanged.connect(self.fine_tune_left_right)

        self.HSlider_FineServo2.setMinimum(-10)
        self.HSlider_FineServo2.setMaximum(10)
        self.HSlider_FineServo2.setSingleStep(1)
        self.HSlider_FineServo2.setValue(0)
        self.HSlider_FineServo2.valueChanged.connect(self.fine_tune_up_down)

        self.VSlider_Servo2.setMinimum(80)
        self.VSlider_Servo2.setMaximum(180)
        self.VSlider_Servo2.setSingleStep(1)
        self.VSlider_Servo2.setValue(self.servo2)
        self.VSlider_Servo2.valueChanged.connect(self.change_up_down)

        self.checkBox_Led1.setChecked(False)
        self.checkBox_Led1.stateChanged.connect(lambda: self.led_change(self.checkBox_Led1))
        self.checkBox_Led2.setChecked(False)
        self.checkBox_Led2.stateChanged.connect(lambda: self.led_change(self.checkBox_Led2))
        self.checkBox_Led3.setChecked(False)
        self.checkBox_Led3.stateChanged.connect(lambda: self.led_change(self.checkBox_Led3))
        self.checkBox_Led4.setChecked(False)
        self.checkBox_Led4.stateChanged.connect(lambda: self.led_change(self.checkBox_Led4))
        self.checkBox_Led5.setChecked(False)
        self.checkBox_Led5.stateChanged.connect(lambda: self.led_change(self.checkBox_Led5))
        self.checkBox_Led6.setChecked(False)
        self.checkBox_Led6.stateChanged.connect(lambda: self.led_change(self.checkBox_Led6))
        self.checkBox_Led7.setChecked(False)
        self.checkBox_Led7.stateChanged.connect(lambda: self.led_change(self.checkBox_Led7))
        self.checkBox_Led8.setChecked(False)
        self.checkBox_Led8.stateChanged.connect(lambda: self.led_change(self.checkBox_Led8))

        self.checkBox_Led_Mode1.setChecked(False)
        self.checkBox_Led_Mode1.stateChanged.connect(lambda: self.led_change(self.checkBox_Led_Mode1))
        self.checkBox_Led_Mode2.setChecked(False)
        self.checkBox_Led_Mode2.stateChanged.connect(lambda: self.led_change(self.checkBox_Led_Mode2))
        self.checkBox_Led_Mode3.setChecked(False)
        self.checkBox_Led_Mode3.stateChanged.connect(lambda: self.led_change(self.checkBox_Led_Mode3))
        self.checkBox_Led_Mode4.setChecked(False)
        self.checkBox_Led_Mode4.stateChanged.connect(lambda: self.led_change(self.checkBox_Led_Mode4))

        self.Btn_Mode1.setChecked(True)
        self.Btn_Mode1.toggled.connect(lambda: self.on_btn_mode(self.Btn_Mode1))
        self.Btn_Mode2.setChecked(False)
        self.Btn_Mode2.toggled.connect(lambda: self.on_btn_mode(self.Btn_Mode2))
        self.Btn_Mode3.setChecked(False)
        self.Btn_Mode3.toggled.connect(lambda: self.on_btn_mode(self.Btn_Mode3))
        self.Btn_Mode4.setChecked(False)
        self.Btn_Mode4.toggled.connect(lambda: self.on_btn_mode(self.Btn_Mode4))

        self.Btn_Ultrasonic.clicked.connect(self.on_btn_ultrasonic)
        self.Btn_Light.clicked.connect(self.on_btn_light)

        self.Btn_Forward.pressed.connect(self.on_btn_forward)
        self.Btn_Forward.released.connect(self.on_btn_stop)

        self.Btn_Turn_Left.pressed.connect(self.on_btn_turn_left)
        self.Btn_Turn_Left.released.connect(self.on_btn_stop)

        self.Btn_Backward.pressed.connect(self.on_btn_backwards)
        self.Btn_Backward.released.connect(self.on_btn_stop)

        self.Btn_Turn_Right.pressed.connect(self.on_btn_turn_right)
        self.Btn_Turn_Right.released.connect(self.on_btn_stop)

        self.Btn_Video.clicked.connect(self.on_btn_video)

        self.Btn_Up.clicked.connect(self.on_btn_up)
        self.Btn_Left.clicked.connect(self.on_btn_left)
        self.Btn_Down.clicked.connect(self.on_btn_down)
        self.Btn_Home.clicked.connect(self.on_btn_home)
        self.Btn_Right.clicked.connect(self.on_btn_right)

        self.Btn_Buzzer.pressed.connect(self.on_btn_buzzer)
        self.Btn_Buzzer.released.connect(self.on_btn_buzzer)

        self.Btn_Connect.clicked.connect(self.on_btn_connect)

        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.display_video)
        self.disable_gui()
        self.connected = False

    def keyPressEvent(self, event):
        if not self.connected:
            return

        if event.key() == Qt.Key_Up:
            self.on_btn_up()
        elif event.key() == Qt.Key_Left:
            self.on_btn_left()
        elif event.key() == Qt.Key_Down:
            self.on_btn_down()
        elif event.key() == Qt.Key_Right:
            self.on_btn_right()
        elif event.key() == Qt.Key_Home:
            self.on_btn_home()

        if event.key() == Qt.Key_Q:
            if self.Btn_Mode1.isChecked():
                self.Btn_Mode2.setChecked(True)
            elif self.Btn_Mode2.isChecked():
                self.Btn_Mode3.setChecked(True)
            elif self.Btn_Mode3.isChecked():
                self.Btn_Mode4.setChecked(True)
            elif self.Btn_Mode4.isChecked():
                self.Btn_Mode1.setChecked(True)

        if event.key() == Qt.Key_L:
            count = 0
            if self.checkBox_Led_Mode1.isChecked():
                self.checkBox_Led_Mode2.setChecked(True)
            elif self.checkBox_Led_Mode2.isChecked():
                self.checkBox_Led_Mode3.setChecked(True)
            elif self.checkBox_Led_Mode3.isChecked():
                self.checkBox_Led_Mode4.setChecked(True)
            elif self.checkBox_Led_Mode4.isChecked():
                self.checkBox_Led_Mode1.setChecked(True)

            for i in range(1, 5):
                check_box_led_mode = getattr(self, "check_box_led_mode%d" % i)
                if not check_box_led_mode.isChecked():
                    count += 1
                else:
                    break
            if count == 4:
                self.checkBox_Led_Mode1.setChecked(True)

        if event.key() == Qt.Key_C:
            self.on_btn_connect()
        if event.key() == Qt.Key_V:
            self.on_btn_video()

        if event.key() == Qt.Key_1:
            if self.checkBox_Led1.isChecked():
                self.checkBox_Led1.setChecked(False)
            else:
                self.checkBox_Led1.setChecked(True)
        elif event.key() == Qt.Key_2:
            if self.checkBox_Led2.isChecked():
                self.checkBox_Led2.setChecked(False)
            else:
                self.checkBox_Led2.setChecked(True)
        elif event.key() == Qt.Key_3:
            if self.checkBox_Led3.isChecked():
                self.checkBox_Led3.setChecked(False)
            else:
                self.checkBox_Led3.setChecked(True)
        elif event.key() == Qt.Key_4:
            if self.checkBox_Led4.isChecked():
                self.checkBox_Led4.setChecked(False)
            else:
                self.checkBox_Led4.setChecked(True)
        elif event.key() == Qt.Key_5:
            if self.checkBox_Led5.isChecked():
                self.checkBox_Led5.setChecked(False)
            else:
                self.checkBox_Led5.setChecked(True)
        elif event.key() == Qt.Key_6:
            if self.checkBox_Led6.isChecked():
                self.checkBox_Led6.setChecked(False)
            else:
                self.checkBox_Led6.setChecked(True)
        elif event.key() == Qt.Key_7:
            if self.checkBox_Led7.isChecked():
                self.checkBox_Led7.setChecked(False)
            else:
                self.checkBox_Led7.setChecked(True)
        elif event.key() == Qt.Key_8:
            if self.checkBox_Led8.isChecked():
                self.checkBox_Led8.setChecked(False)
            else:
                self.checkBox_Led8.setChecked(True)

        if event.isAutoRepeat():
            pass
        else:
            if event.key() == Qt.Key_W:
                self.on_btn_forward()
                self.Key_W = True
            elif event.key() == Qt.Key_S:
                self.on_btn_backwards()
                self.Key_S = True
            elif event.key() == Qt.Key_A:
                self.on_btn_turn_left()
                self.Key_A = True
            elif event.key() == Qt.Key_D:
                self.on_btn_turn_right()
                self.Key_D = True
            elif event.key() == Qt.Key_Space:
                self.on_btn_buzzer()
                self.Key_Space = True

    def keyReleaseEvent(self, event):
        if not self.connected:
            return

        if event.key() == Qt.Key_W:
            time.sleep(0.05)
            if event.key() == Qt.Key_W:
                if not (event.isAutoRepeat()) and self.Key_W is True:
                    self.on_btn_stop()
                    self.Key_W = False
        elif event.key() == Qt.Key_A:
            if not (event.isAutoRepeat()) and self.Key_A is True:
                self.on_btn_stop()
                self.Key_A = False
        elif event.key() == Qt.Key_S:
            if not (event.isAutoRepeat()) and self.Key_S is True:
                self.on_btn_stop()
                self.Key_S = False
        elif event.key() == Qt.Key_D:
            if not (event.isAutoRepeat()) and self.Key_D is True:
                self.on_btn_stop()
                self.Key_D = False

        if event.key() == Qt.Key_Space:
            if not (event.isAutoRepeat()) and self.Key_Space is True:
                self.on_btn_buzzer()
                self.Key_Space = False

    def on_btn_forward(self):
        forward = COMMAND_SEPARATOR + str(4095) + COMMAND_SEPARATOR + str(4095) + COMMAND_SEPARATOR + str(
            4095) + COMMAND_SEPARATOR + str(4095) + COMMAND_TERMINATOR
        self.control.send_data(COMMAND.CMD_MOTOR + forward)

    def on_btn_turn_left(self):
        turn_left = COMMAND_SEPARATOR + str(-4095) + COMMAND_SEPARATOR + str(-1500) + COMMAND_SEPARATOR + str(
            1500) + COMMAND_SEPARATOR + str(1500) + COMMAND_TERMINATOR
        self.control.send_data(COMMAND.CMD_MOTOR + turn_left)

    def on_btn_backwards(self):
        backwards = COMMAND_SEPARATOR + str(-4095) + COMMAND_SEPARATOR + str(-4095) + COMMAND_SEPARATOR + str(
            -4095) + COMMAND_SEPARATOR + str(-4095) + COMMAND_TERMINATOR
        self.control.send_data(COMMAND.CMD_MOTOR + backwards)

    def on_btn_turn_right(self):
        turn_right = COMMAND_SEPARATOR + str(1500) + COMMAND_SEPARATOR + str(1500) + COMMAND_SEPARATOR + str(
            -1500) + COMMAND_SEPARATOR + str(-1500) + COMMAND_TERMINATOR
        self.control.send_data(COMMAND.CMD_MOTOR + turn_right)

    def on_btn_stop(self):
        stop = COMMAND_SEPARATOR + str(0) + COMMAND_SEPARATOR + str(0) + COMMAND_SEPARATOR + str(
            0) + COMMAND_SEPARATOR + str(0) + COMMAND_TERMINATOR
        self.control.send_data(COMMAND.CMD_MOTOR + stop)

    def on_btn_video(self):
        if self.Btn_Video.text() == 'Show Video':
            self.video_timer.start(34)
            self.Btn_Video.setText('Hide Video')
        elif self.Btn_Video.text() == 'Hide Video':
            self.video_timer.stop()
            self.Btn_Video.setText('Show Video')

    def on_btn_up(self):
        self.servo2 = self.servo2 + 10
        if self.servo2 >= 180:
            self.servo2 = 180
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_left(self):
        self.servo1 = self.servo1 - 10
        if self.servo1 <= 0:
            self.servo1 = 0
        self.HSlider_Servo1.setValue(self.servo1)

    def on_btn_down(self):
        self.servo2 = self.servo2 - 10
        if self.servo2 <= 80:
            self.servo2 = 80
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_right(self):
        self.servo1 = self.servo1 + 10
        if self.servo1 >= 180:
            self.servo1 = 180
        self.HSlider_Servo1.setValue(self.servo1)

    def on_btn_home(self):
        self.servo1 = 90
        self.servo2 = 90
        self.HSlider_Servo1.setValue(self.servo1)
        self.VSlider_Servo2.setValue(self.servo2)

    def on_btn_buzzer(self):
        if self.Btn_Buzzer.text() == 'Buzzer':
            self.control.send_data(COMMAND.CMD_BUZZER + COMMAND_SEPARATOR + '1' + COMMAND_TERMINATOR)
            self.Btn_Buzzer.setText('Noise')
        else:
            self.control.send_data(COMMAND.CMD_BUZZER + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
            self.Btn_Buzzer.setText('Buzzer')

    def on_btn_ultrasonic(self):
        if self.Btn_Ultrasonic.text() == "Ultrasonic":
            self.control.send_data(COMMAND.CMD_SONIC + COMMAND_SEPARATOR + '1' + COMMAND_TERMINATOR)
        else:
            self.control.send_data(COMMAND.CMD_SONIC + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
            self.Btn_Ultrasonic.setText("Ultrasonic")

    def on_btn_light(self):
        if self.Btn_Light.text() == "Light":
            self.control.send_data(COMMAND.CMD_LIGHT + COMMAND_SEPARATOR + '1' + COMMAND_TERMINATOR)
        else:
            self.control.send_data(COMMAND.CMD_LIGHT + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
            self.Btn_Light.setText("Light")

    def change_left_right(self):  # Left or Right
        self.servo1 = self.HSlider_Servo1.value()
        self.control.send_data(
            COMMAND.CMD_SERVO + COMMAND_SEPARATOR + '0' + COMMAND_SEPARATOR + str(self.servo1) + COMMAND_TERMINATOR)
        self.label_Servo1.setText("%d" % self.servo1)

    def change_up_down(self):  # Up or Down
        self.servo2 = self.VSlider_Servo2.value()
        self.control.send_data(
            COMMAND.CMD_SERVO + COMMAND_SEPARATOR + '1' + COMMAND_SEPARATOR + str(self.servo2) + COMMAND_TERMINATOR)
        self.label_Servo2.setText("%d" % self.servo2)

    def fine_tune_left_right(self):  # fine tune Left or Right
        self.label_FineServo1.setText(str(self.HSlider_FineServo1.value()))
        data = self.servo1 + self.HSlider_FineServo1.value()
        self.control.send_data(
            COMMAND.CMD_SERVO + COMMAND_SEPARATOR + '0' + COMMAND_SEPARATOR + str(data) + COMMAND_TERMINATOR)

    def fine_tune_up_down(self):  # fine tune Up or Down
        self.label_FineServo2.setText(str(self.HSlider_FineServo2.value()))
        data = self.servo2 + self.HSlider_FineServo2.value()
        self.control.send_data(
            COMMAND.CMD_SERVO + COMMAND_SEPARATOR + '1' + COMMAND_SEPARATOR + str(data) + COMMAND_TERMINATOR)

    def minimize_window(self):
        self.showMinimized()

    def led_change(self, b):
        red = self.Color_R.text()
        green = self.Color_G.text()
        blue = self.Color_B.text()
        color = self.color_command(blue, green, red)
        if b.text() == "Led1":
            self.led_index = str(0x01)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led2":
            self.led_index = str(0x02)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led3":
            self.led_index = str(0x04)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led4":
            self.led_index = str(0x08)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led5":
            self.led_index = str(0x10)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led6":
            self.led_index = str(0x20)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led7":
            self.led_index = str(0x40)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led8":
            self.led_index = str(0x80)
            if b.isChecked():
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + color)
            else:
                self.control.send_data(COMMAND.CMD_LED + COMMAND_SEPARATOR + self.led_index + CMD_LED_OFF)
        if b.text() == "Led_Mode1":
            if b.isChecked():
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '1' + COMMAND_TERMINATOR)
            else:
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
        if b.text() == "Led_Mode2":
            if b.isChecked():

                self.checkBox_Led_Mode1.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '2' + COMMAND_TERMINATOR)
            else:
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
        if b.text() == "Led_Mode3":
            if b.isChecked():
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode1.setChecked(False)
                self.checkBox_Led_Mode4.setChecked(False)
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '3' + COMMAND_TERMINATOR)
            else:
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)
        if b.text() == "Led_Mode4":
            if b.isChecked():
                self.checkBox_Led_Mode2.setChecked(False)
                self.checkBox_Led_Mode3.setChecked(False)
                self.checkBox_Led_Mode1.setChecked(False)
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '4' + COMMAND_TERMINATOR)
            else:
                self.control.send_data(COMMAND.CMD_LED_MOD + COMMAND_SEPARATOR + '0' + COMMAND_TERMINATOR)

    def color_command(self, blue, green, red):
        return COMMAND_SEPARATOR + str(red) + COMMAND_SEPARATOR + str(green) + COMMAND_SEPARATOR + str(
            blue) + COMMAND_TERMINATOR

    def on_btn_mode(self, mode):
        if mode.text() == "M-Free":
            if mode.isChecked():
                self.control.send_data(COMMAND.CMD_MODE + COMMAND_SEPARATOR + MODE.OFF + COMMAND_TERMINATOR)
        if mode.text() == "M-Light":
            if mode.isChecked():
                self.control.send_data(COMMAND.CMD_MODE + COMMAND_SEPARATOR + MODE.FOLLOW_LIGHT + COMMAND_TERMINATOR)
        if mode.text() == "M-Sonic":
            if mode.isChecked():
                self.control.send_data(
                    COMMAND.CMD_MODE + COMMAND_SEPARATOR + MODE.ULTRASONIC_OBSTACLE_DETECTION + COMMAND_TERMINATOR)
        if mode.text() == "M-Line":
            if mode.isChecked():
                self.control.send_data(COMMAND.CMD_MODE + COMMAND_SEPARATOR + MODE.FOLLOW_LINE + COMMAND_TERMINATOR)

    def on_btn_connect(self):
        if not self.connected:
            self.target_host = self.IP.text()
            try:
                self.control = Control(self.target_host)
                self.receive_thread = Thread(target=self.recv_message)
                self.receive_thread.start()
            except Exception as e:
                print(e)
                print('control error')
                return
            try:
                self.video_streaming = VideoStreaming(self.target_host)
                self.streaming_thread = Thread(target=self.video_streaming.start_streaming)
                self.streaming_thread.start()
            except Exception as e:
                print(e)
                print('video error')
                return
            self.Btn_Connect.setText("Disconnect")
            print('Server address:' + str(self.target_host) + '\n')
            self.enable_gui()
            self.connected = True
        else:
            self.Btn_Connect.setText("Connect")
            try:
                stop_thread(self.receive_thread)
                stop_thread(self.streaming_thread)
            except Exception as e:
                print(e)
                pass
            self.video_streaming.stop_tcp_client()
            self.disable_gui()
            self.connected = False

    def close(self):
        self.video_timer.stop()
        try:
            stop_thread(self.receive_thread)
            stop_thread(self.streaming_thread)
        except Exception as e:
            print(e)
            pass
        self.video_streaming.stop_tcp_client()
        try:
            os.remove("video.jpg")
        except Exception as e:
            print(e)
            pass
        QCoreApplication.instance().quit()
        quit()

    def recv_message(self):
        while True:
            buffer = str(self.control.recv_data())
            print(buffer)
            if buffer == '':
                break
            else:
                messages = buffer.split(COMMAND_TERMINATOR)
                if messages[-1] == "":
                    messages = messages[:-1]
            for message in messages:
                cmd, *params = message.split(COMMAND_SEPARATOR)
                if COMMAND.CMD_SONIC in cmd:
                    distance = params[0]
                    self.Btn_Ultrasonic.setText(f'Obstruction: {distance} cm')
                elif COMMAND.CMD_LIGHT in cmd:
                    left_v, right_v = params
                    self.Btn_Light.setText(f'Left: {left_v}V Right: {right_v}V')
                elif COMMAND.CMD_POWER in cmd:
                    voltage = params[0]
                    percent_power = int((float(voltage) - 7) / 1.40 * 100)
                    self.progress_Power.setValue(percent_power)

    def is_valid_jpg(self, jpg_file):
        b_valid = True
        try:
            if jpg_file.split('.')[-1].lower() == 'jpg':
                with open(jpg_file, 'rb') as f:
                    buf = f.read()
                    if not buf.startswith(b'\xff\xd8'):
                        b_valid = False
                    elif buf[6:10] in (b'JFIF', b'Exif'):
                        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                            b_valid = False
                    else:
                        try:
                            Image.open(f).verify()
                        except:
                            b_valid = False
            else:
                return b_valid
        except:
            pass
        return b_valid

    def find_face(self, face_x, face_y):
        if face_x != 0 and face_y != 0:
            offset_x = float(face_x / 400 - 0.5) * 2
            offset_y = float(face_y / 300 - 0.5) * 2
            delta_degree_x = 4 * offset_x
            delta_degree_y = -4 * offset_y
            self.servo1 = self.servo1 + delta_degree_x
            self.servo2 = self.servo2 + delta_degree_y
            if -0.15 < offset_x < 0.15 and -0.15 < offset_y < 0.15:
                pass
            else:
                self.HSlider_Servo1.setValue(int(self.servo1))
                self.VSlider_Servo2.setValue(int(self.servo2))

    def display_video(self):
        self.video_streaming.connected = False
        try:
            if self.is_valid_jpg('video.jpg'):
                self.label_Video.setPixmap(QPixmap('video.jpg'))
                if self.checkBox_Tracking_Faces.isChecked():
                    self.find_face(self.video_streaming.face_x, self.video_streaming.face_y)
        except Exception as e:
            print(e)
        self.video_streaming.connected = True

    def enable_gui(self):
        self.controls_set(True)

    def disable_gui(self):
        self.controls_set(False)

    def controls_set(self, flag: bool):
        self.Btn_Video.setEnabled(flag)

        self.checkBox_Led1.setEnabled(flag)
        self.checkBox_Led2.setEnabled(flag)
        self.checkBox_Led3.setEnabled(flag)
        self.checkBox_Led4.setEnabled(flag)
        self.checkBox_Led5.setEnabled(flag)
        self.checkBox_Led6.setEnabled(flag)
        self.checkBox_Led7.setEnabled(flag)
        self.checkBox_Led8.setEnabled(flag)

        self.checkBox_Led_Mode1.setEnabled(flag)
        self.checkBox_Led_Mode2.setEnabled(flag)
        self.checkBox_Led_Mode3.setEnabled(flag)
        self.checkBox_Led_Mode4.setEnabled(flag)

        self.Color_R.setEnabled(flag)
        self.Color_G.setEnabled(flag)
        self.Color_B.setEnabled(flag)

        self.Btn_Up.setEnabled(flag)
        self.Btn_Down.setEnabled(flag)
        self.Btn_Right.setEnabled(flag)
        self.Btn_Left.setEnabled(flag)
        self.Btn_Home.setEnabled(flag)

        self.Btn_Turn_Left.setEnabled(flag)
        self.Btn_Turn_Right.setEnabled(flag)
        self.Btn_Backward.setEnabled(flag)
        self.Btn_Forward.setEnabled(flag)
        self.Btn_Buzzer.setEnabled(flag)

        self.checkBox_Tracking_Faces.setEnabled(flag)
        self.Btn_Mode1.setEnabled(flag)
        self.Btn_Mode2.setEnabled(flag)
        self.Btn_Mode3.setEnabled(flag)
        self.Btn_Mode4.setEnabled(flag)

        self.Btn_Ultrasonic.setEnabled(flag)
        self.Btn_Light.setEnabled(flag)

        self.HSlider_FineServo1.setEnabled(flag)
        self.HSlider_FineServo2.setEnabled(flag)

        self.HSlider_Servo1.setEnabled(flag)
        self.VSlider_Servo2.setEnabled(flag)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = ClientWindow()
    myshow.show()
    app.exec()
