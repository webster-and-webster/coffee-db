import datetime

import pytest

from coffee_db.coffee import Country, Roastery, Coffee, Process, CoffeeUser, Variety


@pytest.fixture(scope="session")
def dummy_coffee_list():
    country = Country(id=1, name="Test Country")
    roastery = Roastery(id=1, name="Test Roastery", country=country)
    process = Process(id=1, name="Test Process")
    coffee_user = CoffeeUser(id=1, name="Test User")
    variety = Variety(id=1, name="Test Variety")

    coffee = Coffee(
        id=1,
        name="Test Coffee",
        date_added=datetime.datetime.now(),
        added_by=coffee_user,
        country_of_origin=country,
        roastery=roastery,
        process=process,
        varietal=[variety],
        elevation=1000,
        tasting_notes="one, two, three",
    )

    yield [coffee]


@pytest.fixture(scope="session")
def dummy_roastery_list():
    country = Country(id=1, name="Test Country")
    roastery = Roastery(id=1, name="Test Roastery", country=country)

    yield [roastery]
