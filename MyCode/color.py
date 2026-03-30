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

    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    result = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Color Threshold', result)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FPS, 30)
ret, frame = cap.read()


# 读取输入图像
#image = cv2.imread('D:\python_code\my_code\color1.jpg')
image = frame
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 创建窗口和滑动条
cv2.namedWindow('Color Threshold')
cv2.createTrackbar('Hue Min', 'Color Threshold', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Min', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Min', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Hue Max', 'Color Threshold', 0, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Max', 'Color Threshold', 0, 255, on_trackbar_change)
cv2.createTrackbar('Value Max', 'Color Threshold', 0, 255, on_trackbar_change)

# 初始化颜色阈值
lower_color = np.array([0, 0, 0])
upper_color = np.array([179, 255, 255])

while True:
    # 获取滑动条的当前值
    on_trackbar_change(0)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放窗口
cv2.destroyAllWindows()
