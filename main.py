import ollama
from audio_gemma4_ollama.ollama_audio import wav_to_base64
from audio_gemma4_ollama.tts import speak
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def voice_chat():
    print("--- Gemma 4 Voice Chat ---")
    print("Presiona Ctrl+C para salir")
    
    # Ruta al archivo de audio que se espera que el sistema de grabación actualice
    AUDIO_INPUT_PATH = "data/live-audio/latest.wav"
    
    try:
        while True:
            # 1. Verificar si hay un nuevo archivo de audio
            if os.path.exists(AUDIO_INPUT_PATH):
                print("\nProcesando audio...")
                
                # 2. Convertir audio a base64 para Ollama
                audio_b64 = wav_to_base64(AUDIO_INPUT_PATH)
                
                # 3. Enviar a Gemma 4
                print("Gemma 4 pensando...")
                response = ollama.chat(
                    model='gemma4-audio',
                    messages=[{
                        'role': 'user',
                        'content': 'Responde de forma concisa y natural para un chat de voz.',
                        'images': [audio_b64] # Asumiendo que el modelo acepta audio en el campo images o similar según la implementación de ollama-audio
                    }]
                )
                
                text_response = response['message']['content']
                print(f"Gemma 4: {text_response}")
                
                # 4. TTS y Reproducción
                print("Sintetizando voz...")
                speak(text_response)
                
                # 5. Limpiar el archivo de entrada para evitar procesar el mismo audio
                # Nota: En un sistema real, esto dependería de cómo se graba el audio.
                # Aquí lo renombramos o eliminamos para esperar el siguiente.
                os.rename(AUDIO_INPUT_PATH, f"{AUDIO_INPUT_PATH}.processed")
                
            # Pequeña pausa para no saturar la CPU
            import time
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nChat finalizado.")

if __name__ == "__main__":
    voice_chat()
