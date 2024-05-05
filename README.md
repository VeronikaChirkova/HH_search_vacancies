# Получение вакансий по API

1 Скачайте проект:<br>
```bash
git clone https://github.com/VeronikaChirkova/HH_search_vacancies.git
```
2 Создайте виртуальное окружение:<br>
```bash
python -m venv venv
```
3 Активируйте виртуальное окружение:
```
. ./venv/bin/activate
```
4 Установите зависимости:<br>
```bash
pip install -r requirements.txt
```
5 Зарегистрируйте приложение на:<br>
```text
https://dev.hh.ru
```
6 Создайте файл .env и заполните неоходимыми данными:<br>
`CLIENT_EMAIL=` email пользователя<br>
`CLIENT_ID=` Client ID из [dev.hh.ru](https://dev.hh.ru/)<br>
`CLIENT_SECRET=` Client Secret из [dev.hh.ru](https://dev.hh.ru/)<br>
`ID_RESUME=` id резюме, которым вы будете откликаться на вакансии<br>

Данные для отправки сообщений:<br>
`EMAIL_LOGIN=`your_login<br>
`EMAIL_PASSWORD=`пароль приложения (не почты)<br>
`SENDER_MAIL=`your_login@yandex.ru<br>
`RECEIVERS_MAIL`=your_login@yandex.ru<br>

### Отправка писем через yandex почту
1 Войти в профиль yandex почты.<br>
2 Перейти во вкладку безопасность -> пароли приложений -> создать пароль приложения<br>
![Текст с описанием картинки](/images/safety.png)<br>
3 Придумать имя пароля -> далее скопировать пароль в переменную `EMAIL_PASSWORD`.<br>
![Текст с описанием картинки](/images/password.png)

### Как узнать id резюме
1 Зайдите на сайт [hh.ru](https://hh.ru).<br>
2 Во вкладке **Мои резюме** выберите то резюме, которым будете откликаться.<br>
3 В адресной строке браузера скопируйте все символы после resume/<br>
```text
https://novosibirsk.hh.ru/resume/9f123ed4ff0591a2420039ed1f8b5372627с00
```
4 Вручную добавить `ID_RESUME` в файл .env.<br>
```text
ID_RESUME=9f123ed4ff0591a2420039ed1f8b5372627с00
```
### Авторизация приложения
1 Вызывается функция `get_app_token()`.<br>
2 Токен приложения вызывается 1 раз, затем он появляется в [Личном кабинете](https://dev.hh.ru/).<br>
3 Новый токен возможно запросить через Х секунд.<br>

### Авторизация пользователя
1 Необходимо получить временный код для авторизации  `TEMP_USER_CODE`.<br>
2 На почту придет письмо с сылкой:<br>
```text
https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}
```
3 Перейди по ссылке, авторизуйся и забери code.<br>
Example code:<br>
 ```text
 code=P2TQRI2EJGMQVE6NIR8V8GC0EDAU9G5US8ONKE7MQ3GO5J0CD5HKDFUMMCU6BEOR
 ```
4 Code вставить в консоль, там где запущено приложение.<br>
`CODE` - каждый раз новый, срок действия короткий (Х секунд).<br>

5 Для получения access и refresh token необходимо вызвать функцию `get_user_token()`.<br>

Точно до последнего знака указать в функции значение `redirect_uri`, как в [Личном кабинете](https://dev.hh.ru/).<br>
```text
USER_ACCESS_TOKEN=
USER_REFRESH_TOKEN=
ACCESS_TOKEN_VALID=
```
6 Данные записываются в файл .env автоматически.<br>

`USER_ACCESS_TOKEN` выдается на 14 дней.<br>

### Если не отправляются отклики
1 Проверить наличие необходимых переменных в файле .env, вызвав функцию `check_envs()`.<br>
2 Проверить в файле .env до какой даты активен access token:<br>
```text
ACCESS_TOKEN_VALID=2024-02-12 00:00:00
```
Access token выдается на 14 дней.<br>

### Ошибки
**Exceptions.EnvNotFound:** Приложение ожидает, что вы укажете в .env следующие переменные вручную:<br>
```text
"USER_AGENT",
"CLIENT_EMAIL",
"ID_RESUME",
"CLIENT_ID",
"CLIENT_SECRET",
"EMAIL_LOGIN",
"EMAIL_PASSWORD",
"SENDER_MAIL",
"RECEIVERS_MAIL"
```
Формат записи `USER_AGENT="<название приложения> (${CLIENT_EMAIL})"`.

### Запуск
Задать переменные поиска:

`name_vacancia` - название вакансии,<br>
`area` - страна/город/регион поиска,<br>
`period` - количество дней, в пределах которых производится поиск по вакансиям (max=30),<br>
`schedule` - график работы (remote - удаленная работа, fullDay - полный день, shift - сменный график, flexible - гибкий график),<br>
`experience` - опыт работы (noExperience - нет опыта, <br>
between_1_and_3 - от 1 года до 3 лет,between_3_and_6 = от 3 до 6 лет, more_6 = более 6 лет).<br>
```bash
python main.py
```

## Запуск в докере
1. Создайте нового пользователя `appuser` без домашней директории и добавьте его в группу `appuser` на локальном ПК.<br>

```bash
useradd -M appuser -u 3000 -g 3000 && sudo usermod -L appuser &&sudo usermod -aG appuser appuser
```
Это необходимо для обеспечения безопасности, чтобы запуск процессов внутри контейнера осуществлялся от пользователя, который не имеет никаких прав на хостовой машине.<br>

UID (GID) пользователя в контейнере и пользователя за пределами контейнера, у которого есть соответствующие права на доступ к файлу, должны соответствовать.<br>

2. В Dockerfile необходимо прописать: UID (GID), создание пользователя и передачу ему прав, смену пользователя.<br>
```text
ARG UNAME=appuser
ARG UID
ARG GID

# create user
RUN groupadd -g ${GID} ${UNAME} &&\
useradd ${UNAME} -u ${UID} -g ${GID} &&\
usermod -L ${UNAME} &&\
usermod -aG ${UNAME} ${UNAME}

# chown all the files to the app user
RUN chown -R ${UNAME}:${UNAME} /app

USER ${UNAME}
```
3. Команда для создания образа (обязательно указать UID (GID)):<br>

```bash
docker build . --build-arg UID=3000 --build-arg GID=3000 -f Dockerfile -t hh_api
```
4. Создайте и запустите контейнер:<br>
```bash
docker run --rm --name hh_api --env-file .env hh_api
```
Файл с конфиденциальными данными передается `--env-file`.<br>