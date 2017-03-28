import RPi.GPIO as GPIO
import pigpio
#import TDOA
from scipy.optimize import *
import numpy as np
import math
import time



pi = pigpio.pi()

if not pi.connected:
        exit()
 
GPIO.setmode(GPIO.BOARD)


GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #using pin 16, as a pull up / down 
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #using pin 18, as a pull up / down
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #using pin 22, as a pull up




Motor1A = 11 #input 2
Motor1B = 13 #input 1
Motor1E = 15 #enable
EncoderA = 38 #A channel
#EncoderB = 40 #B channel
#Index = 36 #Index channel

#setting up GPIO pins on the pi for the l293d motor driver and for the encoder 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(EncoderA,GPIO.IN)
#GPIO.setup(EncoderB,GPIO.IN)
#GPIO.setup(Index,GPIO.IN)


GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.HIGH) #turns motor on

currentpos = 0
Max = 18200.0
counter = 0
var = 0

counter = pi.callback(20)

#GPIO.add_event_detect(38, GPIO.RISING, callback = edgeCountA)


#position of mics in the first quadrant 12inch per side Triangle
offset = 1000.0
offset2 = 1000*10.0
A = (offset+12.0), offset+(math.sqrt(108)+6)
B = (offset+6.0), (offset+6.0)
C = (offset+18.0), (offset+6.0)

#center of triangle
center = offset+12.0, offset+9.46410162

#Speed of Sound in inches
speedSound = 13385.8 #inches/s



global stampArray1, stampArray2, stampArray3, stampArray
stampArray1 = []
stampArray2 = []
stampArray3 = []
stampArray = []



def stampA(channel): 
        GPIO.remove_event_detect(16) #remove detection
		temp1 = time.time(), A, "A"
		print "A"
        stampArray1.append(temp1)
        print "Mic A"

def stampB(channel):
        GPIO.remove_event_detect(18) #remove detection
		temp2 = time.time(), B, "B"
        stampArray2.append(temp2)
        print "Mic B"

def stampC(channel):
        GPIO.remove_event_detect(22) #remove detection
		temp3 = time.time(), C, "C"
        stampArray3.append(temp3)
        print "Mic C"
    
def calcTDiff():
        Bs = stampArray[1][0]-stampArray[0][0]
        Cs = stampArray[2][0]-stampArray[0][0]
        return Bs, Cs
        

def angleCalc(array): #passes in an array of numbers containing [x,y,r]
	xCenter=center[0]
	yCenter=center[1]
	x=math.fabs(xCenter-array[1]) #deals with offset
	y=math.fabs(yCenter-array[2]) #deals with offset
	h=distance(array[1],array[2],center[0],center[1])
	
	if array[1]>=xCenter and array[2]>=yCenter: #first quadrant
		return math.degrees(math.asin(y/h))
	elif array[1]<=xCenter and array[2]>=yCenter: #second quadrant
		return math.degrees(math.asin(x/h))+90.0
	elif array[1]<=xCenter and array[2]<=yCenter: #third quadrant
		return math.degrees(math.asin(y/h))+180.0
	elif array[1]>=xCenter and array[2]<=yCenter: #fourth quadrant
		return math.degrees(math.asin(x/h))+270.0

def func(z):
	r = z[0]
	x = z[1]
	y = z[2]
	F = np.zeros(3)
	
	F[0] = (ax-x)**2+(ay-y)**2-r**2
	F[1] = (bx-x)**2+(by-y)**2-(r+(speedSound*BTime))**2
	F[2] = (cx-x)**2+(cy-y)**2-(r+(speedSound*CTime))**2
	return F

def findSol(x1,x2,x3,x4):
	temp1 = x1[0], x1[1], x1[2]
	temp2 = x2[0], x2[1], x2[2]
	temp3 = x3[0], x3[1], x3[2]
	temp4 = x4[0], x4[1], x4[2]
	temp = temp1,temp2,temp3,temp4
	return sorted(temp)

def distance(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2+(y2-y1)**2)

def resetInterrupt():
        GPIO.add_event_detect(16, GPIO.RISING, callback = stampA)
        GPIO.add_event_detect(18, GPIO.RISING, callback = stampB)
        GPIO.add_event_detect(22, GPIO.RISING, callback = stampC)
        print "Listening"

def resetArray():
        stampArray = []
        stampArray1 = []
        stampArray2 = []
        stampArray3 = []



print "Enter in 1 to start listening, otherwise press anykey to exit: "
loop = input()
resetInterrupt()

