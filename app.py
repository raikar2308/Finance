from flask import Flask
from dotenv import load_dotenv
import os
from datetime import timedelta

from routes.admin import *
from extensions import bcrypt, mail

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ================= SECURITY CONFIG =================
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # True in HTTPS production
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
)

# ================= MAIL CONFIG =================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

# ================= INIT EXTENSIONS =================
bcrypt.init_app(app)
mail.init_app(app)


# ================= SECURITY HEADERS =================
@app.after_request
def secure_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# ================= REGISTER BLUEPRINTS =================
blueprints = [
admin_login_bp, dashboard_bp, user_bp, financial_bp
]


for bp in blueprints:
    app.register_blueprint(bp)



if __name__ == '__main__':
    app.run(debug=True)