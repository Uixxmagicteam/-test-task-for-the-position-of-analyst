import csv
import datetime
import math
from os import path

import pytz


class DataProvider:

    """ Работа с дата-файлом """

    geonames = dict()
    geonames_sorted = []

    def __init__(self):
        with open(path.join(path.dirname(path.realpath(__file__)), 'RU.txt'), newline="",
                  encoding='utf-8') as geonametable:
            geonames_list = csv.reader(geonametable, delimiter="\t")
            for item in geonames_list:
                parsed_item = self.parse_geo_item(item)
                self.geonames[item[0]] = parsed_item
                self.geonames_sorted.append(parsed_item)

            self.geonames_sorted.sort(key=lambda item: int(item.get('geonameid')))


    def parse_geo_item(self, raw_item):
        """Оформление информации о городе в виде словаря"""
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

    def get_by_id(self, id: str):
        """ Принимаем geonameid и возвращаем информацию о городе """
        return self.geonames.get(id)

    def get_page(self, page_size: int, page: int):
        """Пагинация: принимаем размер страницы и номер страницы - возвращаем информацию о городах """
        cursor = page_size * page
        return self.geonames_sorted[cursor:(cursor + page_size)]

    def find_city_by_name(self, name: str):
        """Находим город по названию на русском языке,
            если города с одинаковым названием, выбираем с наибольшим количеством населения"""
        suitable_cities = []
        for entry in self.geonames_sorted:
            alternatenames = entry['alternatenames'].split(',')
            if name in alternatenames:
                suitable_cities.append(entry)

        if len(suitable_cities) == 0:
            raise Exception('City not found')

        popsorted_city = (sorted(suitable_cities, key=lambda x: x['population'])[-1])
        return popsorted_city

    def compare_cities(self, city_1, city_2):
        """Принимаем название двух городов и выводим информацию о городах,
            который из них севернее, какая разница во времени в часах"""

        c1 = self.find_city_by_name(city_1)
        c2 = self.find_city_by_name(city_2)

        response = {
            'city_1': c1,
            'city_2': c2,
            'northest': None,
            'is_same_timezone': None,
            'timezone_delta': None
        }

        if c1['latitude'] > c2['latitude']:
            response['northest'] = c1
        elif c1['latitude'] == c2['latitude']:
            response['northest'] = 'c1 and c2 have latitude the same'
        else:
            response['northest'] = c2

        response['is_same_timezone'] = c1['timezone'] == c2['timezone']

        response['timezone_delta'] = self.get_timezone_diff(c1['timezone'], c2['timezone'])
        return response

    def autocomplete(self, symbols: str):
        """Принимаем от пользователя часть названия города, на русском или английском языке,
            возвращаем список с возможными вариантами продолжения"""
        limit = 10 # Изменяемая возможность ограничить количество выдаваемых подсказок
        possible_results = []
        for geoitem in self.geonames_sorted:
            if len(possible_results) >= limit: break
            supstr1 = geoitem['alternatenames'].replace(',', '')
            if symbols in supstr1:
                names = geoitem['alternatenames'].split(',')
                for item in names:
                    if symbols in item:  # Можно использовать startswith(str).
                        possible_results.append(item)
        return sorted(possible_results[:limit])

    def get_timezone_diff(self, tz1: str, tz2: str):
        """Определяем по модулю часовую разницу в двух городах, находящихся в разных временных зонах"""
        dt1 = datetime.datetime.now(pytz.timezone(tz1))
        offset1 = dt1.utcoffset().total_seconds() / 3600

        dt2 = datetime.datetime.now(pytz.timezone(tz2))
        offset2 = dt2.utcoffset().total_seconds() / 3600

        return math.fabs(offset1 - offset2)  # Берем абсолютное значение
