from pygeos.creation import linestrings
import numpy as np

centre_crossroads = linestrings([
    [(2, 2), (2, 1)],
    [(2, 2), (3, 2)],
    [(2, 2), (2, 3)],
    [(2, 2), (1, 2)]
])

ring_road = linestrings([
    [(3, 1), (3, 3)],
    [(3, 3), (1, 3)],
    [(1, 3), (1, 1)],
    [(1, 1), (3, 1)]
])

spoke_roads = linestrings([
    [(0, 4), (1, 3)],
    [(3, 3), (4, 4)],
    [(3, 1), (4, 0)],
    [(1, 1), (0, 0)]
])

dummy_roads = np.concatenate([centre_crossroads, ring_road, spoke_roads])
print(dummy_roads)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import geopandas as gpd

    dummy_roads_gdf = gpd.GeoDataFrame({"geometry": dummy_roads,
                                        "id": range(len(dummy_roads))},
                                       crs='epsg:27700')
    fig, ax = plt.subplots()
    dummy_roads_gdf.plot(ax=ax)
    dummy_roads_gdf.iloc[[5, 4, 2, 1, 10, 9, 6, 7]].plot(ax=ax, color='r')
    plt.show()
