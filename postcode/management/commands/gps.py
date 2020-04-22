import time

import requests
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.utils.http import urlencode

from postcode.models import Postcode


class Command(BaseCommand):
    help = 'Tries to fetch GPS location for a postcode'

    def handle(self, *args, **options):
        osm_url = 'https://nominatim.openstreetmap.org/search'
        for postcode in Postcode.objects.filter(active=True, location__isnull=True):
            query = dict(
                country="dk",
                postalcode=postcode.postcode,
                format="geojson"
            )
            full_url = f"{osm_url}?{urlencode(query)}"
            res = requests.get(full_url)
            try:
                coordinates = res.json().get('features')[0].get('geometry').get('coordinates')
                pnt = Point(coordinates)
                postcode.location = pnt
                self.stdout.write(self.style.SUCCESS('Fetched data for "%s"' % postcode.postcode))
            except Exception as ex:
                postcode.active = False
                self.stdout.write(self.style.ERROR('Unable to fetch data for "%s"' % postcode.postcode))
                self.stdout.write(self.style.ERROR(' Exception: "%s"' % ex))
            postcode.save()
            time.sleep(2)

        self.stdout.write(self.style.SUCCESS('Successfully fetched data for all postcodes'))