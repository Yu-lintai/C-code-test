import cv2
import numpy as np

def on_trackbar_change(value):
    global lower_color, upper_color
    
    lower_color[0] = cv2.getTrackbarPos('Hue Min', 'Trackbars')
    lower_color[1] = cv2.getTrackbarPos('Saturation Min', 'Trackbars')
    lower_color[2] = cv2.getTrackbarPos('Value Min', 'Trackbars')
    upper_color[0] = cv2.getTrackbarPos('Hue Max', 'Trackbars')
    upper_color[1] = cv2.getTrackbarPos('Saturation Max', 'Trackbars')
    upper_color[2] = cv2.getTrackbarPos('Value Max', 'Trackbars')

cap = cv2.VideoCapture(1)  # Use 0 for default camera, or change to the desired camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create window for trackbars
cv2.namedWindow('Trackbars')
cv2.createTrackbar('Hue Min', 'Trackbars', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Min', 'Trackbars', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Min', 'Trackbars', 0, 255, on_trackbar_change)
cv2.createTrackbar('Hue Max', 'Trackbars', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Max', 'Trackbars', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Max', 'Trackbars', 0, 255, on_trackbar_change)

# Initialize color threshold values
lower_color = np.array([0, 0, 0])
upper_color = np.array([179, 255, 255])

# Create window for displaying camera feed
cv2.namedWindow('Camera Feed')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbar values
    on_trackbar_change(0)

    # Apply color thresholding
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the result in the camera feed window
    cv2.imshow('Camera Feed', result)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the windows
cap.release()
cv2.destroyAllWindows()
