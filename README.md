<img src=https://img.shields.io/github/license/kendrajmoore/hackathon-portfolio>
<p align="center">
 <img width="460" src="https://user-images.githubusercontent.com/51943194/121562739-98dd0680-c9ce-11eb-897a-579780e50c9a.jpg">
</p>

# Sourced from Team KENARGI Portfolio Webpage
by Armando, Gigi, and Kendra in Pod 3.3.5

## Introduction

Design a portfolio-blog

## Description

Working as a team, we created a portfolio website using Flask. The website uses dynamic links and is scaled for more projects or team memebers.
After forking the project, I added Flask FlatPages and Frozen to include a blog section. Then I deployed the website as a service with an AWS
instance in a docker container.

## Visuals (updated 6/19/2021)

![Screenshot_2021-06-19_23-06-36](https://user-images.githubusercontent.com/51943194/122663966-36fd6900-d153-11eb-95f5-8de33304a87f.png)

![page_3](https://user-images.githubusercontent.com/51943194/121791615-b19d1600-cba0-11eb-94d5-3d5ca7d3837a.png)

![page_2](https://user-images.githubusercontent.com/51943194/121791614-af3abc00-cba0-11eb-9976-d6ecb0f0b7de.png)

## Pre-requisites / requirements

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies

```bash
pip install -r requirements.txt
```

## Technologies Used

- Python-Flask
- Flatpages
- Frozen
- HTML
- CSS
- JSON
- sqlite
- AWS instance
- NGINX
- Docker

## Installation

Make sure you have python3 and pip installed


Create and activate virtual environment using virtualenv
```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

## Usage

Create a .env file using the example.env template


Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```
Start a web browser and type in localhost:5000, page will render and can be intereact like any other webpage.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
