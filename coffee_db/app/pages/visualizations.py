import streamlit as st
from streamlit_folium import folium_static

from coffee_db.app.utils import Page, Tab
from coffee_db.visualizations.datetime_plot import DatetimePlotter
from coffee_db.visualizations.map_visualizations import plot_coffees_by_country


class Visualizations(Page):
    @property
    def header(self):
        return "Visualizations"


class WorldMapPlot(Tab):
    @property
    def header(self):
        return "World Map Plot"

    def write(self):
        st.title(self.header)
        folium_static(plot_coffees_by_country(coffees=st.cache.coffees))


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
