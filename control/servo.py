import RPi.GPIO as GPIO
from time import sleep

# global pinout
GPIO_SERVO_X = 12
GPIO_SERVO_Y = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_SERVO_X, GPIO.OUT)
GPIO.setup(GPIO_SERVO_Y, GPIO.OUT)
 # 50 Hz 
pwm_x = GPIO.PWM(GPIO_SERVO_X, 100)
pwm_y = GPIO.PWM(GPIO_SERVO_Y, 100)
pwm_x.start(0)
pwm_y.start(0)

def starting_position():
    pwm_x.ChangeDutyCycle(10)
    pwm_y.ChangeDutyCycle(10)

def using_keys():
    global x
    x = 10
    global y
    y = 10
    while True:
        inp = input()
        if inp == 'a':
            x += 2
            pwm_x.ChangeDutyCycle(x)
        elif inp == 'd':
            x -= 2
            pwm_x.ChangeDutyCycle(x)
        elif inp == 'w':
            y -= 2
            pwm_y.ChangeDutyCycle(y)
        elif inp == 's':
            y += 2
            pwm_y.ChangeDutyCycle(y)
        elif inp == 'q':
            break

        print("X : %3d, Y : %3d" % (x, y))


def cleanup():
    pwm_x.stop()
    pwm_y.stop()
    GPIO.cleanup()

if __name__ == "__main__":

    starting_position()
    print("start")

    using_keys()
    cleanup()