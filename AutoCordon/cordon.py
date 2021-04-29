import geopandas as gpd
from pygeos.constructive import buffer
from pygeos.creation import points, prepare
from pygeos.geometry import get_dimensions, get_exterior_ring, get_parts
from pygeos.io import from_shapely
from pygeos.predicates import is_empty
from pygeos.set_operations import difference, intersection


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


def remove_roads_within_cordon(centre_coord, distance, roads):
    diff = difference(roads, buffer(points(centre_coord), distance))
    return diff[~is_empty(diff)]


def get_buffer_zone(centre_coord, min_distance, max_distance):
    min_cordon = buffer(points(centre_coord), min_distance)
    max_cordon = buffer(points(centre_coord), max_distance)
    return difference(max_cordon, min_cordon)


def get_non_empty_linestrings(geometries):
    non_empty = geometries[~is_empty(geometries)]
    return non_empty[get_dimensions(non_empty) == 1]


def extract_closure_candidates(centre_coord, min_distance, max_distance, roads):
    buffer_zone = get_buffer_zone(centre_coord, min_distance, max_distance)
    candidates = intersection(roads, buffer_zone)
    return get_non_empty_linestrings(candidates)
