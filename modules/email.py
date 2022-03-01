from modules import validate, settings
import smtplib as _smtplib
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.text import MIMEText as _MIMEText
import jinja2 as _jinja2

class EmailAccount:
    email:str
    password:str
    hostname:str
    port:int
    sitename:str = settings.get("settings.site.name")
    
    def __init__(self, email:str, password:str, hostname:str, port:int):
        self.email = email
        self.password = password
        self.hostname = hostname
        self.port = port
    
    def send_email(self,to:str,subject:str,jinja_template:str,**kwargs):
        """Raises:
        - ValueError("Invalid Target Address")
        - ValueError("Subject is over 78 characters")
        """
        if not validate.email(to):
            raise ValueError("Invalid Target Address")
        if len(subject) > 78:
            raise ValueError("Subject is over 78 characters")

        email_message = self._render_jinja_template(jinja_template, **kwargs)
        formatted_email = self._construct_email(to, subject, email_message)
        self._send_email_to_server(to, formatted_email)

    def send_password_reset(self,targetAddress:str,name:str,reset_link:str):
        """Raises:
            ValueError: The destination email address is not valid
        """
        with open("./data/emails/password_reset.html") as f:
            password_reset_template = f.read()
        
        subject = f"{self.sitename}: Password Reset"
        self.send_email(
            to=targetAddress,
            subject=subject,
            jinja_template=password_reset_template,
            sitename=self.sitename,
            link=reset_link,
            name=name
        )
    
    def send_email_verification(self, targetAddress:str,name:str,verification_link:str):
        """Raises:
            ValueError: The destination email address is not valid
        """
        with open("./data/emails/email_verification.html") as f:
            verification_email_template = f.read()
        
        subject = f"{self.sitename}: Verify Email"
        self.send_email(
            to=targetAddress,
            subject=subject,
            jinja_template=verification_email_template,
            link=verification_link,
            sitename=self.sitename,
            name=name
        )
    
    def _send_email_to_server(self,toEmail:str,message:str):
        with _smtplib.SMTP(self.hostname, self.port) as session:
            session.starttls()
            session.login(self.email, self.password)
            session.sendmail(self.email, toEmail, message)

    def _construct_email(self,to:str,subject:str,body:str) -> str:
        message = _MIMEMultipart()
        message["From"] = self.email
        message["To"] = to
        message["Subject"] = subject
        message.attach(_MIMEText(body, "html"))
        return message.as_string()

    def _render_jinja_template(self, template_string:str, **kwargs:dict) -> str:
        _jinja_env = _jinja2.Environment(loader=_jinja2.BaseLoader())
        template = _jinja_env.from_string(template_string)
        body = template.render(**kwargs)
        return body
