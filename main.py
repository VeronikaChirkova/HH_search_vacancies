import logging
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from requests import Session, session

import authorization
from authorization import get_app_token, get_temp_user_code, get_user_token, write_file
from exceptions import EnvNotFoundError, NeedAuthOnHHError, NeedStopProgramError
from hh_API import filter_vacancies, get_vacancies, response_vacancy
from send_email import send_email

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="mylog.log",
)

DAY_IN_SECONDS = 86400


def auth():
    """Получение необходимых токенов для работы приложения"""
    code = get_temp_user_code()
    tokens = get_user_token(code)
    write_file(name_file=".env", tokens=tokens)


def response_vacancies(session: Session):
    """Отклик на вакансии"""
    while True:
        try:
            vacancies = get_vacancies(
                name_vacancia="Python",
                area="Новосибирск",
                period=30,
                schedule="remote",
                experience="noExperience",
                session=session,
            )
        except NeedAuthOnHHError:
            auth()
            continue
        except Exception:
            raise NeedStopProgramError("Произошла непредвиденная ошибка")

        filtered_vacancies = filter_vacancies(
            vacancies=vacancies,
            blacklist=[
                "Python 2",
                "PyQt",
                "C++",
                "Преподаватель",
                "Курсовые работы",
                "Middle",
                "Senior",
                "Auto QA",
                "Наставник",
            ],
        )
        report = []
        counter = 0
        if len(filtered_vacancies) > 0:
            for vacancy in filtered_vacancies:
                info = response_vacancy(vacancy_id=vacancy["id"], session=session)
                report.append(info)
                logging.info("Осуществлен отклик на все вакансии.")
                counter += 1
                if counter == 50:
                    break
            send_email(message=report)
        else:
            info = "Новых вакансий нет."
            send_email(message=info)
            logging.debug(info)
            time.sleep(DAY_IN_SECONDS)


def check_envs() -> bool:
    """
    Проверка переменныъх в .env
    """
    with open(".env", "r") as file:
        readed_file = file.read()
        res = readed_file.split("\n")

    # checked_variables = ["CLIENT_EMAIL", "ID_RESUME", "CLIENT_ID", "CLIENT_SECRET", "APP_TOKEN", "TEMP_USER_CODE", "EMAIL_LOGIN", "EMAIL_PASSWORD", "SENDER_MAIL", "RECEIVERS_MAIL"]
    checked_variables = [
        "USER_AGENT",
        "CLIENT_EMAIL",
        "ID_RESUME",
        "CLIENT_ID",
        "CLIENT_SECRET",
        "EMAIL_LOGIN",
        "EMAIL_PASSWORD",
        "SENDER_MAIL",
        "RECEIVERS_MAIL",
    ]
    res_keys = [res_str.split("=")[0] for res_str in res if len(res_str) > 1]
    for key in checked_variables:
        if not key in res_keys:
            return False
        for env_str in res:
            splitted_str: list = env_str.split("=")
            if key == splitted_str[0]:
                if len(splitted_str) < 2:
                    return False
    return True


def main():
    """Точка входа"""
    if not check_envs():
        msg = "Прочти ридми и установи необходимые переменные."
        logging.critical(msg)
        raise EnvNotFoundError(msg)

    with requests.Session() as session:
        response_vacancies(session)


if __name__ == "__main__":
    main()
    # print(check_envs())
