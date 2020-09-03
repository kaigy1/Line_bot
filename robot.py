import RPi.GPIO as GPIO
import time
import cv2
import sys
import numpy as np

clockwise = 10
anticlockwise = 5

wheel_l=22
wheel_r=18

camera=picamera.PiCamera()



GPIO.setmode(GPIO.BOARD)

GPIO.setup(wheel_l, GPIO.OUT)
GPIO.setup(wheel_r, GPIO.OUT)


L_MOTOR = GPIO.PWM(wheel_l, 50)
R_MOTOR = GPIO.PWM(wheel_r, 50)



def cameraAlgorithm():
    camera.capture('/home/pi/magic/sonic%s.jpg' % i)
    image = cv2.imread('/home/pi/magic/sonic%s.jpg' % i)
    
    image = cv2.resize(image,(640,640),interpolation=cv2.INTER_AREA)
    v = np.median(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    ret, Bimage = ret, thresh2 = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
    lower = int(max(0, (1.0 - 0.45) * v))
    upper = int(min(255, (1.0 + 0.45) * v))
    edged = cv2.Canny(Bimage, 40, 80)
    
    small = cv2.resize(Bimage,(128,128),interpolation=cv2.INTER_AREA)
    
    lines = cv2.HoughLinesP(Bimage, 1, np.pi/200, threshold = 25, minLineLength = 20, maxLineGap = 10)
    colorededge = cv2.cvtColor(Bimage, cv2.COLOR_GRAY2RGB)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            linedimg = cv2.line(colorededge, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #get the longest line
    longest = 0
    lx1 = 0
    mx1 = 0
    lx2 = 0
    mx2 = 0
    ly1 = 0
    ly2 = 0
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if(y2 - y1) > longest:
                longest = y2 - y1
                ly1 = y1
                ly2 = y2
                lx1 = x1
                lx2 = x2
    mx2 = lx2 - lx1
    for line in lines:
        for x1, y1, x2, y2 in line:
            if(x1 - lx1) > 50:
                mx1 = (x1 + lx1)/2 #find the midway point
                break
    mx2 = (mx1 + mx2)
    
    avglineimg = cv2.line(colorededge, (int(lx1), int(ly1)), (int(lx2), int(ly2)), (255, 0, 0), 2)
    avglineimg = cv2.line(colorededge, (int(mx1), int(ly1)), (int(mx2), int(ly2)), (0, 255, 0), 2)
    avglineimg = cv2.line(colorededge, (int(mx1 + 10), int(ly1)), (int(mx2 + 10), int(ly2)), (0, 255, 2), 2)
                   
    
    file = 'sImage%s.jpg' % i
    cv2.imwrite(file, avglineimg)
    u = mx1-mx2
    return u



def MotorsSetup():

    L_MOTOR.start(1)
    R_MOTOR.start(1)

def foward():
    L_MOTOR.ChangeDutyCycle(10)
    R_MOTOR.ChangeDutyCycle(5)
    time.sleep(0.03)

def turn_Left():
    L_MOTOR.ChangeDutyCycle(5)
    R_MOTOR.ChangeDutyCycle(5)
    time.sleep(0.03)


def turn_Right():
    L_MOTOR.ChangeDutyCycle(10)
    R_MOTOR.ChangeDutyCycle(10)
    time.sleep(0.03)

def Stop():
    time.sleep(10)



def control(angle):
  if(angle<1 or angle>-1):
    foward()
  if(angle <= -1):
    turn_Left()
  if(angle >= 1):
    turn_Right()


#MAin
try:
  MotorsSetup()
  controlVariable=90
  #camera.start_preview()
  camera.start_recording("testsddd.h264")
  for in range(10):
    u = cameraAlgorithm()
    control(u)
    sleep(.5)
  camera.stop_recording("testsddd.h264")


except KeyboardInterrupt:
  print("shutting down")
