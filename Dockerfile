FROM python:3.8-buster
ENV FLASK_APP=app.py
WORKDIR /var/www/full-frame/code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD flask run --host=0.0.0.0
