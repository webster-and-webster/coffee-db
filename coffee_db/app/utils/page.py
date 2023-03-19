from abc import ABC, abstractmethod
import streamlit as st

from coffee_db.app.utils import Tab
from coffee_db.app.utils.custom_title import make_title


class Page(ABC):

    def __init__(self, tabs: list[Tab] = None):
        self.tabs = tabs

    @property
    @abstractmethod
    def header(self):
        return "default header"

    def write(self):
        st.title(make_title(self.header))
        self.write_tabs()

    def write_tabs(self):
        if self.tabs is not None:
            tabs = st.tabs([make_title(tab.header) for tab in self.tabs])
            for i, tab in enumerate(tabs):
                with tab:
                    self.tabs[i].write()

    def __str__(self):
        return self.NAME
