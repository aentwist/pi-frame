FROM python:3.8-buster
WORKDIR /var/www/full-frame
ENV FLASK_APP=app.py

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD flask run
