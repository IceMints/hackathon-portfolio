import os

from flask import Flask, render_template, abort, request
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

import requests

# loads the data files
from app.load_data import load_projects, load_profiles

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

app = Flask(__name__)
app.config.from_object(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

pages = FlatPages(app)
freezer = Freezer(app)


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repre__(self):
        return f"<User {self.username}>"


base_url = os.getenv("URL")
projects_base_url = base_url + "/projects/"
profiles_base_url = base_url + "/profiles/"

projects = load_projects()
profiles = load_profiles()

# Google reCaptcha sitekey
site_key = os.getenv("SITE_KEY")
# reCaptcha verification
def is_human(captcha_response):
    secret = os.getenv("SECRET_KEY")
    payload = {"response": captcha_response, "secret": secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=payload
    )
    response_text = response.json()
    return response_text["success"]


@app.route("/")
def index():
    return render_template(
        "index.html",
        profiles=profiles,
        projects=projects,
        title="Portfolio",
        url=base_url,
    )


@app.route("/projects/<name>")
def get_project(name):
    if name not in projects:
        return abort(404)
    return render_template(
        "project.html", item=projects[name], title=name, url=projects_base_url
    )


@app.route("/profiles/<name>")
def get_profile(name):
    if name not in profiles:
        return abort(404)
    title = name + "'s Profile"
    return render_template(
        "profile.html", item=profiles[name], title=title, url=profiles_base_url
    )


@app.route("/blog")
def blog():
    return render_template("blog.html", pages=pages, title="Blog")


@app.route("/<path:path>.html")
def page(path):
    page = pages.get_or_404(path)
    return render_template("page.html", page=page, title="Blog")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form["g-recaptcha-response"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if is_human(captcha_response):
            if error is None:

                new_user = UserModel(username, generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return f"User {username} created successfully"
            else:
                return error, 418
        else:
            return "recaptcha required"

    return render_template("register.html", title="Register", site_key=site_key)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif password is None:
            error = "Incorrect password."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    return render_template("login.html", title="Login")


@app.route("/<username>/home")
def home(username):
    return render_template("userhome.html", title=username)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Page not found"), 404


@app.route("/health")
def health():
    user_count = UserModel.query.count()
    return f"Total users: {user_count}", 200
