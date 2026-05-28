import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Delay control
prev_time = 0
delay = 1.0  # seconds

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        # Take only ONE hand (avoids multi-hand issue)
        handLms = result.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        total_fingers = count_fingers(handLms)

        cv2.putText(img, f'Fingers: {total_fingers}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        current_time = time.time()

        # Apply delay to avoid multiple triggers
        if current_time - prev_time > delay:
            if total_fingers == 1:
                pyautogui.press('right')
            elif total_fingers == 2:
                pyautogui.press('left')
            elif total_fingers == 3:
                pyautogui.press('volumeup')
            elif total_fingers == 4:
                pyautogui.press('volumedown')
            elif total_fingers == 5:
                pyautogui.press('space')

            prev_time = current_time

    cv2.imshow("Hand Controlled Media Player", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()