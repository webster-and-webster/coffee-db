from coffee_db.app import Site
<<<<<<< HEAD
from coffee_db.app.pages import (
    HomePage,
    AddRemoveData,
    Visualizations,
    WorldMapPlot,
    ViewData,
)
=======
from coffee_db.app.pages import HomePage, AddRemoveData, Visualizations, WorldMapPlot, ViewData
>>>>>>> 966c821 (add view_data and tables pages)
from coffee_db import CoffeeDB
from coffee_db.data_loaders import PostgresDataLoader

from coffee_db.app import forms, tables


pages = [
    HomePage(),
    Visualizations(tabs=[WorldMapPlot()]),
    ViewData(
        tabs=[
<<<<<<< HEAD
            tables.StreamlitTable("roastery"),
            tables.StreamlitTable("coffee"),
            tables.StreamlitTable("country"),
            tables.StreamlitTable("variety"),
            tables.StreamlitTable("process"),
            tables.StreamlitTable("coffee_user"),
=======
            tables.RoasteryTable(),
            tables.CoffeeTable(),
            tables.CountryTable(),
            tables.VarietyTable(),
            tables.ProcessTable(),
            tables.CoffeeUserTable(),
>>>>>>> 966c821 (add view_data and tables pages)
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
