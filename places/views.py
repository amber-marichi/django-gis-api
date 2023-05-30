from rest_framework import generics, mixins
from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from places.models import Place
from places.serializers import PlaceSerializer


def get_point_from_params(longitude, latitude):
    try:
        longitude_val = float(longitude)
        latitude_val = float(latitude)
    except (ValueError, TypeError):
        raise ValidationError(detail="Invalid Params")
    if not -180 <= longitude_val <= 180 or not -90 <= latitude_val <= 90:
        raise ValidationError(detail="Invalid Params")
    return Point(longitude_val, latitude_val, srid=4326)


class ListCreatePlaces(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        query = Place.objects.all()
        longitude = self.request.query_params.get("lng")
        latitude = self.request.query_params.get("lat")

        if latitude or longitude:
            point = get_point_from_params(longitude, latitude)
            query = (
                query.annotate(distance=Distance("geom", point))
                .order_by("distance")[:1]
            )

        return query

    @extend_schema(
        description=(
            "List all existing places by default. "
            "Get closest point by providing latitude and longitude "
            "as query parameters."
        ),
        parameters=[
            OpenApiParameter(
                name="lat",
                type=OpenApiTypes.STR,
                description="Enter latitude of point",
            ),
            OpenApiParameter(
                name="lng",
                type=OpenApiTypes.STR,
                description="Enter longitude of point",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Create new place with name, description and coordinates."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateDeletePlace(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    @extend_schema(
        description="Update existing place by ID"
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        description="Partially update existing place by ID"
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Delete existing place by ID"
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