#Motor
while (loop == 1):
        if(len(stampArray1) >= 1 and len(stampArray2) >= 1 and len(stampArray3) >= 1):

                stampArray.append(stampArray1[0])
                stampArray.append(stampArray2[0])
                stampArray.append(stampArray3[0])
                
                
                stampArray = sorted(stampArray)
                
                print "Organized Array --> ", stampArray[0]
                print "Organized Array --> ", stampArray[1]
                print "Organized Array --> ", stampArray[2]
                TempVar = calcTDiff()
                
                print " "
                print "Time of Bs: ", TempVar[0]
                print "Time of Cs: ", TempVar[1]
                print " "

                #pos of A
                ax = stampArray[0][1][0]
                ay = stampArray[0][1][1]
                #pos of B
                bx = stampArray[1][1][0]
                by = stampArray[1][1][1]
                #pos of C
                cx = stampArray[2][1][0]
                cy = stampArray[2][1][1]

                BTime = TempVar[0]
                CTime = TempVar[1]
                        

                x1 = fsolve(func, [offset2,offset2,1]) #first quadrant
                #print "#first quadrant[x,y,r]-->", x1
                x2 = fsolve(func, [0,offset2,1]) #second quadrant
                #print "#second quadrant[x,y,r]-->", x2
                x3 = fsolve(func, [0,0,1]) #third quadrant
                #print "#third quadrant[x,y,r]-->", x3
                x4 = fsolve(func, [offset2,0,1]) #fourth quadrant
                #print "#fourth quadrant[x,y,r]-->", x4

                arraySol = findSol(x1,x2,x3,x4)
                print "Calculated (x,y) position -->", "(", arraySol[3][1],",", arraySol[3][2], ")"
                print "Calculated \"r\" distance -->", arraySol[3][0]
                print "Alternate Solutions:"
                print arraySol[0]
                print arraySol[1]
                print arraySol[2]
                print arraySol[3]
                x = angleCalc(arraySol[3])

                print "The Angle is -->", x
                print " "  




                if currentpos < x :
                        angle = (abs(currentpos - x))
                if currentpos > x :
                        angle = 360 - abs(currentpos - x)
                counter.reset_tally()
                #print "Counter just after entering in an angle:", counter.tally()
                if angle >= 180.0 and angle <= 360.0:
                        print "Motor turning clockwise"
                        if (angle >= 180) :         
                                temp = 360.0 / (360 - angle)
                        else :
                                temp = 360 / angle
                        counter.reset_tally()
                        while counter.tally() < Max / temp:
                                GPIO.output(Motor1E,GPIO.HIGH)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.LOW)
                                #print "Pre-if Counter:", counter.tally()
                                if counter.tally() >= Max / temp:
                                        #print "Entered if statement tally:", counter.tally()
                                        counter.reset_tally()
                                        #print "After reset:", counter.tally()
                                        GPIO.output(Motor1A,GPIO.LOW)
                                        GPIO.output(Motor1B,GPIO.LOW)
                                        GPIO.output(Motor1E,GPIO.LOW)
                                        break
                                time.sleep(.01)
                                GPIO.output(Motor1B,GPIO.LOW)
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1E,GPIO.LOW)
                                time.sleep(.015)
                        currentpos = x
                elif angle <= 180.0 and angle >=0.0:
                        print "Motor turning counter-clockwise"	
                        temp = 360.0 / angle
                        while True : 
                                GPIO.output(Motor1E,GPIO.HIGH)
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                #print "Pre-if Counter:", counter.tally()
                                if counter.tally() >= Max / temp:
                                        #print "Entered if statement tally:", counter.tally()
                                        counter.reset_tally()
                                        #print "After reset:", counter.tally()
                                        GPIO.output(Motor1A,GPIO.LOW)
                                        GPIO.output(Motor1B,GPIO.LOW)
                                        GPIO.output(Motor1E,GPIO.LOW)
                                        break
                                time.sleep(.01)
                                GPIO.output(Motor1B,GPIO.LOW)
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1E,GPIO.LOW)
                                time.sleep(.015)
                        currentpos = x
                else :
                        break
                print "Enter in 1 to Listen again: "

                loop = input()
                resetArray()
                resetInterrupt()
                        
                        
         
print "Disabling motor"
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.LOW)
GPIO.cleanup()
        
#except KeyboardInterrupt :
 #       GPIO.output(Motor1A, GPIO.LOW)
 #       GPIO.output(Motor1B, GPIO.LOW)
  #      GPIO.output(Motor1E, GPIO.LOW)
   #     GPIO.cleanup()
