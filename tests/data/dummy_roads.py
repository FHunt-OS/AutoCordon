from pygeos.creation import linestrings
import numpy as np

centre_crossroads_coords = [
    [(2, 2), (2, 1)],
    [(2, 2), (3, 2)],
    [(2, 2), (2, 3)],
    [(2, 2), (1, 2)]
]

ring_road_coords = [
    [(3, 1), (3, 3)],
    [(3, 3), (1, 3)],
    [(1, 3), (1, 1)],
    [(1, 1), (3, 1)]
]

spoke_roads_coords = [
    [(0, 4), (1, 3)],
    [(3, 3), (4, 4)],
    [(3, 1), (4, 0)],
    [(1, 1), (0, 0)]
]

dummy_roads_coords = centre_crossroads_coords + ring_road_coords + spoke_roads_coords

# print(dummy_roads)
centre_crossroads = linestrings(centre_crossroads_coords)
ring_road = linestrings(ring_road_coords)
spoke_roads = linestrings(spoke_roads_coords)
dummy_roads = linestrings(dummy_roads_coords)



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import geopandas as gpd

    from pygeos.coordinates import get_coordinates
    import networkx as nx

    # print(get_coordinates(centre_crossroads))
    G = nx.DiGraph(centre_crossroads_coords)
#     G.add_edges_from([
#     [(2, 2), (2, 1)],
#     [(2, 2), (3, 2)],
#     [(2, 2), (2, 3)],
#     [(2, 2), (1, 2)]
# ])
    print(G.nodes)
    print(G.edges)
    exit()


    dummy_roads_gdf = gpd.GeoDataFrame({"geometry": dummy_roads,
                                        "id": range(len(dummy_roads))},
                                       crs='epsg:27700')
    fig, ax = plt.subplots()
    dummy_roads_gdf.plot(ax=ax)
    dummy_roads_gdf.iloc[[5, 4, 2, 1, 10, 9, 6, 7]].plot(ax=ax, color='r')
    plt.show()
