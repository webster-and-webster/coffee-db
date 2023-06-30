import os

import pytest
from testcontainers.postgres import PostgresContainer

from coffee_db import CoffeeDB


@pytest.fixture(scope="session")
def postgres_container():
    yield PostgresContainer("postgres:14.8")


def get_postgres_url(postgres):
    connection_url = postgres.get_connection_url().split(":", 1)
    connection_url[0] = "postgres"
    url = ":".join(connection_url)
    return url


def init_sql_db(db):
    # load sql commands from .sql file
    with open("helpers/db_init.sql", "r") as file:
        sql_script = file.read()
    sql_commands = sql_script.split(";")

    # execute each command
    for i, command in enumerate(sql_commands[:-1]):
        db._execute(command)


def test_get_data(postgres_container, mocker):
    with postgres_container as postgres:
        mocker.patch.dict(os.environ, {"DATABASE_URL": get_postgres_url(postgres)})
        coffee_db = CoffeeDB()
        init_sql_db(coffee_db)

        roasteries = coffee_db.get_data(table="roastery")
        expected = [{"id": 1, "name": "Carrow", "country": "Ireland"}]

        assert roasteries == expected


def test_get_next_id(postgres_container, mocker):
    with postgres_container as postgres:
        mocker.patch.dict(os.environ, {"DATABASE_URL": get_postgres_url(postgres)})
        coffee_db = CoffeeDB()
        init_sql_db(coffee_db)

        countries = coffee_db.get_data(table="country")
        country_ids = [country["id"] for country in countries]
        assert country_ids == [1, 2]
        assert coffee_db._get_next_id("country") == 3


def test_insert_row(postgres_container, mocker):
    with postgres_container as postgres:
        mocker.patch.dict(os.environ, {"DATABASE_URL": get_postgres_url(postgres)})
        coffee_db = CoffeeDB()
        init_sql_db(coffee_db)

        countries = coffee_db.get_data(table="country")
        assert len(countries) == 2

        coffee_db.insert_row(table="country", values=("test_country",))
        countries = coffee_db.get_data(table="country")
        assert len(countries) == 3
        assert countries[-1]["id"] == 3


def test_remove_row(postgres_container, mocker):
    with postgres_container as postgres:
        mocker.patch.dict(os.environ, {"DATABASE_URL": get_postgres_url(postgres)})
        coffee_db = CoffeeDB()
        init_sql_db(coffee_db)

        countries = coffee_db.get_data(table="country")
        assert len(countries) == 2

        coffee_db.remove_row(table="country", row_id=(2,))
        countries = coffee_db.get_data(table="country")
        assert len(countries) == 1
