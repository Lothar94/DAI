#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class RestaurantsDBHandler(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test.restaurants

    def find_restaurant(self, key, value):
        cursor = self.db.find({key: value})
        return cursor

    def find_ZIPcode(self, ZIPcode):
        print(ZIPcode)
        cursor = self.db.find({"address.zipcode": ZIPcode})
        return cursor

    def find_address(self, street, building, ZIPcode):
        cursor = self.db.find({"address.street": street, "address.building": building, "address.zipcode": ZIPcode})
        return cursor

RestaurantsHandler = RestaurantsDBHandler()
