import unittest
import mock
import os

from celebration_app import guests


class GuestListTest(unittest.TestCase):

    def setUp(self):
        office_location = (53.339428, -6.257664)
        self.test_file_err = os.path.join(
            os.path.dirname(__file__), "test_assets/invalid_inputs.txt")
        self.test_file_ok = os.path.join(
            os.path.dirname(__file__), "test_assets/ok_inputs.txt")
        self.guests = guests.FindGuests(office_location)

    @mock.patch.object(guests.logger, "warning")
    def test_file_not_found_warning(self, mock_logger):
        """Checks for an invalid source file"""
        self.guests.get_guest_list("invalid")
        mock_logger.assert_called()

    @mock.patch.object(guests.logger, "warning")
    def test_invalid_coordinates(self, mock_logger):
        """
        This test checks for invalid json, latitude, longitude,
        json schema completeness, latitude range, and longitude range.
        """
        self.guests.get_guest_list(self.test_file_err)
        self.assertEqual(mock_logger.call_count, 6)

    def test_load_inputs(self):
        """Test Load all inputs with permissive distance radius."""
        result = self.guests.get_guest_list(self.test_file_ok, 1000)
        self.assertEqual(len(result), 8)

    def test_load_inputs_by_distance(self):
        """Test filtered inputs by radius."""
        result = self.guests.get_guest_list(self.test_file_ok, 100)
        self.assertEqual(len(result), 3)

    def test_result_order(self):
        """Check the ordering of the result list."""
        result = self.guests.get_guest_list(self.test_file_ok, 100)
        self.assertListEqual([8, 12, 26], [item[0] for item in result])
        result = self.guests.get_guest_list(
            self.test_file_ok, 100, ascending=False)
        self.assertListEqual([26, 12, 8], [item[0] for item in result])

    def test_invalid_location_point(self):
        """Validates the creation of the instance using a tuple."""
        with self.assertRaises(ValueError):
            office_location = (53.339428, -1116.257664)
            guests.FindGuests(office_location)
        with self.assertRaises(ValueError):
            office_location = ("invalid", -116.257664)
            guests.FindGuests(office_location)


if __name__ == '__main__':
    unittest.main()
