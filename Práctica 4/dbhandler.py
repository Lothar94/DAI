#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class RestaurantsDBHandler(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test.restaurants

    def find_borough(self, borough):
        cursor = self.db.find({"borough": borough})
        return cursor

    def find_cuisine(self, cuisine):
        cursor = self.db.find({"cuisine": cuisine})
        return cursor

    def find_name(self, name):
        cursor = self.db.find({"name": name})
        return cursor

    def find_ZIPcode(self, ZIPcode):
        cursor = self.db.find({"address":{ "zipcode": ZIPcode}})
        return cursor

    def find_address(self, street, building, ZIPcode):
        cursor = self.db.find({"address":{ "street": street, "building": building, "zipcode": ZIPcode}})
        return cursor

RestaurantsHandler = RestaurantsDBHandler()
