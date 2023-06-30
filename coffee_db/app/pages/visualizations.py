import streamlit as st
from streamlit_folium import folium_static

from coffee_db.app.utils import Page, Tab
from coffee_db.visualizations.datetime_plot import DatetimePlotter
from coffee_db.visualizations.map_visualizations import WorldMapPlotter
from coffee_db.visualizations.diversity_plotter import DiversityPlotter


class Visualizations(Page):
    @property
    def header(self):
        return "Visualizations"


class WorldMapPlot(Tab):
    @property
    def header(self):
        return "World Map Plot"

    def write(self):
        world_map_plotter = WorldMapPlotter()
        st.title(self.header)
        option = st.selectbox(
            "plot_type",
            ("Coffees", "Roasteries"),
            label_visibility="hidden",
        )
        if option == "Coffees":
            folium_static(
                world_map_plotter.plot_objects_by_country(
                    objects=st.cache.coffees, object_name=option
                )
            )
        else:
            folium_static(
                world_map_plotter.plot_objects_by_country(
                    objects=st.cache.roasteries, object_name=option
                )
            )


class CoffeesByUser(Tab):
    @property
    def header(self):
        return "Coffees by User"

    def write(self):
        st.title(self.header)
        datetime_plotter = DatetimePlotter(col="added_by")
        st.plotly_chart(
            datetime_plotter.plot_data(
                coffees=st.cache.coffees,
                value="# Coffees Purchased",
            )
        )


class CoffeeDiversity(Tab):
    @property
    def header(self):
        return "Diversity by User"

    def write(self):
        st.title(self.header)
        diversity_plotter = DiversityPlotter()
        st.plotly_chart(
            diversity_plotter.plot_data(
                coffees=st.cache.coffees, users=st.cache.coffee_users, title=""
            )
        )
