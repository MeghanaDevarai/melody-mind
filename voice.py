import sounddevice as sd
import numpy as np
import webbrowser
import time

# -------------------------------
# Spotify Playlists
# -------------------------------
emotion_to_playlist = {
    "Happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "Sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "Neutral": "https://open.spotify.com/playlist/4T4g5GiIjz2yFc4Ca5oJvy"
}

# -------------------------------
# Cooldown
# -------------------------------
last_emotion = None
last_open_time = 0
COOLDOWN = 30

# -------------------------------
# Detect Voice Emotion
# -------------------------------
def detect_voice_emotion():

    duration = 3
    fs = 44100

    print("Speak something...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    audio_data = np.abs(recording)

    energy = np.mean(audio_data)

    if energy > 0.1:
        return "Happy"

    elif energy < 0.03:
        return "Sad"

    else:
        return "Neutral"

# -------------------------------
# Main Loop
# -------------------------------
while True:

    emotion = detect_voice_emotion()

    print(f"Detected Emotion: {emotion}")

    current_time = time.time()

    if (
        emotion != last_emotion
        and current_time - last_open_time > COOLDOWN
    ):

        playlist = emotion_to_playlist.get(emotion)

        if playlist:
            webbrowser.open(playlist)

            last_emotion = emotion
            last_open_time = current_time

            print(f"Opened {emotion} playlist")

    choice = input("Press q to quit or Enter to continue: ")

    if choice.lower() == 'q':
        break