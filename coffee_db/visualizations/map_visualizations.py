# Responsible for defining map plots.
import folium
from folium.plugins import MarkerCluster

from coffee_db.coffee import Coffee, Country


def _get_popup_text(country_name: str, num_coffees: int) -> str:
    return f"Country: {country_name}<br>" f"Coffees: {num_coffees}"


def _get_coffees_by_country(coffees: list[Coffee]) -> dict[Country, int]:
    """
    Returns a dictionary of counts of coffees by country.
    """
    coffee_counts_by_country = {}
    for coffee in coffees:
        country = coffee.country_of_origin.name
        if country in coffee_counts_by_country:
            coffee_counts_by_country[country] += 1
        else:
            coffee_counts_by_country[country] = 1
    return coffee_counts_by_country


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
