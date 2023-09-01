#Option Module for integrating text messaging upon anomaly detectio 

import email, smtplib, ssl
from providers import PROVIDERS
import contextlib
import sys

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
): 
    sender_email, email_password = sender_credentials 
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def main(message):
    number = "6108883335"
    provider = "AT&T"
    subject = "ALERT"
    sender_credentials = ("kaosam76@gmail.com", PROVIDERS.get("App Password"))
    send_sms_via_email(number, message, provider, sender_credentials, subject)

if __name__ == "__main__":
    main(sys.argv[1])

