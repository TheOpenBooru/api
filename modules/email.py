from modules import validation,settings
import os
import smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2


_smtp_email:str = settings.get('config.smtp.email')
_smtp_pass:str = settings.get('config.smtp.password')
_smpt_hostname:str = settings.get('config.smtp.hostname')
_smtp_port:int = settings.get('config.smtp.port')

_jinja_env = _jinja2.Environment(loader=_jinja2.BaseLoader())

def send_mail(to:str,subject:str,email_template:str,**kwargs):
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
    if not validation.email(to):
        raise ValueError('The to email address is not valid')
    if len(subject) > 78:
        raise ValueError('The subject is to long')

    template = _jinja_env.from_string(email_template)
    body = template.render(**kwargs)
    
    message = _MIMEMultipart()
    message['From'] = _smtp_email
    message['To'] = to
    message['Subject'] = subject
    
    
    message.attach(_MIMEText(body, 'html'))
    
    with smtplib.SMTP(_smpt_hostname,_smtp_port) as session:
        session.starttls()
        session.login(_smtp_email,_smtp_pass)
        session.sendmail(_smtp_email, to, message.as_string())

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
    sitename = settings.get('settings.site.name')
    subject = f"{sitename}: Password Reset"
    send_mail(to,subject,PASSWORD_TEMPLATE,link=link,name=name)

