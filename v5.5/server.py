###Code Version: 3.0
import socket
from moves import Move
from threading import Thread

class IobyServer():

    def __init__(self):
        self.moves = Move()
        self.moves.stop()
        self.flag = True
        self.tmpDirectionalValue = 0
        self.tmpVelocityValue = 0
        self.s = socket.socket()
        self.host = "0.0.0.0"
        self.port = 2603
        self.sc = 0
        self.addr = 0
        help1 = "Instructions:\n Use the left axis for forward and backward movements, and the right axis for laterals movements.\n"
        help2 = " 'l1' = forward and left.\n 'l2' = backward and left.\n 'r1' = forward and right.\n 'r2' = backward and right.\n"
        self. helps = help1+help2
	self.data = ""


    def run(self):
        try:
            self.s.bind((self.host, self.port))
            self.s.listen(1)
            print "Server up"

        except:
            print "Server Error"

        while True:

            self.sc, self.addr = self.s.accept()

            print "Received Connection from: " + str(self.addr[0]) + ":" + str(self.addr[1])
            self.sc.send("Password: \n")
            passwd = self.sc.recv(1024)

            if(passwd == "bop"):

                self.sc.send("on")
		self.flag=True

                while self.flag:

                    try:
                        #axis mode
                        self.data = self.sc.recv(1024)
                        rcvData = self.data.split(":")
                        axi = int(rcvData[0])
                        value = int(rcvData[1])
                        directAxi = int(rcvData[2])
                        directValue = int(rcvData[3])

                        if(value > 100):
                            value = 100
                        elif(value < -100):
                            value = -100

                        if(directValue> 100):
                            directValue = 100
                        elif(directValue < -100):
                            directValue = -100

                        print "Received: ", rcvData[0], ":", rcvData[1] , ":", rcvData[2] , ":", rcvData[3]
                        Thread(target=self.selectMove,args=(axi,directAxi,value,directValue)).start()

                    except:
                        #button mode
                        btn = self.data
                        print "Received button", btn
			#direcciones android
			if(btn=='w'):
				self.moves.stop()
				self.moves.forward(50)
			if(btn=='s'):
				self.moves.stop()
				self.moves.backward(50)
			if(btn=='a'):
				self.moves.stop()
				self.moves.left(50)
			if(btn=='d'):
				self.moves.stop()
				self.moves.right(50)
			
			if(btn=="x"):
				self.moves.stop()
			
			if(btn=="h"):
				print "Closing..."
                            	self.flag = False
                            	self.sc.close()
                            	print "Client Disconected"
			#cuadrado
                        if(btn == "3" or btn=="i"):
                            self.moves.laserOn()

                        #l1
                       # if(btn == "4"):
                       #     print "up left"
                       #     self.moves.forwardLeft()

                        #r1
                        #if(btn == "5"):
                        #    print "up right"
                        #    self.moves.forwardRight()

                        #l2
                        #if(btn == "6"):
                        #    print "down left"
                        #    self.moves.backwardLeft()

                        ##r2
                        #if(btn == "7"):
                        #    print "down right"
                        #    self.moves.backwardRight()

                        #select
                        if(btn == "8"):
                            print "Sending instructions..."
                            self.sc.send(self.helps)
                            print "Instructions sent!"

#                        r3
                        if(btn == "11"):
                            print "Closing..."
                            self.flag = False
                            self.sc.close()
                            print "Client Disconected"


			#triangulo
			if (btn=="0" or btn=="u"):
			   print "lights"
			   self.moves.lights()
			
			#circulo
			if (btn=="1" or btn=="j"):
			   print "tracker"
			   self.moves.tracker()
            else:
                #invalid password
                f = open(".loginError.txt", "a")
                f.write(self.addr[0] + ":" + passwd + "\n")
                f.close()
                self.sc.send("off")
                self.sc.close()


    def moveUpDown(self,value):
        if(value > 0):
            print "UpDown "+str(value)
            if(value != self.tmpVelocityValue):
                self.moves.forward(value)
                self.tmpVelocityValue = value
        elif(value < 0):
            print "UpDown "+str(value)
            value = (value * -1);
            if(value != self.tmpVelocityValue):
                self.moves.backward(value)
                self.tmpVelocityValue = value
        else:
            print "UpDown "+str(value)
            self.moves.stop()


    def moveRightLeft(self,value):
        if(value > 0):
            print "RightLeft "+str(value)
            if(value != self.tmpDirectionalValue):
                self.moves.right(value)
                self.tmpDirectionalValue = value
        elif(value < 0):
            print "RightLeft "+str(value)
            value = (value * -1);
            if(value != self.tmpDirectionalValue):
                self.moves.left(value)
                self.tmpDirectionalValue = value
        else:
            print "RightLeft "+str(value)
            self.moves.stop()


    def selectMove(self,axi,directAxi,value,directValue):
        if(axi == 1):
            Thread(target=self.moveUpDown,args=(value,)).start()
        if(directAxi== 2):
            Thread(target=self.moveRightLeft, args=(directValue,)).start()
