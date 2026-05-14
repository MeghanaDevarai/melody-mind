from auth import signup, login

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import plotly.express as px
from collections import deque
import time

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="MelodyMind",
    page_icon="🎧",
    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "last_played" not in st.session_state:
    st.session_state.last_played = "Neutral"

# -----------------------------------
# FIX ANALYTICS RESET
# -----------------------------------
if "emotion_history" not in st.session_state:

    st.session_state.emotion_history = deque(
        maxlen=10
    )

if "analytics_data" not in st.session_state:

    st.session_state.analytics_data = []

emotion_history = st.session_state.emotion_history

analytics_data = st.session_state.analytics_data

# -----------------------------------
# LOGIN / SIGNUP
# -----------------------------------
if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='text-align:center;
    font-size:70px;
    color:#1DB954;'>
    🎧 MelodyMind
    </h1>

    <h3 style='text-align:center;
    color:gray;'>
    AI Emotion + Music Dashboard
    </h3>
    """, unsafe_allow_html=True)

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Signup"]
    )

    # LOGIN
    if menu == "Login":

        st.subheader("🔐 Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login(
                username,
                password
            )

            if user:

                st.success(
                    "Login Successful"
                )

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    # SIGNUP
    else:

        st.subheader("📝 Signup")

        new_user = st.text_input(
            "Create Username"
        )

        new_pass = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Signup"):

            success = signup(
                new_user,
                new_pass
            )

            if success:

                st.success(
                    "Account Created Successfully"
                )

            else:

                st.error(
                    "Username Already Exists"
                )

    st.stop()

# -----------------------------------
# THEME
# -----------------------------------
theme = st.sidebar.selectbox(
    "🎨 Theme",
    ["Dark", "Light"]
)

if theme == "Dark":

    bg_color = "#0F172A"
    card_color = "#1E293B"
    text_color = "white"

else:

    bg_color = "#F8FAFC"
    card_color = "#FFFFFF"
    text_color = "#111827"

# -----------------------------------
# LOGOUT
# -----------------------------------
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.rerun()

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown(f"""
<style>

.stApp {{
    background:{bg_color};
    color:{text_color};
}}

.card {{
    background:{card_color};
    padding:20px;
    border-radius:20px;
    margin-bottom:20px;
    box-shadow:0 4px 20px rgba(0,0,0,0.2);
}}

.main-title {{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:{text_color};
}}

.sub-title {{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}}

