# from os_paw.wfs_api import WFS_API
import geopandas as gpd
from osdatahub import Extent, FeaturesAPI

SRS = 'EPSG:27700'


def get_roads(api_key, polygon):
    extent = Extent(polygon, crs='epsg:27700')
    roads = []
    for product in ['zoomstack_roads_local',
                    'zoomstack_roads_national',
                    'zoomstack_roads_regional']:
        features_api = FeaturesAPI(api_key, product, extent)
        result = features_api.query(10000000)
        roads.extend(result['features'])
    features_gdf = gpd.GeoDataFrame.from_features(roads, crs=SRS)
    return features_gdf.explode().reset_index(drop=True)

# Choose a Spatial Reference System
# FEATURE_TYPES = ["Zoomstack_RoadsLocal",
#                  "Zoomstack_RoadsNational",
#                  "Zoomstack_RoadsRegional"]


# def get_roads(centre_coord, distance, OS_API_KEY):
#     x, y = centre_coord
#     bbox = f"{x - distance}, {y - distance}, {x + distance}, {y + distance}"
#     features = []
#     for type_name in FEATURE_TYPES:
#         wfs_api = WFS_API(api_key=OS_API_KEY)
#         payload = wfs_api.get_all_features_within_bbox(type_name=type_name,
#                                                        bbox=bbox,
#                                                        srs=SRS,
#                                                        allow_premium=True)
#         features.extend(payload["features"])
#     features_gdf = gpd.GeoDataFrame.from_features(features, crs=SRS)
#     return features_gdf.explode().reset_index(drop=True)
