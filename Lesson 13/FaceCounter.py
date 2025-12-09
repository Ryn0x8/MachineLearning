import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Sorry Couldnot open the camera!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not captUre the image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30,30))
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"People Count: {len(faces)}", (10,30), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.imshow("Face Tracking and Counting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

