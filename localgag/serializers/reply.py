from rest_framework import serializers

from localgag.models import Reply as ReplyModel, Status as StatusModel
from localgag.serializers import Comment as CommentSerializer, Status as StatusSerializer


class Reply(serializers.Serializer):

    uuid = serializers.UUIDField(read_only=True)
    status = StatusSerializer(read_only=True)
    comment = CommentSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = ReplyModel
        fields = ('uuid', 'status', 'comment')

    def create(self, validated_data):
        comment_serializer = CommentSerializer(data=validated_data.get('comment'))
        if comment_serializer.is_valid():
            validated_data['comment'] = comment_serializer.save()

        return ReplyModel.objects.create(**validated_data)

    def validate(self, attrs):
        qs = StatusModel.objects.filter(pk=self.context['status_id'])

        if qs.exists():
            attrs['status'] = qs.first()
        else:
            raise serializers.ValidationError('Status object does not exist.')

        if 'reply_id' in self.context:
            qs = ReplyModel.objects.filter(pk=self.context['reply_id'])

            if qs.exists():
                attrs['_reply'] = qs.first()
            else:
                raise serializers.ValidationError('Reply object does not exist.')

        return attrs

    def to_representation(self, instance):
        self.fields['_reply'] = Reply(read_only=True)

        return super(Reply, self).to_representation(instance)
