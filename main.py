import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_app_token():
    # в течение Х секунд не дает новый токен
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MyApp/1.0 (my-app-feedback@example.com)",
    }
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }
    resp = requests.post("https://hh.ru/oauth/token", params=params, headers=headers)
    print(resp.json())


def get_user_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MyApp/1.0 (my-app-feedback@example.com)",
    }
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": os.getenv("TEMP_USER_CODE"),
        "grant_type": "authorization_code",
        "redirect_uri": "https://hh.ru",
    }
    resp = requests.post("https://hh.ru/oauth/token", params=params, headers=headers)
    print(resp.json())


if __name__ == "__main__":
    # get_app_token()
    # get_user_token()
    CLIENT_ID = os.getenv("CLIENT_ID")

    print(CLIENT_ID)
