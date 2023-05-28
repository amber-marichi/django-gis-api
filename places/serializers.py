from rest_framework import serializers

from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(
        source="distance.km",
        max_digits=10,
        decimal_places=2,
        required=False,
        read_only=True
    )

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom", "distance")

    def validate_geom(self, value):
        if not -90 <= value.y <= 90:
            raise serializers.ValidationError("invalid latitude in coordinates")
        if not -180 <= value.x <= 180:
            raise serializers.ValidationError("invalid longitude in coordinates")
        return value
