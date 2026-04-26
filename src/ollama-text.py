import ollama

response = ollama.generate(
    model='gemma4:latest',
    prompt='Hola',
    stream=False
)

print(response['response'])
