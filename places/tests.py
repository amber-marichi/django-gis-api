from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Point

from places.models import Place
from places.serializers import PlaceSerializer


URL_LIST_CREATE = reverse("places:place-list")

class PlaceTests(APITestCase):
    def setUp(self):
        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom=Point(1, 1)
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom=Point(2, 2)
        )

    def test_list_places(self):
        response = self.client.get(URL_LIST_CREATE)
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_place_valid_point(self):
        data = {
            "name": "New Place",
            "description": "New Description",
            "geom": {"type": "Point", "coordinates": [3, 3]},
        }
        response = self.client.post(URL_LIST_CREATE, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)
        self.assertEqual(Place.objects.latest("id").name, "New Place")

    def test_create_place_invalid_point(self):
        data = {
            "name": "New Place",
            "description": "New Description",
            "geom": {"type": "Point", "coordinates": [181, 30]},
        }
        response = self.client.post(URL_LIST_CREATE, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_place(self):
        data = {
            "name": "Updated Place",
            "description": "Updated Description",
            "geom": {"type": "Point", "coordinates": [4, 4]},
        }
        response = self.client.put(
            reverse("places:place-update-delete", args=[self.place1.id]),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place1.refresh_from_db()
        self.assertEqual(self.place1.name, "Updated Place")

    def test_delete_place(self):
        response = self.client.delete(
            reverse("places:place-update-delete", args=[self.place1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)


class PlaceDistanceTests(APITestCase):
    def setUp(self):
        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom=Point(1, 1)
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom=Point(2, 2)
        )

    def test_get_place_with_valid_params(self):
        query_params = {"lat": "1", "lng": "1"}
        response = self.client.get(URL_LIST_CREATE, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["distance"], "0.00")

    def test_get_error_with_invalid_params(self):
        query_params = {"lat": "ab", "lng": "1"}
        response = self.client.get(URL_LIST_CREATE, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
