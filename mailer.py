from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
mail = Mail()

def init_mail(app):
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
    )
    mail.init_app(app)

def send_alert(to, subject, body):
    msg = Message(subject, sender=os.getenv("MAIL_USERNAME"), recipients=[to])
    msg.body = body
    mail.send(msg)