import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(0)

ret, frame = vid.read()

# Display the resulting frame
cv2.imwrite("test.jpg", frame)

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
