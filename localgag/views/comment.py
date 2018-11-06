from django.db import transaction
from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from localgag.models import Comment as CommentModel, User as UserModel
from localgag.serializers import Comment as CommentSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_comment(request, comment_id):
    comment = CommentModel.objects.get(pk=comment_id)
    if request.user.id == comment.user.id:
        serializer = CommentSerializer(instance=comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
