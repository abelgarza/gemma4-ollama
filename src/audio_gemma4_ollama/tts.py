from gtts import gTTS
import os
import subprocess
from pathlib import Path

def text_to_speech(text: str, lang: str = 'es', output_file: str = "response.mp3"):
    """
    Converts text to speech and saves it to a file.
    """
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    return output_file

def play_audio(file_path: str, speed: float = 1.0):
    """
    Plays the audio file using ffmpeg with speed control.
    """
    # Usamos ffplay con filtro de audio atempo para cambiar velocidad sin afectar el tono
    # Nota: atempo solo acepta valores entre 0.5 y 2.0.
    speed_filter = f"atempo={speed}"
    
    cmd = [
        "ffplay",
        "-nodisp",
        "-autoexit",
        "-loglevel", "quiet",
        "-af", speed_filter,
        file_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Respaldo usando ffmpeg + aplay si ffplay no está disponible
        try:
            p1 = subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i", file_path, "-filter:a", speed_filter, "-f", "wav", "-"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["aplay", "-q"], stdin=p1.stdout)
            if p1.stdout:
                p1.stdout.close()
            p2.communicate()
            if p2.returncode == 0:
                return
        except Exception:
            pass

    print(f"Error: No se pudo reproducir el audio con velocidad {speed}x")

def speak(text: str, speed: float = 1.0, lang: str = 'es'):
    """
    Converts text to speech and plays it immediately.
    """
    file_path = text_to_speech(text, lang=lang)
    play_audio(file_path, speed=speed)
    
    try:
        os.remove(file_path)
    except OSError:
        pass
