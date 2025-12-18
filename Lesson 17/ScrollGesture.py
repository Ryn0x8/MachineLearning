import cv2, pyautogui, time
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7
)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
finger_tips = [4, 8, 12, 16, 20]
last_scroll_time = time.time()
def count_fingers(hand_landmarks):
    finger = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        finger +=1

    for tip in finger_tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            finger +=1

    return finger

while True:
    ret, frame = cap.read()
    if  not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            if time.time() - last_scroll_time >0.4:
                if fingers_up >= 4:
                    pyautogui.scroll(400)
                    cv2.putText(frame, "OPEN-HANDS (Scrolling Up)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                elif fingers_up == 0:
                    pyautogui.scroll(-400)
                    cv2.putText(frame, "CLOSED-FISTS (Scrolling Down)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                last_scroll_time = time.time()
    cv2.imshow("Scroll Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()