.emotion-box {{
    padding:25px;
    border-radius:20px;
    background:linear-gradient(
    135deg,
    #1DB954,
    #191414
    );
    color:white;
    text-align:center;
    font-size:35px;
    font-weight:bold;
}}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("""
<div class='main-title'>
🎧 MelodyMind
</div>

<div class='sub-title'>
AI Emotion + Music Recommendation Dashboard
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# CLOCK
# -----------------------------------
current_time = time.strftime(
    "%I:%M:%S %p"
)

st.markdown(f"""
<div class="card">

<h3>🕒 Current Time</h3>

<h2>{current_time}</h2>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# GREETING
# -----------------------------------
st.markdown("""
<div class="card">

<h1 style="
color:#1DB954;
text-align:center;
">
🎧 Welcome to MelodyMind
</h1>

<h4 style="
text-align:center;
color:gray;
">
AI-Powered Emotion + Music Experience
</h4>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# STATUS
# -----------------------------------
st.markdown("""
<div class="card">

<h3>🔥 MelodyMind Status</h3>

<p>AI Dashboard Running Successfully</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("⚙ Settings")

run = st.sidebar.toggle(
    "📷 Camera ON/OFF"
)

if run:

    st.sidebar.success(
        "🟢 Camera Active"
    )

else:

    st.sidebar.warning(
        "🔴 Camera Off"
    )

# -----------------------------------
# PLAYLISTS
# -----------------------------------
emotion_to_playlist = {

    "Happy":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",

    "Sad":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",

    "Angry":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYxwmBaMqxsl",

    "Surprised":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DWTJ7xPn4vNaz",

    "Neutral":
    "https://open.spotify.com/embed/playlist/4T4g5GiIjz2yFc4Ca5oJvy"
}

# -----------------------------------
# SIDEBAR MUSIC
# -----------------------------------
with st.sidebar:

    st.markdown("## 🎵 Manual Song Player")

    manual_song = st.text_input(
        "Paste Spotify Embed URL"
    )

    st.markdown("## ❤️ Favorite Playlists")

    favorite_playlist = st.selectbox(
        "Choose Playlist",
        [
            "Happy Hits",
            "Sad Songs",
            "Chill Mood"
        ]
    )

favorite_links = {

    "Happy Hits":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",

    "Sad Songs":
    "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",

    "Chill Mood":
    "https://open.spotify.com/embed/playlist/4T4g5GiIjz2yFc4Ca5oJvy"
}

# -----------------------------------
# FAVORITE PLAYLIST
# -----------------------------------
st.markdown(f'''
<div class="card">

<h3>❤️ Favorite Playlist</h3>

<iframe
style="border-radius:12px"
src="{favorite_links[favorite_playlist]}"
width="100%"
height="352"
frameBorder="0"
allow="autoplay; encrypted-media">
</iframe>

</div>
''', unsafe_allow_html=True)

# -----------------------------------
# TEXT RECOGNITION
# -----------------------------------
st.markdown("""
<div class="card">

<h2>
📝 AI Text Recognition
</h2>

<p>
Type text and MelodyMind will analyze the mood
</p>

</div>
""", unsafe_allow_html=True)

user_text = st.text_area(
    "✍ Enter Your Text",
    height=150,
    placeholder="Type something here..."
)

if user_text:

    text = user_text.lower()

    # TEXT EMOTION DETECTION
    if any(word in text for word in [

        "happy",
        "great",
        "awesome",
        "love",
        "fun",
        "excited"
    ]):

        detected_text_emotion = "Happy"

    elif any(word in text for word in [

        "sad",
        "cry",
        "alone",
        "depressed",
        "upset"
    ]):

        detected_text_emotion = "Sad"

    elif any(word in text for word in [

        "angry",
        "mad",
        "hate",
        "annoyed"
    ]):

        detected_text_emotion = "Angry"

    else:

        detected_text_emotion = "Neutral"

    # SAVE ANALYTICS
    analytics_data.append(
        detected_text_emotion
    )

    emotion_history.append(
        detected_text_emotion
    )

    st.session_state.last_played = (
        detected_text_emotion
    )

    # SHOW RESULT
    st.markdown(f"""
    <div class="card">

    <h3>
    🤖 Text Emotion Analysis
    </h3>

    <h2>
    {detected_text_emotion}
    </h2>

    </div>
    """, unsafe_allow_html=True)

    # TEXT PLAYLIST
    text_playlist = emotion_to_playlist[
        detected_text_emotion
    ]

    st.markdown(f'''
    <iframe
    style="border-radius:12px"
    src="{text_playlist}"
    width="100%"
    height="352"
    frameBorder="0"
    allow="autoplay; encrypted-media"
    loading="lazy">
    </iframe>
    ''', unsafe_allow_html=True)

# -----------------------------------
# MEDIAPIPE
# -----------------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

LANDMARKS = {

    "left_mouth": 61,
    "right_mouth": 291,
    "top_lip": 13,
    "bottom_lip": 14,
    "left_eye_top": 159,
    "left_eye_bottom": 145,
    "right_eye_top": 386,
    "right_eye_bottom": 374,
}

# -----------------------------------
# HELPER
# -----------------------------------
def get_point(landmarks, idx, width, height):

    lm = landmarks.landmark[idx]

    return np.array([
        int(lm.x * width),
        int(lm.y * height)
    ])

# -----------------------------------
# LAYOUT
# -----------------------------------
col1, col2 = st.columns([2,1])

# -----------------------------------
# CAMERA ON
# -----------------------------------
if run:

    cap = cv2.VideoCapture(0)

    frame_placeholder = col1.empty()

    emotion_placeholder = col2.empty()

    stats_placeholder = col2.empty()

    graph_placeholder = col2.empty()

    spotify_placeholder = col2.empty()

    while True:

        ret, frame = cap.read()

        if not ret:

            st.error("Camera not working")
            break

        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb)

        emotion = "Neutral"

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:

                pts = {

                    key: get_point(
                        face_landmarks,
                        idx,
                        w,
                        h
                    )

                    for key, idx in LANDMARKS.items()
                }

                mouth_width = np.linalg.norm(
                    pts["right_mouth"]
                    - pts["left_mouth"]
                )

                mouth_open = abs(
                    pts["bottom_lip"][1]
                    - pts["top_lip"][1]
                )

                eye_height = (

                    abs(
                        pts["left_eye_bottom"][1]
                        - pts["left_eye_top"][1]
                    )

                    +

                    abs(
                        pts["right_eye_bottom"][1]
                        - pts["right_eye_top"][1]
                    )

                ) / 2

                smile_ratio = (
                    mouth_open / mouth_width
                )

                eye_ratio = (
                    eye_height / mouth_width
                )

                if smile_ratio > 0.30:
                    emotion = "Happy"

                elif smile_ratio < 0.08:
                    emotion = "Sad"

                elif eye_ratio > 0.35:
                    emotion = "Surprised"

                else:
                    emotion = "Neutral"

                for pt in pts.values():

                    cv2.circle(
                        frame,
                        tuple(pt),
                        2,
                        (0,255,0),
                        -1
                    )

        emotion_history.append(emotion)

        dominant_emotion = max(
            set(emotion_history),
            key=emotion_history.count
        )

        analytics_data.append(
            dominant_emotion
        )

        st.session_state.last_played = dominant_emotion

        # WEBCAM
        frame_placeholder.image(
            cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

        # EMOTION
        emotion_placeholder.markdown(f'''
        <div class="emotion-box">
        😊 {dominant_emotion}
        </div>
        ''', unsafe_allow_html=True)

        # STATS
        stats_placeholder.markdown(f'''
        <div class="card">

        <h3>📊 Live Analysis</h3>

        <p><b>Emotion:</b> {dominant_emotion}</p>

        <p><b>Camera:</b> Active</p>

        <p><b>Last Played:</b>
        {st.session_state.last_played}</p>

        </div>
        ''', unsafe_allow_html=True)

        # ANALYTICS GRAPH
        emotion_df = pd.DataFrame({

            "Frame":
            list(range(len(analytics_data))),

            "Emotion":
            analytics_data
        })

        fig = px.area(

            emotion_df,

            x="Frame",

            y=[1] * len(emotion_df),

            color="Emotion",

            title="📈 Live Emotion Trend Analytics"
        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor=bg_color,

            plot_bgcolor=card_color,

            font_color=text_color,

            height=400
        )

        graph_placeholder.plotly_chart(
            fig,
            use_container_width=True
        )

        # PLAYLIST
        spotify_url = emotion_to_playlist[
            dominant_emotion
        ]

        spotify_placeholder.markdown(f'''
        <iframe
        style="border-radius:12px"
        src="{spotify_url}"
        width="100%"
        height="352"
        frameBorder="0"
        allow="autoplay; encrypted-media"
        loading="lazy">
        </iframe>
        ''', unsafe_allow_html=True)

        time.sleep(0.03)

    cap.release()

# -----------------------------------
# CAMERA OFF
# -----------------------------------
else:

    st.info(
        "📷 Camera is OFF"
    )

    neutral_song = emotion_to_playlist[
        "Neutral"
    ]

    st.markdown(f'''
    <iframe
    style="border-radius:12px"
    src="{neutral_song}"
    width="100%"
    height="352"
    frameBorder="0"
    allow="autoplay; encrypted-media"
    loading="lazy">
    </iframe>
    ''', unsafe_allow_html=True)

# -----------------------------------
# RECENT HISTORY
# -----------------------------------
emotion_table = pd.DataFrame({

    "Emotion History":
    list(emotion_history)
})

st.markdown(
    "### 📋 Recent Emotion History"
)

st.dataframe(
    emotion_table,
    use_container_width=True
)

# -----------------------------------
# MANUAL SONG
# -----------------------------------
if manual_song:

    st.sidebar.markdown(f'''
    <iframe
    style="border-radius:12px"
    src="{manual_song}"
    width="100%"
    height="352"
    frameBorder="0"
    allow="autoplay; encrypted-media">
    </iframe>
    ''', unsafe_allow_html=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("""
<hr>

<center>

🎧 MelodyMind • AI Emotion Music Dashboard

</center>
""", unsafe_allow_html=True)