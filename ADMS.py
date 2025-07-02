import cv2
import time
import math
import threading
from playsound import playsound
import mediapipe as mp

# Mediapipe face mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Eye landmarks from MediaPipe FaceMesh (approximate)
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# EAR threshold and frame threshold
EAR_THRESHOLD = 0.25
CLOSED_SECONDS = 3
FPS = 20
FRAME_THRESHOLD = CLOSED_SECONDS * FPS

closed_frames = 0
alert_active = False

def play_alert():
    playsound("alert.mp3")  # Ensure alert.mp3 exists in the script directory

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

print("[INFO] Starting video stream...")
cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape

            # Extract eye landmarks
            left_eye = []
            right_eye = []

            for idx in LEFT_EYE_IDX:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))

            for idx in RIGHT_EYE_IDX:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))

            # Calculate EAR
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < EAR_THRESHOLD:
                closed_frames += 1
            else:
                closed_frames = 0
                if alert_active:
                    print("Driver woke up, alert stopped.")
                    alert_active = False

            if closed_frames >= FRAME_THRESHOLD and not alert_active:
                alert_active = True
                print("Applied brakes for three intervals of time.")
                print("Vehicle Auto parking.")
                print("Vehicle parked, please press the SPACEBAR (horn) to stop the alert.")

                threading.Thread(target=play_alert, daemon=True).start()

                # Wait for spacebar (in OpenCV window)
                while True:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord(' '):  # Spacebar
                        print("Driver woke up, alert stopped.")
                        closed_frames = 0
                        alert_active = False
                        break
                    elif key == 27:  # ESC to force quit alert
                        raise KeyboardInterrupt

        # Show frame
        cv2.imshow("Driver Monitor (Mediapipe)", frame)

        # ESC to quit main loop
        if cv2.waitKey(1) & 0xFF == 27:
            print("[INFO] ESC pressed. Exiting...")
            break

except KeyboardInterrupt:
    print("\n[INFO] Program interrupted by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Resources released. Program closed.")
