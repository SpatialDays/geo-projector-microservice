FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
