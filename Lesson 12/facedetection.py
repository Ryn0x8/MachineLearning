import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
if not cap:
    print("Error: Could not open camera!")
    exit()

print("Camera has opened. Press q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error Failed to capture.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        frame, 1.1, 5, minSize=(30,30)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0,0), 2)
        cv2.putText(frame, "Face", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
        cv2.imshow("Real-Time Face Detection (Press 'q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("Camera Closed. Program ended")
