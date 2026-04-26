import os
import ollama

model = os.getenv("OLLAMA_MODEL", "gemma4:latest")

response = ollama.generate(
    model=model,
    prompt='Hola',
    stream=False
)

print(response['response'])
