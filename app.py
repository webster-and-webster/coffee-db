from coffee_db.app import Site
from coffee_db.app.pages import (
    HomePage,
    AddRemoveData,
    Visualizations,
    WorldMapPlot,
    ViewData,
)
from coffee_db import CoffeeDB
from coffee_db.data_loaders import PostgresDataLoader

from coffee_db.app import forms, tables


pages = [
    HomePage(),
    Visualizations(tabs=[WorldMapPlot()]),
    ViewData(
        tabs=[
            tables.StreamlitTable("roastery"),
            tables.StreamlitTable("coffee"),
            tables.StreamlitTable("country"),
            tables.StreamlitTable("variety"),
            tables.StreamlitTable("process"),
            tables.StreamlitTable("coffee_user"),
        ]
    ),
    AddRemoveData(
        tabs=[
            forms.RoasteryForm(),
            forms.CoffeeForm(),
            forms.CountryForm(),
            forms.VarietyForm(),
            forms.ProcessForm(),
            forms.CoffeeUserForm(),
        ]
    ),
]

site = Site(
    pages=pages, name="Coffee DB", data_loader=PostgresDataLoader, db=CoffeeDB()
)


def main():
    site.write()


if __name__ == "__main__":
    main()
