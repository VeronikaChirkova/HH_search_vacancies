import os
import requests
import time
from requests import Session
from dotenv import load_dotenv
from pprint import pprint
from send_email import send_email
from hh_API import response_vacancy
from hh_API import get_vacancies
load_dotenv()


def auth():
    """Получение необходимых токенов для работы приложения"""
    # files in auth.py
    pass

def response_vacancies(session: Session):
    """Отклик на вакансии"""
    filtered_vacancies = get_vacancies(name_vacancia="python junior", area="Новосибирск",
    period=30, schedule="remote", experience="noExperience", session=session)
    for vacancy in filtered_vacancies:
        response_vacancy(vacancy_id=vacancy['id'], session=session)

def check_envs() -> bool:
    """
    Прочитать файл с переменными .env
    Убедиться что переменные которые надо установить вручную - есть и имеют значения.
    Если все ок-  вернуть True, иначе False
    """
    with open(".env", "r") as file:
        readed_file = file.read()
        res = readed_file.split("\n")

    checked_variables = ["CLIENT_EMAIL", "ID_RESUME", "CLIENT_ID", "CLIENT_SECRET", "APP_TOKEN", "TEMP_USER_CODE", "EMAIL_LOGIN", "EMAIL_PASSWORD", "SENDER_MAIL", "RECEIVERS_MAIL"]
    res_keys = [res_str.split("=")[0] for res_str in res if len(res_str)>1]
    for key in checked_variables:
        if not key in res_keys:
            return False
            # raise ValueError("Необходимо указать ключ и значение. Прочти Readme!")
        for env_str in res:
            splitted_str: list = env_str.split("=")
            if key == splitted_str[0]:
                if len(splitted_str) <2:
                    return False
                    # raise ValueError("Значение тоже надо указать. Пример: ключ=значение")
    return True

def check_auth():
    """
    Проверить в .env дату последнего получения ключей авторизации.
    """

def main():
    """Точка входа"""
    if not check_envs():
        print("Прочти ридми и установи необходимые переменные.")
        raise Exception("Прочти ридми и установи необходимые переменные.")

    with requests.Session() as session:
            response_vacancies(session)


if __name__ == "__main__":
    # main()
    print(check_envs())