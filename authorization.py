import code
import logging
import os
import textwrap as tw
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv, set_key

from consts import PATH_TO_ENV
from send_email import send_email

load_dotenv()


def get_app_token():
    """Получение токена приложения.
    Интервал запроса токена приложения - Х секунд.
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": os.getenv("USER_AGENT"),
    }

    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }

    response = requests.post("https://hh.ru/oauth/token", data=data, headers=headers)
    response.raise_for_status()
    response.json()
    logging.info(response.status_code)


def get_temp_user_code() -> str:
    """Получение временного кода, необходимого для получения access и refresh токенов."""

    msg = tw.dedent(
        f"""Сходи по ссылке, авторизуйся и в адресной строке забери code
    https://hh.ru/oauth/authorize?response_type=code&client_id={os.getenv("CLIENT_ID")}
    (example code: code=P2TQRI2EJGMQVE6NIR8V8GC0EDAU9G5US8ONKE7MQ3GO5J0CD5HKDFUMMCU6BEOR)

    После этого введи в консоли этот код (там где запущено приложение)"""
    )
    send_email(msg)
    run = True
    code = ""
    while run:
        code = input("Вставь code: ")
        if len(code) != 64:
            run = False
        else:
            break
    return code

    # TODO прикути django и сработает.
    # headers = {
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "User-Agent": os.getenv("USER_AGENT"),
    # }
    # params = {
    #     "response_type": "code",
    #     "client_id": os.getenv("CLIENT_ID"),
    #     "redirect_uri": "https://hh.ru",
    # }
    # url = "https://hh.ru/oauth/authorize"
    # response = requests.get(url, params=params, headers=headers)
    # response.raise_for_status()
    # logging.info(response.status_code)


def get_user_token(code: str) -> dict:
    """Получение access и refresh токенов.

    Args:
        code (str): временный код, полученный при авторизации.

    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": os.getenv("USER_AGENT"),
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://hh.ru/",
    }

    response = requests.post("https://api.hh.ru/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()
    logging.info(response.status_code)
    return tokens


def write_file(tokens: dict):
    """Записывает access и refresh токены в файл.

    Args:
        tokens (dict): словарь токенов.
    """
    # set variables in .env file
    set_key(PATH_TO_ENV, "USER_ACCESS_TOKEN", tokens["access_token"])
    set_key(PATH_TO_ENV, "USER_REFRESH_TOKEN", tokens["refresh_token"])
    set_key(PATH_TO_ENV, "EXPIRES_IN", str(round((tokens["expires_in"]) / 86400 - 1)))
    date_now = datetime.now()
    date_need_auth = date_now + timedelta(days=13)
    date_to_str = date_need_auth.strftime("%d.%m.%y")
    set_key(PATH_TO_ENV, "ACCESS_TOKEN_VALID", date_to_str)

    # update variables in memory
    os.environ["USER_ACCESS_TOKEN"] = tokens["access_token"]
    os.environ["USER_REFRESH_TOKEN"] = tokens["refresh_token"]
    os.environ["EXPIRES_IN"] = str(round((tokens["expires_in"]) / 86400 - 1))
    os.environ["ACCESS_TOKEN_VALID"] = date_to_str


if __name__ == "__main__":
    code = get_temp_user_code()
    tokens = get_user_token(code)
    write_file(tokens)
