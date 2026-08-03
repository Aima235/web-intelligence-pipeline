from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

response = client.chat.completions.create(
    model="qwen2.5-1.5b-instruct",
    messages=[
        {
            "role": "user",
            "content": "What is 2 + 2?"
        }
    ]
)

print(response.choices[0].message.content)