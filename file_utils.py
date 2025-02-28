import os
import ffmpeg
import streamlit as st

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

def save_uploaded_file(uploaded_file):
    """Save uploaded file to the uploads directory."""
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Handle file writing safely
        try:
            with open(file_path, "wb") as buffer:
                buffer.write(uploaded_file.read())  # Use read() instead of getvalue()
            return file_path
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return None
    return None

def extract_audio(video_path):
    """Extract audio from a video file using FFmpeg."""
    try:
        audio_path = os.path.splitext(video_path)[0] + ".wav"  # Safer filename handling

        # Ensure FFmpeg works
        ffmpeg.input(video_path).output(audio_path, ar=16000, ac=1, format="wav").run(overwrite_output=True)
        
        return audio_path
    except ffmpeg.Error as e:
        st.error(f"FFmpeg error: {e}")
        return None

def overlay_subtitles(video_path, srt_path_1, srt_path_2):
    """Burn two subtitles onto video using FFmpeg"""
    output_video = video_path.replace(".mp4", "_subtitled.mp4")

    ffmpeg.input(video_path).output(
        output_video,
        vf=f"[in]subtitles={srt_path_1}:force_style='Alignment=1,FontSize=8'[tmp]; [tmp]subtitles={srt_path_2}:force_style='Alignment=5,FontSize=8'[out]"
    ).run(overwrite_output=True)

    return output_video
