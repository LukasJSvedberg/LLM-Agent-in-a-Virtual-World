from openai import OpenAI
import os
client = OpenAI()

print("before request")
print("KEY:", os.getenv("OPENAI_API_KEY"))
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hello in one word."
)
print("after request")
print(response.output_text)