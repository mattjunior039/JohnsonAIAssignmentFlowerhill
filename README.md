# Johnson AI Assignment – Touchless Controller

This project was developed as part of the Johnson AI assignment and is hosted at:

https://github.com/mattjunior039/JohnsonAIAssignmentFlowerhill

A hand-tracking desktop controller that lets you navigate your computer using gestures instead of a mouse, keyboard, or touchpad. This project combines computer vision, MediaPipe hand detection, and PyAutoGUI automation to create a touchless interaction system for everyday laptop use.

## Overview

Touchless Controller is designed for users who want a more natural and futuristic way to interact with a computer. It uses a webcam to detect hand landmarks in real time and maps those gestures to actions such as:

- moving the cursor
- clicking and dragging
- swiping through browser pages or app navigation
- adjusting system volume
- launching common tools or websites

The result is a lightweight, accessible, and interactive gesture control system built in Python for demonstration and experimentation.

## Key Features Explained

### Gesture Control Reference

| Hand | Gesture Symbol | Function Name | Action |
| --- | --- | --- | --- |
| Left | All fingers up | `trackpad mode` | Swipes trigger browser navigation shortcuts and acts like a trackpad. |
| Left | Pinky finger only up | `fail-safe kill switch` | Raises `pyautogui.FailSafeException` to stop the gesture system safely. |
| Left | Index and middle fingers up | `scroll mode` | Uses finger movement to trigger vertical scrolling with `pyautogui.scroll()`. |
| Left | Index finger only up | `virtual mouse mode` | Moves the cursor across the screen using fingertip coordinates. |
| Left | Thumb and index finger close together | `click / pinch trigger` | Triggers a mouse click once the pinch ratio crosses the threshold. |
| Left | Pinch while moving | `drag and release` | Starts dragging when pinched and releases when the pinch ends. |
| Right | Index finger only up | `volume control` | Converts hand angle into a volume percentage and adjusts the system volume. |
| Right | Peace sign | `LaunchOS shortcut` | Opens the LaunchOS app with a cooldown to avoid repeated triggers. |
| Right | Three fingers up | `Google Classroom shortcut` | Opens the Google Classroom site in the browser. |
| Both hands | Hands clap | `easter egg prompt` | Starts the hidden prompt sequence waiting for a nod. |
| Face | Nod during prompt | `Sharingan awakening` | Activates the face-based easter egg and reveals the Sharingan effect. |
| Face | Mouth opens wide | `fire jutsu effect` | Creates fire-particle overlays around the mouth region. |
| Face | Active Sharingan state | `draw_sharingan` | Draws animated eye-like patterns on both irises. |

### 1. Real-time hand tracking
The app uses MediaPipe hand tracking to detect live landmarks from the webcam. Each frame is converted to RGB, processed through `mp.solutions.hands`, and mapped into gesture logic. This gives the project real-time input detection without any physical device.

### 2. Virtual mouse control
The left hand acts as a cursor controller. When the index finger is raised and the rest of the hand is mostly relaxed, the fingertip position is mapped to screen coordinates and the mouse moves smoothly. This allows the user to control the pointer without a mouse or trackpad.

### 3. Click interaction
The system supports click actions using a pinch-style trigger. Once the distance between the thumb and index finger becomes small enough, the app detects a pinch and issues a mouse click. A visual green indicator appears on screen as confirmation.

### 4. Drag and release behavior
When a pinch is held while the hand moves, the app enters drag mode and performs a mouse press. The cursor follows the finger movement, allowing the user to drag items or windows around the screen. When the pinch is released, the system automatically drops the item by releasing the mouse button.

### 5. Smooth cursor movement
The controller does not map the fingertip directly 1:1 onto the screen because this would be too jittery. Instead, it smooths the movement using a filter, which reduces noise and makes the pointer feel stable and usable.

### 6. Scroll mode
The left hand can also activate a scrolling mode when the index and middle fingers are raised and the ring and pinky are curled down. The app compares finger position to a stored anchor and calls `pyautogui.scroll()` to move the page or document up and down.

### 7. Trackpad navigation mode
When all five fingers are extended on the left hand, the app enters a trackpad-style mode. It stores the wrist point as an anchor and detects whether the user swiped horizontally or vertically. The app then triggers browser/navigation shortcuts:

- right swipe = `Ctrl + Left`
- left swipe = `Ctrl + Right`
- up swipe = `Ctrl + Up`
- down swipe = `Ctrl + Down`

