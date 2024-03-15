FROM python:3.10.12

#docker build --build-arg UID=3000 --build-arg GID=3000...
ARG UNAME=appuser
ARG UID
ARG GID

# create user
RUN groupadd -g ${GID} ${UNAME} &&\
useradd ${UNAME} -u ${UID} -g ${GID} &&\
usermod -L ${UNAME} &&\
usermod -aG ${UNAME} ${UNAME}

RUN apt update && apt -y upgrade && apt -y install nano && apt -y install bash bash-doc bash-completion
RUN apt install -y libglib2.0-0\
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# chown all the files to the app user
RUN chown -R ${UNAME}:${UNAME} /app

USER ${UNAME}

CMD [ "python", "main.py" ]
