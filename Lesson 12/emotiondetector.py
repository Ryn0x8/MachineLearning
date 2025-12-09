import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("emotion_model.h5")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

emotion_models = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'suprise']

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48,48))
        roi_gray = roi_gray.astype("float") / 255.0
        roi_gray = np.expand_dims(roi_gray, 0)
        roi_gray = np.expand_dims(roi_gray, -1)
        pred = model.predict(roi_gray)
        emo = emotion_models[np.argmax(pred)]
        cv2.putText(frame, emo, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)

    cv2.imshow("Emotion Detector (Press 'q' to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera Closed. Program ended")
