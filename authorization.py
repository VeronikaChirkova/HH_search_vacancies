import os
from sys import exception
import requests
from dotenv import load_dotenv
# import datetime
from datetime import datetime, timedelta
import logging
import textwrap as tw

from send_email import send_email
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename = "mylog.log")

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
    """Получение временного кода, необходимого для получения access и refresh токенов.
    """
    # TODO расширить описание сообщения
    msg = tw.dedent(f"""Сходи по ссылке и забери code
    https://hh.ru/oauth/authorize?response_type=code&client_id={os.getenv("CLIENT_ID")}&redirect_uri=https://hh.ru
    (example code: code=P2TQRI2EJGMQVE6NIR8V8GC0EDAU9G5US8ONKE7MQ3GO5J0CD5HKDFUMMCU6BEOR)
    
    После этого введи в консоли этот код (там где запущено приложение)""")
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
        "redirect_uri": "https://hh.ru",
    }

    response = requests.post("https://api.hh.ru/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()
    logging.info(response.status_code)
    return tokens


def write_file(name_file: str, tokens: dict):
    """Записывает access и refresh токены в файл.

    Args:
        name_file (str): название файла для записи.
    """
    try:
        with open(name_file, "a") as file:
            file.write(f'\nUSER_ACCESS_TOKEN={tokens['access_token']}')
            file.write(f'\nUSER_REFRESH_TOKEN={tokens['refresh_token']}')
            file.write(f'\nEXPIRES_IN={round((tokens['expires_in'])/86400 - 1)}')
            date_now = datetime.now()
            date_need_auth = date_now + timedelta(days=13)
            date_to_str = date_need_auth.strftime("%d.%m.%y")
            file.write(f'\nACCESS_TOKEN_VALID={date_to_str}')
    except Exception:
        logging.error('Ошибка при работе с файлом')
        raise



if __name__ == "__main__":
    tokens = get_user_token()
    write_file('temp3.env',tokens=tokens)