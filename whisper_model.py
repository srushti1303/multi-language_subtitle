import whisper
import ffmpeg
import os
from models.translate import TranslateModel  # Import the translation model

class WhisperModel:
    def __init__(self, model_name="small"):
        self.model = whisper.load_model(model_name)
        self.translator = TranslateModel()  # Initialize translation model

    def extract_audio_and_generate_subtitles(self, video_path, lang1="es", lang2="fr"):
        """Extracts audio and generates subtitles in two languages."""
        audio_path = video_path.replace(".mp4", ".wav")
        
        # Extract audio
        ffmpeg.input(video_path).output(audio_path, ar=16000, ac=1, format="wav").run(overwrite_output=True)

        # Transcribe audio with Whisper
        result = self.model.transcribe(audio_path)

        # Create subtitle files for both languages
        srt_path_1 = video_path.replace(".mp4", f"_{lang1}.srt")
        srt_path_2 = video_path.replace(".mp4", f"_{lang2}.srt")

        with open(srt_path_1, "w") as f1, open(srt_path_2, "w") as f2:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]

                # Translate text into two languages
                translated_text_1 = self.translator.translate_text(text, lang1)
                translated_text_2 = self.translator.translate_text(text, lang2)

                # Write to first subtitle file
                f1.write(f"{segment['id']}\n")
                f1.write(f"{self.format_time(start)} --> {self.format_time(end)}\n")
                f1.write(f"{translated_text_1}\n\n")

                # Write to second subtitle file
                f2.write(f"{segment['id']}\n")
                f2.write(f"{self.format_time(start)} --> {self.format_time(end)}\n")
                f2.write(f"{translated_text_2}\n\n")

        return audio_path, srt_path_1, srt_path_2  # Return both subtitle files

    def format_time(self, seconds):
        """Convert seconds to SRT timestamp format"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
