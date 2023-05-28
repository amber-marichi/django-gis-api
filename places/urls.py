from django.urls import path

from places.views import ListCreatePlaces


urlpatterns = [
    path("", ListCreatePlaces.as_view(), name="places-list"),
]

app_name = "places"
