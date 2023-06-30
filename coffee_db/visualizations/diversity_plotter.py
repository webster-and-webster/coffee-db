from typing import Optional
import plotly.graph_objects as go
import numpy as np

from coffee_db.coffee import Coffee, CoffeeUser
from coffee_db.app.utils.flatten_list import flatten_list


def unique_value_ratio(X: list) -> float:
    """
    Calculates the number of unique values divided by the total number of
    values in a list-like object. Used to measure diversity in the list.
    """
    return len(set(X)) / len(X)


def variance(X: list) -> float:
    """ "
    Returns variance for all non-NoneType values in a list
    """
    return np.var([x for x in X if x is not None])


class DiversityPlotter:
    """
    Class to plot diversity in attributes by user.

    Creates a radial plot of diversity indexes for each attribute by user.
    Each attribute is point on the circumference of the circle, and each user's
    diveristy scores are plotted as separate traces by user.
    """

    # Functions to calculate diversity scores for each attribute. Diversity
    # score functions must receive a single list argument and return a float.
    DIVERSITY_FUNCTION_MAP = {
        "Country of Origin": unique_value_ratio,
        "Roastery": unique_value_ratio,
        "Process": unique_value_ratio,
        "Varietal": unique_value_ratio,
        "Elevation": variance,
        "Tasting Notes": unique_value_ratio,
    }

    def get_coffee_attributes(self, coffees: list[Coffee]) -> dict[str, list]:
        """
        Return attribute values from a coffee class in plot-friendly format.

        Returns
        -------
        dict
            A dictionary of attribute names (keys) mapping to lists of
            attribute values for each coffee in the input coffees list.
        """
        attributes = [
            {
                "Country of Origin": coffee.country_of_origin.name,
                "Roastery": coffee.roastery.name,
                "Process": coffee.process.name,
                "Varietal": [varietal.name for varietal in coffee.varietal],
                "Elevation": coffee.elevation,
                "Tasting Notes": []
                if coffee.tasting_notes is None
                else coffee.tasting_notes.split(", "),
            }
            for coffee in coffees
        ]

        # converts to a dictionary where each key's value is a list of values
        # extracted from the list of dictionaries.
        return {
            key: flatten_list([d[key] for d in attributes]) for key in attributes[0]
        }

    def get_diversity_scores(self, coffees: list[Coffee]) -> dict[str, float]:
        """
        Converts list of attribute values to diversity scores. Each attribute
        has its own function to calculate the diversity score, which is defined
        in the DIVERSITY_FUNCTION_MAP class attribute.

        Returns
        -------
        dict
            A dictionary of attribute names (keys) mapping to diversity scores.
        """
        coffee_attributes = self.get_coffee_attributes(coffees=coffees)
        return {
            attribute_name: self.DIVERSITY_FUNCTION_MAP[attribute_name](values)
            for attribute_name, values in coffee_attributes.items()
        }

    def get_normalized_scores(
        self, coffees: list[Coffee], users: list[CoffeeUser]
    ) -> dict[str, dict]:
        """
        Returns normalized diversity scores for each user. Scorse are
        normalized by dividing by the respective score for the entire group of
        users.

        Returns
        -------
        dict[dict]
            Returns a dictionary of diversity scores
        """
        diversity_scores_all_users = self.get_diversity_scores(coffees=coffees)
        diversity_scores = {}
        for user in users:
            user_coffees = [coffee for coffee in coffees if coffee.added_by == user]
            if not user_coffees:
                continue
            user_diversity_scores = self.get_diversity_scores(coffees=user_coffees)
            normalized_scores = {
                attribute_name: user_score / diversity_scores_all_users[attribute_name]
                for attribute_name, user_score in user_diversity_scores.items()
            }
            for attribute_name, score in normalized_scores.items():
                if np.isnan(score):
                    normalized_scores[attribute_name] = 1.0

            diversity_scores[user.name] = normalized_scores
        return diversity_scores

    def make_plot(self, diversity_scores, title: Optional[str] = ""):
        """
        Returns a radial plot of diversity indexes for each attribute by user.
        Each attribute is point on the circumference of the circle, and each
        user gets their own trace.

        Parameters
        ----------
        diversity_scores : dict[str, dict]
            A nested dictionary of user names (keys) and user's diversity
            scores for each attribute (values).
        title : str
            Optional title for the plot.

        Returns
        -------
        plotly graph object.
            A radial plot of users' diversity scores for each coffee attribute.
        """
        fig = go.Figure()
        for user, scores in diversity_scores.items():
            fig.add_trace(
                go.Scatterpolar(
                    r=list(scores.values()),
                    theta=list(scores.keys()),
                    fill="toself",
                    name=user,
                    hovertemplate="Diversity Index: %{r:.2f}",
                )
            )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=False)), showlegend=True, title=title
        )
        return fig

    def plot_data(
        self, coffees: list[Coffee], users: list[CoffeeUser], title: Optional[str] = ""
    ):
        """
        Returns a radial plot of diversity indexes for each attribute by user.
        Each attribute is point on the circumference of the circle, and each
        user gets their own trace.

        Parameters
        ----------
        coffees : list[Coffee]
            A list of coffees.
        users : List[CoffeeUser]
            A list of cofee users.
        title : str
            Optional title for the plot.

        Returns
        -------
        plotly graph object.
            A radial plot of users' diversity scores for each coffee attribute.
        """
        normalized_diversity_scores = self.get_normalized_scores(
            coffees=coffees, users=users
        )
        plot = self.make_plot(diversity_scores=normalized_diversity_scores, title=title)
        return plot
