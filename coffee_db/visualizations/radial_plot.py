from typing import Optional, Union
import pandas as pd
import plotly.graph_objects as go
import re

from coffee_db.coffee import Coffee


class RadialVariationPlotter:
    """
    Class to plot variation in attributes by entity.

    Attributes
    ----------
    entity_col : str
        The column specifying the groupby clause. Each value in this field will
        receive its own trace in the final plot.
    variation_functions : dict[str, callable], optional
        Optional custom variation functions. Supplied as the attribute name (keys)
        and function (values).
    """

    # columns to be dropped from the radial plot
    drop_cols = ["date_added", "id"]
    conversion_cols = [
        "country_of_origin", "roastery", "process", "varietal", "added_by"
    ]

    def __init__(
        self,
        entity_col: str,
        variation_functions: Optional[dict] = None
    ):
        self.entity_col = entity_col
        self.variation_functions = variation_functions
        if self.variation_functions is None:
            self.variation_functions = {}

        for variation_function in self.variation_functions.values():
            if not callable(variation_function):
                raise TypeError("Values within variation_functions must be of type callable")
            test_run = variation_function([1, 2])
            if not isinstance(test_run, float):
                raise ValueError("Callables inside variation_functions must return a float")

    def _create_dataframe(self, coffees: list[Coffee]) -> pd.DataFrame:
        data = pd.DataFrame([dict(coffee) for coffee in coffees])

        for col in self.drop_cols:
            if col in data.columns:
                data.drop(columns=[col], inplace=True)

        for col in self.conversion_cols:
            data[col] = data[col].astype(str)

        # fix columns
        data.tasting_notes = data.tasting_notes.str.split(pat=", ")

        return data

    def _unique_value_ratio(self, X):
        """
        Default method for calculating variation of an attribute. Compares the number
        of unique values against the total number of values. Alternative functions
        must be specified outside of the RadialVariationPlotter class.
        """
        return len(set(X)) / len(X)

    def _get_attribute_variation(self, data: pd.DataFrame, attribute: str) -> dict:
        """
        Returns a variation index for each entity for a given attribute.

        Returns
        -------
        dict
            A dictionary with the variation index (values) for each entity (keys)
            in the input data.
        """
        if attribute not in data.columns:
            raise ValueError(f"Attribute '{attribute}' not found in data.")

        if attribute in self.variation_functions.keys():
            variation_function = self.variation_functions[attribute]
        else:
            variation_function = self._unique_value_ratio

        variation = {}
        # calculate each entity's variation value
        for entity, group in data.groupby(self.entity_col):
            variation[entity] = variation_function(group[attribute])

        # calculate an overall variation value
        group_variation = variation_function(data[attribute])

        # normalize by dividing each entitys' value by the group value
        normalized_variation = {}
        for entity, index in variation.items():
            normalized_variation[entity] = index / group_variation

        return normalized_variation

    def _get_data_variation(self, data: pd.DataFrame) -> Union[dict, pd.DataFrame]:
        """
        Calculate variation for all attributes
        """
        variation = {}
        for attribute in [column for column in data.columns if column != self.entity_col]:
            variation[attribute] = self._get_attribute_variation(data=data, attribute=attribute)
        variation_df = pd.DataFrame(variation)
        variation_df.columns = [re.sub("_", " ", column).title() for column in variation_df.columns]
        return variation_df

    def _make_plot(self, plot_data: pd.DataFrame, title: Optional[str] = ""):
        """
        Create the radial plotly plot.
        """
        fig = go.Figure()
        for entity in plot_data.index.unique():
            fig.add_trace(go.Scatterpolar(
                r=[round(x, 2) for x in plot_data.loc[entity, :].tolist()],
                theta=plot_data.columns.tolist(),
                fill='toself',
                name=entity
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=False)),
            showlegend=True,
            title=title
        )
        return fig

    def plot_data(self, coffees: list[Coffee], title: Optional[str] = ""):
        data = self._create_dataframe(coffees=coffees)
        plot_data = self._get_data_variation(data=data)
        plot = self._make_plot(plot_data=plot_data, title=title)
        return plot


def list_unique_ratio(X):
    """
    Custom variation function to handle columns where each cell is a list.
    """
    def collapse_nested_list(nested_list):
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(collapse_nested_list(item))
            else:
                result.append(item)
        return result
    X_new = collapse_nested_list(X)
    return len(set(X_new)) / len(X_new)
