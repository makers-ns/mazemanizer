import cv2 as cv
  
  
# define a video capture object
vid = cv.VideoCapture(0)

ret, frame = vid.read()

# Display the resulting frame
cv.imwrite("test.jpg", frame)

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
