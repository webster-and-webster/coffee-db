import datetime

import plotly
import pandas as pd
import pytest

from coffee_db.coffee import Country, Roastery, Coffee, Process, CoffeeUser, Variety
from coffee_db.visualizations.datetime_plot import DatetimePlotter


@pytest.fixture(scope="module")
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


@pytest.mark.parametrize(
    "attribute_name, attribute_value",
    [("datetime_col", "date_added"), ("col", "dummy_col")],
)
def test_init(attribute_name, attribute_value):

    dt_plotter = DatetimePlotter(col="dummy_col")

    assert hasattr(dt_plotter, attribute_name)
    assert getattr(dt_plotter, attribute_name) == attribute_value


def test_init_failure():

    with pytest.raises(ValueError, match="col cannot be the datetime_col 'date_added'"):
        _ = DatetimePlotter(col="date_added")


def test_create_dataframe(dummy_coffee_list):

    dt_plotter = DatetimePlotter(col="dummy_col")

    dataframe = dt_plotter._create_dataframe(dummy_coffee_list)

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape == (1, 10)


def test_plot_data(dummy_coffee_list):

    dt_plotter = DatetimePlotter(col="added_by")

    output_plot = dt_plotter.plot_data(coffees=dummy_coffee_list)

    assert isinstance(output_plot, plotly.graph_objs._figure.Figure)
