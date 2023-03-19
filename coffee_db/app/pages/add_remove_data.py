import streamlit as st

from coffee_db.app.utils import Page
from coffee_db.app import forms
from coffee_db.app.utils.custom_title import make_title


class AddRemoveData(Page):

    def __init__(self, tabs: list[forms.EntryForm]):
        self.tabs = tabs

    @property
    def header(self):
        return "Add/Remove Data"

    def _get_args(self, form_header) -> dict:
        if form_header == "coffee":
            return {
                "coffee_users": st.cache.coffee_users,
                "countries": st.cache.countries,
                "roasteries": st.cache.roasteries,
                "processes": st.cache.processes,
                "varieties": st.cache.varieties,
            }
        if form_header == "roastery":
            return {
                "countries": st.cache.countries,
            }
        return {}

    def write_tabs(self):
        tabs = st.tabs([make_title(form.header) for form in self.tabs])

        for i, tab in enumerate(tabs):
            with tab:
                col1, col2 = st.columns(2)
                with col1:
                    self.tabs[i].add(**self._get_args(self.tabs[i].header))
                with col2:
                    self.tabs[i].remove()
