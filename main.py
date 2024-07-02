from flask import Flask, render_template, request, abort
from flask_bootstrap import Bootstrap5
import os
import smtplib
from email.message import EmailMessage
from flask_sqlalchemy import SQLAlchemy
import requests


# Init Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']


recaptcha_site_key = os.environ['RECAPTCHA_SITE_KEY']
recaptcha_secret_key = os.environ['RECAPTCHA_SECRET_KEY']
verify_url = "https://www.google.com/recaptcha/api/siteverify"


# Init Boostrap
Bootstrap5(app)

# Init SQLAlchemy
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///portfolio.db")
db = SQLAlchemy()
db.init_app(app)

# Declare variables
MY_EMAIL = os.environ["MY_EMAIL"]
MY_EMAIL_PASSWORD = os.environ["MY_EMAIL_PASSWORD"]
TARGET_EMAIL = os.environ["TARGET_EMAIL"]


# Database layout for projects
# Not currently in use
# class Projects(db.Model):
#     __tablename__ = "portfolio_projects"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), unique=True, nullable=False)
#     summary = db.Column(db.String(250), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     github_link = db.Column(db.String(250), nullable=True)
#     thumbnail = db.Column(db.String(250), nullable=True)
#     image = db.Column(db.String(250), nullable=True)
#
#
# # Create database
# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")


@app.route('/design')
def design():
    return render_template("design.html")


@app.route('/dragonbot')
def dragonbot():
    return render_template("dragonbot.html")


@app.route('/snowagerbot')
def snowagerbot():
    return render_template("snowagerbot.html")


@app.route('/travelblog')
def travelblog():
    return render_template("travelblog.html")


@app.route('/morsetranslator')
def morsetranslator():
    return render_template("morsetranslator.html")


@app.route('/watermarker')
def watermarker():
    return render_template("watermarker.html")


@app.route('/typingtest')
def typingtest():
    return render_template("typingtest.html")


@app.route('/breakout')
def breakout():
    return render_template("breakout.html")


@app.route('/coffeeapi')
def coffeeapi():
    return render_template("coffeeapi.html")


@app.route('/wheelanddeal')
def wheelanddeal():
    return render_template("wheelanddeal.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f"{verify_url}?secret={recaptcha_secret_key}&response={secret_response}").json()
        if not verify_response['success']:
            abort(401)
        else:
            data = request.form
            send_email(data["name"], data["email"], data["phone"], data["message"])
            return render_template("contact.html", form_submitted=True)
    else:
        return render_template("contact.html", form_submitted=False, site_key=recaptcha_site_key)


def send_email(name, email, phone, message):
    smtp_server = 'mail.privateemail.com'
    port = 465
    login = MY_EMAIL
    password = MY_EMAIL_PASSWORD
    email_message = EmailMessage()
    email_message["Subject"] = "New Message Received"
    email_message["From"] = MY_EMAIL
    email_message["To"] = TARGET_EMAIL
    content = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    email_message.set_content(content)
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(login, password)
    server.send_message(email_message)
    server.quit()


if __name__ == "__main__":
    app.run(debug=True)