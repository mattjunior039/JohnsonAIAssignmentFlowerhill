import math
import subprocess
import time
import webbrowser
import random

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# =======================================================
# MEDIAPIPE SETUP (Hands & Face Mesh for Easter Egg)
# =======================================================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Right-hand controls
last_action_time = 0
cooldown = 3
previous_volume = -1

# Left-hand controls
left_swipe_anchor = None
scroll_anchor_y = None  
last_swipe_time = 0
last_click_time = 0  # <--- Added for pinch-click cooldown
swipe_cooldown = 1.0
swipe_threshold = 0.30
prev_mouse_x, prev_mouse_y = 0, 0
smoothing = 5

# =======================================================
# EASTER EGG STATE VARIABLES
# =======================================================
easter_egg_state = "IDLE"  
clap_time = 0
nod_baseline_y = None
fire_particles = []  

print("Dual-Hand Controller Active. Show gestures to the camera!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    hand_results = hands.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    left_wrist = None
    right_wrist = None

    if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
        for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
            hand_label = handedness.classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_label == 'Left':
                left_wrist = (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y)
            elif hand_label == 'Right':
                right_wrist = (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y)

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

                if not r1_up and r2_up and not r3_up and not r4_up and not r5_up:
                    wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                    index_tip_x, index_tip_y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                    
                    angle = math.degrees(math.atan2(index_tip_y - wrist_y, index_tip_x - wrist_x))
                    raw_vol = np.interp(angle, [-170, -10], [0, 100])
                    vol_percent = float(np.clip(raw_vol, 0, 100))

                    cv2.putText(frame, f"Volume: {int(vol_percent)}%", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                    cv2.rectangle(frame, (50, 50), (int(50 + (vol_percent * 4)), 80), (255, 0, 0), -1)
                    cv2.rectangle(frame, (50, 50), (450, 80), (255, 255, 255), 2)

                    if abs(vol_percent - previous_volume) > 2:
                        subprocess.Popen(["osascript", "-e", f"set volume output volume {int(vol_percent)}"])
                        previous_volume = vol_percent

                elif current_time - last_action_time > cooldown:
                    if not r1_up and r2_up and r3_up and not r4_up and not r5_up:
                        subprocess.run(["open", "-a", "LaunchOS"])
                        last_action_time = current_time
                    elif not r1_up and r2_up and r3_up and r4_up and not r5_up:
                        webbrowser.open('https://classroom.google.com')
                        last_action_time = current_time

            # =======================================================
            # LEFT HAND: VIRTUAL TRACKPAD, SCROLLING & MOUSE
            # =======================================================
            elif hand_label == 'Left':
                l1_up = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x
                l2_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                l3_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                l4_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                l5_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
                current_time = time.time()

                # 1. 🚨 FAIL-SAFE: Only the pinky finger is up
                if not l1_up and not l2_up and not l3_up and not l4_up and l5_up:
                    raise pyautogui.FailSafeException("Left pinky kill switch activated.")

                # 2. Trackpad mode: all five fingers up
                elif l1_up and l2_up and l3_up and l4_up and l5_up:
                    scroll_anchor_y = None  
                    wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                    h, w, _ = frame.shape
                    cv2.circle(frame, (int(wrist_x * w), int(wrist_y * h)), 15, (0, 255, 0), -1)

                    if left_swipe_anchor is None:
                        left_swipe_anchor = (wrist_x, wrist_y)
                    elif current_time - last_swipe_time > swipe_cooldown:
                        dx, dy = wrist_x - left_swipe_anchor[0], wrist_y - left_swipe_anchor[1]
                        if abs(dx) > swipe_threshold and abs(dx) > abs(dy):
                            pyautogui.hotkey('ctrl', 'left') if dx > 0 else pyautogui.hotkey('ctrl', 'right')
                            last_swipe_time = current_time; left_swipe_anchor = (wrist_x, wrist_y)
                        elif abs(dy) > swipe_threshold and abs(dy) > abs(dx):
                            pyautogui.hotkey('ctrl', 'up') if dy < 0 else pyautogui.hotkey('ctrl', 'down')
                            last_swipe_time = current_time; left_swipe_anchor = (wrist_x, wrist_y)

                # 3. Two-Finger Scroll Mode: Index and Middle up, Ring and Pinky down
                elif l2_up and l3_up and not l4_up and not l5_up:
                    index_y = hand_landmarks.landmark[8].y
                    middle_y = hand_landmarks.landmark[12].y
                    avg_y = (index_y + middle_y) / 2

                    h, w, _ = frame.shape
                    cx = int(hand_landmarks.landmark[8].x * w)
                    cy = int(avg_y * h)
                    
                    cv2.circle(frame, (cx, cy), 16, (255, 255, 0), -1)
                    cv2.putText(frame, "SCROLLING", (cx - 40, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                    if scroll_anchor_y is None:
                        scroll_anchor_y = avg_y
                    else:
                        dy = avg_y - scroll_anchor_y
                        if abs(dy) > 0.015: 
                            scroll_amount = int(-dy * 1000) 
                            pyautogui.scroll(scroll_amount)
                            scroll_anchor_y = avg_y 
                    
                    left_swipe_anchor = None

                # 4. Virtual mouse mode: Only Index is up (Stabilized & Dynamic Pinch)
                elif l2_up and not l3_up and not l4_up and not l5_up:
                    scroll_anchor_y = None  
                    index_x, index_y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                    thumb_x, thumb_y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
                    
                    # --- DYNAMIC PINCH CALCULATION ---
                    # 1. Measure the size of the user's hand (wrist to middle knuckle)
                    wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                    mcp_x, mcp_y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                    hand_size = math.hypot(mcp_x - wrist_x, mcp_y - wrist_y)
                    
                    # 2. Calculate relative pinch ratio (invariant to camera depth)
                    raw_pinch_dist = math.hypot(index_x - thumb_x, index_y - thumb_y)
                    pinch_ratio = raw_pinch_dist / (hand_size + 1e-6) # +1e-6 prevents division by zero
                    
                    # A ratio < 0.35 is a reliable threshold for a pinch
                    is_pinching = pinch_ratio < 0.35 

                    screen_w, screen_h = pyautogui.size()
                    target_x = np.interp(index_x, [0.15, 0.85], [0, screen_w])
                    target_y = np.interp(index_y, [0.15, 0.85], [0, screen_h])
                    
                    dist = math.hypot(target_x - prev_mouse_x, target_y - prev_mouse_y)
                    
                    # --- CURSOR FREEZE & MOVEMENT ---
                    # Only move if passing the deadzone AND the user isn't currently pinching
                    if dist > 3.0 and not is_pinching:
                        mouse_x = prev_mouse_x + (target_x - prev_mouse_x) / 7.0
                        mouse_y = prev_mouse_y + (target_y - prev_mouse_y) / 7.0
                        
                        pyautogui.PAUSE = 0
                        pyautogui.moveTo(mouse_x, mouse_y)
                        
                        prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

                    h, w, _ = frame.shape
                    cx, cy = int(index_x * w), int(index_y * h)

                    # --- TRIGGER CLICK ---
                    if is_pinching and (current_time - last_click_time > 0.5):
                        pyautogui.click()
                        print("Virtual Mouse: Clicked!")
                        last_click_time = current_time
                        
                        cv2.circle(frame, (cx, cy), 16, (0, 255, 0), -1)
                        cv2.putText(frame, "CLICK!", (cx - 30, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    else:
                        cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
                        cv2.circle(frame, (cx, cy), 16, (0, 0, 255), 2)
                    
                    left_swipe_anchor = None

    # =======================================================
    # EASTER EGG LOGIC (SHARINGAN & FIRE STYLE)
    # =======================================================
    
    if left_wrist and right_wrist and easter_egg_state == "IDLE":
        wrist_dist = math.hypot(left_wrist[0] - right_wrist[0], left_wrist[1] - right_wrist[1])
        if wrist_dist < 0.1:  
            print("Clap Detected! Prompting for Nod...")
            easter_egg_state = "PROMPTING"
            clap_time = time.time()
            nod_baseline_y = None
            fire_particles = []

    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            nose_tip_y = face_landmarks.landmark[1].y
            
            if easter_egg_state == "PROMPTING":
                if time.time() - clap_time > 5:
                    easter_egg_state = "IDLE"
                else:
                    cv2.putText(frame, "NOD TO AWAKEN", (150, 200), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
                    
                    if nod_baseline_y is None:
                        nod_baseline_y = nose_tip_y
                    elif nose_tip_y - nod_baseline_y > 0.05:  
                        print("Sharingan Awakened!")
                        easter_egg_state = "ACTIVE"
                        
            elif easter_egg_state == "ACTIVE":
                h, w, _ = frame.shape
                
                # --- DRAW SHARINGAN ---
                left_iris = (int(face_landmarks.landmark[468].x * w), int(face_landmarks.landmark[468].y * h))
                right_iris = (int(face_landmarks.landmark[473].x * w), int(face_landmarks.landmark[473].y * h))
                spin_angle = (time.time() * 200) % 360
                eye_radius = 18

                def draw_sharingan(img, center, radius, angle):
                    cv2.circle(img, center, radius, (0, 0, 255), -1)
                    cv2.circle(img, center, radius, (0, 0, 0), 2)
                    cv2.circle(img, center, max(1, radius // 4), (0, 0, 0), -1)
                    cv2.circle(img, center, int(radius * 0.6), (0, 0, 0), 1)

                    for i in [0, 120, 240]:
                        theta = math.radians(angle + i)
                        tomoe_x = int(center[0] + (radius * 0.6) * math.cos(theta))
                        tomoe_y = int(center[1] + (radius * 0.6) * math.sin(theta))
                        cv2.circle(img, (tomoe_x, tomoe_y), max(1, radius // 5), (0, 0, 0), -1)
                        
                        tail_theta = math.radians(angle + i + 45)
                        tail_x = int(tomoe_x + (radius * 0.2) * math.cos(tail_theta))
                        tail_y = int(tomoe_y + (radius * 0.2) * math.sin(tail_theta))
                        cv2.line(img, (tomoe_x, tomoe_y), (tail_x, tail_y), (0, 0, 0), max(1, radius//6))

                draw_sharingan(frame, left_iris, eye_radius, spin_angle)
                draw_sharingan(frame, right_iris, eye_radius, spin_angle)
                
                # --- FIRE STYLE JUTSU ---
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]
                mouth_open_dist = lower_lip.y - upper_lip.y
                
                if mouth_open_dist > 0.035:
                    clap_time = time.time()
                    mouth_x = int((upper_lip.x + lower_lip.x) / 2 * w)
                    mouth_y = int((upper_lip.y + lower_lip.y) / 2 * h)
                    
                    for _ in range(15):
                        fire_particles.append({
                            "x": mouth_x + random.randint(-15, 15),
                            "y": mouth_y + random.randint(0, 15),
                            "radius": random.randint(10, 25),
                            "life": random.randint(15, 35),
                            "max_life": 35,
                            "vx": random.uniform(-15, 15), 
                            "vy": random.uniform(10, 25)   
                        })

                if fire_particles:
                    fire_overlay = np.zeros_like(frame)
                    
                    for p in fire_particles[:]:
                        p["x"] += p["vx"]
                        p["y"] += p["vy"]
                        p["radius"] += 1.8 
                        p["life"] -= 1
                        
                        if p["life"] <= 0:
                            fire_particles.remove(p)
                        else:
                            life_ratio = p["life"] / p["max_life"]
                            if life_ratio > 0.8:
                                color = (255, 255, 255) 
                            elif life_ratio > 0.5:
                                color = (0, 255, 255)   
                            elif life_ratio > 0.2:
                                color = (0, 140, 255)   
                            else:
                                color = (0, 0, 150)     
                            
                            cv2.circle(fire_overlay, (int(p["x"]), int(p["y"])), int(p["radius"]), color, -1)
                    
                    fire_overlay = cv2.GaussianBlur(fire_overlay, (31, 31), 0)
                    frame = cv2.add(frame, fire_overlay)

                if time.time() - clap_time > 15:
                    easter_egg_state = "IDLE"
                    fire_particles.clear()

    cv2.imshow("Touchless Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()