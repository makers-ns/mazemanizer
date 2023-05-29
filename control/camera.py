import cv2 as cv
import time 
  
# define a video capture object
vid = cv.VideoCapture(0)

#while True:

ret, frame = vid.read()
if ret == True:
    cv.imwrite("images/s.jpg", frame)
    print('New image written!')
else:
    print('Camera error: %d' % ret)
time.sleep(3)

# After the loop release the cap object
vid.release()
