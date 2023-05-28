from rest_framework import serializers

from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")

    def validate_geom(self, value):
        if not -90 <= value.y <= 90:
            raise serializers.ValidationError("invalid latitude in coordinates")
        if not -180 <= value.x <= 180:
            raise serializers.ValidationError("invalid longitude in coordinates")
        return value
