FROM python:3.11

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

EXPOSE 3001

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# CMD ["sh", "-c", "pipenv run migrate && pipenv run upgrade && pipenv run start"]