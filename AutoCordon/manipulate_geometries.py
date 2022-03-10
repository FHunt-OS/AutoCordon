import geopandas as gpd
import pygeos as pyg


def overlay_gdf_with_geom(gdf, geom):
    geom_gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs=gdf.crs)
    overlay_gdf = gpd.overlay(gdf, geom_gdf, how='intersection',
                              keep_geom_type=False)
    return overlay_gdf.explode().reset_index(drop=True)


def get_geoms(lines, centre, distance, distance_max):
    centre = pyg.from_shapely(centre)

    shell = pyg.buffer(centre, distance_max)
    shell_ring = pyg.get_exterior_ring(shell)
    shell_nodes = get_intersecting_points(lines, shell_ring)

    hole = pyg.buffer(centre, distance)
    hole_ring = pyg.get_exterior_ring(hole)
    hole_nodes = get_intersecting_points(lines, hole_ring)

    donut = pyg.polygons(shell_ring, holes=[hole_ring])
    return {"nodes": {"shell": shell_nodes,
                      "hole": hole_nodes},
            "polygons": {"donut": donut,
                         "hole": hole}}


def get_intersecting_points(lines, ring):
    points = overlay_gdf_with_geom(lines, ring)
    ring_points = list(set(zip(points.geometry.x,
                               points.geometry.y)))
    return ring_points
