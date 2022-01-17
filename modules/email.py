from . import Validate
import os
import smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2


_sender_email:str = os.getenv('SMTP_USER') # type: ignore
_sender_pass:str = os.getenv('SMTP_PASS') # type: ignore
_smtp_server:tuple[str,int] = os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT') # type: ignore
_jinja_env = _jinja2.Environment(loader=_jinja2.BaseLoader())

def send_mail(to:str,subject:str,email_template:str,**kwargs) -> None:
    """Send an email using the given template and arguments.

    Args:
        to: The target recipient
        subject: The email's subject
        email_template: the email template filename
        **kwargs: passed to jinja to render template

    Raises:
        ValueError: The to email address is not valid
        ValueError: The subject is too long, longer than 78 characters
    """
    if not Validate.email(to):
        raise ValueError('The to email address is not valid')
    if len(subject) > 78:
        raise ValueError('The subject is to long')

    template = _jinja_env.from_string(email_template)
    body = template.render(**kwargs)
    
    message = _MIMEMultipart()
    message['From'] = _sender_email
    message['To'] = to
    message['Subject'] = subject
    
    
    message.attach(_MIMEText(body, 'html'))
    
    with smtplib.SMTP(*_smtp_server) as session:
        session.starttls()
        session.login(_sender_email,_sender_pass)
        session.sendmail(_sender_email, to, message.as_string())

with open('./data/emails/password_reset.html') as f:
    PASSWORD_TEMPLATE = f.read()
def password_reset(to:str,name:str,link:str):
    """Sends a password reset email to the given email address

    Args:
        to (str): The recipient's email address
        name (str): The user's name
        link (str): Reset Password Link

    Raises:
        ValueError: The to email address is not valid
    """
    subject = f"{os.getenv('SITE_NAME')}: Password Reset"
    send_mail(to,subject,PASSWORD_TEMPLATE,link=link,name=name)

