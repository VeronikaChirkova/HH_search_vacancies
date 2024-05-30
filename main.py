import json
import logging
import os
import time

import requests
from dotenv import load_dotenv
from requests import HTTPError, Session

from authorization import get_temp_user_code, get_user_token, write_file
from consts import DAY_IN_SECONDS, PATH_TO_ENV
from exceptions import EnvNotFoundError, NeedAuthOnHHError, NeedStopProgramError
from hh_API import filter_vacancies, get_vacancies, response_vacancy
from send_email import send_email

load_dotenv(dotenv_path=PATH_TO_ENV)


def auth():
    """Получение необходимых токенов для работы приложения"""
    code = get_temp_user_code()
    tokens = get_user_token(code)
    write_file(tokens=tokens)


def response_vacancies(session: Session):
    """Отклик на вакансии"""
    while True:
        try:
            vacancies = get_vacancies(
                name_vacancia="python",
                area="Новосибирск",
                period=30,
                schedule="fullDay",
                # schedule="remote",
                experience="noExperience",
                # experience="between1And3",
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
                "middle" "Senior",
                "Auto QA",
                "QA",
                "Наставник",
                "Продакт",
                "SDET",
                "Аналитик",
                "Старший инженер",
                "Ведущий",
                "AI",
            ],
        )

        count = 0
        report = []
        if len(filtered_vacancies) > 0:
            for vacancy in filtered_vacancies:
                if vacancy["id"] in open("already_applied_vacancies.txt").read():
                    continue
                else:
                    try:
                        info = response_vacancy(
                            vacancy_id=vacancy["id"], session=session
                        )
                        with open("already_applied_vacancies.txt", "a") as file:
                            json.dump(
                                obj=vacancy["id"], fp=file, ensure_ascii=False, indent=4
                            )
                            msg = vacancy["url"]
                            report.append(msg)
                    except HTTPError as err:
                        logging.info(err.response.content)
                        with open("already_applied_vacancies.txt", "a") as file:
                            json.dump(
                                obj=vacancy["id"], fp=file, ensure_ascii=False, indent=4
                            )
                        continue

            count += 1
            msg = f"Откликнулся на {report}. Новых вакансий нет."
            send_email(message=msg)
            logging.info(msg)
            time.sleep(DAY_IN_SECONDS)

        else:
            info = "По запросу ничего не найдено."
            send_email(message=info)
            logging.debug(info)
            break


def check_envs() -> bool:
    """
    Проверка переменныъх в .env

    --env-file .env
    """
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
    for env_var in checked_variables:
        token = os.getenv(env_var)
        if token is None:
            return False
    return True


def main():
    """Точка входа"""

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename="mylog.log", encoding="utf-8")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=[stream_handler, file_handler],
    )

    if not check_envs():
        msg = "Прочти ридми и установи необходимые переменные."
        logging.critical(msg)
        raise EnvNotFoundError(msg)
    print("ok")
    with requests.Session() as session:
        response_vacancies(session)


if __name__ == "__main__":
    main()
