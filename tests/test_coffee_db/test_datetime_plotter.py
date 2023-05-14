import plotly
import pandas as pd
import pytest

from coffee_db.visualizations.datetime_plot import DatetimePlotter


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
