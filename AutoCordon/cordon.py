from pygeos.constructive import buffer
from pygeos.creation import points, prepare, linestrings
from pygeos.set_operations import intersection, difference, intersection_all
from pygeos.geometry import get_exterior_ring, get_dimensions, get_parts
from pygeos.predicates import intersects
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from pygeos.io import from_shapely


def get_basic_cordon(centre_coord, distance):
    cordon = buffer(points(centre_coord), distance)
    return get_exterior_ring(cordon)


def get_intersecting_points(intersection_result):
    points_bool = get_dimensions(intersection_result) == 0
    intersecting_points = intersection_result[points_bool]
    return get_parts(intersecting_points)


def get_road_closure_locations(centre_coord, distance, roads):
    basic_cordon = get_basic_cordon(centre_coord, distance)
    prepare(roads)
    intersecting_roads = intersection(roads, basic_cordon)
    return get_intersecting_points(intersecting_roads)


def split_roads_with_cordon(centre_coord, distance, roads):
    roads_gdf = gpd.GeoDataFrame({"geometry": roads,
                                  "road_id": range(len(roads))})
    cordon = get_basic_cordon(centre_coord, distance)
    cordon_gdf = gpd.GeoDataFrame({"geometry": [cordon],
                                   "cordon_id": ["cordon"]})
    overlay = gpd.overlay(roads_gdf, cordon_gdf, how="union",
                          keep_geom_type=False).explode()
    overlay.reset_index(drop=True, inplace=True)
    is_linestring = overlay.geometry.geom_type == "LineString"
    is_not_cordon = overlay["cordon_id"] != "cordon"
    overlay_bool = is_linestring & is_not_cordon
    return from_shapely(overlay[overlay_bool].geometry)

