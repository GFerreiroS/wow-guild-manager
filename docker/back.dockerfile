FROM python:3.11

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

EXPOSE 3001

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["sh", "-c", "pipenv run migrate && pipenv run upgrade && pipenv run start"]