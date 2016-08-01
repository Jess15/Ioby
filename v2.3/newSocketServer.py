import socket
from newMove import Move
moves = Move()
moves.stop()
flag = True

try:
    s = socket.socket()
    host = "0.0.0.0"
    port = 2608

    s.bind((host, port))
    s.listen(1)
    print "Server up"

except:
    print "Server Error"

while True:

    sc, addr = s.accept()

    print "Received Connection from: " + str(addr[0]) + ":" + str(addr[1])
    sc.send("Password: \n")
    passwd = sc.recv(1024)
    if(passwd == "bop"):

        sc.send("on")

        while flag:
            data = sc.recv(1024)
            rcvData = data.split(":")
            axi = int(rcvData[0])
            value = int(rcvData[1])

            if(data == "exit"):
                print data
                print "Closing..."
                flag = False
                moves.exit()
                sc.close()

            elif (data == "help"):
                print data
                helps = "Instructions:\n Use the left axis for forward and backward movements, and the right axis for laterals movements."
                sc.send(helps)

            else:
                #print data
                print "Received: ", rcvData[0], ":", rcvData[1]
		if(axi == 1):
                    if(value > 0):
                        print value
                        moves.stop()
                        moves.forward(value)
                    elif(value < 0):
                        print value
			value = (value * -1);			
                        moves.stop()
                        moves.backward(value)
                    else:
                        print value
                        moves.stop()

                elif(axi == 2):
                    if(value > 0):
                        print value
                        moves.directionalStop()
                        moves.right(value)
                    elif(value < 0):
                        print value
			value = (value * -1);
                        moves.directionalStop()
                        moves.left(value)
                    else:
                        print value
                        moves.stop()

                else:
                    pass
                    moves.stop()
    else:
        f = open("./logs/loginError.txt", "a")
        f.write(addr[0] + ":" + passwd + "\n")
        f.close()
        #moves.exit()
        sc.send("off")
        sc.close()
