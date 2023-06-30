import os
from pathlib import Path
from configparser import ConfigParser
from decouple import config


LOCAL_SETTINGS_PATH = Path(os.getcwd(), "settings.ini")


def get_environment():
    return config("ENVIRONMENT", default="LOCAL")


def get_local_db_url(filename=LOCAL_SETTINGS_PATH, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db_url = ""
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_url = db_url + f"{param[0]}={param[1]} "
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db_url


def get_database_url():
    environment = get_environment()

    if environment in ["HEROKU", "TEST"]:
        database_url = config("DATABASE_URL")
    elif environment == "LOCAL":
        database_url = get_local_db_url()

    return database_url
