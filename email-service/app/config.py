import os
import json
from dotenv import load_dotenv

from pydantic import AmqpDsn, EmailStr
from pydantic_settings import BaseSettings

from .logging import logger


load_dotenv()


class EmailSettings(BaseSettings):
    # SMTP SSL Port (ex. 465)
    email_port: int = int(os.getenv("email_port", "465"))

    # SMTP host (ex. smtp.gmail.com)
    email_host: str = os.getenv("email_host", "smtp.gmail.com")

    # SMTP Login credentials
    email_user: EmailStr = os.getenv(
        "email_user", "your_email_address@gmail.com")

    # Check this link [StackOverflow](https://stackoverflow.com/a/27515833/22663290)
    email_app_password: str = os.getenv(
        "email_app_password", "abcd abcd abcd abcd")

    # Receivers, can be multiple.
    # Contains a string with comma separated email addresses
    email_receivers: str = os.getenv(
        "email_receivers", "address@gmail.com, example@gmail.com")

    # Theme of the email
    email_subject: str = os.getenv(
        "email_subject", "Message from Bank service")


class AppSettings(BaseSettings):
    '''Custom configuration class for centralizing app settings'''

    amqp_dsn: AmqpDsn = os.getenv(
        'AMQP_URI', 'amqp://guest:guest@rabbitmq:5672'
    )
    queue_name: str = os.getenv('QUEUE_NAME', 'email-service')


email_settings = EmailSettings()
app_settings = AppSettings()
