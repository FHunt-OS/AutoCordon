import geopandas as gpd
import pygeos as pyg

from AutoCordon.structure_nodes import get_junction_closures


def get_cordon_layers(road_lines, centre, distance, distance_max, wider_factor):
    removals, candidates, default_closures = get_junction_closures(road_lines, centre, distance, distance_max, wider_factor)

    mls_road_lines = pyg.multilinestrings(road_lines)
    # display_roads = pyg.clip_by_rect(mls_road_lines, *pyg.bounds(pyg.buffer(pyg.points(*centre), distance_max + 500)))
    
    print("removals", len(removals))
    min_cordon = pyg.buffer(pyg.points(*centre), distance)
    buffer_zone = pyg.difference(pyg.buffer(pyg.points(*centre), distance_max), min_cordon)
    points = gpd.GeoDataFrame({"geometry": removals + [pyg.points(*centre)],
                               "type": ["removal"] * len(removals) + ["centre"]},
                              crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    min_cordon = gpd.GeoDataFrame({"geometry": [min_cordon],
                                 "type": ["min_cordon"]},
                                crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    max_cordon = gpd.GeoDataFrame({"geometry": [buffer_zone],
                                 "type": ["max_cordon"]},
                                crs="EPSG:27700").to_crs("EPSG:4326").to_json()
    return {"closures": points,
            "min_cordon": min_cordon,
            "max_cordon": max_cordon}