This gives the user a trackpad-like experience without needing a hardware touchpad.

### 8. Right-hand volume control
The right hand is dedicated to system control. In volume mode, only the index finger is raised. The system calculates the angle between the wrist and fingertip, converts it into a volume percentage, and sends it to macOS via `osascript`. A live bar is rendered in the camera feed so the user sees the resulting sound level immediately.

### 9. LaunchOS shortcut
The right-hand peace-sign gesture triggers the LaunchOS app. It uses a cooldown timer to prevent repeated firing while the hand remains in the same pose, which makes the shortcut reliable and less noisy.

### 10. Google Classroom shortcut
A three-finger right-hand pose opens the Google Classroom website in the default browser. This shows how the project can support simple productivity actions while still using a gesture-first interaction model.

### 11. Fail-safe logic
The left-hand pinky-only gesture acts as a fail-safe mode. If the system detects that this specific pose is active, it raises `pyautogui.FailSafeException`, immediately halting the gesture logic to prevent accidental or unsafe system control.

### 12. Dual-hand interaction design
The project intentionally splits tasks by hand:

- Left hand = point, click, drag, scroll, and swipe navigation
- Right hand = volume and app launch shortcuts

This separation reduces accidental triggers and keeps the interaction model understandable.

### 13. Face mesh integration and easter egg
The project also includes a hidden face-driven mode using MediaPipe Face Mesh. It detects when both hands clap together, waits for a head nod, and then activates a custom face effect. This adds an extra entertainment layer for demos and shows how the project extends beyond pure productivity tasks.

### 14. Sharingan effect
Once the nod is detected, the system draws animated eye rings around both irises using a custom `draw_sharingan()` function. The eyes spin and the patterns shift over time, creating a stylized anime-inspired visual overlay.

### 15. Fire-particle effect
When the face is in the active state and the mouth opens widely, the app spawns particles around the mouth and blends them into the camera frame. This produces a stylized fire effect and demonstrates how the project can go beyond standard AI input and into creative visual effects.

### 16. Real-time visual feedback
The app overlays the webcam feed with visible markers, drag indicators, click confirmations, and volume bars. This means the user always sees what the system is interpreting and can refine their gestures in real time.

### 17. Full project purpose
Together, these features turn the webcam into a hands-free desktop control system. The project combines webcam capture, landmark tracking, geometric gesture recognition, browser and system automation, visual overlays, and creative effects into one interactive AI-powered prototype.

## Example Gestures

| Hand | Gesture | Action |
| --- | --- | --- |
| Left | Index finger up | Move mouse |
| Left | Pinch | Drag and release |
| Left | All fingers up | Trackpad swipe mode |
| Right | Index finger only | Volume control |
| Right | Peace sign | Open LaunchOS |
| Right | Three fingers up | Open Google Classroom |

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- macOS system automation via `osascript`

## Project Goals

This assignment aims to:

- explore computer vision as an input method
- reduce dependence on physical devices for simple tasks
- create an accessible control experience for users with limited hardware access
- demonstrate how AI and vision tools can turn webcam input into useful desktop actions
- showcase a practical AI-powered interaction prototype suitable for a GitHub portfolio or coursework submission

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mattjunior039/JohnsonAIAssignmentFlowerhill.git
cd JohnsonAIAssignmentFlowerhill
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python controller.py
```

If `python` is not recognized, use:

```bash
python3 controller.py
```

## Demo

This project is intended to be demonstrated live with a webcam and a clear hand gesture setup. A screenshot or GIF can be added here to showcase the system in action:

```md
![Touchless Controller Demo](demo.gif)
```

## Notes

- The app requires a webcam.
- Best results are achieved with good lighting and a clear background.
- The volume control uses AppleScript, so it is intended for macOS.
- Gesture detection may need tuning depending on camera quality and lighting conditions.

## Future Improvements

Potential upgrades for this project include:

- more robust gesture recognition
- reduced false positives in noisy environments
- customizable gesture mapping
- support for more platforms and shortcuts
- a cleaner UI overlay and gesture tutorial screen

## License

This project is available for educational and experimental use.

## Contributing

Contributions are welcome. If you improve the gesture logic, add new actions, or improve the recognition pipeline, feel free to open a pull request.

## Repository Context

This repository is intended to present the Johnson AI assignment in a clear, professional, and reusable way. It demonstrates a practical application of computer vision and AI-based interaction design in a real-world desktop environment.
