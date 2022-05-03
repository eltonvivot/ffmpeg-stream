FROM python:3.8-slim-buster

RUN apt-get update && apt-get install python3-matplotlib -y && apt-get clean

WORKDIR /app

COPY ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app /app

CMD [ "python3", "app.py"] 