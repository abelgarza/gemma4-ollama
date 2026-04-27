from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
from pathlib import Path

import customtkinter as ctk
import ollama
from dotenv import load_dotenv

from gemma4_ollama.audio import audio_to_base64, speak

# Configuración visual de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

load_dotenv()

SYSTEM_PROMPT = """
Eres un asistente de voz llamado Gemma 4.
Responde de forma natural, breve y en el mismo idioma del usuario.
No menciones el audio adjunto.
""".strip()

class VoiceChatApp(ctk.CTk):
    def __init__(self, args: argparse.Namespace):
        super().__init__()

        self.args = args
        self.client = ollama.Client(host=args.host)
        self.workdir = Path(args.workdir)
        self.context: list[int] | None = None
        self.recording_process: subprocess.Popen | None = None
        self.is_recording = False
        self.is_processing = False
        self.lock = threading.Lock()
        self._release_timer = None
        
        self.tts_speed = float(os.getenv("TTS_SPEED", 1.2))
        self.tts_lang = os.getenv("TTS_LANG", "es")
        self.workdir.mkdir(parents=True, exist_ok=True)

        # ---- UI Setup ----
        self.title("Gemma 4 Voice Chat")
        self.geometry("500x650")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Arial", 15))
        self.chat_box.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.status_label = ctk.CTkLabel(self, text="Mantén ESPACIO para hablar", font=("Arial", 14, "bold"), text_color="gray")
        self.status_label.grid(row=1, column=0, padx=20, pady=(5, 5))

        self.mic_button = ctk.CTkButton(
            self, text="🎙️", font=("Arial", 32), fg_color="#1f538d", hover_color="#14375e",
            corner_radius=100, height=80, width=80
        )
        self.mic_button.grid(row=2, column=0, padx=20, pady=(0, 20))

        self.bind("<KeyPress-space>", self.on_press)
        self.bind("<KeyRelease-space>", self.on_release)
        self.mic_button.bind("<ButtonPress-1>", self.on_press)
        self.mic_button.bind("<ButtonRelease-1>", self.on_release)

        self.append_chat("Sistema", f"Modelo {self.args.model} listo.")

    def append_chat(self, sender: str, message: str):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{sender}: {message}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def update_status(self, text: str, color: str = "gray"):
        self.status_label.configure(text=text, text_color=color)

    def on_press(self, event=None):
        # Cancelar el evento de soltar si ocurre casi inmediatamente (Key Repeat del OS)
        if self._release_timer:
            self.after_cancel(self._release_timer)
            self._release_timer = None
            
        if self.is_processing: return
        with self.lock:
            if self.is_recording: return
            self.is_recording = True
            
        self.update_status("Grabando...", color="#ff4a4a")
        self.mic_button.configure(fg_color="#ff4a4a")
        
        wav_path = self.workdir / "input.wav"
        
        cmd = [
            "ffmpeg", "-hide_banner",
            "-f", "pulse", "-i", self.args.source,
            "-ac", "1", "-ar", str(self.args.sample_rate),
            "-y", str(wav_path)
        ]
        
        # Guardar stdout/stderr para no saturar la terminal y poder debuggear
        self.recording_process = subprocess.Popen(
            cmd, 
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

    def on_release(self, event=None):
        # Aplicar un pequeño "debounce" si el evento viene del teclado
        if event and getattr(event, 'keysym', '') == 'space':
            self._release_timer = self.after(100, self._do_release)
        else:
            self._do_release()

    def _do_release(self):
        with self.lock:
            if not self.is_recording: return
            self.is_recording = False
            
        if self.recording_process:
            try:
                # Enviar 'q' para detener ffmpeg suavemente y que escriba bien el header WAV
                _, stderr = self.recording_process.communicate(input=b"q", timeout=2)
            except subprocess.TimeoutExpired:
                self.recording_process.kill()
            self.recording_process = None

        self.is_processing = True
        self.mic_button.configure(fg_color="#1f538d")
        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        wav_path = self.workdir / "input.wav"
        
        # Validación
        if not wav_path.exists() or wav_path.stat().st_size < 1000:
            self.after(0, lambda: self.update_status("No se detectó audio (muy corto)", "orange"))
            self.after(2000, self.reset_ui)
            return

        self.after(0, lambda: self.update_status("Gemma 4 pensando...", "#f1c40f"))
        
        try:
            audio_b64 = audio_to_base64(wav_path)
            response = self.client.generate(
                model=self.args.model,
                prompt=SYSTEM_PROMPT,
                images=[audio_b64],
                context=self.context,
                stream=False
            )
            
            response_text = response.get("response", "")
            self.context = response.get("context")
            
            self.after(0, lambda: self.append_chat("Usuario", "🎤 (Audio)"))
            self.after(0, lambda: self.append_chat("Gemma", response_text))
            
            if response_text:
                self.after(0, lambda: self.update_status("Hablando...", "#2ecc71"))
                speak(response_text, speed=self.tts_speed, lang=self.tts_lang)
            
        except Exception as err:
            error_msg = str(err)
            self.after(0, lambda msg=error_msg: self.append_chat("Error de Ollama", msg))
        finally:
            if not self.args.keep_audio:
                wav_path.unlink(missing_ok=True)
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.is_processing = False
        self.update_status("Mantén ESPACIO para hablar", "gray")

def main() -> None:
    parser = argparse.ArgumentParser(description="Gemma 4 PTT Voice Chat UI")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL_AUDIO", "gemma4-audio:latest"))
    parser.add_argument("--host", default=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    parser.add_argument("--source", default=os.getenv("AUDIO_SOURCE", "default"))
    parser.add_argument("--sample-rate", type=int, default=int(os.getenv("AUDIO_SAMPLE_RATE", 16000)))
    parser.add_argument("--workdir", default="data/live-audio")
    parser.add_argument("--keep-audio", action="store_true")
    
    args = parser.parse_args()
    app = VoiceChatApp(args)
    app.mainloop()

if __name__ == "__main__":
    main()
