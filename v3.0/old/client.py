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
        self.host = "192.168.1.252"  # "192.168.1.252"
        self.port = 2609 #2602

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
            flag = 0


    def sendData(self,isOk,flag):
        if (isOk == "on"):

            print "Send 'exit' for close, 'help' for instructions."

            while flag:

                joystick_count = pygame.joystick.get_count()
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()

                    for event in pygame.event.get():
                        if event.type == pygame.JOYAXISMOTION:
                            #arriba y abajo
                            peer = "0:0"
                            directionalPeer = "0:0"
                            if(event.axis==1):
                                axis = joystick.get_axis(1)
                                value = axis * -100
                                peer = str(event.axis)+":"+str(int(value))

                            if(event.axis==2):

                                axis = joystick.get_axis(2)
                                value = axis * 100
                                directionalPeer = str(event.axis)+":"+str(int(value))

                            globalPeer = peer + ":" + directionalPeer
                            self.s.send(globalPeer)

    #           action = raw_input()
    #           s.send(action)

    #           if (action == "help"):
    #                instructions = s.recv(1024)
    #                print instructions

    #           if (action == "exit"):
    #                print "Closing..."
    #                flag = False
    #                s.close()
        else:
            if flag:
                print "Invalid Password"
                self.s.close()

Ioby = IobyClient()
Ioby.run()
