#서브모터이용한 4족 보행 
import pigpio
import time
import RPi.GPIO as GPIO

servoFR = 23 #front right
servoFL = 24 #front left
servoBR = 27 #back right 
servoBL = 22 #back left
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # move butt
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # rest butt
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # off butt
GPIO.setup(19,GPIO.OUT) # rest state LED
GPIO.setup(26,GPIO.OUT) # move state LED
           
count = 0 # button count
# print(GPIO.input(5)) # butt test
# print(GPIO.input(6)) # butt test
# print(GPIO.input(13)) # butt test
pi = pigpio.pi()
angle = 0 #servomoter move angle
# angle1 = 0 #for test
# servo_pulsewidth must be 500(0 degree) ~ 2500(180 degree)
# initialize pulsewidth
pi.set_servo_pulsewidth(servoFR, (angle * 2000 / 18) + 500)
pi.set_servo_pulsewidth(servoFL, (angle * 2000 / 18) + 500)
pi.set_servo_pulsewidth(servoBR, (angle * 2000 / 18) + 500)
pi.set_servo_pulsewidth(servoBL, (angle * 2000 / 18) + 500)

while True:
    goState = GPIO.input(5)
    restState = GPIO.input(6)
    offState = GPIO.input(13)
    if restState == True: # rest button pressed
        goState = False
        angle = 0
        count = 0
        GPIO.output(19, True) #rest led on
        GPIO.output(26, False) # go led off
        print("Resting! ")
        time.sleep(0.5)
    
    if goState == True: # go button pressed
        angle += 5
        count = count + 1
        GPIO.output(19, False) #rest led off
        GPIO.output(26, True) # go led on
        print("MovingCount =", count)
        time.sleep(0.5)
        time.sleep(0.1)
    
    if offState == True: # off button pressed
        angle = 0
        count = 0
        GPIO.output(19, False) #rest led on
        GPIO.output(26, False) # go led off
        print("Robot OFF!")
        time.sleep(0.5)
    
    # Change Servo angle if degree is over 140 / under 30
    if angle < 0:
        angle = 14
    elif angle > 14:
        angle = 0
    
    # Move ServoMotor
    # Changed value "angle" insert to servo
    pi.set_servo_pulsewidth(servoFR, (angle * 2000 / 18) + 500)
    pi.set_servo_pulsewidth(servoFL, (angle * 2000 / 18) + 500)
    pi.set_servo_pulsewidth(servoBR, (angle * 2000 / 18) + 500)
    pi.set_servo_pulsewidth(servoBL, (angle * 2000 / 18) + 500)
