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
        self.port = 2609
        self.sc = 0
        self.addr = 0

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

                while self.flag:
                    data = self.sc.recv(1024)
                    rcvData = data.split(":")
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



                    if(data == "exit"):
                        print data
                        print "Closing..."
                        self.flag = False
                        self.moves.exit()
                        self.sc.close()

                    elif (data == "help"):
                        print data
                        helps = "Instructions:\n Use the left axis for forward and backward movements, and the right axis for laterals movements."
                        self.sc.send(helps)

                    else:
                        #print data
                        print "Received: ", rcvData[0], ":", rcvData[1] , ":", rcvData[2] , ":", rcvData[3]
                        pass
                        Thread(target=self.selectMove,args=(axi,directAxi,value,directValue)).start()
                        #self.selectMove(axi,directAxi,value,directValue)
            else:
                f = open("./logs/loginError.txt", "a")
                f.write(self.addr[0] + ":" + passwd + "\n")
                f.close()
                #moves.exit()
                self.sc.send("off")
                self.sc.close()

    def moveUpDown(self,value):
        if(value > 0):
            print "UpDown "+str(value)
            #self.moves.stop()
            if(value != self.tmpVelocityValue):
                self.moves.forward(value)
                self.tmpVelocityValue = value
        elif(value < 0):
            print "UpDown "+str(value)
            value = (value * -1);
            #self.moves.stop()
            if(value != self.tmpVelocityValue):
                self.moves.backward(value)
                self.tmpVelocityValue = value
        else:
            print "UpDown "+str(value)
            self.moves.stop()

    def moveRightLeft(self,value):
        if(value > 0):
            print "RightLeft "+str(value)
            #self.moves.directionalStop()
            if(value != self.tmpDirectionalValue):
                self.moves.right(value)
                self.tmpDirectionalValue = value
        elif(value < 0):
            print "RightLeft "+str(value)
            value = (value * -1);
            #self.moves.directionablStop()
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
