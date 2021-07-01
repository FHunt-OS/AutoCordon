import geopandas as gpd
import pygeos as pyg


def intersect(geom1, geom2):
    intersection = pyg.intersection(geom1, geom2)
    return pyg.get_parts(intersection[~pyg.is_empty(intersection)])


def get_donut(point_coords, inner_radius, outer_radius):
    point = pyg.points(point_coords)
    hole = pyg.get_exterior_ring(pyg.buffer(point, inner_radius))
    shell = pyg.get_exterior_ring(pyg.buffer(point, outer_radius))
    return pyg.polygons(shell, holes=[hole])


def overlay_gdf_with_geom(gdf, geom):
    geom_gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs=gdf.crs)
    overlay_gdf = gpd.overlay(gdf, geom_gdf, how='intersection', keep_geom_type=False)
    return overlay_gdf.explode().reset_index(drop=True)
