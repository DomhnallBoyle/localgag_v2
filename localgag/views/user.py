from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from localgag.serializers import User as UserSerializer, Location as LocationSerializer
from localgag.models import User as UserModel, Location as LocationModel


@api_view(['GET'])
# @permission_classes((IsAdminUser,))
def get_users(request):
    data = [user.to_dict for user in UserModel.objects.all()]

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def get_user(request, user_id):
    try:
        user = UserModel.objects.get(pk=user_id)

        return Response(UserSerializer(user).data, status=HTTP_200_OK)
    except UserModel.DoesNotExist:
        return Response({'error': 'User not found.'}, status=HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
# @permission_classes((IsAuthenticated, ))
def delete_user(request, user_id):
    if request.user.id == user_id:
        try:
            UserModel.objects.filter(pk=user_id).delete()

            return Response(status=HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found.'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def update_user_location(request, user_id):
    if request.user.id == user_id:
        request.data['uuid'] = UserModel.objects.get(pk=user_id).location.uuid
        serializer = LocationSerializer(instance=LocationModel(**request.data), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
