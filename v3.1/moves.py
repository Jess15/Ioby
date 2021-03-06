###Code Version: 3.0
import RPi.GPIO as GPIO
import time

class Move():

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        # traction
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        # direction
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

        self.forwardObj = GPIO.PWM(7, 100)
        self.backwardObj = GPIO.PWM(11, 100)
        self.rightObj = GPIO.PWM(15, 100)
        self.leftObj = GPIO.PWM(13, 100)

        self.forwardObj.start(0)
        self.backwardObj.start(0)
        self.rightObj.start(0)
        self.leftObj.start(0)
	self.laserOn=False

    def stop(self):
        self.forwardObj.ChangeDutyCycle(0)
        self.backwardObj.ChangeDutyCycle(0)
        self.rightObj.ChangeDutyCycle(0)
        self.leftObj.ChangeDutyCycle(0)


    def directionalStop(self):
        self.rightObj.ChangeDutyCycle(0)
        self.leftObj.ChangeDutyCycle(0)


    def forward(self, value):
        #self.stop()
        self.forwardObj.ChangeDutyCycle(value)


    def backward(self, value):
        #self.stop()
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


    def forwardRight(self):
        self.stop()
        self.right(100)
        time.sleep(0.1)
        self.forward(50)


    def forwardLeft(self):
        self.stop()
        self.left(100)
        time.sleep(0.1)
        self.forward(50)


    def backwardRight(self):
        self.stop()
        self.right(100)
        time.sleep(0.1)
        self.backward(100)


    def backwardLeft(self):
        self.stop()
        self.left(100)
        time.sleep(0.1)
        self.backward(100)

    def shot(self):
	self.laserOn=True
        GPIO.output(18, True)

    def shotOff(self):
        self.laserOn=False
	GPIO.output(18, False)
	
