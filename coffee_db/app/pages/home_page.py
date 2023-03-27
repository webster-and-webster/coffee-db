import streamlit as st

from coffee_db.app.utils import Page, Tab


class HomePage(Page):
    def __init__(self, tabs: list[Tab] = None):
        self.tabs = tabs

    @property
    def header(self):
        return "Home Page"

    def body(self):
        st.markdown(
            """
        Welcome to Coffee DB! Coffee DB is a webapp designed to store and track purchases of bags of coffee. Check out
         the coffee visualisations by clicking the 'Visualisations' tab on the left, or add a new coffee in the
         'Add/Remove Data' tab.
        """
        )

    def write(self):
        st.title(self.header)
        self.body()
        self.write_tabs()
