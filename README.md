# Backend Application
## The Application is live [here](https://votres.herokuapp.com) and the documentation [here](https://votres.herokuapp.com)


The backend uses the following technologies:

- [FastAPI](https://fastapi.tiangolo.com/) for the application itself.
- [PostgreSQL](https://www.postgresql.org/docs/) for database.
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html) for handling PostgreSQL interactions
- [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) for handling deployments, 
- [Pytest](https://docs.pytest.org/en/6.2.x/contents.html) for handling tests,
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for handling database migrations,
- [pyJWT](https://pyjwt.readthedocs.io/en/stable/) for handling JSON WEB TOKEN,

## Setup for development

This application can be run locally, check app/utils/commands 
for the commands used during development.

Clone the repo -:
```console
$ git clone https://github.com/r-scheele/votre.git
```
Clone the repo in the current directory-:
```console
$ git clone https://github.com/r-scheele/votre.git .
```

Start by creating a virtual environment - windows:

```console
$ py3 -m venv venv
$ . venv/bin/activate
```

Install the application's requirement:
```console
$ pip install -r requirements.txt
```

Create a `.env` file and replace the values of `.env.sample` into `.env`:

```console
$ cp .env.sample .env
```

Run the application:

```console
$ uvicorn app.main:app --reload
```
After install each package run:
```console
$ pip freeze > requirements.txt
```

## Making Changes

Features, bug fixes, improvements etc are to be made in a different branch after which PRs will be sent for review before merging.