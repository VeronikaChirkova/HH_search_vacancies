import logging
import os
import time
from venv import logger

import requests
from dotenv import load_dotenv
from requests import Session, session

from exceptions import NeedAuthOnHHError
from send_email import send_email

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename = "mylog.log")

def get_areas(name: str, session: Session):
    """Поиск id страны/региона/города.

    Args:
        name (str): название страны/региона/города.

    Returns:
        str: id страны/региона/города.
    """

    headers = {
        "Authorization": f"Bearer {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": os.getenv("USER_AGENT"),
    }

    url = "https://api.hh.ru/areas"
    response = session.get(url, headers=headers)
    response.raise_for_status
    countries = response.json()

    for country in countries:
        if country["name"] == name:
            return country["id"]
        for region in country["areas"]:
            if region["name"] == name:
                return region["id"]
            else:
                for city in region["areas"]:
                    if city["name"] == name:
                        return city["id"]
    logging.critical(f'{name}: не найдено')


def get_vacancies(name_vacancia: str, area: str, period: int, schedule: str,
experience: str, session: Session) -> list[dict]:
    """Поиск вакансий на HeadHunter.

    name_vacancia: название вакансии,
    area: название города или региона,
    period: количество дней, в пределах которых производится поиск по вакансиям,
    schedule: график работы (remote - удаленная работа, fullDay - полный день, shift - сменный график, flexible - гибкий график),
    experience: опыт работы (noExperience - нет опыта,
    between_1_and_3 - от 1 года до 3 лет, between_3_and_6 = от 3 до 6 лет, more_6 = более 6 лет.
    """

    headers = {
        "Authorization": f"Bearer {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": os.getenv("USER_AGENT"),
    }

    params = {
        "per_page": "100",
        "text": name_vacancia,
        "search_field": "name",
        "experience": experience,
        "employment": "full",
        "schedule": schedule,
        "area": get_areas(name=area, session=session),
        "period": period
    }

    response = session.get("https://api.hh.ru/vacancies", params=params, headers=headers)
    response.raise_for_status
    logging.info(response.status_code)
    vacancia: dict = response.json()

    if vacancia.get("errors"):
        raise NeedAuthOnHHError("Need authorization on Headhunter")

    vacancies: list[dict] = []
    for item in vacancia["items"]:
        vacancies.append(
        {"name": item["name"], "id": item["id"], "url": item["url"], "salary": item["salary"],
        "experience": item["experience"]}
        )
    return vacancies


def filter_vacancies(vacancies: list, blacklist: list) -> list:
    """Фильтр списка вакансий:
    1. На наличие заработной платы.
    2. На вхождение слов из названия вакансии в blacklist.

    Args:
        vacancies (list): список вакансий.
        blacklist (list): список недопустимых слов.

    Returns:
        list: список отфильтрованных вакансий.
    """

    filtered_vacancies = []
    blacklist = ['Python 2', 'PyQt', 'C++', 'Преподаватель', 'Курсовые работы',
                'Middle', 'Senior', 'Auto QA', 'Наставник']

    for vacancy in vacancies:
        if vacancy["salary"] == None:
            continue
        elif blacklist:
            for word in blacklist:
                if word in vacancy['name']:
                    break
            else:
                filtered_vacancies.append(vacancy)
    logger.debug("Составлен список отфильтрованых вакансий")
    return filtered_vacancies


def response_vacancy(vacancy_id:int, session: Session):
    """Отклик на вакансию.
    """
    headers = {
        "Authorization": f"Bearer {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": os.getenv("USER_AGENT"),
    }
    print(headers)
    params = {
        "resume_id": os.getenv("ID_RESUME"),
        "vacancy_id": vacancy_id,
        "message": "Здравствуйте! Данный отклик отправлен в рамках реализации проекта по автоматизации поиска вакансий."
        }

    url = "https://api.hh.ru/negotiations"
    response = session.post(url, params=params, headers=headers)
    response.raise_for_status
    time.sleep(30)
    logging.info(response.status_code)


if __name__ == "__main__":
    get_vacancies(name_vacancia="python junior",
                    area="Новосибирск",
                    period=30,
                    schedule="remote",
                    experience="noExperience",
                    session=session())
