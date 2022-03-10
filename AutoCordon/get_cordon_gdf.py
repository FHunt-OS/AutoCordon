import geopandas as gpd
import momepy as mm
import pygeos as pyg

from AutoCordon.get_roads import get_roads
from AutoCordon.graph_info import get_edge_info
from AutoCordon.manipulate_geometries import get_geoms, overlay_gdf_with_geom
from AutoCordon.remove_nodes import get_removals


def get_cordon_layers(centre, distance, distance_max, OS_API_KEY):
    roads = get_roads(centre, distance_max + 10, OS_API_KEY)
    geoms = get_geoms(roads, centre, distance, distance_max)
    donut_roads = overlay_gdf_with_geom(roads, geoms["polygons"]["donut"])
    graph = mm.gdf_to_nx(donut_roads)

    removals = get_removals(graph,
                            geoms['nodes']["hole"],
                            geoms['nodes']["shell"])
    removal_names = get_edge_info(graph, removals, ["Name", "Number"],
                                  invalid_fill="Unnamed Road")

    all_points = pyg.points(removals + [centre])
    points_types = ["removal"] * len(removals) + ["centre"]
    points_names = removal_names + [""]
    points = gpd.GeoDataFrame({"geometry": all_points,
                               "type": points_types,
                               "names": points_names},
                              crs="EPSG:27700").to_crs("EPSG:4326")

    min_cordon = gpd.GeoDataFrame({"geometry": [geoms["polygons"]["hole"]],
                                   "type": ["min_cordon"]},
                                  crs="EPSG:27700").to_crs("EPSG:4326")

    max_cordon = gpd.GeoDataFrame({"geometry": [geoms["polygons"]["donut"]],
                                   "type": ["max_cordon"]},
                                  crs="EPSG:27700").to_crs("EPSG:4326")
    return {"closures": points.to_json(),
            "min_cordon": min_cordon.to_json(),
            "max_cordon": max_cordon.to_json()}


def get_closures(roads, centre, distance, distance_max):
    geoms = get_geoms(roads, centre, distance, distance_max)
    donut_roads = overlay_gdf_with_geom(roads, geoms["polygons"]["donut"])
    graph = mm.gdf_to_nx(donut_roads)

    removals = get_removals(graph,
                            geoms['nodes']["hole"],
                            geoms['nodes']["shell"])
    removal_names = get_edge_info(graph, removals, ["Name", "Number"],
                                  invalid_fill="Unnamed Road")

    all_points = pyg.points(removals + [centre])
    points_types = ["removal"] * len(removals) + ["centre"]
    points_names = removal_names + [""]
    points = gpd.GeoDataFrame({"geometry": all_points,
                               "type": points_types,
                               "names": points_names},
                              crs="EPSG:27700").to_crs("EPSG:4326")
    return points.to_json(drop_id=True)
