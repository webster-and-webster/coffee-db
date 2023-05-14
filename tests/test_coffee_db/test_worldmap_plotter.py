from coffee_db.visualizations.map_visualizations import WorldMapPlotter


def test_get_country_count(dummy_coffee_list, dummy_roastery_list):
    world_map_plotter = WorldMapPlotter()

    coffee_output = world_map_plotter._get_country_count(dummy_coffee_list)
    assert coffee_output == {"Test Country": 1}

    roastery_output = world_map_plotter._get_country_count(dummy_roastery_list)
    assert roastery_output == {"Test Country": 1}
