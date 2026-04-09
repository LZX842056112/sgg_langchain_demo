from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": "你是谁"}])
print(res)
