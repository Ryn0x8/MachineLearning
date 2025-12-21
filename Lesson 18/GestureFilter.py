import numpy as np
import mediapipe as mp
import cv2
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_tracking_confidence = 0.7, min_detection_confidence = 0.7)

FILTERS = [None, "SEPIA", "NEGATIVE", "BLUR", "GRAYSCALE"]
current_filter = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

last_action_time = 0
debounce_time = 1
pinch_in_progress = False
capture_requested = False

def apply_filter(frame, filter_type):
    if filter_type == "SEPIA":
        kernel = np.array([[0.272, 0.534, 0.131], 
                            [0.349, 0.686, 0.168], 
                           [0.393, 0.769, 0.189]])
        return cv2.transform(frame, kernel)
    elif filter_type == "NEGATIVE":
        return cv2.bitwise_not(frame)
    elif filter_type == "BLUR":
        return cv2.GaussianBlur(frame, (15,15), 0)
    elif filter_type == "GRAYSCALE":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    img = cv2.flip(img, 1)
    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    capture_requested = False
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            tips = {name: (int(lm[idx].x * w), int(lm[idx].y * h)) 
                        for name, idx in {
                            'thumb': mp_hands.HandLandmark.THUMB_TIP,
                            'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
                            'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                            'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
                            'pinky': mp_hands.HandLandmark.PINKY_TIP
                        }.items()
                    }
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
            for i, (name, (x,y)) in enumerate(tips.items()):
                cv2.circle(img, (x,y), 10, colors[i], cv2.FILLED)

            thumb_x, thumb_y = tips['thumb']
            index_x, index_y = tips['index']
            current_time = time.time()
            pinch = abs(thumb_x-index_x) <30 and abs(thumb_y - index_y) < 30
            if pinch and not pinch_in_progress:
                pinch_in_progress = True
                capture_requested = True
            
            if not pinch and pinch_in_progress:
                pinch_in_progress = False
            elif any(abs(thumb_x - tips[finger][0]) < 40 and abs(thumb_y - tips[finger][1]) < 40 
                     for finger in ['middle', 'ring', 'pinky']):
                if current_time - last_action_time > debounce_time:
                    last_action_time = current_time
                    current_filter = (current_filter + 1) % len(FILTERS)
                    print(f"Filter changed to: {FILTERS[current_filter] or None}")

            break
    
    filtered_img = apply_filter(img, FILTERS[current_filter])
    display_img = filtered_img if FILTERS[current_filter] != "GRAYSCALE" else cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)

    if capture_requested:
        cv2.putText(display_img, "PICTURE CAPTURED", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
        ts = int(time.time())
        filename = f"capture_{ts}.png"
        cv2.imwrite(filename, filtered_img)
        print(f"Picture saved as {filename}")
    
    cv2.imshow("Gesture Filter", display_img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()