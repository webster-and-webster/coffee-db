from abc import ABC, abstractmethod

import streamlit as st

from coffee_db.database.heroku_psql import CoffeeDB


class Table(ABC):

    def __init__(self):
        self.db = CoffeeDB()

    @property
    @abstractmethod
    def header(self):
        """
        Abstract property to define the form header. This should be based on the coffee_db class
         that is represents, eg 'roastery'
        """

        return "default_header"

    def build_table(self):
        st.dataframe(self.db.get_data(self.header))


class RoasteryTable(Table):

    @property
    def header(self):
        return "roastery"


class CountryTable(Table):

    @property
    def header(self):
        return "country"


class VarietyTable(Table):

    @property
    def header(self):
        return "variety"


class ProcessTable(Table):

    @property
    def header(self):
        return "process"


class CoffeeUserTable(Table):

    @property
    def header(self):
        return "coffee_user"


class CoffeeTable(Table):

    @property
    def header(self):
        return "coffee"
