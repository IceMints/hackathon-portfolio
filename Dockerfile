FROM python:3.8-slim-buster

RUN mkdir /portfolio-blog
COPY requirements.txt /portfolio-blog
WORKDIR /portfolio-blog
RUN pip3 install -r requirements.txt

COPY . /portfolio-blog

CMD ["gunicorn", "wsgi:app", "-w 4", "-b 0.0.0.0:80"]
