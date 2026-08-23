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

# =======================================================
# MAC CAMERA FIX: Force AVFoundation to bypass FFmpeg bug
# =======================================================
print("Initializing Camera...")
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION) # Try internal Mac camera first

if not cap.isOpened():
    print("Camera 1 failed. Falling back to Camera 0...")
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("CRITICAL ERROR: No cameras could be accessed.")
    exit()

# Right-hand controls
last_action_time = 0
cooldown = 3
previous_volume = -1

active_r_gesture = None    
r_gesture_start = 0        

# Left-hand controls
left_swipe_anchor = None
scroll_anchor_y = None  
last_swipe_time = 0
last_click_time = 0  
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

# =======================================================
# AIR KEYBOARD STATE VARIABLES
# =======================================================
keyboard_active = False
left_key_pressed = False
right_key_pressed = False

# Tracking variables for the 5-finger nod confirmation
kb_prompt_state = "IDLE"
kb_prompt_time = 0
kb_nod_baseline_y = None

keyboard_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['SPACE', 'BACKSPACE', 'CLOSE KEYBOARD']
]

print("Dual-Hand Controller Active. Show gestures to the camera!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    hand_results = hands.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    # Trackers for Both Hands
    left_index_tip = None
    right_index_tip = None
    left_hand_landmarks = None
    right_hand_landmarks = None

    if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
        for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
            # REVERTED the manual label swap that caused the mirroring issue
            hand_label = handedness.classification[0].label
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_label == 'Left':
                left_hand_landmarks = hand_landmarks
                left_index_tip = (hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y)
            elif hand_label == 'Right':
                right_hand_landmarks = hand_landmarks
                right_index_tip = (hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y)

    # =======================================================
    # AIR KEYBOARD MODE
    # =======================================================
    if keyboard_active:
        h, w, _ = frame.shape
        overlay = frame.copy()
        
        # Draw translucent background for the keyboard
        cv2.rectangle(overlay, (0, int(h * 0.5)), (w, h), (20, 20, 20), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        
        active_keys = []
        start_y = int(h * 0.55)
        key_h = int(h * 0.08)
        gap = 10
        
        # Render Keys
        for r_idx, row in enumerate(keyboard_layout):
            row_w = len(row) * (int(w * 0.08) + gap)
            start_x = int((w - row_w) / 2)
            
            for k_idx, key in enumerate(row):
                if key == 'SPACE': key_w = int(w * 0.3)
                elif key in ['BACKSPACE', 'CLOSE KEYBOARD']: key_w = int(w * 0.18)
                else: key_w = int(w * 0.08)
                    
                x = start_x
                y = start_y + (r_idx * (key_h + gap))
                active_keys.append({"char": key, "rect": (x, y, key_w, key_h)})
                
                cv2.rectangle(frame, (x, y), (x + key_w, y + key_h), (255, 255, 255), 2)
                cv2.putText(frame, key, (x + 15, y + int(key_h * 0.65)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                start_x += key_w + gap

        # Detect Typing (Apple Vision Pro style: Hover and Pinch)
        def process_typing(hand_landmarks, is_left_hand):
            global left_key_pressed, right_key_pressed, keyboard_active
            
            # Cursor position (Index finger tip)
            ix = int(hand_landmarks.landmark[8].x * w)
            iy = int(hand_landmarks.landmark[8].y * h)
            
            # Dynamic Pinch Math
            index_x, index_y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
            thumb_x, thumb_y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
            wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
            mcp_x, mcp_y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
            
            hand_size = math.hypot(mcp_x - wrist_x, mcp_y - wrist_y)
            raw_pinch_dist = math.hypot(index_x - thumb_x, index_y - thumb_y)
            pinch_ratio = raw_pinch_dist / (hand_size + 1e-6) 
            
            # A ratio < 0.35 means the thumb and index are pinched
            is_tapping = pinch_ratio < 0.35 
            was_pressed = left_key_pressed if is_left_hand else right_key_pressed
            
            # Change cursor color when pinching for immediate visual feedback
            cursor_color = (0, 255, 0) if is_tapping else (0, 255, 255)
            cv2.circle(frame, (ix, iy), 12, cursor_color, -1)
            
            if is_tapping and not was_pressed:
                # Find which key is being pressed
                for key_data in active_keys:
                    kx, ky, kw, kh = key_data["rect"]
                    if kx < ix < kx + kw and ky < iy < ky + kh:
                        char = key_data["char"]
                        
                        # Visual feedback: Flash the key green
                        cv2.rectangle(frame, (kx, ky), (kx + kw, ky + kh), (0, 255, 0), -1)
                        
                        if char == 'CLOSE KEYBOARD':
                            keyboard_active = False
                            print("Air Keyboard Closed.")
                        elif char == 'SPACE':
                            pyautogui.press('space')
                        elif char == 'BACKSPACE':
                            pyautogui.press('backspace')
                        else:
                            pyautogui.typewrite(char.lower())
                            
                        break
                        
                if is_left_hand: left_key_pressed = True
                else: right_key_pressed = True
                
            elif not is_tapping:
                if is_left_hand: left_key_pressed = False
                else: right_key_pressed = False

        if left_hand_landmarks: process_typing(left_hand_landmarks, True)
        if right_hand_landmarks: process_typing(right_hand_landmarks, False)

    # =======================================================
    # NORMAL CONTROLS (Only run if Keyboard is NOT active)
    # =======================================================
    else:
        # --- KEYBOARD NOD CONFIRMATION LOGIC ---
        if kb_prompt_state == "PROMPTING":
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    nose_tip_y = face_landmarks.landmark[1].y
                    if time.time() - kb_prompt_time > 5:
                        kb_prompt_state = "IDLE"
                    else:
                        cv2.putText(frame, "NOD TO OPEN KEYBOARD", (150, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                        if kb_nod_baseline_y is None:
                            kb_nod_baseline_y = nose_tip_y
                        else:
                            kb_nod_baseline_y = min(kb_nod_baseline_y, nose_tip_y)
                            head_drop = nose_tip_y - kb_nod_baseline_y
                            progress = int(max(0, head_drop / 0.05 * 100))
                            cv2.putText(frame, f"Nod progress: {progress}%", (150, 140), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                            
                            if head_drop > 0.05:
                                print("Nod Confirmed! Activating Air Keyboard.")
                                keyboard_active = True
                                kb_prompt_state = "IDLE"

        if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
            for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                hand_label = handedness.classification[0].label
                
                # --- RIGHT HAND: UTILITY & SYSTEM CONTROL ---
                if hand_label == 'Right':
                    def get_dist(idx1, idx2):
                        return math.hypot(hand_landmarks.landmark[idx1].x - hand_landmarks.landmark[idx2].x,
                                          hand_landmarks.landmark[idx1].y - hand_landmarks.landmark[idx2].y)

                    r_index_up = get_dist(8, 0) > get_dist(5, 0) * 1.25
                    r_middle_up = get_dist(12, 0) > get_dist(9, 0) * 1.25
                    r_ring_up = get_dist(16, 0) > get_dist(13, 0) * 1.25
                    r_pinky_up = get_dist(20, 0) > get_dist(17, 0) * 1.25
                    
                    r_main_fingers = sum([r_index_up, r_middle_up, r_ring_up, r_pinky_up])
                    current_time = time.time()

                    if r_index_up and r_main_fingers == 1:
                        active_r_gesture = None 
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
                        detected_gesture = None
                        
                        if r_index_up and r_middle_up and r_main_fingers == 2:
                            detected_gesture = "PEACE"
                        elif r_index_up and r_middle_up and r_ring_up and r_main_fingers == 3:
                            detected_gesture = "THREE"
                        elif r_main_fingers == 4:
                            detected_gesture = "FIVE"
                            
                        if detected_gesture:
                            cv2.putText(frame, f"Detecting: {detected_gesture}...", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                            
                        if detected_gesture == active_r_gesture and detected_gesture is not None:
                            hold_time = current_time - r_gesture_start
                            h, w, _ = frame.shape
                            wx, wy = int(hand_landmarks.landmark[0].x * w), int(hand_landmarks.landmark[0].y * h)
                            cv2.circle(frame, (wx, wy), int(hold_time * 80), (0, 255, 0), 4)

                            if hold_time > 0.5:
                                if detected_gesture == "PEACE":
                                    subprocess.run(["open", "-a", "LaunchOS"])
                                    last_action_time = current_time
                                elif detected_gesture == "THREE":
                                    webbrowser.open('https://classroom.google.com')
                                    last_action_time = current_time
                                elif detected_gesture == "FIVE":
                                    if kb_prompt_state == "IDLE":
                                        print("Open Palm Detected! Prompting for nod...")
                                        kb_prompt_state = "PROMPTING"
                                        kb_prompt_time = current_time
                                        kb_nod_baseline_y = None
                                        last_action_time = current_time
                                active_r_gesture = None
                        else:
                            active_r_gesture = detected_gesture
                            r_gesture_start = current_time

                # --- LEFT HAND: VIRTUAL TRACKPAD, SCROLLING & MOUSE ---
                elif hand_label == 'Left':
                    def get_dist_l(idx1, idx2):
                        return math.hypot(hand_landmarks.landmark[idx1].x - hand_landmarks.landmark[idx2].x,
                                          hand_landmarks.landmark[idx1].y - hand_landmarks.landmark[idx2].y)

                    l_index_up = get_dist_l(8, 0) > get_dist_l(5, 0) * 1.25
                    l_middle_up = get_dist_l(12, 0) > get_dist_l(9, 0) * 1.25
                    l_ring_up = get_dist_l(16, 0) > get_dist_l(13, 0) * 1.25
                    l_pinky_up = get_dist_l(20, 0) > get_dist_l(17, 0) * 1.25
                    
                    l_main_fingers = sum([l_index_up, l_middle_up, l_ring_up, l_pinky_up])
                    current_time = time.time()

                    if l_pinky_up and l_main_fingers == 1:
                        raise pyautogui.FailSafeException("Left pinky kill switch activated.")

                    elif l_main_fingers == 4:
                        scroll_anchor_y = None  
                        palm_x, palm_y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                        wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                        hand_size = math.hypot(palm_x - wrist_x, palm_y - wrist_y)
                        
                        h, w, _ = frame.shape
                        cv2.circle(frame, (int(palm_x * w), int(palm_y * h)), 15, (255, 0, 255), -1)
                        cv2.putText(frame, "SWIPE MODE", (int(palm_x * w) - 40, int(palm_y * h) - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

                        dynamic_swipe_threshold = hand_size * 1.2 

                        if left_swipe_anchor is None:
                            left_swipe_anchor = (palm_x, palm_y)
                        elif current_time - last_swipe_time > 0.4:
                            dx, dy = palm_x - left_swipe_anchor[0], palm_y - left_swipe_anchor[1]
                            
                            if abs(dx) > dynamic_swipe_threshold and abs(dx) > abs(dy):
                                if dx > 0: pyautogui.hotkey('ctrl', 'left')
                                else: pyautogui.hotkey('ctrl', 'right')
                                last_swipe_time = current_time
                                left_swipe_anchor = (palm_x, palm_y)
                                
                            elif abs(dy) > dynamic_swipe_threshold and abs(dy) > abs(dx):
                                if dy < 0: pyautogui.hotkey('ctrl', 'up')
                                else: pyautogui.hotkey('ctrl', 'down')
                                last_swipe_time = current_time
                                left_swipe_anchor = (palm_x, palm_y)

                    elif l_index_up and l_middle_up and l_main_fingers == 2:
                        index_y, middle_y = hand_landmarks.landmark[8].y, hand_landmarks.landmark[12].y
                        avg_y = (index_y + middle_y) / 2
                        h, w, _ = frame.shape
                        cx, cy = int(hand_landmarks.landmark[8].x * w), int(avg_y * h)
                        
                        cv2.circle(frame, (cx, cy), 16, (255, 255, 0), -1)
                        cv2.putText(frame, "SCROLLING", (cx - 40, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                        if scroll_anchor_y is None: scroll_anchor_y = avg_y
                        else:
                            dy = avg_y - scroll_anchor_y
                            if abs(dy) > 0.015: 
                                pyautogui.scroll(int(-dy * 1000))
                                scroll_anchor_y = avg_y 
                        left_swipe_anchor = None

                    elif l_index_up and l_main_fingers == 1:
                        scroll_anchor_y = None  
                        index_x, index_y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                        thumb_x, thumb_y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
                        wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                        mcp_x, mcp_y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                        
                        hand_size = math.hypot(mcp_x - wrist_x, mcp_y - wrist_y)
                        raw_pinch_dist = math.hypot(index_x - thumb_x, index_y - thumb_y)
                        is_pinching = (raw_pinch_dist / (hand_size + 1e-6)) < 0.35 

                        screen_w, screen_h = pyautogui.size()
                        target_x = np.interp(index_x, [0.15, 0.85], [0, screen_w])
                        target_y = np.interp(index_y, [0.15, 0.85], [0, screen_h])
                        dist = math.hypot(target_x - prev_mouse_x, target_y - prev_mouse_y)
                        
                        if dist > 3.0 and not is_pinching:
                            mouse_x = prev_mouse_x + (target_x - prev_mouse_x) / 7.0
                            mouse_y = prev_mouse_y + (target_y - prev_mouse_y) / 7.0
                            pyautogui.PAUSE = 0
                            pyautogui.moveTo(mouse_x, mouse_y)
                            prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

                        h, w, _ = frame.shape
                        cx, cy = int(index_x * w), int(index_y * h)

                        if is_pinching and (current_time - last_click_time > 0.5):
                            pyautogui.click()
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
    if left_index_tip and right_index_tip and easter_egg_state == "IDLE":
        finger_dist = math.hypot(left_index_tip[0] - right_index_tip[0], left_index_tip[1] - right_index_tip[1])
        if finger_dist < 0.2:
            h, w, _ = frame.shape
            cv2.line(frame, (int(left_index_tip[0]*w), int(left_index_tip[1]*h)), 
                           (int(right_index_tip[0]*w), int(right_index_tip[1]*h)), (0, 255, 255), 2)
        if finger_dist < 0.05:  
            print("Jutsu Seal Detected! Prompting for Nod...")
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
                    if nod_baseline_y is None: nod_baseline_y = nose_tip_y
                    elif nose_tip_y - nod_baseline_y > 0.05: easter_egg_state = "ACTIVE"
                        
            elif easter_egg_state == "ACTIVE":
                h, w, _ = frame.shape
                left_iris = (int(face_landmarks.landmark[468].x * w), int(face_landmarks.landmark[468].y * h))
                right_iris = (int(face_landmarks.landmark[473].x * w), int(face_landmarks.landmark[473].y * h))
                spin_angle = (time.time() * 200) % 360

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

                draw_sharingan(frame, left_iris, 18, spin_angle)
                draw_sharingan(frame, right_iris, 18, spin_angle)
                
                upper_lip, lower_lip = face_landmarks.landmark[13], face_landmarks.landmark[14]
                if lower_lip.y - upper_lip.y > 0.035:
                    clap_time = time.time()
                    mouth_x, mouth_y = int((upper_lip.x + lower_lip.x) / 2 * w), int((upper_lip.y + lower_lip.y) / 2 * h)
                    for _ in range(15):
                        fire_particles.append({
                            "x": mouth_x + random.randint(-15, 15), "y": mouth_y + random.randint(0, 15),
                            "radius": random.randint(10, 25), "life": random.randint(15, 35), "max_life": 35,
                            "vx": random.uniform(-15, 15), "vy": random.uniform(10, 25)   
                        })

                if fire_particles:
                    fire_overlay = np.zeros_like(frame)
                    for p in fire_particles[:]:
                        p["x"] += p["vx"]
                        p["y"] += p["vy"]
                        p["radius"] += 1.8 
                        p["life"] -= 1
                        if p["life"] <= 0: fire_particles.remove(p)
                        else:
                            ratio = p["life"] / p["max_life"]
                            if ratio > 0.8: color = (255, 255, 255) 
                            elif ratio > 0.5: color = (0, 255, 255)   
                            elif ratio > 0.2: color = (0, 140, 255)   
                            else: color = (0, 0, 150)     
                            cv2.circle(fire_overlay, (int(p["x"]), int(p["y"])), int(p["radius"]), color, -1)
                    
                    frame = cv2.add(frame, cv2.GaussianBlur(fire_overlay, (31, 31), 0))

                if time.time() - clap_time > 15:
                    easter_egg_state = "IDLE"
                    fire_particles.clear()

    cv2.imshow("Touchless Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()