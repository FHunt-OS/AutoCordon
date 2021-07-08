import geopandas as gpd
import momepy as mm
import pygeos as pyg

from AutoCordon.get_roads import get_roads
from AutoCordon.graph_info import get_edge_info
from AutoCordon.manipulate_geometries import get_geoms, overlay_gdf_with_geom
from AutoCordon.structure_nodes_copy_copy import get_removals


def get_cordon_layers(centre, distance, distance_max):
    roads = get_roads(centre, distance_max + 10)
    geoms = get_geoms(roads, centre, distance, distance_max)
    donut_roads = overlay_gdf_with_geom(roads, geoms["polygons"]["donut"])
    graph = mm.gdf_to_nx(donut_roads)

    removals = get_removals(graph,
                            geoms['nodes']["hole"],
                            geoms['nodes']["shell"])
    removal_names = get_edge_info(graph, removals, ["Name", "Number"],
                                  invalid_fill="Unnamed Road")

    points = gpd.GeoDataFrame({"geometry": pyg.points(removals + [centre]),
                               "type": ["removal"] * len(removals) + ["centre"],
                               "names": removal_names + [""]},
                              crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    min_cordon = gpd.GeoDataFrame({"geometry": [geoms["polygons"]["hole"]],
                                   "type": ["min_cordon"]},
                                  crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    max_cordon = gpd.GeoDataFrame({"geometry": [geoms["polygons"]["donut"]],
                                   "type": ["max_cordon"]},
                                  crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    return {"closures": points,
            "min_cordon": min_cordon,
            "max_cordon": max_cordon}
