# ADMS
Advanced Driver Monitoring System 
Driver Drowsiness Detection Using MediaPipe and OpenCV

🔍 Project Overview
This project implements a real-time Driver Drowsiness Detection System using Python, OpenCV, and MediaPipe. It tracks the eye aspect ratio (EAR) to detect signs of drowsiness and triggers alerts to simulate vehicle braking and auto-parking.
🚗 Key Features
- Real-time face and eye landmark detection using MediaPipe
- Eye Aspect Ratio (EAR) based drowsiness detection
- Automatic alert system when driver’s eyes remain closed for 3 seconds
- Audio alert and message simulation for auto-parking
- Safe, cross-platform input handling using OpenCV’s waitKey()
🛠️ Technologies Used
- Python 3.11
- OpenCV
- MediaPipe
- playsound
- threading
⚙️ Setup Instructions
1. Clone this repository and navigate to the project directory.
2. Install dependencies using pip:
  pip install opencv-python mediapipe playsound
3. Place an 'alert.mp3' file in the project directory.
4. Run the script using:
  python ADMS.py
📈 How It Works
The system uses MediaPipe to extract facial landmarks and isolates key points around the eyes. Using these points, it calculates the Eye Aspect Ratio (EAR). If the average EAR falls below 0.25 for more than 3 seconds, the system considers the driver to be drowsy and triggers an alert. The user can press the SPACEBAR to stop the alert. Press ESC to exit the program.
⚠️ Disclaimer
This project is a prototype for educational purposes and is not certified for use in real-world driving applications.
