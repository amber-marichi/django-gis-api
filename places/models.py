from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = "places"

    def __str__(self) -> str:
        return self.name
