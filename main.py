import streamlit as st
import os
import time 
import whisper
from models.whisper_model import WhisperModel
from models.translate import TranslateModel
from utils.file_utils import overlay_subtitles

# Initialize models
whisper_model = WhisperModel()
translator = TranslateModel()

st.title("Multi-Language Subtitle Generator 🎥")
# File Upload
uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.info("Processing video...")

    # Subtitle Language Selection
    lang1 = st.selectbox("Select First Subtitle Language", ["en","es", "fr", "de", "hi", "zh"])
    lang2 = st.selectbox("Select Second Subtitle Language", ["en","es", "fr", "de", "hi", "zh"])

    # Extract audio & generate subtitles in two languages
    audio_path, srt_path_1, srt_path_2 = whisper_model.extract_audio_and_generate_subtitles(file_path, lang1, lang2)

    # Overlay both subtitles on video
    subtitled_video = overlay_subtitles(file_path, srt_path_1, srt_path_2)

    st.success("Subtitles generated! 🎉")

    # Display Video
    st.video(subtitled_video)

    # Display both subtitles in real-time
    subtitle_display = st.empty()

    def read_subtitles(srt_file):
        """Read subtitles line by line"""
        with open(srt_file, "r") as f:
            lines = f.readlines()
        subtitles = []
        for i in range(0, len(lines), 4):  
            if i + 2 < len(lines):
                timestamp = lines[i + 1].strip()
                text = lines[i + 2].strip()
                start_time = timestamp.split(" --> ")[0]
                subtitles.append((start_time, text))
        return subtitles

    subtitles_1 = read_subtitles(srt_path_1)
    subtitles_2 = read_subtitles(srt_path_2)

    # Read both subtitle files
    def read_srt_file(srt_file):
        """Reads an SRT file and returns the subtitles as a list."""
        with open(srt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        subtitles = []
        for i in range(0, len(lines), 4):  
            if i + 2 < len(lines):
                text = lines[i + 2].strip()
                subtitles.append(text)
        return "\n".join(subtitles)

    # Display all subtitles at once (without real-time mapping)
    if srt_path_1 and srt_path_2:
        lang1_subtitles = read_srt_file(srt_path_1)
        lang2_subtitles = read_srt_file(srt_path_2)

        st.markdown("### **Generated Subtitles**")
        st.markdown(f"**Language 1:**\n```{lang1_subtitles}```", unsafe_allow_html=True)
        st.markdown(f"**Language 2:**\n```{lang2_subtitles}```", unsafe_allow_html=True)
