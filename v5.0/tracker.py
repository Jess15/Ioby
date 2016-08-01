import cv2, math
import numpy as np
import os
import time
from moves import Move
class ColourTracker(Move):
    def __init__(self):
	self.pid = os.getpid()
	self.moves = Move()
	if(self.pid != 0):
		f = open("TrackerPid.txt","w")
		f.write(str(self.pid))
		f.close()
        #cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
        self.capture = cv2.VideoCapture(0)
        self.scale_down = 4
    def run(self):
        while True:
            f, orig_img = self.capture.read()
            orig_img = cv2.flip(orig_img, 1)

            #Creo Filtros
            img = cv2.GaussianBlur(orig_img, (5,5), 0)
            img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
            img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))

            #Establesco colores a Filtrar
            gren_lower = np.array([10, 40, 100])
            gren_upper = np.array([10, 255, 255])

            #Inicio los Filtros
            gren_binary = cv2.inRange(img, gren_lower, gren_upper)
            dilation = np.ones((15, 15), "uint8")
            gren_binary = cv2.dilate(gren_binary, dilation)

            #Obtengo contornos
            contours, hierarchy = cv2.findContours(gren_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            largest_contour = None

            for idx, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    largest_contour = contour
            if not largest_contour == None:
                moment = cv2.moments(largest_contour)
                if moment["m00"] > 1000 / self.scale_down:
                    rect = cv2.minAreaRect(largest_contour)

                    #Genero un ciruclo de enfoque
                    (x,y),radius = cv2.minEnclosingCircle(contour)
                    x = rect[0][0] * self.scale_down
                    y = rect[0][1] * self.scale_down
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(orig_img,center,radius,(0,255,0),2)
                    #Muestro el resultado
                    #cv2.imshow("ColourTrackerWindow", orig_img)

                    #En Base a X giro hacia un lado u otro
	            print x
                    if(x>100):
                        print("giro a la izquierda")
			self.moves.left(25)
			time.sleep(0.5)
			self.moves.stop()
			time.sleep(1)
                    else:
                        if(x<70):
                            print("giro a la derecha")
			    self.moves.right(25)
			    time.sleep(0.5)
			    self.moves.stop()
			    time.sleep(1)
                        else:
                            print("centrado")
			    self.moves.stop()
			    self.moves.forward(25)
			    time.sleep(0.5)
		   	    self.moves.stop()
			    time.sleep(1)	
                    if cv2.waitKey(20) == 27:
                        #cv2.destroyWindow("ColourTrackerWindow")
                        self.capture.release()
                        break
if __name__ == "__main__":
    colour_tracker = ColourTracker()
    colour_tracker.run()
