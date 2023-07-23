import streamlit as st
from streamlit_folium import folium_static

from coffee_db import CoffeeDB
from coffee_db.data_loaders import PostgresDataLoader
from coffee_db.app import forms
from coffee_db.app.visualizations.datetime_plotter import DatetimePlotter
from coffee_db.app.visualizations.world_map_plotter import (
    WorldMapPlotter
)
from coffee_db.app.visualizations.diversity_plotter import (
    DiversityPlotter
)


APP_NAME = "Coffee DB"
LOGO = "docs/logo.png"


def format_app():
    st.set_page_config(page_title=APP_NAME, page_icon=None)


def format_sidebar():
    st.sidebar.image(LOGO, width=125)
    st.markdown(
        """
        <style>

        .css-1vq4p4l.e1fqkh3o4 {
            margin-top: -50px;
        }

            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")


def read_data() -> tuple:
    data_loader = PostgresDataLoader(db=CoffeeDB())
    return data_loader.get_data()


coffees, coffee_users, countries, processes, roasteries, varieties = read_data()


@st.cache_data
def home_page() -> None:
    st.header("Home Page")
    st.markdown(
        """
    Welcome to Coffee DB! Coffee DB is a webapp designed to store and track purchases
    of bags of coffee. Check out the coffee visualisations by clicking the
    'Visualisations' tab on the left, or add a new coffee in the 'Add/Remove Data' tab.
    """
    )


def get_form_arguments(form_header: str) -> dict:
    if form_header == "coffee":
        return {
            "coffee_users": coffee_users,
            "countries": countries,
            "roasteries": roasteries,
            "processes": processes,
            "varieties": varieties,
        }
    if form_header == "roastery":
        return {
            "countries": countries,
        }
    return {}


def add_remove_data_page() -> None:
    data_forms = [
        forms.RoasteryForm(),
        forms.CoffeeForm(),
        forms.CountryForm(),
        forms.VarietyForm(),
        forms.ProcessForm(),
        forms.CoffeeUserForm(),
    ]

    st.header("Add/Remove Data")
    tabs = st.tabs([form.header for form in data_forms])
    for tab, form in zip(tabs, data_forms):
        with tab:
            col1, col2 = st.columns(2)
            with col1:
                form_arguments = get_form_arguments(form.header)
                form.add(**form_arguments)
            with col2:
                form.remove()


def visualizations_page() -> None:
    world_map_plotter = WorldMapPlotter()

    st.title("Visualizations")

    world_map_tab, datetime_tab, diversity_tab = st.tabs(["world_map_plot", "datetime_plot", "diversity_plot",])

    with world_map_tab:
        option = st.selectbox(
            "plot_type",
            ("Coffees", "Roasteries"),
            label_visibility="hidden",
        )
        if option == "Coffees":
            folium_static(
                world_map_plotter.plot_objects_by_country(
                    objects=coffees, object_name=option
                )
            )
        else:
            folium_static(
                world_map_plotter.plot_objects_by_country(
                    objects=roasteries, object_name=option
                )
            )

    with diversity_tab:
        diversity_plotter = DiversityPlotter()
        st.plotly_chart(
            diversity_plotter.plot_data(coffees=coffees, users=coffee_users)
        )

    with datetime_tab:
        datetime_plotter = DatetimePlotter(col="added_by")
        st.plotly_chart(
            datetime_plotter.plot_data(coffees=coffees, value="# Coffees Purchased")
        )


def view_data_page():
    st.markdown("View Data")
    names = [
        "roastery",
        "coffee",
        "country",
        "variety",
        "process",
        "coffee_user",
    ]
    tabs = st.tabs(names)
    for name, tab in zip(names, tabs):
        with tab:
            st.header(name)
            st.dataframe(CoffeeDB().get_data(name))


def main():
    format_app()
    format_sidebar()
    tab_1, tab_2, tab_3, tab_4 = st.tabs([
        "home page", "view_data_page", "add_remove_data_page", "visualizations_page"
    ])
    with tab_1:
        home_page()
    with tab_2:
        view_data_page()
    with tab_3:
        add_remove_data_page()
    with tab_4:
        visualizations_page()


if __name__ == "__main__":
    main()
