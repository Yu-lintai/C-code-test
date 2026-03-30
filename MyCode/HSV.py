import cv2
import numpy as np

def on_trackbar_change(value):
    global lower_color, upper_color
    
    lower_color[0] = cv2.getTrackbarPos('Hue Min', 'Color Threshold')
    lower_color[1] = cv2.getTrackbarPos('Saturation Min', 'Color Threshold')
    lower_color[2] = cv2.getTrackbarPos('Value Min', 'Color Threshold')
    upper_color[0] = cv2.getTrackbarPos('Hue Max', 'Color Threshold')
    upper_color[1] = cv2.getTrackbarPos('Saturation Max', 'Color Threshold')
    upper_color[2] = cv2.getTrackbarPos('Value Max', 'Color Threshold')

cap = cv2.VideoCapture(1)  # Use 0 for default camera, or change to the desired camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create window and trackbars
cv2.namedWindow('Color Threshold')
cv2.createTrackbar('Hue Min', 'Color Threshold', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Min', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Min', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Hue Max', 'Color Threshold', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Max', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Max', 'Color Threshold', 0, 255, on_trackbar_change)

# Initialize color threshold values
lower_color = np.array([0, 0, 0])
upper_color = np.array([179, 255, 255])

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

    # Display the result
    cv2.imshow('Color Threshold', result)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
