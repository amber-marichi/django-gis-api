from rest_framework import generics

from places.models import Place
from places.serializers import PlaceSerializer


class ListCreatePlaces(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
