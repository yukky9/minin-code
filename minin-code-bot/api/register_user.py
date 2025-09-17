import requests
from config import API


def register_user(username, user_id):
    req = requests.post(API + "/user", json={"username": username, "id": user_id})
    if req.status_code != 200:
        raise requests.exceptions.RequestException
