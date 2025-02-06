import cv2 as cv
print("OpenCV Version:", cv.__version__)


# Load and display an image
# img = cv.imread("images/test.png")  # Make sure test.jpg exists
# cv.imshow("Test Image", img) #name of the window, and type of file
# cv.waitKey(0)  # Press any key to close the window

#reading videos 
capture = cv.VideoCapture('videos/test_chamber.mp4') #numer reference the camera number

while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'): #if press d, destroy the window
        break

capture.release()

cv.destroyAllWindows()

