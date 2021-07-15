from os_paw.wfs_api import WFS_API
import geopandas as gpd

# Choose a Spatial Reference System
SRS = 'EPSG:27700'
FEATURE_TYPES = ["Zoomstack_RoadsLocal",
                 "Zoomstack_RoadsNational",
                 "Zoomstack_RoadsRegional"]


def get_roads(centre_coord, distance, OS_API_KEY):
    x, y = centre_coord
    bbox = f"{x - distance}, {y - distance}, {x + distance}, {y + distance}"
    features = []
    for type_name in FEATURE_TYPES:
        wfs_api = WFS_API(api_key=OS_API_KEY)
        payload = wfs_api.get_all_features_within_bbox(type_name=type_name,
                                                       bbox=bbox,
                                                       srs=SRS,
                                                       allow_premium=True)
        features.extend(payload["features"])
    features_gdf = gpd.GeoDataFrame.from_features(features, crs=SRS)
    return features_gdf.explode().reset_index(drop=True)
