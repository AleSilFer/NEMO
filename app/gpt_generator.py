import openai
from app import config

# Configura a API Key da OpenAI
openai.api_key = config.OPENAI_API_KEY

def generate_code(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200,
        temperature=0.2
    )
    result = response['choices'][0]['message']['content']
    return {"generated_code": result}
