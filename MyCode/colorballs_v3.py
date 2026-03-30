import cv2
import numpy as np
import os

# 定义白色圆形物体的颜色范围
lower_white = np.array([0, 0, 170])
upper_white = np.array([75, 100, 255])
lower_blue = np.array([100, 90, 120])
upper_blue = np.array([112, 255, 255])

# 打开摄像头
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 設定拍照次數為照片文件命名做依據
photo_count = 0
photo_catch = False

while True:
    # 读取视频流的帧
    ret, frame = cap.read()

    cv2.imshow("real time picture", frame)

    # 按下 'p' 键进行拍照
    if cv2.waitKey(1) & 0xFF == ord('p'):
        # 将当前帧保存为照片
        photo = frame.copy()
        # 将照片的文件名设为"photo_数字.jpg"，其中数字是拍摄的照片数量
        photo_name = f"D:/billiards image/photo_{photo_count}.jpg"
        # 将照片保存到指定路径
        cv2.imwrite(photo_name , photo)
        # 将计数器变量加一
        photo_count += 1
        # 照片截取信息
        photo_catch = True
        # 打印提示信息
        print(f"Photo taken and saved as {photo_name}.")

        cv2.imshow("photo", photo)

        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)

        # 进行颜色阈值分割，提取白色圆形物体
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        # 进行形态学操作，去除噪声
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)


        # 尋找母球轮廓，即白球
        contours, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历每个轮廓
        for contour in contours:
            # 计算轮廓的面积和圆心坐标
            area = cv2.contourArea(contour)
            if 1200 < area < 3000:  # 控制最小面积阈值，排除噪声
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                center_white = center

                # 绘制圆和圆心
                cv2.circle(photo, center, radius, (0, 255, 0), 2)
                cv2.circle(photo, center, 3, (0, 0, 255), -1)
                # 绘制坐标（0，0）以及白色圆形物体和蓝色圆形物体坐标的直线
                #cv2.line(frame, center_blue, center_white, (255, 0, 0), 1)

                # 添加文字备注
                text = f"Color: White, Center: ({center[0]}, {center[1]})"
                cv2.putText(photo, text, (int(x - radius), int(y - radius - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


        # 寻找目標球轮廓，即藍球
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
                cv2.circle(photo, center, radius, (0, 255, 0), 2)
                cv2.circle(photo, center, 3, (0, 0, 255), -1)

                # 計算出撞擊折射點P
                point_x = ((640 - x) / 2 ) + x
                point_y = 650
                point_p = (int(point_x), int(point_y))
                

                # 绘制坐标（0，0）以及白色圆形物体和蓝色圆形物体坐标的直线
                cv2.line(photo, center_blue, point_p, (255, 255, 255), 2)
                cv2.line(photo, point_p, (640, 90), (255, 255, 255), 2)

                # 计算延长后的新端点坐标（假设延长200个像素）
                extension_length = 200
                dx = point_p[0] - center_blue[0]
                dy = point_p[1] - center_blue[1]
                extended_point2 = (center_blue[0] - extension_length * dx / np.sqrt(dx**2 + dy**2),
                                center_blue[1] - extension_length * dy / np.sqrt(dx**2 + dy**2))

                cv2.line(photo, center_blue, (int(extended_point2[0]), int(extended_point2[1])), (0, 0, 150), 2)

                # 在延长的线段上距离center_blue为50的地方绘制一个半径为26的圆形
                distance_to_center = 50
                angle = np.arctan2(extended_point2[1] - center_blue[1], extended_point2[0] - center_blue[0])
                circle_center = (int(center_blue[0] + distance_to_center * np.cos(angle)),
                                    int(center_blue[1] + distance_to_center * np.sin(angle)))

                cv2.circle(photo, circle_center, 26, (0, 0, 150), 2)
                
                # 标注圆心坐标
                text_offset = 15  # 调整这个值来控制文本的垂直偏移量
                text_position = (int(circle_center[0]), int(circle_center[1] - text_offset))
                text = f"Circle Center: {circle_center}"
                cv2.putText(photo, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # 繪製白球撞擊軌跡
                cv2.line(photo, center_white, circle_center, (0, 200, 0), 2)

                # 繪製并計算白球撞擊角度計算
                # 在图像上绘制经过 circle_center 并且垂直于 X 轴的直线
                vertical_line_point1 = (circle_center[0] , circle_center[1] - 100)  # 选择一个 x 坐标，可以根据需要调整
                vertical_line_point2 = (circle_center[0] , circle_center[1] + 100)  # 选择一个 x 坐标，可以根据需要调整
                cv2.line(photo, vertical_line_point1, vertical_line_point2, (0, 0, 255), 2)

                # 计算白球撞击轨迹直线的方向向量
                vector1 = np.array([circle_center[0] - center_white[0], circle_center[1] - center_white[1]])

                # 计算y = 0直线的方向向量，y = 0直线的方向向量是[0, 1]
                vector2 = np.array([0, 1])

                # 计算两个向量的点积
                dot_product = np.dot(vector1, vector2)

                # 计算两个向量的模
                magnitude_vector1 = np.sqrt(vector1[0]**2 + vector1[1]**2)
                magnitude_vector2 = np.sqrt(vector2[0]**2 + vector2[1]**2)

                # 计算夹角的弧度值
                cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)
                angle_radians = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

                # 将弧度值转换为角度值
                angle_degrees = np.degrees(angle_radians)

                # 在图像中标注夹角的角度
                angle_offset = 50  # 调整这个值来控制文本的垂直偏移量
                angle_position = (int(circle_center[0]) - angle_offset, int(circle_center[1] - angle_offset))
                angle_text = f"Angle: {angle_degrees:.2f} degrees"
                cv2.putText(photo, angle_text, angle_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # 添加文字备注
                text = f"Color: blue, Center: ({center_blue[0]}, {center_blue[1]})"
                cv2.putText(photo, text, (int(x - radius), int(y - radius - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    # 显示结果图像
    if photo_catch:
        cv2.imshow("Object Detection", photo)
        photo_name = f"D:/billiards image/photo_{photo_count}.jpg"
    # 按下 'esc' 键退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        # for i in range(photo_count):
        #         # 拼接照片的文件名
        #         photo_name = f"D:/billiards image/photo_{i}.jpg"
        #         # 删除照片文件
        #         os.remove(photo_name)
        #         # 打印提示信息
        #         print(f"Photo {photo_name} deleted.")
        break   

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()