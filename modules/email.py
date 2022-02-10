from modules import validate, settings
import smtplib as _smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2

class SMTPConfig():
    email = settings.get("config.smtp.email")
    password = settings.get("config.smtp.password")
    hostname = settings.get("config.smtp.hostname")
    port = settings.get("config.smtp.port")

def send(to:str,subject:str,jinja_template:str,**kwargs):
    """Raises:
    - ValueError("Invalid Target Address")
    - ValueError("Subject is over 78 characters")
    """
    config = SMTPConfig()
    _verify_send_paramters(to, subject)
    email_message = _render_template(jinja_template, **kwargs)
    formatted_email = _construct_email(config.email, to, subject, email_message)
    _send_email(config, to, formatted_email)

def _verify_send_paramters(toEmail:str, subject:str):
    if not validate.email(toEmail):
        raise ValueError("Invalid Target Address")
    if len(subject) > 78:
        raise ValueError("Subject is over 78 characters")

def _construct_email(fromEmail:str ,to:str, subject:str, body:str) -> str:
    message = _MIMEMultipart()
    message["From"] = fromEmail
    message["To"] = to
    message["Subject"] = subject
    message.attach(_MIMEText(body, "html"))
    return message.as_string()

def _render_template(template, **kwargs:dict) -> str:
    _jinja_env = _jinja2.Environment(loader=_jinja2.BaseLoader())
    template = _jinja_env.from_string(template)
    body = template.render(**kwargs)
    return body

def _send_email(config:SMTPConfig,toEmail:str,message:str):
    with _smtplib.SMTP(config.hostname, config.port) as session:
        session.starttls()
        session.login(config.email, config.password)
        session.sendmail(config.email, toEmail, message)


def send_password_reset(to: str, name: str, reset_link: str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    sitename = settings.get("settings.site.name")
    subject = f"{sitename}: Password Reset"
    with open("./data/emails/password_reset.html") as f:
        PASSWORD_RESET_TEMPLATE = f.read()
    send(to,subject,PASSWORD_RESET_TEMPLATE,
        link=reset_link,name=name
    )

def send_email_verification(to:str, name:str, verification_link:str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    sitename = settings.get("settings.site.name")
    subject = f"{sitename}: Verify Email"
    with open("./data/emails/email_verification.html") as f:
        EMAIL_VERIFICATION_TEMPLATE = f.read()
    send(to,subject,EMAIL_VERIFICATION_TEMPLATE,
        link=verification_link,name=name
    )

