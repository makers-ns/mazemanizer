#include <Servo.h>

Servo servoX;
Servo servoY;

#define ANGLE_MIN 50
#define ANGLE_MAX 130
#define OFFSET_X 0
#define OFFSET_Y 20
#define ANGLE_MID (ANGLE_MAX - ((ANGLE_MAX - ANGLE_MIN) / 2.0))
#define STEP 10
#define INC_WAIT 0 //ms
#define STEP_WAIT 1300 //ms

void setup() 
{
  servoX.attach(0);
  servoY.attach(16);
  Serial.begin(9600);
}

void writeServo(int x, int y, int wait)
{
  servoX.write(OFFSET_X + x);
  servoY.write(OFFSET_Y + y);
  Serial.print(x);
  Serial.print(", ");
  Serial.println(y);
  if(wait) delay(wait);  
}

void crazy()
{
  for(int i = ANGLE_MID; i > ANGLE_MIN; i -= STEP) writeServo(i, ANGLE_MAX - i + ANGLE_MIN, INC_WAIT); delay(STEP_WAIT);
  for(int i = ANGLE_MIN; i < ANGLE_MAX; i += STEP) writeServo(i, ANGLE_MAX - i + ANGLE_MIN, INC_WAIT); delay(STEP_WAIT);
  for(int i = ANGLE_MAX; i > ANGLE_MIN; i -= STEP) writeServo(i, ANGLE_MAX - i + ANGLE_MIN, INC_WAIT); delay(STEP_WAIT);
  for(int i = ANGLE_MIN; i < ANGLE_MID; i += STEP) writeServo(i, ANGLE_MAX - i + ANGLE_MIN, INC_WAIT); delay(STEP_WAIT);
}

void stop()  { writeServo(ANGLE_MID, ANGLE_MID, INC_WAIT);                   }
void up()    { writeServo(ANGLE_MID, ANGLE_MIN, INC_WAIT); delay(STEP_WAIT); }
void down()  { writeServo(ANGLE_MID, ANGLE_MAX, INC_WAIT); delay(STEP_WAIT); }
void left()  { writeServo(ANGLE_MIN, ANGLE_MID, INC_WAIT); delay(STEP_WAIT); }
void right() { writeServo(ANGLE_MAX, ANGLE_MID, INC_WAIT); delay(STEP_WAIT); }

void loop() 
{
  // Green -> Red
  right();
  up();
  left();
  down();
  right();
  up();
  left();
  down();
  right();
  up();
  stop();
  delay(STEP_WAIT);

  // Red - Green
  down();
  left();
  up();
  right();
  down();
  left();
  up();
  right();
  down();
  left();
  delay(STEP_WAIT);

}