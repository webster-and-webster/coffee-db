import os

from coffee_db.database.config import config


def get_environment():
    return os.environ.get("ENVIRONMENT", "LOCAL")


def get_database_url():
    environment = get_environment()

    if environment == "HEROKU":
        database_url = os.environ["DATABASE_URL"]
    elif environment == "LOCAL":
        database_url = config()

    return database_url
