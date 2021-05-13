from pygeos.constructive import buffer
from pygeos.creation import points
from pygeos.geometry import get_dimensions, get_exterior_ring, get_parts
from pygeos.predicates import is_empty
from pygeos.set_operations import difference, intersection


class BufferZone:

    GEOM_TYPE = {
        "points": 0,
        "lines": 1,
        "polygons": 2
        }

    def __init__(self, centre_coord, min_distance, max_distance):
        self.centre_coord = centre_coord
        self.min_distance = min_distance
        self.max_distance = max_distance

    @property
    def centre_coord(self):
        return self.__centre_coord

    @centre_coord.setter
    def centre_coord(self, new_value):
        self.__centre_coord = points(new_value)

    @property
    def min_distance(self):
        return self.__min_distance

    @min_distance.setter
    def min_distance(self, new_value):
        self.__min_distance = new_value
        self.__min_buffer = buffer(self.centre_coord, self.min_distance)

    @property
    def min_buffer(self):
        return self.__min_buffer

    @property
    def max_distance(self):
        return self.__max_distance

    @max_distance.setter
    def max_distance(self, new_value):
        self.__max_distance = new_value
        self.__max_buffer = buffer(self.centre_coord, self.max_distance)

    @property
    def max_buffer(self):
        return self.__max_buffer

    def get_geometry(self):
        return difference(self.max_buffer, self.min_buffer)

    def get_intersection(self, geometries):
        return intersection(self.get_geometry(), geometries)

    def get_intersecting_lines(self, geometries):
        intersecting = self.get_intersection(geometries)
        inter_lines = self.__filter_for_geom_type("lines", intersecting)
        return get_parts(inter_lines)

    def get_intersecting_perimeter_points(self, edge, geometries):
        if edge == "interior":
            linear_ring = get_exterior_ring(self.min_buffer)
        elif edge == "exterior":
            linear_ring = get_exterior_ring(self.max_buffer)
        else:
            raise ValueError("edge must be either 'interior' or 'exterior'")
        intersecting = intersection(linear_ring, geometries)
        inter_points = self.__filter_for_geom_type("points", intersecting)
        return get_parts(inter_points)

    def __filter_for_geom_type(self, geom_type, geometries):
        non_empty = geometries[~is_empty(geometries)]
        return non_empty[get_dimensions(non_empty) == self.GEOM_TYPE[geom_type]]
