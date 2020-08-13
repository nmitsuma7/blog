FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app

CMD gunicorn --bind 0.0.0.0:$PORT mysite.wsgi
