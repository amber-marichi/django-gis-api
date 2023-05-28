from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from places.models import Place
from places.serializers import PlaceSerializer


class ListCreatePlaces(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        query = Place.objects.all()
        longitude = self.request.query_params.get("lng")
        latitude = self.request.query_params.get("lat")

        if latitude and longitude:
            try:
                pnt = Point(float(longitude), float(latitude), srid=4326)
            except ValueError:
                raise ValidationError(detail="Invalid Params")
            query = query.annotate(distance=Distance("geom", pnt)).order_by("distance")[:1]

        return query

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lat",
                type=OpenApiTypes.STR,
                description="Enter latitude of coordinates",
            ),
            OpenApiParameter(
                name="lng",
                type=OpenApiTypes.STR,
                description="Enter longitude of coordinates",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
