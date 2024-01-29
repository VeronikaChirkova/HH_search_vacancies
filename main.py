import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


def get_app_token():
    """Получение токена приложения.
    Интервал запроса токена приложения - Х секунд.
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }

    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }

    response = requests.post("https://hh.ru/oauth/token", data=data, headers=headers)
    response.raise_for_status()

def get_temp_user_code():
    """Получение временного кода, необходимого для получения access и refresh токенов.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }
    params = {
        "response_type": "code",
        "client_id": os.getenv("CLIENT_ID"),
        "redirect_uri": "https://hh.ru",
    }
    url = "https://hh.ru/oauth/authorize"
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    print(response.text)

def get_user_token():
    """Получение access и refresh токенов.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": os.getenv("TEMP_USER_CODE"),
        "grant_type": "authorization_code",
        "redirect_uri": "https://hh.ru",
    }
    response = requests.post("https://hh.ru/oauth/token", data=data, headers=headers)
    response.raise_for_status()

def get_vacancies() -> list[dict]:
    """Поиск вакансий на HeadHunter.
    """

    headers = {
        "Authorization": f"{"Bearer"} {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent":  f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }
    params = {
        "per_page": "100",
        "text": "Ведущий инженер-химик",
        "search_field": "name",
        "experience": "between1And3",
        "employment": "full",
        "schedule": "fullDay",
        "area": "4"
    }
    response = requests.get(
        "https://api.hh.ru/vacancies", params=params, headers=headers
    )
    response.raise_for_status
    vacancia: dict = response.json()
    # print(vacancia)

    vacancies: list[dict] = []
    for item in vacancia["items"]:
        vacancies.append(
        {"name": item["name"], "url": item["url"], "salary": item["salary"],
        "experience": item["experience"]}
        )
    return vacancies


def get_areas(name: str):
    """Получает id страны/региона/города

    Args:
        name (str): название страны/региона/города

    Returns:
        _type_: id страны/региона/города
    """
    headers = {
        "Authorization": f"{"Bearer"} {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }

    url = "https://api.hh.ru/areas"
    response = requests.get(url, headers=headers)
    response.raise_for_status
    countries = response.json()

    for country in countries:
        #FIXME hardcode
        if country["name"] == name:
            return country["id"]
        for region in country["areas"]:
            if region["name"] == name:
                return region["id"]
            else:
                for city in region["areas"]:
                    if city["name"] == name:
                        return city["id"]
    return f'{name}: не найдено'

def filter_vacancies(vacancies: list, blacklist: list) -> list:
    """Фильтр списка вакансий:
    1. На наличие заработной платы
    2. На вхождение слов из названия вакансии в blacklist

    Args:
        vacancies (list): список вакансий
        blacklist (list): список недопустимых слов.

    Returns:
        list: список отфильтрованных вакансий.
    """
    filtered_vacancies = []
    blacklist = ['Python 2', 'PyQt', 'C++', 'Преподаватель', 'Курсовые работы',
                'Middle', 'Senior', 'Auto QA']

    for vacancy in vacancies:
        if vacancy["salary"] == None:
            continue
        elif blacklist:
            for word in blacklist:
                if word in vacancy['name']:
                    break
            else:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies

def get_id_resume():
    """Получение id моего резюме.
    """

    headers = {
        "Authorization": f"{"Bearer"} {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }

    url = "https://api.hh.ru/resumes/mine"
    response = requests.get(url, headers=headers)
    response.raise_for_status
    resume: dict = response.json()
    #resumes_id
    id_resume: list[dict] = []
    for item in resume["items"]:
        id_resume.append(
        {"id": item["id"]}
        )
    return id_resume
    # print(id_resume)

def response_vacancy():
    """Отклик на вакансию.
    """
    headers = {
        "Authorization": f"{"Bearer"} {os.getenv("USER_ACCESS_TOKEN")}",
        "HH-User-Agent": f"{"MyApp/1.0"} {os.getenv("CLIENT_EMAIL")}",
    }

    params = {
        "resume_id": os.getenv("ID_RESUME"),
        "vacancy_id": "91417807",
        "message": "Здравствуйте! Данный отклик отправлен в рамках реализации проекта по автоматизации поиска вакансий."
        }

    url = "https://api.hh.ru/negotiations"
    response = requests.post(url, params=params, headers=headers)
    response.raise_for_status
    print(response)
    #logging.info(response.status_code)


if __name__ == "__main__":
    # get_app_token()
    # get_user_token()
    # get_temp_code()
    # get_vacancies()
    # vacancies = get_vacancies()
    # get_vacancies_with_salary(vacancies=vacancies)
    # area_id = get_areas(name="Новосибирск")
    # print(area_id)
    # get_id_resume()
    # response_vacancy()
    # blacklist = ['Python 2', 'PyQt', 'C++', 'Преподаватель', 'Курсовые работы',
    #             'Middle', 'Senior', 'Auto QA']
    # filter_vacancies(vacancies=vacancies, blacklist=blacklist)