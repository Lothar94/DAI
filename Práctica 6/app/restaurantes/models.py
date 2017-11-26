from django.db import models
from pymongo import MongoClient

client = MongoClient()
db = client.test
restaurants = db.restaurants

# Create your models here.
