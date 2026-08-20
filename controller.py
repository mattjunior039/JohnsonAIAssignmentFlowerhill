import math
import subprocess
import time
import webbrowser

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

# Right-hand controls
last_action_time = 0
cooldown = 3
previous_volume = -1

# Left-hand controls
left_swipe_anchor = None
last_swipe_time = 0
swipe_cooldown = 1.0
swipe_threshold = 0.30
is_dragging = False
prev_mouse_x, prev_mouse_y = 0, 0
smoothing = 5

print("Dual-Hand Controller Active. Show gestures to the camera!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # =======================================================
            # RIGHT HAND: UTILITY & SYSTEM CONTROL
            # =======================================================
            if hand_label == 'Right':
                r1_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
                r2_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                r3_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                r4_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                r5_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

                current_time = time.time()

                # Continuous volume control: index finger up, others closed
                if not r1_up and r2_up and not r3_up and not r4_up and not r5_up:
                    wrist_x = hand_landmarks.landmark[0].x
                    wrist_y = hand_landmarks.landmark[0].y
                    index_tip_x = hand_landmarks.landmark[8].x
                    index_tip_y = hand_landmarks.landmark[8].y

                    dy = index_tip_y - wrist_y
                    dx = index_tip_x - wrist_x
                    angle = math.degrees(math.atan2(dy, dx))

                    raw_vol = np.interp(angle, [-170, -10], [0, 100])
                    vol_percent = float(np.clip(raw_vol, 0, 100))

                    cv2.putText(
                        frame,
                        f"Volume: {int(vol_percent)}%",
                        (50, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 0),
                        2,
                    )
                    cv2.rectangle(frame, (50, 50), (int(50 + (vol_percent * 4)), 80), (255, 0, 0), -1)
                    cv2.rectangle(frame, (50, 50), (450, 80), (255, 255, 255), 2)

                    if abs(vol_percent - previous_volume) > 2:
                        subprocess.Popen(["osascript", "-e", f"set volume output volume {int(vol_percent)}"])
                        previous_volume = vol_percent

                # Discrete gestures with cooldown
                elif current_time - last_action_time > cooldown:
                    if not r1_up and r2_up and r3_up and not r4_up and not r5_up:
                        print("Gesture: Peace Sign! Opening LaunchOS...")
                        subprocess.run(["open", "-a", "LaunchOS"])
                        last_action_time = current_time

                    elif not r1_up and r2_up and r3_up and r4_up and not r5_up:
                        print("Gesture: 3-Fingers! Opening Classroom...")
                        webbrowser.open('https://classroom.google.com')
                        last_action_time = current_time

            # =======================================================
            # LEFT HAND: VIRTUAL TRACKPAD & SYSTEM MOUSE
            # =======================================================
            elif hand_label == 'Left':
                l1_up = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x
                l2_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                l3_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                l4_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                l5_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
                current_time = time.time()

                # Trackpad mode: all five fingers up
                if l1_up and l2_up and l3_up and l4_up and l5_up:
                    wrist_x = hand_landmarks.landmark[0].x
                    wrist_y = hand_landmarks.landmark[0].y

                    h, w, _ = frame.shape
                    cv2.circle(frame, (int(wrist_x * w), int(wrist_y * h)), 15, (0, 255, 0), -1)

                    if left_swipe_anchor is None:
                        left_swipe_anchor = (wrist_x, wrist_y)
                    elif current_time - last_swipe_time > swipe_cooldown:
                        dx = wrist_x - left_swipe_anchor[0]
                        dy = wrist_y - left_swipe_anchor[1]

                        if abs(dx) > swipe_threshold and abs(dx) > abs(dy):
                            if dx > 0:
                                pyautogui.hotkey('ctrl', 'left')
                            else:
                                pyautogui.hotkey('ctrl', 'right')
                            last_swipe_time = current_time
                            left_swipe_anchor = (wrist_x, wrist_y)
                        elif abs(dy) > swipe_threshold and abs(dy) > abs(dx):
                            if dy < 0:
                                pyautogui.hotkey('ctrl', 'up')
                            else:
                                pyautogui.hotkey('ctrl', 'down')
                            last_swipe_time = current_time
                            left_swipe_anchor = (wrist_x, wrist_y)

                # Virtual mouse mode
                elif (l2_up or is_dragging) and not l4_up and not l5_up:
                    index_x = hand_landmarks.landmark[8].x
                    index_y = hand_landmarks.landmark[8].y
                    thumb_x = hand_landmarks.landmark[4].x
                    thumb_y = hand_landmarks.landmark[4].y

                    screen_w, screen_h = pyautogui.size()
                    target_x = np.interp(index_x, [0.1, 0.9], [0, screen_w])
                    target_y = np.interp(index_y, [0.1, 0.9], [0, screen_h])

                    mouse_x = prev_mouse_x + (target_x - prev_mouse_x) / smoothing
                    mouse_y = prev_mouse_y + (target_y - prev_mouse_y) / smoothing
                    prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

                    pyautogui.PAUSE = 0
                    pyautogui.moveTo(mouse_x, mouse_y)

                    h, w, _ = frame.shape
                    cx, cy = int(index_x * w), int(index_y * h)
                    pinch_dist = math.hypot(index_x - thumb_x, index_y - thumb_y)

                    if pinch_dist < 0.05 and not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                        print("Virtual Mouse: Grabbed Window!")
                    elif pinch_dist > 0.08 and is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                        print("Virtual Mouse: Released Window!")

                    if is_dragging:
                        cv2.circle(frame, (cx, cy), 16, (0, 255, 255), -1)
                        cv2.putText(frame, "DRAGGING", (cx - 40, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    else:
                        if l3_up:
                            if current_time - last_swipe_time > 0.5:
                                pyautogui.click()
                                print("Virtual Mouse: Clicked!")
                                cv2.circle(frame, (cx, cy), 16, (0, 255, 0), -1)
                                last_swipe_time = current_time
                        else:
                            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
                            cv2.circle(frame, (cx, cy), 16, (0, 0, 255), 2)

                    left_swipe_anchor = None

                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                        print("Virtual Mouse: Failsafe Drop!")
                    left_swipe_anchor = None

    cv2.imshow("Touchless Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()