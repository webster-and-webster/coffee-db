# TODO: Finish implementation
import streamlit as st

from coffee_db.app import tables
from coffee_db.app.utils import Page
from coffee_db.app.utils.custom_title import make_title


class ViewData(Page):
    def __init__(self, tabs: list[tables.Table]):
        self.tabs = tabs

    @property
    def header(self):
        return "View Data"

    def build_table(self):
        return st.dataframe(self.db.get_data(self.header))

    def write_tabs(self):
        tabs = st.tabs([make_title(table.header) for table in self.tabs])

        for i, tab in enumerate(tabs):
            with tab:
                self.tabs[i].build_table()
