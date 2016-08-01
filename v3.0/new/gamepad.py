###Code Version: 3.0
from moves import Move
from threading import Thread
import pygame
import time

class gamepadConnect():

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.moves = Move()
        self.moves.stop()
        self.flag = True
        self.tmpDirectionalValue = 0
        self.tmpVelocityValue = 0
        self.passCounter = 0
        self.passwordFlag = False


    def run(self):
        self.passCounter = 0
        while self.flag:
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                for event in pygame.event.get():

                    #password (start)
                    if(event.type == pygame.JOYBUTTONDOWN):
                        if(event.button==9):
                            if(self.passCounter == 0):
                                self.passwordFlag = True
                                self.passCounter = 1
                            else:
                                self.passwordFlag = False
                                self.passCounter = 0

                    if(self.passCounter):
                        #axis mode
                        if (event.type == pygame.JOYAXISMOTION):
                            #forward/backward
                            if(event.axis==1):
                                axis = joystick.get_axis(1)
                                value = axis * -100

                                if(value > 100):
                                    value = 100
                                elif(value < -100):
                                    value = -100
                                self.moves.directionalStop()
                                self.moveUpDown(value)

                            #right/left
                            if(event.axis==2):
                                directAxis = joystick.get_axis(2)
                                directValue = directAxis * 100
                                if(directValue> 100):
                                    directValue = 100
                                elif(directValue < -100):
                                    directValue = -100
                                self.moveRightLeft(directValue)

                        #print event.button
                        if(event.type == pygame.JOYBUTTONDOWN):
                            #l1
                            if(event.button==4):
                                print "up left"
                                self.moves.forwardLeft()
                            #r1
                            if(event.button==5):
                                print "up right"
                                self.moves.forwardRight()
                            #l2
                            if(event.button==6):
                                print "down left"
                                self.moves.backwardLeft()
                            #r2
                            if(event.button==7):
                                print "down right"
                                self.moves.backwardRight()


    def moveUpDown(self,value):
        if(value > 0):
            if(value != self.tmpVelocityValue):
                self.moves.forward(value)
                self.tmpVelocityValue = value
        elif(value < 0):
            value = (value * -1);
            if(value != self.tmpVelocityValue):
                self.moves.backward(value)
                self.tmpVelocityValue = value
        else:
            self.moves.stop()


    def moveRightLeft(self,value):
        if(value > 0):
            if(value != self.tmpDirectionalValue):
                self.moves.right(value)
                self.tmpDirectionalValue = value
        elif(value < 0):
            value = (value * -1);
            if(value != self.tmpDirectionalValue):
                self.moves.left(value)
                self.tmpDirectionalValue = value
        else:
            self.moves.stop()
