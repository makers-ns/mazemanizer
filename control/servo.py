import RPi.GPIO as GPIO
from time import sleep

SERVO_X = 12
SERVO_Y = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_X, GPIO.OUT)
GPIO.setup(SERVO_Y, GPIO.OUT)

pwm_x = GPIO.PWM(SERVO_X, 50)
pwm_x.start(0)

pwm_y = GPIO.PWM(SERVO_Y, 50)
pwm_y.start(0)

i = 0 

yaw = 72 # mapped to 0
roll = 82 # mapped to 0
def set_angle(angle, SERVO=SERVO_X, pwm=pwm_x):
    duty = angle / 18 + 2
    GPIO.output(SERVO, True)

    pwm.ChangeDutyCycle(duty)

    sleep(0.3)
    
    GPIO.output(SERVO, False)
	
    pwm.ChangeDutyCycle(0)

def loopl():
    while True:
        set_angle(75, SERVO_X, pwm_x)
        set_angle(82, SERVO_Y, pwm_y)
        sleep(0.1)
        set_angle(105, SERVO_X, pwm_x)
        set_angle(112, SERVO_Y, pwm_y)

        setAngle(45, SERVO_X, pwm_x)
        setAngle(52, SERVO_Y, pwm_y)


def starting_position():
    set_angle(48, SERVO_X, pwm_x)
    set_angle(82, SERVO_Y, pwm_y)

def using_keys():
    global yaw, roll
    while True:
        inp = input()
        if inp == 'a':
            yaw -= 6
            #setAngle(yaw, SERVO_X, pwm_x)
        elif inp == 'd':
            yaw += 6
            #setAngle(yaw, SERVO_X, pwm_x)
        elif inp == 'w':
            roll += 6
            #setAngle(roll, SERVO_Y, pwm_y)
        elif inp == 's':
            roll -= 6
            #setAngle(roll, SERVO_Y, pwm_y)
    
        print(f"{roll=} {yaw=}")
    

        for _ in range(0, 4):
            if inp in ['a', 'd']:
                set_angle(yaw, SERVO_X, pwm_x)
            elif inp in ['w', 's']:
                set_angle(roll, SERVO_Y, pwm_y)

def cleanup():
    pwm_x.stop()
    pwm_y.stop()
    GPIO.cleanup()


if __name__ == "__main__":

    starting_position()
    using_keys()
