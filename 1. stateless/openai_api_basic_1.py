import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {
            'role': 'system',
            'content': '日本語で返答してください',
        },
        {
            'role': 'user',
            'content': "日本の現在の首領は誰ですか?",
        },
        {
            'role': 'assistant',
            'content': " 現在の日本の内閣総理大臣は菅義偉（すが・よしひで）です。"
        },
        {
            'role': 'user',
            'content': '彼の出身地は？'
        },
    ],
)

print(f'response: {response}')
print(f'message_content: {response.get("choices")[0].get("message").get("content")}')

