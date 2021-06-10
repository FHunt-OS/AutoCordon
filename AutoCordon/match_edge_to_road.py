import geopandas as gpd
import pygeos as pyg
import numpy as np
import matplotlib.pyplot as plt

edges = pyg.from_shapely(gpd.read_file("removed_lines_1.geojson").geometry)
roads = pyg.from_shapely(gpd.read_file("closable_lines.geojson").geometry)

pyg.prepare(roads)
intersection1 = np.array([pyg.intersects(roads, edge) for edge in pyg.get_point(edges, 0)])
intersection2 = np.array([pyg.intersects(roads, edge) for edge in pyg.get_point(edges, -1)])
intersection = np.max(intersection1 * intersection2, axis=0)

print(pyg.get_num_geometries(pyg.multilinestrings(roads[intersection])), len(edges))

f, ax = plt.subplots()
gpd.GeoDataFrame({"geometry": roads}).plot(ax=ax, color="grey")
gpd.GeoDataFrame({"geometry": roads[intersection]}).plot(ax=ax)
gpd.GeoDataFrame({"geometry": edges}).plot(ax=ax, color="r")
plt.show()

# pyg.get_point(roads, [0, -1])
