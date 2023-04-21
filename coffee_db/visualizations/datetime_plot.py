import pandas as pd

from coffee_db.coffee import Coffee

pd.options.plotting.backend = "plotly"


class DatetimePlotter:
    """Class to plot the cumulative sum of data over time.

    For example, plotting the cumulative number of coffees added by each user of time.

    Attributes
    ----------
    datetime_col: str
        The datetime column in the data, this will be the x-axis in the final plot.

    col: str
        The column of data to plot, for example, 'added_by'.

    """

    datetime_col = "date_added"

    def __init__(self, col: str):
        if col == self.datetime_col:
            raise ValueError("col cannot be the datetime_col 'date_added'")
        self.col = col

    def _create_dataframe(self, coffees: list[Coffee]) -> pd.DataFrame:
        """Create a pandas dataframe out of the Coffee pydantic data."""

        data = pd.DataFrame([dict(coffee) for coffee in coffees])

        return data

    def _create_plottable_data(self, data: pd.DataFrame):
        """Reformat the data to be in a plottable format."""

        plot_subset = data[[self.datetime_col, self.col]].copy()
        plot_subset[self.col] = plot_subset[self.col].astype(str)
        plot_subset[self.datetime_col] = pd.to_datetime(plot_subset[self.datetime_col])
        plot_subset.set_index(self.datetime_col, inplace=True)

        plot_subset = pd.get_dummies(plot_subset)
        plot_subset = plot_subset.resample("d").sum()

        for col in plot_subset.columns:
            col_name = col.lstrip(self.col + "_")
            plot_subset[col_name] = plot_subset[col].cumsum()
            plot_subset.drop(columns=[col], inplace=True)

        return plot_subset

    def _make_plot(self, plot_data: pd.DataFrame, title: str = "", value: str = ""):
        """Create the plotly plot."""

        plot = plot_data.plot(
            title=title,
            template="plotly_dark",
            labels={"value": value, "variable": self.col},
        )

        return plot

    def plot_data(self, coffees: list[Coffee], title: str = "", value: str = ""):
        """Wrapper for above functions."""

        data = self._create_dataframe(coffees=coffees)
        plot_data = self._create_plottable_data(data=data)
        plot = self._make_plot(plot_data=plot_data, title=title, value=value)
        return plot
