import socket
import pygame
import time
from colorama import Fore
pygame.init()
pygame.joystick.init()


def sendData(isOk,flag):
    #print isOk
    if (isOk == "on"):

        print "Send 'exit' for close, 'help' for instructions."

        while flag:

            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()

                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                         #arriba y abajo
                        if(event.axis==1):
                            axis = joystick.get_axis(1)
                            value = axis * -100
                            peer = str(event.axis)+":"+str(int(value))+":"
                            if (value > 0):
                                print Fore.GREEN + "Acelero"
#                               time.sleep(0.5)
                                s.send(peer)
                                print Fore.RESET + peer
                            elif (value < 0):
                                print Fore.GREEN + "Desacelero"
#                                time.sleep(0.5)
                                s.send(peer)
                                print Fore.RESET + peer
                            else:
                                print Fore.RED + "Value", str(value)
#                               time.sleep(0.5)
                                s.send(peer)
                                print peer

                        #derecha y izq
                        if(event.axis==2):

                            axis = joystick.get_axis(2)
                            value = axis * 100
                            peer = str(event.axis)+":"+str(int(value))+":"

                            if (value > 0):
                                print Fore.GREEN + "Derecha"
#                               time.sleep(0.5)
                                s.send(peer)
                                print peer
                            elif (value < 0):
                                print Fore.GREEN + "Izquierda"
#                               time.sleep(0.5)
                                s.send(peer)
                                print peer
                            else:
                                print Fore.RED + "Value", str(value)
#                               time.sleep(0.5)
                                s.send(peer)
                                print peer

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
            s.close()

try:
    flag = True
    isOk = ""
    s = socket.socket()
    host = "192.168.1.35"  # "192.168.1.252"
    port = 2608 #2602
    s.connect((host, port))
    data = s.recv(1024)
    empty = "empty"
    passwd = raw_input(data)
    if (not passwd):
        passwd = empty

    s.send(passwd)
    isOk = ""+s.recv(1024)
    isOK=isOk.replace('\n','')
    print isOk

    sendData(isOk,flag);

except:
    print "Connection Error"
    flag = 0


