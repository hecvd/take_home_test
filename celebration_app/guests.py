import logging
import json
from distance_calculator import great_circle
from jsonschema import validate, ValidationError

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


class FindGuests(object):

    def __init__(self, location_point):
        """Class to load, filter and sorts a list of guests.

        :param location_point: The location of reference to filter
            guests by distance. It's a tuple of latitude and longitude.
            Example: (53.339428, -6.257664)
        :type location_point: tuple
        """
        if not isinstance(location_point, great_circle.Point):
            self.location_point = great_circle.Point.from_tuple(location_point)
        else:
            self.location_point = location_point

    def _load_json(self, json_string):
        """Tries to load a json.

        :param json_string: A json encoded string.
        :type json_string: str
        :return: A python representation of the json.
        """
        loaded_json = None
        try:
            loaded_json = json.loads(json_string)
        except ValueError:
            logger.warning("Couldn't load invalid entry: %s", json_string)
        return loaded_json

    @staticmethod
    def _validate_guest_object(guest_object):
        """Validates all the possible errors a guest input might have.

        This function tests for a valid longitude and latitude, and json schema
        correctness.

        :param guest_object: The python dict containing the guest json object.
        :type guest_object: dict
        :return: True if the entry is valid, False otherwise.
        :rtype: bool
        """
        try:
            validate(guest_object, guest_schema)
            latitude, longitude = great_circle.Point.validate(
                guest_object["latitude"], guest_object["longitude"])
            guest_object["latitude"] = latitude
            guest_object["longitude"] = longitude
        except (ValidationError, ValueError):
            logger.warning("Invalid guest discarded: %s", guest_object)
            return False
        return True

    def _load_guest_list(self, guest_file_url):
        """Loads the guest list from source file.

        :param guest_file_url: url of the file.
        :type guest_file_url: str
        :return: A list of dicts with the guests information.
        """
        guest_list = []
        try:
            with open(guest_file_url) as guest_file:
                line = guest_file.readline()
                while line:
                    guest_object = self._load_json(line)
                    if (guest_object is not None
                            and self._validate_guest_object(guest_object)):
                        guest_list.append(guest_object)
                    line = guest_file.readline()
        except IOError:
            logger.warning("File %s Not Found.", guest_file_url)
        return guest_list

    def _filter_by_radius(self, guest_object, proximity_radius):
        """Filters out a guest if its distance is outside the radius.

        :param guest_object: The guest object.
        :type guest_object: dict
        :param proximity_radius: The maximum radius to filter guests. All guests
            that are inside the radius will not be filtered.
        :return: True if the guest is within the proximity_radius,
            False otherwise.
        :rtype: bool
        """
        latitude = guest_object["latitude"]
        longitude = guest_object["longitude"]
        point = (latitude, longitude)
        measure = great_circle.measure_distance(point, self.location_point)
        return measure < proximity_radius

    def get_guest_list(self, guest_file_url, proximity_radius=100, ascending=1):
        """Gets a filtered and sorted list of guests from the source file.

        :param guest_file_url: The URL of the file to read the guests from.
        :type guest_file_url: str
        :param proximity_radius: The radius to limit guest distance.
        :type proximity_radius: int
        :param ascending: If the ordering should be ascending or descending.
        :type ascending: bool
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
