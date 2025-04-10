from flask import Flask
from .database import init_db
from .mailer import init_mail
from .main import routes
from .database import db

def create_app():
    app = Flask(__name__)
    init_db(app)
    init_mail(app)

    with app.app_context():
        db.create_all()  # ✅ This replaces before_app_first_request

    app.register_blueprint(routes)
    return app
