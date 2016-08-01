###Code Version: 3.0
import os.path
import time
from gamepad import gamepadConnect
from server import IobyServer
#time.sleep(5)

if(os.path.exists('/dev/gamepad')):
	print "gamepad"
	gamepad = gamepadConnect()
	gamepad.run()
else:
    print "SocketServer"
    socketServer = IobyServer()
    socketServer.run()
