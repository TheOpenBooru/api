from modules import validate, settings
import smtplib as _smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2

class Templates:
    with open(settings.EMAIL_TEMPLATE_PASSWORD_RESET_PATH) as f:
        PASSWORD_RESET = f.read()
    with open(settings.EMAIL_TEMPLATE_EMAIL_VERIFICATION_PATH) as f:
        VERIFICATION_EMAIL = f.read()

def send_password_reset(self, to:str, username:str, reset_link:str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    subject = f"{self.sitename}: Password Reset"
    email_html = _render_jinja_template(
        Templates.PASSWORD_RESET,
        sitename=self.sitename,
        link=reset_link,
        name=username
    )
    email_data = _construct_email(to, subject, email_html)
    _send_email(to,email_data)


def send_email_verification(self,to:str ,name:str ,verification_link:str):
    """Raises:
        ValueError: The destination email address is not valid
    """
    subject = f"{self.sitename}: Verify Email"
    email_html = _render_jinja_template(
        Templates.VERIFICATION_EMAIL,
        link=verification_link,
        sitename=self.sitename,
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
