import random
from django.contrib.gis.geos import Point
from factory.fuzzy import BaseFuzzyAttribute

class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0),
                     random.uniform(-90.0, 90.0))
