from scipy.optimize import *
import numpy as np
import matplotlib.pyplot as plt
import math

#position of mics in the first quadrant 12inch per side Triangle
A = (5012.0), 5000.0+(math.sqrt(108)+6)
B = (5006.0), (5006.0)
C = (5018.0), (5006.0)

#center of triangle
Centeroid = 5012.0, 5009.46410162 

#Speed of Sound in inches
speedSound = 13622.0 #inches/s
	
def calcTime(ordered):
	firstMicTime = ordered[0][0]/speedSound
	Bs = ordered[1][0]/speedSound - firstMicTime
	Cs = ordered[2][0]/speedSound - firstMicTime
	return Bs, Cs

def fun1(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (A[0]-x)**2.0+(A[1]-y)**2-r**2
	F[1] = (B[0]-x)**2+(B[1]-y)**2-(r+13622*time[0])**2
	F[2] = (C[0]-x)**2+(C[1]-y)**2-(r+13622*time[1])**2
	return F

def fun2(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (A[0]-x)**2.0+(A[1]-y)**2-r**2
	F[1] = (C[0]-x)**2+(C[1]-y)**2-(r+13622*time[0])**2
	F[2] = (B[0]-x)**2+(B[1]-y)**2-(r+13622*time[1])**2
	return F
	
def fun3(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (B[0]-x)**2.0+(B[1]-y)**2-r**2
	F[1] = (A[0]-x)**2+(A[1]-y)**2-(r+13622*time[0])**2
	F[2] = (C[0]-x)**2+(C[1]-y)**2-(r+13622*time[1])**2
	return F

def fun4(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (B[0]-x)**2.0+(B[1]-y)**2-r**2
	F[1] = (C[0]-x)**2+(C[1]-y)**2-(r+13622*time[0])**2
	F[2] = (A[0]-x)**2+(A[1]-y)**2-(r+13622*time[1])**2
	return F
	
def fun5(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (C[0]-x)**2.0+(C[1]-y)**2-r**2
	F[1] = (A[0]-x)**2+(A[1]-y)**2-(r+13622*time[0])**2
	F[2] = (B[0]-x)**2+(B[1]-y)**2-(r+13622*time[1])**2
	return F
	
def fun6(z, time):
	x = z[0]
	y = z[1]
	r = z[2]
	F = np.zeros(3)
	F[0] = (C[0]-x)**2.0+(C[1]-y)**2-r**2
	F[1] = (B[0]-x)**2+(B[1]-y)**2-(r+13622*time[0])**2
	F[2] = (A[0]-x)**2+(A[1]-y)**2-(r+13622*time[1])**2
	return F
def distance(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2+(y2-y1)**2)

def angleCalc(array): #passes in an array of numbers containing [x,y,r]
	xCenter=centeroid[0]
	yCenter=centeroid[1]
	x=math.fabs(xCenter-array[0]) #deals with offset
	y=math.fabs(yCenter-array[1]) #deals with offset
	h=distance(array[0],array[1],center[0],center[1])
	
	if array[0]>xCenter and array[1]>yCenter: #first quadrant
		print math.degrees(math.asin(x/h)), "degrees -->First Quadrant"
	elif array[0]<xCenter and array[1]>yCenter: #second quadrant
		print math.degrees(math.asin(x/h))+90.0, "degrees -->Second Quadrant"
	elif array[0]<xCenter and array[1]<yCenter: #third quadrant
		print math.degrees(math.asin(x/h))+180.0, "degrees -->Third Quadrant"
	elif array[0]>xCenter and array[1]<yCenter: #fourth quadrant
		print math.degrees(math.asin(x/h))+270.0, "degrees -->Fourth Quadrant"
	
def calcOrderMic(xpos,ypos):
	x = distance(xpos, ypos, A[0], A[1]), "A"
	y = distance(xpos, ypos, B[0], B[1]), "B"
	z = distance(xpos, ypos, C[0], C[1]), "C"
	temp = x,y,z
	return sorted(temp) #return in order closest mic in distance

def findFunc(ordered):
	
	
def mainTest():
	xpos = float(input("Enter an X position: "))
	ypos = float(input("Enter an Y position: "))
	ordered = calcOrderMic(xpos,ypos)
	time = calcTime(ordered)
	arraySol = fsolve(func(z,time), [1.0,1.0,1.0])
	angleCalc(arraySol)
	
mainTest()

