# Получение вакансий по API

1.Создание проекта, файл main.py, файл с инструкцией формата .md<br>
2.Виртуальное окружение, активировать!<br>
Create
```bash
python -m venv venv
```
Activate
```
.\venv\Scripts\activate
```
3.Установили библиотеку import requests<br>
```bash
pip install requests
```
4.Регистрация приложения<br>
```text
https://dev.hh.ru/
```
5.Авторизация приложения (новый токен через Х секунд)<br>
6.Авторизация пользователя (code-каждый раз новый, срок жизни короткий)<br>
7. access_token - на 14 дней

### Авторизация приложения
Токен приложения вызывается 1 раз, затем он появляется в [Личный кабинет](https://dev.hh.ru/admin)<br>
Вызывается функция `get_app_token()`

### Авторизация пользователя
Получение временного кода для авторизации: ввести вручную в браузере <br>
```text
https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}
```
Добавить его в .env