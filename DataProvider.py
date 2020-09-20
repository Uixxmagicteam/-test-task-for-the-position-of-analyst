import csv
from os import path


class DataProvider:
    """
    работа с дата-файлом
    """
    geonames = dict()
    geonames_sorted = []

    def __init__(self):
        with open(path.join(path.dirname(path.realpath(__file__)), 'RU.txt'), newline="", encoding='utf-8') as geonametable:
            geonames_list = csv.reader(geonametable, delimiter="\t")
            for item in geonames_list:
                parsed_item = self.parse_geo_item(item)
                self.geonames[item[0]] = parsed_item
                self.geonames_sorted.append(parsed_item)

            self.geonames_sorted.sort(key=lambda item: item.get('geonameid'))

    def parse_geo_item(self, raw_item):
        return {
            "geonameid": raw_item[0],
            "name": raw_item[1],
            "asciiname": raw_item[2],
            "alternatenames": raw_item[3],
            "latitude": raw_item[4],
            "longitude": raw_item[5],
            "feature_class": raw_item[6],
            "feature_code": raw_item[7],
            "country_code": raw_item[8],
            "cc2": raw_item[9],
            "admin1_code": raw_item[10],
            "admin2_code": raw_item[11],
            "admin3_code": raw_item[12],
            "admin4_code": raw_item[13],
            "population": raw_item[14],
            "elevation": raw_item[15],
            "dem": raw_item[16],
            "timezone": raw_item[17],
            "modification_date": raw_item[18],
        }

    # задание 1
    def get_by_id(self, id: str):
        return self.geonames.get(id)

    def get_page(self, page_size: int, page: int):
        return self.geonames_sorted[(page_size * page):(page_size * page + page_size):1]

    """
            у нас есть длина страницы и номер страницы, нужно вывести нужную страницу, для значений
            page_size=100, page=3 нужно вывести элементы из self.geonames_sorted с индексами от 300, до 400
            :param page_size: количество элементов на странице
            :param page: номер страницы
            :return:
          """




    def find_city_by_name(self, name: str):
        suitable_cities = []
        for entry in self.geonames_sorted:
            alternatenames = entry['alternatenames'].split(',')
            if name in alternatenames:
                suitable_cities.append(entry)

        if len(suitable_cities) == 0:
            raise Exception('City not found')

        popsorted_city = [(sorted(suitable_cities, key=lambda x: x['population'])[-1])]
        # TODO: select with higher pops
        return popsorted_city


    def compare_cities(self, city_1, city_2):

        city_1 = self.find_city_by_name(city_1)
        city_2 = self.find_city_by_name(city_2)
        c1=city_1[0]
        c2=city_2[0]
        if c1['latitude'] > c2['latitude'] and c1['timezone'] == c2['timezone']:
            return c1 + "Севернее и временная зона одинаковая"
        elif c1['latitude'] > c2['latitude'] and c1['timezone'] != c2['timezone']:
            return c1 + "Севернее и временная зона разная"
        elif c1['latitude'] < c2['latitude'] and c1['timezone'] == c2['timezone']:
            return c2 + "Севернее и временная зона одинаковая"
        elif c1['latitude'] < c2['latitude'] and c1['timezone'] != c2['timezone']:
            return c2 + "Севернее и временная зона разная"
        else:
            return "compare error"
