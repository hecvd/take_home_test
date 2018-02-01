from collections import namedtuple
from math import radians, sin, cos, atan2, sqrt

EARTH_RADIUS = 6371.009


class Point(object):

    def __init__(self, latitude, longitude):
        """A convenience class to work with geographic points.

        :param latitude: The latitude of a point in degrees.
        :type latitude: float
        :param longitude: The longitude of a point in degrees.
        :type longitude: float
        """
        self.latitude = latitude
        self.longitude = longitude

        self.radians_latitude = radians(latitude)
        self.radians_longitude = radians(longitude)

        self.sin_latitude = sin(self.radians_latitude)
        self.cos_latitude = cos(self.radians_latitude)

        self.sin_longitude = sin(self.radians_longitude)
        self.cos_longitude = cos(self.radians_longitude)

    @classmethod
    def from_tuple(cls, tuple_point):
        """

        :param tuple_point: A Tuple containing the longitude
            and latitude of a point, in that order.
        :type tuple_point: tuple
        :return: An instance of Point.
        :rtype: Point
        """
        point = Point(tuple_point[0], tuple_point[1])
        return point


def measure_distance(point1, point2):
    """Measures the distance of two points using great-circle formula.

    :Example:

    >>>from distance_calculator.great_circle import measure_distance, Point
    >>>mexico_city = (19.39068, -99.283696)
    >>>dublin = (53.3242381, -6.3857844)
    >>>measure_distance(mexico_city, dublin)
    8477.904573873151
    >>>mexico_city = Point(19.39068, -99.283696)
    >>>mullingar = Point(53.5260787, -7.3614596)
    >>>measure_distance(mexico_city, mullingar)
    8409.782982745912

    :param point1: A Tuple or an instance of Point for the
        starting point.
    :type point1: tuple, Point
    :param point2: A Tuple or an instance of Point for the
        destination point.
    :type point2: tuple, Point
    :return: The distance between the points in Kilometers.
    :rtype float
    """
    if not isinstance(point1, Point):
        point1 = Point.from_tuple(point1)
    if not isinstance(point2, Point):
        point2 = Point.from_tuple(point2)

    delta_longitude = point2.radians_longitude - point1.radians_longitude

    cos_delta_longitude = cos(delta_longitude)
    sin_delta_longitude = sin(delta_longitude)

    quadrant1 = (point2.cos_latitude * sin_delta_longitude) ** 2
    quadrant1 += (point1.cos_latitude
                  * point2.sin_latitude - point1.sin_latitude
                  * point2.cos_latitude * cos_delta_longitude) ** 2
    quadrant1 = sqrt(quadrant1)

    quadrant2 = (point1.sin_latitude * point2.sin_latitude
                 + point1.cos_latitude * point2.cos_latitude
                 * cos_delta_longitude)

    distance = atan2(quadrant1, quadrant2)

    distance *= EARTH_RADIUS

    return distance
