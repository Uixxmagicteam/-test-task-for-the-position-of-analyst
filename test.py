import unittest

from DataProvider import DataProvider


class MyTestCase(unittest.TestCase):
    def test_something(self):
        dp = DataProvider()
        dp.get_by_id('451751')
        self.assertEqual(dp.get_by_id('451751'),{
        "geonameid": "451751",
        "name": "Zhitnikovo",
        "asciiname": "Zhitnikovo",
        "alternatenames": "",
        "latitude": "57.20064",
        "longitude": "34.57831",
        "feature_class": "P",
        "feature_code": "PPL",
        "country_code": "RU",
        "cc2": "",
        "admin1_code": "77",
        "admin2_code": "",
        "admin3_code": "",
        "admin4_code": "",
        "population": "0",
        "elevation": "",
        "dem": "198",
        "timezone": "Europe/Moscow",
        "modification_date": "2011-07-09"
        })


if __name__ == '__main__':
    unittest.main()
