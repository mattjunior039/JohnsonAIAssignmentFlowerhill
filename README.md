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

## Key Features

### Gesture-based cursor control
- Move the mouse with your index finger
- Perform click actions with a middle-finger tap
- Use pinch gestures to drag and release objects on screen
- Maintain smooth cursor motion with real-time hand tracking

### Virtual trackpad mode
- Raise all fingers on the left hand to activate trackpad-style interaction
- Swipe left and right to move through browser history
- Swipe up and down for quick navigation actions
- Toggle between precise motion and quick gestures without needing a physical input device

### App and web shortcuts
- Open LaunchOS with a right-hand gesture
- Open Google Classroom with a dedicated three-finger gesture
- Reduce friction for quick access to commonly used tools

### Volume control
- Use the right hand in a dedicated index-finger mode for volume adjustment
- Control volume by changing the angle of the wrist and hand
- View live volume percentage feedback directly in the camera feed

### Multi-hand interaction design
- Right hand for system actions and volume
- Left hand for cursor and navigation
- Clear separation between gesture sets for more intuitive control

### Real-time visual feedback
- MediaPipe landmarks are drawn directly on the webcam feed
- The app displays live UI indicators for actions like dragging or volume
- Easy to debug and tune while testing gestures in real time

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
