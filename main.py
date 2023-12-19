from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import os
import smtplib
from email.message import EmailMessage
from flask_sqlalchemy import SQLAlchemy


# Init Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']

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


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['phone'])
        print(request.form['message'])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", form_submitted=True)
    else:
        return render_template("contact.html", form_submitted=False)


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