import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import webbrowser
import time

# -------------------------------
# Initialize MediaPipe Face Mesh
# -------------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -------------------------------
# Start Webcam
# -------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

# -------------------------------
# Facial Landmark Indices
# -------------------------------
LANDMARKS = {
    "left_mouth": 61,
    "right_mouth": 291,
    "top_lip": 13,
    "bottom_lip": 14,
    "left_eye_top": 159,
    "left_eye_bottom": 145,
    "right_eye_top": 386,
    "right_eye_bottom": 374,
    "left_brow": 70,
    "right_brow": 300,
}

# -------------------------------
# Emotion Buffer
# -------------------------------
emotion_history = deque(maxlen=15)

last_opened_emotion = None
last_open_time = 0
COOLDOWN = 30  # seconds

# -------------------------------
# Spotify Playlists
# -------------------------------
emotion_to_playlist = {
    "Happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "Sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "Angry": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
    "Surprised": "https://open.spotify.com/playlist/37i9dQZF1DWTJ7xPn4vNaz",
    "Neutral": "https://open.spotify.com/playlist/4T4g5GiIjz2yFc4Ca5oJvy"
}

# -------------------------------
# Helper Function
# -------------------------------
def get_point(landmarks, idx, width, height):
    lm = landmarks.landmark[idx]
    return np.array([int(lm.x * width), int(lm.y * height)])

# -------------------------------
# Main Loop
# -------------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to read webcam")
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process face mesh
    results = face_mesh.process(rgb)

    emotion = "Neutral"

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # Get landmark points
            pts = {
                key: get_point(face_landmarks, idx, w, h)
                for key, idx in LANDMARKS.items()
            }

            # -------------------------------
            # Measurements
            # -------------------------------
            mouth_width = np.linalg.norm(
                pts["right_mouth"] - pts["left_mouth"]
            )

            mouth_open = abs(
                pts["bottom_lip"][1] - pts["top_lip"][1]
            )

            left_eye = abs(
                pts["left_eye_bottom"][1] - pts["left_eye_top"][1]
            )

            right_eye = abs(
                pts["right_eye_bottom"][1] - pts["right_eye_top"][1]
            )

            eye_height = (left_eye + right_eye) / 2

            brow_distance = abs(
                pts["right_brow"][0] - pts["left_brow"][0]
            )

            # -------------------------------
            # Normalized Ratios
            # -------------------------------
            smile_ratio = mouth_open / mouth_width
            eye_ratio = eye_height / mouth_width
            brow_ratio = brow_distance / mouth_width

            # -------------------------------
            # Emotion Logic
            # -------------------------------
            if smile_ratio > 0.30:
                emotion = "Happy"

            elif smile_ratio < 0.08:
                emotion = "Sad"

            elif eye_ratio > 0.38:
                emotion = "Surprised"

            elif brow_ratio < 1.3:
                emotion = "Angry"

            else:
                emotion = "Neutral"

            # -------------------------------
            # Draw Landmarks
            # -------------------------------
            for pt in pts.values():
                cv2.circle(frame, tuple(pt), 2, (0, 255, 0), -1)

    # -------------------------------
    # Smooth Emotion Prediction
    # -------------------------------
    emotion_history.append(emotion)

    dominant_emotion = max(
        set(emotion_history),
        key=emotion_history.count
    )

    # -------------------------------
    # Display Emotion
    # -------------------------------
    cv2.putText(
        frame,
        f"Emotion: {dominant_emotion}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # -------------------------------
    # Open Spotify Playlist
    # -------------------------------
    current_time = time.time()

    if (
        dominant_emotion != last_opened_emotion
        and current_time - last_open_time > COOLDOWN
    ):

        playlist = emotion_to_playlist.get(dominant_emotion)

        if playlist:
            webbrowser.open(playlist)

            last_opened_emotion = dominant_emotion
            last_open_time = current_time

            print(f"Opened {dominant_emotion} playlist")

    # -------------------------------
    # Show Window
    # -------------------------------
    cv2.imshow("Emotion Playlist Recommender", frame)

    # ESC to Exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# -------------------------------
# Cleanup
# -------------------------------
cap.release()
cv2.destroyAllWindows()