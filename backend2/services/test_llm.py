from groq import Groq
import os

# Make sure environment variable is correctly set
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Restart terminal or set it properly.")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Use exact model name from Groq dashboard
    messages=[
        {"role": "user", "content": "Say hello in 2 lines."}
    ],
    temperature=0.4,
    max_tokens=200
)

print(response.choices[0].message.content)