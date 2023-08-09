FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "-t", "300", "app:app"]
