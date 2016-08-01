###Code Version: 3.0
import RPi.GPIO as GPIO
import time
import os
import time
import subprocess
class Move():

    def __init__(self):
        self.lightsCounter=0
        self.laserCounter=0
	self.trackerCounter=0
        GPIO.setmode(GPIO.BOARD)
        # laser
        GPIO.setup(18, GPIO.OUT)
        # traction
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        # direction
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        # on/off
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

        self.forwardObjR = GPIO.PWM(7, 100)
        self.forwardObjL =  GPIO.PWM(15,100)
	self.backwardObjR = GPIO.PWM(11, 100)
	self.backwardObjL = GPIO.PWM(13, 100)  

#        self.rightObj = GPIO.PWM(15, 100)
#        self.leftObj = GPIO.PWM(13, 100)

        self.forwardObjR.start(0)
	self.forwardObjL.start(0)
        self.backwardObjR.start(0)
	self.backwardObjL.start(0)
        #self.rightObj.start(0)
        #self.leftObj.start(0)

        GPIO.output(19, False)
        GPIO.output(21, False)


    def stop(self):
        self.forwardObjR.ChangeDutyCycle(0)
        self.forwardObjL.ChangeDutyCycle(0)
	self.backwardObjR.ChangeDutyCycle(0)
	self.backwardObjL.ChangeDutyCycle(0)
        #self.rightObj.ChangeDutyCycle(0)
        #self.leftObj.ChangeDutyCycle(0)


#    def directionalStop(self):
#        self.rightObj.ChangeDutyCycle(0)
#        self.leftObj.ChangeDutyCycle(0)


    def forward(self, value):
        #self.stop()
        self.forwardObjR.ChangeDutyCycle(value)
	self.forwardObjL.ChangeDutyCycle(value)
	

    def backward(self, value):
        #self.stop()
	#self.leftObj.ChangeDutyCycle(value)	
        self.backwardObjL.ChangeDutyCycle(value)
	self.backwardObjR.ChangeDutyCycle(value)

    def right(self, value):
        #self.directionalStop()
        self.forwardObjL.ChangeDutyCycle(value)
	self.backwardObjR.ChangeDutyCycle(value)

    def left(self, value):
        #self.directionalStop()
        self.forwardObjR.ChangeDutyCycle(value)
	self.backwardObjL.ChangeDutyCycle(value)


    def exit(self):
        self.forwardObjR.stop()
	self.forwardObjL.stop()
        self.backwardObjR.stop()
	self.backwardObjL.stop()
        #self.rightObj.stop()
        #self.leftObj.stop()


#    def forwardRight(self):
#        self.stop()
#        self.right(100)
#        time.sleep(0.1)
#        self.forward(50)


#    def forwardLeft(self):
#        self.stop()
#        self.left(100)
#        time.sleep(0.1)
#        self.forward(50)


#    def backwardRight(self):
#        self.stop()
#        self.right(100)
#        time.sleep(0.1)
#        self.backward(100)


#    def backwardLeft(self):
#        self.stop()
#        self.left(100)
#        time.sleep(0.1)
#        self.backward(100)

    def lights(self):
        if (self.lightsCounter == 0):
            GPIO.output(19, True)
            GPIO.output(21, True)
            self.lightsCounter = 1
            print "Lights on!"

        elif (self.lightsCounter == 1):
            GPIO.output(19, False)
            GPIO.output(21, False)
            self.lightsCounter = 0
            print "Lights off!"

    def laserOn(self):
        if (self.laserCounter == 0):
            GPIO.output(18, True)
            self.laserCounter = 1
            print "Laser on!"

        elif (self.laserCounter == 1):
            GPIO.output(18, False)
            self.laserCounter = 0
            print "Laser off!"

    def tracker(self):
	if(self.trackerCounter == 0):
	   os.system("service motion stop &")
	   time.sleep(1)	
	   #os.system("python tracker.py")
	   process = subprocess.Popen(['python', '/root/Ioby/v4.0/tracker.py'],shell=False)
	   self.trackerCounter = 1
        elif(self.trackerCounter == 1):
	   f = open("TrackerPid.txt","r")
           pid = f.read()   
	   os.system("kill -9 "+pid)
	   time.sleep(1)
	   f.close()
	   os.system("service motion start &")
	   self.trackerCounter = 0
