import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

mode = "normal"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    output = frame.copy()

    if mode in ["r", "g", "b"]:
        output[:] = 0
        ch = {"b": 0, "g": 1, "r": 2}[mode]
        output[:, :, ch] = frame[:, :, ch]

    if mode == "s":
        sx = cv2.Sobel(gray, cv2.CV_64F, 1,0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0,1, ksize=3)
        sob = cv2.bitwise_or(sx.astype(np.uint8), sy.astype(np.uint8))
        output = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)

    if mode == "c":
        output = cv2.Canny(gray, 100, 200)

    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Real-Time Face Detection", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key in [ord("r"), ord("g"), ord("b"), ord("s"), ord("c")]:
        mode = chr(key)
    elif key != 255:
        print("Invalid key. Use r g b s c or q")

cap.release()
cv2.destroyAllWindows()
