#OPENCV를 활용한 움직임 감지하여 차단기 자동 제어
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pigpio
import time
import RPi.GPIO as GPIO

survo = 27 # survo


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


count = 0
pi = pigpio.pi()
angle = 0

 

pi.set_servo_pulsewidth(survo,(angle * 2000 / 18) + 500)

 


def mse(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)

    err /= float(imageA.shape[0] * imageA.shape[1])

 

    return err

 

count_image = 0

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

cv2.imwrite('original.jpg', frame)

cap.release()

original_image = cv2.imread('original.jpg')

original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

while 1:

    count_image +=1

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    cv2.imwrite('compare.jpg', frame)

    cap.release()

    compare_image = cv2.imread('compare.jpg')

    compare_image = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)

    mse_value = mse(original_image, compare_image)

    if mse_value > 400:

        print("succese")

       

        angle +=9

 

        print("Open")

 

        time.sleep(0.1)

 

    elif mse_value < 250:

 

        angle -=9

 

    else:

 

        print("Close")

 

        angle = 0

 

    if angle<0:

 

        angle =0

 

    elif angle>9:

 

        angle =9

  

    pi.set_servo_pulsewidth(survo,(angle *2000 / 18+500))

    time.sleep(0.1)

 

 
    if count_image >10:

        original_image = compare_image

        cv2.imwrite('original.jpg', original_image)

