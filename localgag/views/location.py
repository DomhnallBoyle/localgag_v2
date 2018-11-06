from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.response import Response
from localgag.models import Location as LocationModel
from localgag.serializers import Location as LocationSerializer

