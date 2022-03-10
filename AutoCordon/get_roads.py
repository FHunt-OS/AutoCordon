import geopandas as gpd
from osdatahub import Extent, FeaturesAPI

CRS = 'EPSG:27700'


def get_roads(api_key, polygon):
    extent = Extent(polygon, crs='epsg:27700')
    roads = []
    for product in ['zoomstack_roads_local',
                    'zoomstack_roads_national',
                    'zoomstack_roads_regional']:
        features_api = FeaturesAPI(api_key, product, extent)
        result = features_api.query(10000000)
        roads.extend(result['features'])
    features_gdf = gpd.GeoDataFrame.from_features(roads, crs=CRS)
    return features_gdf.explode().reset_index(drop=True)
