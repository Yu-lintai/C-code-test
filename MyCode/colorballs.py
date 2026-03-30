import cv2
import numpy as np

# 定义白色圆形物体的颜色范围
lower_white = np.array([0, 0, 180])
upper_white = np.array([100, 40, 255])
lower_blue = np.array([100, 100, 60])
upper_blue = np.array([124, 255, 255])

# 打开摄像头
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    # 读取视频流的帧
    ret, frame = cap.read()

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 进行颜色阈值分割，提取白色圆形物体
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # 进行形态学操作，去除噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    # 寻找轮廓
    contours, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历每个轮廓
    for contour in contours:
        # 计算轮廓的面积和圆心坐标
        area = cv2.contourArea(contour)
        if 2300 < area < 3200:  # 控制最小面积阈值，排除噪声
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            center_white = center

            # 绘制圆和圆心
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
            # 绘制坐标（0，0）以及白色圆形物体和蓝色圆形物体坐标的直线
            #cv2.line(frame, center_blue, center_white, (255, 0, 0), 1)

            # 添加文字备注
            text = f"Color: White, Center: ({center[0]}, {center[1]})"
            cv2.putText(frame, text, (int(x - radius), int(y - radius - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    # 寻找轮廓
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历每个轮廓
    for contour in contours:
        # 计算轮廓的面积和圆心坐标
        area = cv2.contourArea(contour)
        if 1000 < area < 2900:  # 控制最小面积阈值，排除噪声
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            center_blue = center

            # 绘制圆和圆心
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
            # 绘制坐标（0，0）以及白色圆形物体和蓝色圆形物体坐标的直线
            #cv2.line(frame, (150, 100), center_blue, (255, 255, 255), 2)
            cv2.line(frame, center_blue, center_white, (255, 255, 255), 2)
            # 计算直线的斜率和截距
            if center_white[0] != center_blue[0]:
                slope = (center_white[1] - center_blue[1]) / (center_white[0] - center_blue[0])
                intercept = center_white[1] - slope * center_white[0]

                # 延伸直线，直到与y=60相交
                x_intersect = int((60 - intercept) / slope)
                cv2.line(frame, center_blue, (x_intersect, 60), (0, 255, 255), 2)
                cv2.line(frame,(640,660),(x_intersect,60),(0,255,255),2)

                # 绘制交点的坐标
                cv2.circle(frame, (x_intersect, 60), 5, (255, 255, 0), -1)

                # 添加文字备注
                text = f"Intersection: ({x_intersect}, 60)"


            # 添加文字备注
            text = f"Color: blue, Center: ({center_blue[0]}, {center_blue[1]})"
            cv2.putText(frame, text, (int(x - radius), int(y - radius - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    # 显示结果图像
    cv2.imshow("Object Detection", frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
