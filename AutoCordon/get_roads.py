from os_paw.wfs_api import WFS_API
import configparser
import geopandas as gpd

import project_paths as paths

config = configparser.ConfigParser()
config.read(paths.config_path)
API_KEY = config['KEYS']['API_KEY']

# Choose a Spatial Reference System
SRS = 'EPSG:27700'


def get_roads(centre_coord, max_distance):
    bbox = f"{centre_coord[0] - max_distance}, {centre_coord[1] - max_distance}, {centre_coord[0] + max_distance}, {centre_coord[1] + max_distance}"
    features = []
    for type_name in ["Zoomstack_RoadsLocal", "Zoomstack_RoadsNational", "Zoomstack_RoadsRegional"]:
        wfs_api = WFS_API(api_key=API_KEY)
        payload = wfs_api.get_all_features_within_bbox(type_name=type_name,
                                                    bbox=bbox,
                                                    srs=SRS,
                                                    allow_premium=True)
        features.extend(payload["features"])
    return gpd.GeoDataFrame.from_features(features, crs=SRS).explode().reset_index(drop=True)