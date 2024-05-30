import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(message):
    login = os.getenv("EMAIL_LOGIN")
    password = os.getenv("EMAIL_PASSWORD")
    sender = os.getenv("SENDER_MAIL")
    receivers = os.getenv("RECEIVERS_MAIL")

    # Open the plain text file whose name is in textfile for reading.
    msg = EmailMessage()
    # me == the sender's email address
    # you == the recipient's email address
    msg["Subject"] = "The contents of HH.API BOT"
    msg["From"] = sender
    msg["To"] = receivers
    msg.set_content(message)

    server = smtplib.SMTP_SSL(host="smtp.yandex.ru", port=465)
    server.login(login, password)
    server.send_message(msg)
    server.quit()
    print("Message sended.")


if __name__ == "__main__":
    send_email(message="hello my friend Veronika")
