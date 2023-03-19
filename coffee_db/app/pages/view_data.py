# TODO: Finish implementation
import streamlit as st

from coffee_db.app.utils import Page


class ViewData(Page):

    @property
    def header(self):
        return "View Data"

    def write(self):
        data_name = st.selectbox(
            "Select Data",
            options=[
                "Coffees",
                "Roasteries",
                "Countries",
                "Processes",
                "Varieties",
                "Coffee Users",
            ]
        )
        return data_name
