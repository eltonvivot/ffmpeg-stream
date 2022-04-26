FROM python:3.8-slim-buster

WORKDIR /app

COPY ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app /app

CMD [ "python3", "ai_workflow.py"]