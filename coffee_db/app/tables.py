import streamlit as st

from coffee_db.database.heroku_psql import CoffeeDB


class StreamlitTable:
    """Table class to represent a data table in streamlit"""

    def __init__(self, header: str):
        self.db = CoffeeDB()
        self._header = header

    @property
    def header(self):
        return self._header

    def build_table(self):
        """Construct a streamlit dataframe from the raw SQL table"""
        st.dataframe(self.db.get_data(self.header))
