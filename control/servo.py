from gpiozero import Servo
from time import sleep

SERVO_PORT = 25
servo = Servo(SERVO_PORT)

try:
    while True:
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
except:
	print("Program stopped")