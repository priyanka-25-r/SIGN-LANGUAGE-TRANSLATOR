import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
import cv2
import random
import pyttsx3

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Chat log
if "chat_log" not in st.session_state:
    st.session_state.chat_log = ["👋 Welcome to the sign translator!"]

# Text-to-Speech
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Video transformer
class HandSignTranslator(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)

            # --- SIMULATED PREDICTION ---
            if random.random() > 0.98:  # Random chance to simulate recognition
                signs = ["Hello", "How are you?", "Thank you", "My name is..."]
                random_sign = random.choice(signs)
                st.session_state.chat_log.append(f"🤟 {random_sign}")
                speak_text(random_sign)

        return img


st.title("🤟 Sign-to-Text Translator (Streamlit)")
st.write("This demo uses *MediaPipe Hands* in Python.")

# Webcam feed
webrtc_streamer(
    key="sign-translator",
    video_transformer_factory=HandSignTranslator,
    media_stream_constraints={"video": True, "audio": False}
)

# Display Translated Text
st.subheader("Translated Text")
if st.session_state.chat_log:
    st.success(st.session_state.chat_log[-1])

# Chat log
st.subheader("Chat Conversation")
for msg in st.session_state.chat_log:
    st.write(msg)

# Reverse Mode (Text → Sign GIFs)
st.subheader("Text-to-Sign (Reverse Mode)")
user_input = st.text_input("Type a word (e.g. hello, thank you, how are you)")
if st.button("Show Sign"):
    signs = {
        "hello": "https://media.giphy.com/media/xT0xeuXk8N5962e2w8/giphy.gif",
        "thank you": "https://media.giphy.com/media/l4pT0S1U81F0zJbQo/giphy.gif",
        "how are you": "https://media.giphy.com/media/Vz2Ff7LdM1K0hS0hQ5/giphy.gif",
    }
    gif_url = signs.get(user_input.lower(), "https://placehold.co/400x150?text=Sign+Not+Found")
    st.image(gif_url, caption=f"Sign for: {user_input}")