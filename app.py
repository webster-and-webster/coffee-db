from coffee_db.app import Site
from coffee_db.app.pages import (
    HomePage, AddRemoveData, Visualizations, ViewData, WorldMapPlot
)
from coffee_db import CoffeeDB
from coffee_db.data_loaders import PostgresDataLoader

from coffee_db.app import forms


pages = [
    HomePage(),
    Visualizations(tabs=[
        WorldMapPlot()
    ]),
    # ViewData(), ## TODO: Implement ViewData functionality
    AddRemoveData(tabs=[
        forms.RoasteryForm(),
        forms.CoffeeForm(),
        forms.CountryForm(),
        forms.VarietyForm(),
        forms.ProcessForm(),
        forms.CoffeeUserForm(),
    ])
]

site = Site(
    pages=pages,
    name="Coffee DB",
    data_loader=PostgresDataLoader,
    db=CoffeeDB()
)


def main():
    site.write()


if __name__ == "__main__":
    main()
