import pytest

from coffee_db import CoffeeDB


@pytest.fixture(scope="session")
def db_table_columns():
    yield [
        {'column_name': 'added_by', 'table_name': 'coffee'},
        {'column_name': 'country_of_origin', 'table_name': 'coffee'},
        {'column_name': 'date_added', 'table_name': 'coffee'},
        {'column_name': 'elevation', 'table_name': 'coffee'},
        {'column_name': 'id', 'table_name': 'coffee'},
        {'column_name': 'name', 'table_name': 'coffee'},
        {'column_name': 'process', 'table_name': 'coffee'},
        {'column_name': 'roastery', 'table_name': 'coffee'},
        {'column_name': 'tasting_notes', 'table_name': 'coffee'},
        {'column_name': 'varietal', 'table_name': 'coffee'},
        {'column_name': 'id', 'table_name': 'coffee_user'},
        {'column_name': 'name', 'table_name': 'coffee_user'},
        {'column_name': 'id', 'table_name': 'country'},
        {'column_name': 'name', 'table_name': 'country'},
        {'column_name': 'id', 'table_name': 'process'},
        {'column_name': 'name', 'table_name': 'process'},
        {'column_name': 'country', 'table_name': 'roastery'},
        {'column_name': 'id', 'table_name': 'roastery'},
        {'column_name': 'name', 'table_name': 'roastery'},
        {'column_name': 'id', 'table_name': 'variety'},
        {'column_name': 'name', 'table_name': 'variety'}
    ]


def test_prod_db(db_table_columns):
    """Test that the production database has the correct tables, and the tables have the correct columns."""
    coffee_db = CoffeeDB()

    output = coffee_db._execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema != 'pg_catalog'
        AND table_schema != 'information_schema'
        AND table_schema != 'heroku_ext'
        ORDER BY table_name, column_name
    """)

    assert output == db_table_columns
