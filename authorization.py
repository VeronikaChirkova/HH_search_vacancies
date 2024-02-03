import os
from sys import exception
import requests
from dotenv import load_dotenv
import datetime
import logging
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


def get_temp_user_code():
    """Получение временного кода, необходимого для получения access и refresh токенов.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": os.getenv("USER_AGENT"),
    }
    params = {
        "response_type": "code",
        "client_id": os.getenv("CLIENT_ID"),
        "redirect_uri": "https://hh.ru",
    }
    url = "https://hh.ru/oauth/authorize"
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    logging.info(response.status_code)


def get_user_token() -> dict:
    """Получение access и refresh токенов.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": os.getenv("USER_AGENT"),
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": os.getenv("TEMP_USER_CODE"),
        "grant_type": "authorization_code",
        "redirect_uri": "https://hh.ru",
    }

    response = requests.post("https://api.hh.ru/token", data=data, headers=headers)
    response.raise_for_status()
    tokens = response.json()
    logging.info(response.status_code)
    return tokens


def write(name_fale: str, tokens: dict, date: str):
    """Записывает access и refresh токены в файл.

    Args:
        name_fale (str): название файла для записи.
    """
    try:
        with open(name_fale, "a") as file:
            file.write(f'\nUSER_ACCESS_TOKEN={tokens['access_token']}')
            file.write(f'\nUSER_REFRESH_TOKEN={tokens['refresh_token']}')
            file.write(f'\nEXPIRES_IN={round((tokens['expires_in'])/86400 - 1)}')
            start_date = datetime.datetime.strptime(date, "%m/%d/%y")
            end_date = start_date + datetime.timedelta(days=13)
            file.write(f'\nACCESS_TOKEN_VALID={end_date}')
    except Exception:
        logging.error('Ошибка при работе с файлом')
        # print('Ошибка при работе с файлом')
        raise



if __name__ == "__main__":
    tokens = get_user_token()
    write('temp.env',tokens=tokens, date="01/30/24")
