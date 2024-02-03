import os
import smtplib
from dotenv import load_dotenv
import textwrap as tw

load_dotenv()
login = os.getenv('EMAIL_LOGIN')
password = os.getenv('EMAIL_PASSWORD')
sender = os.getenv('SENDER_MAIL')
receivers = os.getenv('RECEIVERS_MAIL')


def send_email(message: str):
    headers_and_text = f"""\
    From: {sender}
    To: {receivers}
    Subject: Письмо от приложения Отклики_hh
    Content-Type: text/plain; charset="UTF-8";
    {message}
    """
    letter_without_indent = tw.dedent(headers_and_text)
    letter = letter_without_indent.encode('utf-8')

    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(login, password)
    server.sendmail(sender, [receivers], letter)
    server.quit()
    print("Message sended.")

if __name__ == '__main__':
    send_email(message="hi")