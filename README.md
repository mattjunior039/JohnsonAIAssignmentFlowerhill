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

### 1. Real-time hand tracking
The app uses MediaPipe Hand tracking to detect and analyse hand landmarks from a live webcam feed. Each frame is converted to RGB, processed through MediaPipe, and then mapped to specific gesture logic. This creates a responsive camera-driven input system that can interpret multiple hand poses in real time.

### 2. Gesture-based mouse control
The left hand acts as a virtual mouse controller. When the index finger is raised and other fingers are mostly relaxed, the system maps the fingertip position to screen coordinates and moves the cursor accordingly. This allows the user to control the pointer without a physical mouse.

### 3. Click interaction using the middle finger
The system supports a click action when the middle finger is raised during mouse mode. This acts as a tap-like click trigger and provides a simple, natural alternative to a standard mouse click. The feedback is shown on the screen with a green click indicator for confirmation.

### 4. Drag and release using a pinch gesture
A pinch gesture is used for dragging. When the thumb and index finger come close together, the controller triggers a mouse press and enters drag mode. As the hand moves, the cursor follows, allowing the user to drag windows or objects. When the fingers separate again, the mouse is released and drag mode ends.

### 5. Smooth cursor motion with filtering
The mouse movement is not mapped directly one-to-one from the camera to the screen. Instead, the app applies smoothing to reduce jitter and make cursor movement feel far more natural. This helps convert hand motion into usable desktop movement without sudden jumps or noisy tracking behaviour.

### 6. Left-hand trackpad mode for browser and app navigation
When all five fingers are extended on the left hand, the system switches into a trackpad-like navigation mode. It records the wrist position as an anchor and measures movement from that point. If the movement crosses a threshold, it detects a swipe and triggers browser navigation commands such as:

- right swipe = Ctrl + Left
- left swipe = Ctrl + Right
- up swipe = Ctrl + Up
- down swipe = Ctrl + Down

This gives the user a touchpad-style control surface without a physical device.

### 7. Right-hand system controls and app launching
The right hand is dedicated to utility and system actions. The system separates these controls from mouse movement so the left hand can remain focused on pointer control while the right hand handles overhead tasks.

### 8. Volume control using wrist angle
In volume mode, the right hand is used with only the index finger raised. The program calculates the angle between the wrist and the index fingertip and maps that value to a volume percentage. This transforms the user’s hand angle into a continuous sound control, creating a smooth and intuitive rotary volume effect.

### 9. Real-time volume feedback overlay
As volume changes, the system draws a visual bar and labels the current level on the OpenCV frame. This gives the user immediate visual confirmation and makes the control feel precise and responsive.

### 10. LaunchOS shortcut gesture
The right-hand peace-sign gesture triggers the LaunchOS application. This uses a cooldown timer so the command is not repeatedly fired while the gesture remains held. It offers a quick action shortcut without requiring keyboard or mouse input.

### 11. Google Classroom shortcut gesture
A three-finger gesture on the right hand opens the Google Classroom website in the default browser. This shows how the project can be extended beyond basic computer control and used as a productivity-focused gesture interface.

### 12. Dual-hand interaction model
The app is designed around two separate hand roles:

- Left hand = mouse and navigation
- Right hand = system actions and volume

This split makes the control scheme easier to understand, reduces accidental triggering, and improves usability when both hands are used at once.

### 13. Drag-release safety and failsafe logic
The controller has built-in recovery logic. If a drag is active and the user releases the pinch, the mouse button is released. If the hand disappears or a gesture becomes invalid, the app automatically releases the mouse to prevent the system from getting stuck in a dragging state.

### 14. Camera feed visualization and debugging tools
The webcam feed is displayed in an OpenCV window and overlays are drawn directly onto the image. The app highlights the cursor, shows drag status, and renders volume bars and gestures in real time. This makes the system easier to test and tune while being used live.

### 15. Keyboard-free desktop interaction prototype
Together, these features create a fully hands-free desktop control prototype that demonstrates how computer vision can be used to replace or supplement traditional input devices. It is especially useful for demos, experimentation, accessibility concepts, and future AI-driven interaction design.

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
