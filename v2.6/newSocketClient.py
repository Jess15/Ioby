###Code Version: 2.5
import socket
from newMove import Move
from threading import Thread

class socketServer():

    def __init__(self):
        self.moves = Move()
        self.moves.stop()
        self.flag = True
        self.tmpDirectionalValue = 0
        self.tmpVelocityValue = 0
        self.s = socket.socket()
        self.host = "0.0.0.0"
        self.port = 2608
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

                        if(axi == 1):
                            Thread(target=self.moveUpDown,args=(value,)).start()
                            #self.moveUpDown(value)

                        elif(directAxi== 2):
                            Thread(target=self.moveRightLeft, args=(directValue,)).start()
                            #self.moveRightLeft(directValue)

                        else:
                            self.moves.stop()
            else:
                f = open("./logs/loginError.txt", "a")
                f.write(self.addr[0] + ":" + passwd + "\n")
                f.close()
                #moves.exit()
                self.sc.send("off")
                self.sc.close()

    def moveUpDown(self,value):
        if(value > 0):
            #print value
            #self.moves.stop()
            if(value != self.tmpVelocityValue):
                self.moves.forward(value)
                self.tmpVelocityValue = value
        elif(value < 0):
            #print value
            value = (value * -1);
            #self.moves.stop()
            if(value != self.tmpVelocityValue):
                self.moves.backward(value)
                self.tmpVelocityValue = value
        else:
            #print value
            self.moves.stop()

    def moveRightLeft(self,value):
        if(value > 0):
            #print value
            #self.moves.directionalStop()
            if(value != self.tmpDirectionalValue):
                self.moves.right(value)
                self.tmpDirectionalValue = value
        elif(value < 0):
            #print value
            value = (value * -1);
            #self.moves.directionablStop()
            if(value != self.tmpDirectionalValue):
                self.moves.left(value)
                self.tmpDirectionalValue = value
        else:
            # print value
            self.moves.stop()

Server = socketServer()
Server.run()
