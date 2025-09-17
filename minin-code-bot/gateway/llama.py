import requests
import json

from config import LLAMA


def get_llama_answer(prompt):
    r = requests.post(
        LLAMA,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    data = r.content.decode("utf-8")
    res = json.loads(data)["response"]
    return res
