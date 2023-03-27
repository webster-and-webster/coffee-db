from coffee_db.database.heroku_psql import CoffeeDB


def test_get_next_id(mocker):
    mocker.patch.object(CoffeeDB, "_execute", return_value=[{"id": 1}, {"id": 2}])

    coffee_db = CoffeeDB()

    output = coffee_db._get_next_id(table="dummy")

    assert output == 3
