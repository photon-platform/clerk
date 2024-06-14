import os

API_KEY = os.environ["CODESTRAL_API_KEY"]
import requests

import json

url = "https://codestral.mistral.ai/v1/chat/completions"
data = {
    "model": "codestral-latest",
    "messages": [
        {
            "role": "user",
            "content": "Write code for linear regression model in scikit learn with scaling, you can select  diabetes datasets from the sklearn library.",
        }
    ],
}
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json()["choices"][0]["message"]["content"])

