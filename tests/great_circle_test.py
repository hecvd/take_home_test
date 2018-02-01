import unittest
from distance_calculator import great_circle


class GreatCircleTest(unittest.TestCase):

    def test_mesure_distance(self):
        """Test if the distance is calculated correctly.

        It allows some rounding down to avoid some possible processor
        inconsistencies.
        """
        point1 = (55, 48)
        point2 = (55, 50)
        result = great_circle.measure_distance(point1, point2)
        self.assertAlmostEqual(127.55341409824968, result, places=5)
        point1 = (12, 37)
        point2 = (85, 85)
        result = great_circle.measure_distance(point1, point2)
        self.assertAlmostEqual(8304.346305001314, result, places=5)
        point1 = (90, 48)
        point2 = (86, 58)
        result = great_circle.measure_distance(point1, point2)
        self.assertAlmostEqual(444.7803348967649, result, places=5)
        point1 = (35, 78)
        point2 = (27, 12)
        result = great_circle.measure_distance(point1, point2)
        self.assertAlmostEqual(6241.743650874065, result, places=5)

    def test_invalid_point(self):
        """Tests that the points are valid."""
        with self.assertRaises(ValueError):
            point1 = (96, 78)
            great_circle.Point(*point1)

        with self.assertRaises(ValueError):
            point1 = (86, 198)
            great_circle.Point(*point1)

        with self.assertRaises(ValueError):
            point1 = ("invalid", 198)
            great_circle.Point(*point1)

        with self.assertRaises(ValueError):
            point1 = (78, "invalid")
            great_circle.Point(*point1)

    def test_validate(self):
        """Tests the correct functionality of validate."""
        latitude = "50"
        longitude = "70"
        result_latitude, result_longitude = (
            great_circle.Point.validate(latitude, longitude))
        self.assertEqual(result_latitude, 50.0)
        self.assertEqual(result_longitude, 70.0)

    def test_from_tuple(self):
        """Validates the creation of an instance from a tuple."""
        point1 = (35, 78)
        result = great_circle.Point.from_tuple(point1)
        self.assertTrue(isinstance(result, great_circle.Point))
        self.assertEqual(result.latitude, 35.0)
        self.assertEqual(result.longitude, 78.0)


if __name__ == '__main__':
    unittest.main()
