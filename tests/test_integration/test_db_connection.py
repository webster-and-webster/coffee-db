import psycopg2

from coffee_db.database.heroku_psql import CoffeeDB


def test_connection():
    """Test the CoffeeDB can connect to the database"""

    test_db = CoffeeDB()
    connection = test_db._connect()

    assert isinstance(connection, psycopg2.extensions.connection)

    connection.close()
