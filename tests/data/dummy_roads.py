
centre_crossroads = [
    [(2, 2), (2, 1)],
    [(2, 2), (3, 2)],
    [(2, 2), (2, 3)],
    [(2, 2), (1, 2)]
]

ring_road = [
    [(3, 1), (3, 3)],
    [(3, 3), (1, 3)],
    [(1, 3), (1, 1)],
    [(1, 1), (3, 1)]
]

spoke_roads = [
    [(0, 4), (1, 3)],
    [(3, 3), (4, 4)],
    [(3, 1), (4, 0)],
    [(1, 1), (0, 0)]
]

dummy_roads = centre_crossroads + ring_road + spoke_roads

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import geopandas as gpd
    from shapely.geometry import LineString

    road_linestrings = [LineString(road) for road in dummy_roads]
    dummy_roads = gpd.GeoDataFrame({"geometry": road_linestrings,
                                    "id": range(len(dummy_roads))},
                                   crs='epsg:27700')
    fig, ax = plt.subplots()
    dummy_roads.plot(ax=ax)
    dummy_roads.iloc[[5, 4, 2, 1, 10, 9, 6, 7]].plot(ax=ax, color='r')
    plt.show()
