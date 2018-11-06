from django.db import transaction
from rest_framework import serializers
from localgag.models import User as UserModel, Comment as CommentModel


class Comment(serializers.ModelSerializer):
    """
       Serializer to map the Model instance into JSON format.
    """
    user = serializers.UUIDField(source='user.id', read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = CommentModel
        fields = ('uuid', 'user', 'message', 'votes')

    def create(self, validated_data):
        user = UserModel.objects.get(pk=self.context['user'])

        return CommentModel.objects.create(user=user, message=validated_data.get('message'))

    def update(self, instance, validated_data):
        comment = CommentModel.objects.get(pk=instance.uuid)
        comment.message = validated_data['message']
        comment.votes = validated_data['votes']
        comment.save()

        # with transaction.atomic():
        #     CommentModel.objects.select_for_update().filter(pk=instance.uuid).update(**validated_data)

        return comment
