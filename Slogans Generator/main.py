from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv('api_key'),
)


def generate_slogan(word1, word2, word3, tone):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Stwórz slogan w tonie {tone}, z wykorzystaniem słów {word1}, {word2}, {word3} "},
        ]
    )
    return response.choices[0].message.content

def main():
    word1, word2, word3, tone = input("Type three words and slogan tone (after spacebar): ").split()
    result = generate_slogan(word1, word2, word3, tone)
    print(result)

main()


