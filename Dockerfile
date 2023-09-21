FROM python:3.9

LABEL MAINTAINER="Idris Fagbemi"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "app:app", "--keep-alive", "5", "--log-level", "debug", "--bind", "0.0.0.0:5000" ]
