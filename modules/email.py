from modules import validate, settings
import smtplib as _smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2

class Templates:
    PASSWORD_RESET = Path(settings.EMAIL_TEMPLATE_PASSWORD_RESET_PATH).read_text()
    VERIFICATION = Path(settings.EMAIL_TEMPLATE_VERIFICATION_PATH).read_text()

def send_password_reset(to:str, username:str, token:str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    subject = f"{settings.SITE_NAME}: Password Reset"
    email_html = _render_jinja_template(
        Templates.PASSWORD_RESET,
        sitename=settings.SITE_NAME,
        link=token,
        name=username,
    )
    email_data = _construct_email(to, subject, email_html)
    _send_email(to,email_data)


def send_email_verification(to:str, name:str, token:str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    subject = f"{settings.SITE_NAME}: Verify Email"
    email_html = _render_jinja_template(
        Templates.VERIFICATION,
        link=token,
        sitename=settings.SITE_NAME,
        name=name
    )
    email_data = _construct_email(to, subject, email_html)
    _send_email(to,email_data)


def _render_jinja_template(template_string:str, **kwargs) -> str:
    _jinja_env = _jinja2.Environment(loader=_jinja2.BaseLoader())
    template = _jinja_env.from_string(template_string)
    body = template.render(**kwargs)
    return body


def _construct_email(to:str, subject:str, body:str) -> str:
    message = _MIMEMultipart()
    message["From"] = settings.SMTP_EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(_MIMEText(body, "html"))
    return message.as_string()


def _send_email(to:str, document:str):
    email = settings.SMTP_EMAIL
    password = settings.SMTP_PASSWORD
    hostname = settings.SMTP_HOSTNAME
    port = settings.SMTP_PORT
    with _smtplib.SMTP(hostname, port) as session:
        session.starttls()
        session.login(email, password)
        session.sendmail(email, to, document)
