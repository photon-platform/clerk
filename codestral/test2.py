import os
import requests
import json
from rich import print

API_KEY = os.environ["CODESTRAL_API_KEY"]
BASE_URL = "https://codestral.mistral.ai/v1"

def get_chat(prompt, model="codestral-latest"):
    url = f"{BASE_URL}/chat/completions"
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def get_fim(prompt, suffix, model="codestral-latest"):
    url = f"{BASE_URL}/fim/completions"
    data = {
        "model": model,
        "prompt": prompt,
        "suffix": suffix,
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# Example usage
chat_prompt = "write python module for demonstrating gold and silver ratio"
#  print(get_chat(chat_prompt))

fill_prompt = "def my_function():\n"
suffix = "result = my_function()\nprint(result)"
middle = get_fim(fill_prompt, suffix)

code = f"""
{fill_prompt}
{middle}
{suffix}
"""

print(code)
