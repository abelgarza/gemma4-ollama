from gtts import gTTS
import os
import subprocess
from pathlib import Path

def text_to_speech(text: str, output_file: str = "response.mp3"):
    """
    Converts text to speech and saves it to a file.
    """
    tts = gTTS(text=text, lang='es')
    tts.save(output_file)
    return output_file

def play_audio(file_path: str):
    """
    Plays the audio file using a system player (e.g., mpv or mpg123).
    """
    try:
        # Intentamos usar mpv que es común en linux
        subprocess.run(["mpv", "--no-video", file_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Alternativa: mpg123
            subprocess.run(["mpg123", file_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Error: No se encontró un reproductor de audio compatible (mpv o mpg123) para reproducir {file_path}")

def speak(text: str):
    """
    Converts text to speech and plays it immediately.
    """
    file_path = text_to_speech(text)
    play_audio(file_path)
    # Optional: remove file after playing
    # os.remove(file_path)
