import cv2 
import numpy as np
import math

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read the frame.")
        break

    frame = cv2.flip(frame, 1)

    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100,100), (400,400), (0,255,0), 2)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0,20, 70], dtype = np.uint8)
    upper_skin = np.array([20,255,255], dtype = np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations = 2)
    mask = cv2.dilate(mask, kernel, iterations = 2)
    mask = cv2.GaussianBlur(mask, (5,5), 0)

    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = max(contours, key = cv2.contourArea)
        if cv2.contourArea(cnt)> 5000:
            cv2.drawContours(roi, [cnt], -1, (0,255,0), 2)
            hull = cv2.convexHull(cnt, returnPoints = False)
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
                    angle = math.acos((b*b + c*c - a*a) /(2*b*c)) * 57
                    if angle<=90:
                        finger_count +=1
                        cv2.circle(roi, far, 5, (0,0,255), -1)

                    cv2.line(roi, start, end, (255,0,0), 2)

            finger_count+=1

            if finger_count == 1:
                gesture = "ONE"
            elif finger_count == 2:
                gesture = "TWO"
            elif finger_count == 3:
                gesture = "THREE"
            elif finger_count == 4:
                gesture = "FOUR"
            elif finger_count == 5:
                gesture = "FIVE"
            else:
                gesture = "Unknown"

            cv2.putText(frame, f"Fingers: {finger_count}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)
            cv2.putText(frame, f"Gesture: {gesture}", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0, 0), 2)

    cv2.imshow("Gesture Control", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
