from django.urls import path

from places.views import ListCreatePlaces, UpdateDeletePlace


urlpatterns = [
    path("", ListCreatePlaces.as_view(), name="place-list"),
    path(
        "<int:pk>/",
        UpdateDeletePlace.as_view(),
        name="place-update-delete"
    ),
]

app_name = "places"
