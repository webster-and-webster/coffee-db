from collections import Counter
from typing import Dict, List, Union

import folium
from folium.plugins import MarkerCluster

from coffee_db.coffee import Coffee, Country, Roastery


class WorldMapPlotter:
    """Class to plot coffees and roasteries, by country, onto a world map."""

    def _get_country(self, obj: Union[Coffee, Roastery]) -> str:
        """Get the county for a given Coffee or Roastery."""
        if isinstance(obj, Coffee):
            return obj.country_of_origin.name
        else:
            return obj.country.name

    def _get_popup_text(self, country_name: str, count: int, object_name: str) -> str:
        """Define the text popup for the world map.

        This is what is displayed on the map when you hover over the country.

        """
        return f"Country: {country_name}<br>" f"{object_name}: {count}"

    def _get_country_count(
        self, objects: List[Union[Coffee, Roastery]]
    ) -> Dict[str, int]:
        """Given a list of Country/Roastery objects, get their count by country."""

        country_names = [self._get_country(obj) for obj in objects]

        country_count = Counter(country_names)

        return dict(country_count)

    def plot_objects_by_country(
        self, objects: List[Union[Coffee, Roastery]], object_name: str
    ) -> folium.Map:
        """Plot Coffees/Roasteries on a world map, split by country.

        Parameters
        ----------
        objects: List[Union[Coffee, Roastery]]
            A list of Coffee or Roastery objects to plot on the world map.

        object_name: str
            The objects that are being plotted, eg: 'Coffees'.

        """

        world_map = folium.Map(tiles="cartodbpositron", max_bounds=True)
        marker_cluster = MarkerCluster().add_to(world_map)

        objects_country_count = self._get_country_count(objects)

        for country_name, count in objects_country_count.items():
            country = Country(id=1, name=country_name)
            lat, long = country.get_lat_long()
            popup_text = self._get_popup_text(country.name, count, object_name)
            folium.CircleMarker(
                location=[lat, long], radius=count, popup=popup_text, fill=True
            ).add_to(marker_cluster)
        return world_map
