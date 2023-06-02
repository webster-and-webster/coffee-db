import os

import psycopg2
from testcontainers.postgres import PostgresContainer

from coffee_db import CoffeeDB


class TestPostgresIntegration:

    postgres_container = PostgresContainer("postgres:14.8")

    def test_psql_connection(self):
        with self.postgres_container as postgres:
            connection_url = postgres.get_connection_url().split(":", 1)
            connection_url[0] = "postgres"
            os.environ["DATABASE_URL"] = ":".join(connection_url)
            os.environ["ENVIRONMENT"] = "TEST"
            with CoffeeDB()._connect() as connection:
                assert isinstance(connection, psycopg2.extensions.connection)
