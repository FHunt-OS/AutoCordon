import geopandas as gpd
import momepy as mm
import pygeos as pyg

from AutoCordon.structure_nodes_copy import get_junction_closures
from AutoCordon.graph_info import get_edge_info_for_node
      

def get_cordon_layers(centre, distance, distance_max):
    removals, hole, donut, graph = get_junction_closures(centre, distance, distance_max)
    removal_names = [list(set(get_edge_info_for_node(graph, removal, ["Name", "Number"],
                                                     invalid_fill="Unnamed Road")))
                     for removal in removals]
    print("removals", len(removals))
    # print(removal_names)
    points = gpd.GeoDataFrame({"geometry": pyg.points(removals + [centre]),
                               "type": ["removal"] * len(removals) + ["centre"],
                               "names": removal_names + [""]},
                              crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    min_cordon = gpd.GeoDataFrame({"geometry": [hole],
                                 "type": ["min_cordon"]},
                                crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    max_cordon = gpd.GeoDataFrame({"geometry": [donut],
                                 "type": ["max_cordon"]},
                                crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    return {"closures": points,
            "min_cordon": min_cordon,
            "max_cordon": max_cordon}
