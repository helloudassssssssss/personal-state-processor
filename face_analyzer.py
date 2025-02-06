import cv2


print("OpenCV Version:", cv2.__version__)


# Load and display an image
img = cv2.imread("test.png")  # Make sure test.jpg exists
cv2.imshow("Test Image", img)
cv2.waitKey(0)  # Press any key to close the window
cv2.destroyAllWindows()
