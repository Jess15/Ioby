###Code Version: 3.0
import socket
import pygame

class IobyClient():

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.flag = True
        self.isOk = ""
        self.s = socket.socket()
        self.host = "192.168.1.252"
        self.port = 2602 #2602


    def run(self):
        try:
            self.s.connect((self.host, self.port))
            data = self.s.recv(1024)
            empty = "empty"
            passwd = raw_input(data)
            if (not passwd):
                passwd = empty

            self.s.send(passwd)
            self.isOk = ""+self.s.recv(1024)
            self.isOK=self.isOk.replace('\n','')
            print self.isOk

            self.sendData(self.isOk,self.flag);

        except:
            print "Connection Error"
            self.flag = 0


    def sendData(self,isOk,flag):
        if (isOk == "on"):

            print "Press 'r3' for close, 'select' for instructions."

            while flag:

                joystick_count = pygame.joystick.get_count()
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()

                    for event in pygame.event.get():
                        #axis mode
                        if (event.type == pygame.JOYAXISMOTION):

                            peer = "0:0"
                            directionalPeer = "0:0"

                            #forward/backward
                            if(event.axis==1):
                                axis = joystick.get_axis(1)
                                value = axis * -100
                                peer = str(event.axis)+":"+str(int(value))

                            #right/left
                            if(event.axis==2):
                                axis = joystick.get_axis(2)
                                value = axis * 100
                                directionalPeer = str(event.axis)+":"+str(int(value))

                            globalPeer = peer + ":" + directionalPeer
                            self.s.send(globalPeer)

                        #button mode
                        elif (event.type == pygame.JOYBUTTONDOWN):
                            print "button!"

                            button = str(event.button)
                            print button

                            try:
                                print "Sending..."
                                self.s.send(button)
                                print "Sent", button

                            except:
                                print "Error sending!"

                            #select
                            if (button == "8"):
                                print "Waiting for instructions..."
                                instructions = self.s.recv(1024)
                                print instructions

                            #r3
                            if (button == "11"):
                                print "Closing..."
                                self.flag = False
                                self.s.close()
                                print "Connection closed."

        else:
            if flag:
                print "Invalid Password"
                self.s.close()

Ioby = IobyClient()
Ioby.run()
