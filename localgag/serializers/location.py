from rest_framework import serializers
from localgag.models import Location as LocationModel


class Location(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = LocationModel
        fields = ('uuid', 'country', 'region', 'latitude', 'longitude')

    def update(self, instance, validated_data):
        LocationModel.objects.filter(pk=instance.uuid).update(**validated_data)

        return instance

    # def validate(self, attrs):
    #     uuid = attrs.get('uuid')
    #     if not LocationModel.objects.filter(pk=uuid).exists():
    #         raise serializers.ValidationError('Location object does not exist.')
    #
    #     return attrs
