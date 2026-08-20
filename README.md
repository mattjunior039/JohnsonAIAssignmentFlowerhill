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

### Gesture Feature Matrix

| Hand | Gesture Symbol | Function | What it does |
| --- | --- | --- | --- |
| Left | All fingers up | `trackpad mode` | Activates hand swipe navigation using the wrist as an anchor. Horizontal swipes trigger browser back/forward actions and vertical swipes trigger app navigation shortcuts. |
| Left | Pinky finger only up | `fail-safe kill switch` | Raises `pyautogui.FailSafeException` to stop the app in a safe way if the user intentionally or accidentally leaves the hand in a dangerous position. |
| Left | Index + middle fingers up, ring + pinky down | `scroll mode` | Detects vertical motion between the two fingers and uses `pyautogui.scroll()` to scroll the active screen. |
| Left | Index finger up only | `virtual mouse mode` | Maps fingertip position to screen coordinates and moves the cursor in real time. |
| Left | Index finger + thumb close together | `click / pinch trigger` | Calculates a dynamic pinch ratio; if it drops below threshold, the app triggers a mouse click. |
| Left | Index finger up + pinch gesture while dragging | `drag and release` | Begins drag mode when the pinch ratio indicates a grab, then releases the mouse when the gesture ends. |
| Right | Index finger up only | `volume control` | Measures the angle between the wrist and index fingertip and translates it into a volume percentage using `osascript`. |
| Right | Peace sign (index + middle raised, thumb closed) | `LaunchOS shortcut` | Opens the LaunchOS application and uses a cooldown timer to prevent repeated triggering. |
| Right | Three fingers up | `Google Classroom shortcut` | Opens the Google Classroom website in the browser. |
| Both hands | Hands clap together | `easter egg prompt` | Detects a clap distance between left and right wrists, then waits for a nod to trigger the hidden effect. |
| Face | Nod while prompt active | `Sharingan awakening` | Uses face mesh landmarks and a nose-tip movement threshold to activate the easter-egg mode. |
| Face | Mouth opens wide | `fire jutsu effect` | Spawns particles around the mouth region and adds an orange-red flame overlay to the camera frame. |
| Face | Activated Sharingan state | `draw_sharingan` | Draws animated spinning eye symbols on both irises using a custom function. |

### Feature Details

#### 1. Real-time hand tracking
The application uses MediaPipe hands detection to process every webcam frame and extract 21 hand landmarks. These landmarks are converted into gestures that drive mouse control, scrolling, app launching, and volume changes. This is the core foundation for the entire project.

#### 2. Virtual mouse system
The left hand acts as a cursor controller. When the index finger is extended and the rest are relaxed, the app maps the fingertip location to screen coordinates and moves the mouse pointer smoothly. The function uses smoothing to reduce jitter and create a more natural movement feel.

#### 3. Click interaction
The system includes a click trigger when the pinch ratio between the thumb and index finger is below a threshold. This acts like a tap/click action and is used to perform desktop interaction without a physical mouse.

#### 4. Drag and release behavior
The left-hand pinch logic can also trigger a drag state. Once the pinch is detected, a mouse down action is performed and the cursor follows the hand position. When the pinch is released, a mouse up event is triggered to end the drag safely.

#### 5. Scroll mode
In scroll mode, the user raises the index and middle fingers while the ring and pinky remain down. The app calculates the average vertical distance of those two finger tips and converts motion into a `pyautogui.scroll()` command. This allows the user to scroll through documents, webpages, or app content without a mouse wheel.

#### 6. Browser navigation swipes
The five-finger left-hand mode treats the wrist as a swipe anchor. If the user moves left, right, up, or down enough, the app triggers `Ctrl + Left`, `Ctrl + Right`, `Ctrl + Up`, or `Ctrl + Down` keyboard shortcuts. This gives the system trackpad-like page navigation controls.

#### 7. Right-hand volume mode
The right-hand index-only gesture is treated as a rotary volume control. The app compares the wrist and index fingertip positions to compute an angle, then converts that angle into a volume percentage. The result is sent to macOS using `osascript` and displayed in a visual bar on the camera feed.

#### 8. App launch shortcuts
The system includes two discrete action gestures on the right hand:

- Peace sign = open LaunchOS
- Three fingers = open Google Classroom

The app uses a cooldown delay to avoid repeated launches from a held gesture.

#### 9. Fail-safe logic
The left-hand pinky-only gesture acts as a built-in fail-safe. If the app detects a potentially unsafe or accidental condition, it raises `pyautogui.FailSafeException` to stop the gesture system gracefully instead of continuing with uncertain input.

#### 10. Facial tracking Easter egg
The project also includes a hidden face-based feature using MediaPipe Face Mesh:

- clap with both hands to begin the prompt
- nod your head to activate the Sharingan effect
- open your mouth to trigger fire-particle effects

This is not strictly required for the productivity features, but it adds an entertaining AI-driven secret mode and demonstrates the project’s creative potential.

#### 11. Sharingan visual effect
Once the nod trigger is detected, the app overlays animated circular eye patterns on both irises using custom drawing logic. This creates a stylized anime-inspired effect and shows how the frame-processing pipeline can be expanded beyond simple desktop control.

#### 12. Fire-particle animation effect
When the mouth is opened wide during the active easter-egg state, the app creates a burst of fire particle objects. Each particle is animated with position, size, velocity, and lifetime values, and an overlay is blended into the frame to simulate an energy effect.

#### 13. Visual feedback overlays
The app draws landmarks, circles, and labels directly onto the live camera frame. These visual indicators show:

- cursor position
- drag status
- click confirmation
- volume bar
- scroll mode
- gesture state

This feedback makes the controller easier to understand and much easier to debug while testing in real time.

#### 14. Multi-hand input design
The controller deliberately splits functionality by hand:

- left hand = pointer, scrolling, and navigation
- right hand = system actions and volume control

This separation reduces conflicts between control types and makes the interface more intuitive for users.

#### 15. Full end-to-end system behavior
The project combines:

- webcam capture
- human landmark detection
- dynamic geometric calculations
- OS automation
- browser automation
- visual overlays
- easter-egg effects

into one complete gesture-controlled interaction system. This makes it a strong demonstration of practical AI, CV, and automation integration in a single Python project.

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
