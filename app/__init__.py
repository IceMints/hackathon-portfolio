import os

from flask import Flask, render_template, abort, url_for, request
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# loads the data files
from app.load_data import load_projects, load_profiles

from . import db

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app) # calls the function init_app from db.py

pages = FlatPages(app)
freezer = Freezer(app)

base_url = os.getenv("URL")
projects_base_url = base_url + "/projects/"
profiles_base_url = base_url + "/profiles/"

projects = load_projects()
profiles = load_profiles()

@app.route('/')
def index():
    return render_template('index.html', profiles=profiles, projects=projects, title="Portfolio",
                           url=base_url)

@app.route('/projects/<name>')
def get_project(name):
    if name not in projects:
        return abort(404)
    return render_template('project.html', item=projects[name], title=name, url=projects_base_url + name)


@app.route('/profiles/<name>')
def get_profile(name):
    if name not in profiles:
        return abort(404)
    title = name + "'s Profile"
    return render_template('profile.html', item=profiles[name], title=title, url=profiles_base_url + name)

@app.route('/blog')
def blog():
    return render_template('blog.html', pages=pages, title="Blog")

@app.route('/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, title="Blog")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page not found"), 404

@app.route('/health')
def health():
    return '', 200