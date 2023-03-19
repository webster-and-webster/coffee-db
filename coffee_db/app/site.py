import streamlit as st
from typing import Optional

from coffee_db.app.utils import Page
from coffee_db.app.utils.custom_title import make_title


class Site:
    """
    Coffee website App
    """
    def __init__(
        self,
        pages: list[Page],
        name: str,
        data_loader,
        db
    ):
        self.pages = pages
        self.name = name
        self.data_loader = data_loader(db)
        self._format_app()
        self._format_sidebar()
        self._read_data_to_cache()
        st.cache.db = db

    def _format_app(self):
        st.set_page_config(page_title=self.name, page_icon=None)

    def _format_sidebar(self):
        st.sidebar.image("docs/logo.png", width=125)
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
            """, unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

    def _get_page_by_name(self, page_name) -> Optional[Page]:
        for page in self.pages:
            if make_title(page.header) == page_name:
                return page
        return None

    def _read_data_to_cache(self):
        (
            st.cache.coffees,
            st.cache.coffee_users,
            st.cache.countries,
            st.cache.processes,
            st.cache.roasteries,
            st.cache.varieties,
        ) = self.data_loader.get_data()

    def write(self):
        current_page_name = st.sidebar.radio(
            label=" ",
            options=[make_title(page.header) for page in self.pages],
            label_visibility="hidden"
        )
        current_page = self._get_page_by_name(current_page_name)
        current_page.write()
