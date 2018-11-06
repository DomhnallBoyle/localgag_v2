from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from localgag.helpers.haversine import calculate_distance
from localgag.models import Status as StatusModel, User as UserModel
from localgag.serializers import Reply as ReplySerializer, Status as StatusSerializer


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def get_status(request, status_id):
    try:
        status = StatusModel.objects.get(pk=status_id)

        return Response(StatusSerializer(status).data, status=HTTP_200_OK)
    except StatusModel.DoesNotExist:
        return Response({'error': 'Status not found.'}, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def get_statuses(request):
    user = UserModel.objects.get(pk=request.user.id)

    statuses = []
    for status in StatusModel.objects.filter(location__country=user.location.country,
                                             location__region=user.location.region):
        distance = calculate_distance(status.latitude, status.longitude, user.latitude, user.longitude)
        if distance <= user.radius:
            statuses.append(StatusSerializer(status).data)

    return Response(statuses, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def create_status(request):
    serializer = StatusSerializer(data=request.data, context={"user": request.user.id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes((IsAuthenticated, ))
def delete_status(request, status_id):
    status = StatusModel.objects.get(pk=status_id)
    if request.user.id == status.comment.user.id:
        try:
            status.delete()

            return Response(status=HTTP_200_OK)
        except StatusModel.DoesNotExist:
            return Response({'error': 'Status not found.'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def reply_to_status(request, status_id):
    serializer = ReplySerializer(data=request.data, context={'status_id': status_id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
