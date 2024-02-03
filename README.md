# Получение вакансий по API

1.Скачайте проект<br>
```bash
git clone ссылка
```
2.Создайте виртуальное окружение<br>
```bash
python -m venv venv
```
3.Активируйте виртуальное окружение:
Activate
```
.\venv\Scripts\activate
```
4.Установите библиотеку import requests<br>
```bash
pip install requests
```
5.Зарегистрируйте приложение на:<br>
```text
https://dev.hh.ru/
```
6.Создайте файл .env и заполните неоходимыми данными<br>
`CLIENT_EMAIL` - email пользователя<br>
`CLIENT_ID` - Client ID на [dev.hh.ru](https://dev.hh.ru/)<br>
`CLIENT_SECRET` - Client Secret на [dev.hh.ru](https://dev.hh.ru/)<br>
`ID_RESUME` - id резюме, которым вы будете откликаться на вакнсии.<br>

### Как узнать id резюме
Зайдите на сайт [hh.ru](https://hh.ru).<br>
Во вкладке **Мои резюме** выберите то резюме, которым будете откликаться.<br>
В адресной строке браузера скопируйте все символы после resume/<br>
```text
https://novosibirsk.hh.ru/resume/9f123ed4ff0591a2420039ed1f8b5372627с00
```
Вручную добавить `ID_RESUME` в файл .env.<br>
```text
ID_RESUME=9f123ed4ff0591a2420039ed1f8b5372627с00
```
### Авторизация приложения
Токен приложения вызывается 1 раз, затем он появляется в [Личном кабинете](https://dev.hh.ru/).<br>
Вызывается функция `get_app_token()`.<br>
В файл .env автоматически записываются данные
`APP_TOKEN` - токен приложенияю. <br>
Новый токен возможно запросить через Х секунд.<br>

### Авторизация пользователя
Необходимо получить временный код для авторизации  `TEMP_USER_CODE`.<br>
Для этого в браузере вручную ввести:<br>
```text
https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}
```
Вручную добавить временный код в файл .env.<br>
`TEMP_USER_CODE` - каждый раз новый, срок действия короткий (Х секунд).<br>

Для получения access и refresh token неободимо вызвать функцию `get_user_token()`.<br>
```text
USER_ACCESS_TOKEN=
USER_REFRESH_TOKEN=
```
Данные записываются в файл .env аавтоматически.<br>

`USER_ACCESS_TOKEN` выдается на 14 дней.<br>