#!/usr/bin/python

import time
import VL53L0X
import os
import ctypes

# import libraries
import RPi.GPIO as GPIO
from time import sleep
import time

lib_path = '/home/group14/Desktop/VL53L0X/bin/vl53l0x_python.so'

if not os.path.isfile(lib_path):
    raise FileNotFoundError(f"Library file not found: {lib_path}")

ctypes.CDLL(lib_path)

# decide on which numbering system you are working with
GPIO.setmode(GPIO.BOARD)

trigPin = 11
echoPin = 12
GPIO.setup(trigPin,GPIO.OUT)
GPIO.setup(echoPin,GPIO.IN)

# GPIO.setmode(GPIO.BCM)

# object-oriented programming defines a type of object
class Motor():
    def __init__(self,Ena,In1,In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        self.pwm = GPIO.PWM(self.Ena,100) # operates at 100 Hz (check?)
        self.pwm.start(0)

    def moveF(self,x=50,t=0): # by default, it operates at 50% speed
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(x) # x% of the speed
        # sleep(t)
    
    def moveB(self,x=50,t=0): # by default, it operates at 50% speed
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        self.pwm.ChangeDutyCycle(x) # x% of the speed
        # sleep(t)
    
    def stop(self,t=0):
        self.pwm.ChangeDutyCycle(0)
        # sleep(t)

def read_ultrasonic_distance():
    # 发送触发信号
    GPIO.output(trigPin, False)
    time.sleep(2E-6)
    GPIO.output(trigPin, True)
    time.sleep(10E-6)
    GPIO.output(trigPin, False)

    # 等待回波信号
    while GPIO.input(echoPin) == 0:
        pass
    echo_start = time.time()
    while GPIO.input(echoPin) == 1:
        pass
    echo_end = time.time()

    # 计算距离（单位：cm）
    travel_time = echo_end - echo_start
    distance_mm = travel_time * 343000 / 2  # 343000 mm/s
    return round(distance_mm, 1)


motor1 = Motor(36, 38, 40)  # Left car motor pins (Ena, In1, In2)
motor2 = Motor(33, 35, 37)  # Right car moxtor pins (Ena, In1, In2)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BEST)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

target_distance = 1052  # diameter 30cm
# target_distance = 1082  # diameter 60cm

try:
    while True:
        distance = read_ultrasonic_distance()
        # distance = tof.get_distance()
        print("%d mm" % (distance))
        if distance > target_distance:
            motor1.stop()
            motor2.stop()
            print("Both cars reached the target height!")
            break
        elif distance > target_distance - 50:
            motor1.moveF(20)
            motor2.moveF(20)
        else:
            motor1.moveF(100)
            motor2.moveF(100)
    
    sleep(60)
    while True:
        distance = read_ultrasonic_distance()
        # distance = tof.get_distance()
        print("%d mm" % (distance))
        if distance < 200:
            motor1.stop()
            motor2.stop()
            print("Both cars reached the target height!")
            break
        else:
            motor1.moveB(100)
            motor2.moveB(100)
        # sleep(0.001)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO Good to Go')
finally:
    motor1.stop()
    motor2.stop()
    tof.stop_ranging()
    tof.close()
    GPIO.cleanup()
    print("Clean exit")

tof.stop_ranging()
tof.close()