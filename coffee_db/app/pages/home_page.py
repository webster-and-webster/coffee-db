import streamlit as st

from coffee_db.app.utils import Page, Tab


class HomePage(Page):
    def __init__(self, tabs: list[Tab] = None):
        self.tabs = tabs

    @property
    def header(self):
        return "Home Page"

    def body(self):
        st.markdown("Welcome to Coffee DB!")

    def write(self):
        st.title(self.header)
        self.body()
        self.write_tabs()
