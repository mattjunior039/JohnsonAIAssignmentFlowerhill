# Touchless Controller

A vision-based desktop control system that lets you interact with your computer using natural hand gestures. Instead of a mouse or touchpad, the system tracks your hands in real time and turns them into controls for browsing, navigation, launching tools, and adjusting system volume.

## Features

### 1. Gesture-based mouse control
- Move the cursor with your index finger
- Click with a middle-finger tap
- Drag and release windows using a pinch gesture
- Smooth tracking for a more natural cursor feel

### 2. Virtual trackpad navigation
- Open your left hand with all fingers up to use trackpad-style motion
- Swipe horizontally to move backward and forward in browser history
- Swipe vertically for page or app navigation shortcuts
- Designed for fast, hands-free browsing interactions

### 3. System and app shortcuts
- Use a right-hand gesture to open LaunchOS
- Use another right-hand gesture to open Google Classroom
- Built to reduce reliance on keyboard and mouse for everyday tasks

### 4. Live volume control
- Raise only the index finger on the right hand to activate volume mode
- Adjust sound level by rotating the wrist or changing the angle of the hand
- Real-time visual feedback shows the current volume percentage

### 5. Dual-hand interaction model
- Right hand handles system tasks and volume
- Left hand handles cursor and navigation
- Separate control zones keep gestures intuitive and responsive

### 6. Real-time camera tracking
- Uses OpenCV and MediaPipe for live hand detection
- Draws landmarks directly onto the video feed for feedback
- Works in real time with a webcam

## Example Gesture Set

- Left hand, index finger up: mouse movement
- Left hand, pinch: drag window
- Left hand, all fingers up: swipe-based trackpad mode
- Right hand, index finger only: volume control
- Right hand, peace sign: open LaunchOS
- Right hand, three-finger gesture: open Google Classroom

## Why this project stands out

This project combines computer vision, gesture recognition, and desktop automation into a single interactive experience. It turns the webcam into a natural input device and makes hands-free control feel futuristic while still being practical for real world use.

## Tech Stack

- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- Python

## Setup

```bash
pip install -r requirements.txt
python controller.py
```

## Demo / Screenshots

Add a GIF or screenshot here to show the gestures in action:

```md
![Touchless Controller Demo](demo.gif)
```

## Project Summary

This project is a hands-free desktop control system designed to make digital interaction more natural, more accessible, and more immersive. It focuses on productivity, accessibility, and the excitement of controlling a computer through gesture recognition.
