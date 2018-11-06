from rest_framework import serializers
from rest_framework.decorators import authentication_classes

from localgag.models import Status as StatusModel
from localgag.serializers import Comment as CommentSerializer, Location as LocationSerializer


class Status(serializers.Serializer):
    """Serializer to map the Model instance into JSON format."""
    uuid = serializers.UUIDField(read_only=True)
    comment = CommentSerializer()
    location = LocationSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StatusModel
        fields = ('comment', 'location')

    def create(self, validated_data):
        comment_serializer = CommentSerializer(data=validated_data.get('comment'),
                                               context={'user': self.context['user']})
        if comment_serializer.is_valid():
            validated_data['comment'] = comment_serializer.save()

        location_serializer = LocationSerializer(data=validated_data.get('location'))
        if location_serializer.is_valid():
            validated_data['location'] = location_serializer.save()

        return StatusModel.objects.create(**validated_data)
