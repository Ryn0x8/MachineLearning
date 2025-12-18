import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()

cx, cy = 250, 250
size = 30
color = (0, 255, 0)
prev_center = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, 2)
    mask = cv2.dilate(mask, kernel, 2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 5000:
            cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)

            M = cv2.moments(cnt)
            if M["m00"] != 0:
                hand_x = int(M["m10"] / M["m00"])
                hand_y = int(M["m01"] / M["m00"])

                if prev_center is not None:
                    dx = hand_x - prev_center[0]
                    dy = hand_y - prev_center[1]
                    if abs(dx) > abs(dy):
                        cx += 15 if dx > 0 else -15
                    else:
                        cy += 15 if dy > 0 else -15

                prev_center = (hand_x, hand_y)

            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)

            finger_count = 0
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])

                    a = math.dist(start, end)
                    b = math.dist(start, far)
                    c = math.dist(end, far)
                    angle = math.acos((b*b + c*c - a*a) / (2*b*c)) * 57

                    if angle <= 90:
                        finger_count += 1
                        cv2.circle(roi, far, 5, (0, 0, 255), -1)

            finger_count += 1

            if finger_count == 1:
                color = (0, 0, 255)
            elif finger_count == 2:
                color = (0, 255, 0)
            elif finger_count == 3:
                color = (255, 0, 0)
            elif finger_count == 5:
                size = min(100, size + 2)
            elif finger_count == 4:
                size = max(20, size - 2)

            cv2.putText(frame, f"Fingers: {finger_count}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        prev_center = None

    cx = max(size, min(frame.shape[1] - size, cx))
    cy = max(size, min(frame.shape[0] - size, cy))

    cv2.circle(frame, (cx, cy), size, color, -1)

    cv2.imshow("Gesture Control", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
