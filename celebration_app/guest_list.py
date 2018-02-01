from distance_calculator import great_circle
import json
from pylru import lrudecorator
from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger(__name__)


guest_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "number"},
        "name": {"type": "string"},
        "latitude": {"type": ["number", "string"]},
        "longitude": {"type": ["number", "string"]},
    },
    "required": ["user_id", "name", "latitude", "longitude"]
}


class Guests(object):

    def __init__(self, location_point):
        """

        :param location_point:
        :type location_point: tuple, great_circle.Point
        :param proximity_radius:
        :type proximity_radius: int
        """
        self.location_point = location_point

    def _validate_guest_object(self, guest_object):
        try:
            validate(guest_object, guest_schema)
            latitude = float(guest_object["latitude"])
            longitude = float(guest_object["longitude"])
            if longitude < -180 or longitude > 180:
                raise ValueError
            if latitude < -90 or latitude > 90:
                raise ValueError
            guest_object["latitude"] = latitude
            guest_object["longitude"] = longitude
        except (ValidationError, ValueError):
            logger.warning("Invalid guest discarded: %s", guest_object)
            return False
        return True

    @lrudecorator(size=32)
    def _load_guest_list(self, guest_file_url):
        """
        :param guest_file_url:
        :type guest_file_url: str
        :return:
        """
        guest_list = []
        with open(guest_file_url) as guest_file:
            line = guest_file.readline()
            while line:
                guest_object = json.loads(line)
                if self._validate_guest_object(guest_object):
                    guest_list.append(guest_object)
                line = guest_file.readline()
        return guest_list

    def _filter_by_radius(self, guest_object, proximity_radius):
        latitude = guest_object["latitude"]
        longitude = guest_object["longitude"]
        point = (latitude, longitude)
        mesure = great_circle.measure_distance(point, self.location_point)
        return mesure < proximity_radius

    def get_guest_list(self, guest_file_url, proximity_radius=100, ascending=1):
        """


        :param guest_file_url:
        :type guest_file_url: str
        :return:
        """

        guest_list = self._load_guest_list(guest_file_url)
        guest_list = [(guest["user_id"], guest["name"])
                      for guest in guest_list
                      if self._filter_by_radius(guest, proximity_radius)]

        if ascending:
            reverse = False
        else:
            reverse = True

        guest_list.sort(key=lambda x: x[0], reverse=reverse)

        return guest_list

