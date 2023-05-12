# Responsible for defining map plots.
from collections import Counter

import folium
from folium.plugins import MarkerCluster

from coffee_db.coffee import Coffee, Country, Roastery


def _get_popup_text(country_name: str, num_coffees: int) -> str:
    return f"Country: {country_name}<br>" f"Coffees: {num_coffees}"


def _get_coffees_by_country(coffees: list[Coffee]) -> dict[str, int]:
    """
    Returns a dictionary of counts of coffees by country.
    """
    country_names = [coffee.country_of_origin.name for coffee in coffees]
    coffees_by_country = Counter(country_names)

    return dict(coffees_by_country)


def _get_roasteries_by_country(roasteries: list[Roastery]) -> dict[str, int]:
    """
    Returns a dictionary of counts of roasteries by country.
    """
    country_names = [roastery.country.name for roastery in roasteries]
    roasteries_by_country = Counter(country_names)

    return dict(roasteries_by_country)


def plot_coffees_by_country(coffees: list[Coffee]) -> folium.Map:
    """
    PLots a world map with cluster points for coffee counts by country.
    """
    world_map = folium.Map(tiles="cartodbpositron", max_bounds=True)
    marker_cluster = MarkerCluster().add_to(world_map)

    coffee_counts_by_country = _get_coffees_by_country(coffees)
    for country_name, coffee_count in coffee_counts_by_country.items():
        country = Country(id=1, name=country_name)
        lat, long = country.get_lat_long()
        popup_text = _get_popup_text(country.name, coffee_count)
        folium.CircleMarker(
            location=[lat, long], radius=coffee_count, popup=popup_text, fill=True
        ).add_to(marker_cluster)
    return world_map


def plot_roasteries_by_country(roasteries: list[Roastery]) -> folium.Map:
    """
    Plots a world map with cluster points for roastery counts by country.
    """

    world_map = folium.Map(tiles="cartodbpositron", max_bounds=True)
    marker_cluster = MarkerCluster().add_to(world_map)

    roastery_counts_by_country = _get_roasteries_by_country(roasteries)
    for country_name, roastery_count in roastery_counts_by_country.items():
        country = Country(id=1, name=country_name)
        lat, long = country.get_lat_long()
        popup_text = _get_popup_text(country.name, roastery_count)
        folium.CircleMarker(
            location=[lat, long], radius=roastery_count, popup=popup_text, fill=True
        ).add_to(marker_cluster)
    return world_map
