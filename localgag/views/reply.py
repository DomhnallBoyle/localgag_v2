from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_401_UNAUTHORIZED

from localgag.models import Reply as ReplyModel
from localgag.serializers import Reply as ReplySerializer


@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def get_replies(request):
    pass


@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def reply_to_reply(request, reply_id):
    status_id = ReplyModel.objects.get(pk=reply_id).status.uuid
    serializer = ReplySerializer(data=request.data, context={'status_id': status_id, 'reply_id': reply_id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes((IsAuthenticated, ))
def delete_reply(request, reply_id):
    reply = ReplyModel.objects.get(pk=reply_id)
    if request.user.id == reply.comment.user.id:
        try:
            reply.delete()

            return Response(status=HTTP_200_OK)
        except ReplyModel.DoesNotExist:
            return Response({'error': 'Reply not found.'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
