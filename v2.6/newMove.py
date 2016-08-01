###Code Version: 2.5
import RPi.GPIO as GPIO
from time import sleep


class Move():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        # traction
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        # direction
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)

        self.forwardObj = GPIO.PWM(11, 100)
        self.backwardObj = GPIO.PWM(7, 100)
        self.rightObj = GPIO.PWM(15, 100)
        self.leftObj = GPIO.PWM(13, 100)

        self.forwardObj.start(0)
        self.backwardObj.start(0)
        self.rightObj.start(0)
        self.leftObj.start(0)

    def stop(self):
        self.forwardObj.ChangeDutyCycle(0)
        self.backwardObj.ChangeDutyCycle(0)
        self.rightObj.ChangeDutyCycle(0)
        self.leftObj.ChangeDutyCycle(0)
        #sleep(0.5)

    def directionalStop(self):
        self.rightObj.ChangeDutyCycle(0)
        self.leftObj.ChangeDutyCycle(0)
        #sleep(0.5)

    def forward(self, value):
        self.stop()
        self.forwardObj.ChangeDutyCycle(value)

    def backward(self, value):
        self.stop()
        self.backwardObj.ChangeDutyCycle(value)

    def right(self, value):
        self.directionalStop()
        self.rightObj.ChangeDutyCycle(value)

    def left(self, value):
        self.directionalStop()
        self.leftObj.ChangeDutyCycle(value)

    def exit(self):
        self.forwardObj.stop()
        self.backwardObj.stop()
        self.rightObj.stop()
        self.leftObj.stop()
