from gtts import gTTS
import os
import tempfile

def speak_text_to_file(text):
    """Convert text to speech and return the path to the audio file."""
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name  # Path can be returned to frontend for audio playback
