import RPi.GPIO as GPIO
from time import sleep

# constants
FREQ = 100 # Hz
START_X = 10
START_Y = 10
STEP = 0.5

class Servo:

    def __init__(self, GPIO_SERVO_X = 12, GPIO_SERVO_Y = 13):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_SERVO_X, GPIO.OUT)
        GPIO.setup(GPIO_SERVO_Y, GPIO.OUT)
        self.pwm_x = GPIO.PWM(GPIO_SERVO_X, FREQ)
        self.pwm_y = GPIO.PWM(GPIO_SERVO_Y, FREQ)
        self.pwm_x.start(0)
        self.pwm_y.start(0)

    def update_motors(self):

        self.pwm_x.ChangeDutyCycle(self.m_x)
        self.pwm_y.ChangeDutyCycle(self.m_y)
        print("X : %3f, Y : %3f" % (self.m_x, self.m_y))

    def starting_position(self):
        self.m_x = START_X
        self.m_y = START_Y

    def cleanup(self):
        self.pwm_x.stop()
        self.pwm_y.stop()
        GPIO.cleanup()

    def using_keys(self):

        while True:
            inp = input()
            if inp   == 'a': self.m_x += STEP
            elif inp == 'd': self.m_x -= STEP
            elif inp == 'w': self.m_y -= STEP
            elif inp == 's': self.m_y += STEP
            elif inp == 'e': self.starting_position()
            elif inp == 'q': break

            self.update_motors()

