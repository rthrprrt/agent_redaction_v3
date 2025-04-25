from ollama import chat

response = chat(
    model="llama3.1:8b-instruct-q8_0",
    messages=[{"role": "user", "content": "Bonjour, teste !"}],
)
print(response.message.content)
