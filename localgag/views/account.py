from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework_jwt.views import ObtainJSONWebToken

from localgag.helpers.email import EmailClient
from localgag.helpers.verification import create_verification_code
from localgag.models import User as UserModel


class Account(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        if UserModel.objects.get(username=request.data['username']).is_verified:
            return super(Account, self).post(request, args, kwargs)
        else:
            return Response({'error': 'Please verify your account before logging in.'}, status=HTTP_401_UNAUTHORIZED)


login = Account.as_view()


@api_view(['POST'])
def send_code(request):
    username = request.data.get('username', None)
    if username:
        try:
            verification_code = create_verification_code()
            user = UserModel.objects.get(username=username)
            user.verification_code = verification_code
            user.save()

            email_client = EmailClient()
            email_client.send_email(user.email, verification_code)

            return Response({'message': 'Verification code sent.'}, status=HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found.'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You must supply a username.'}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify(request):
    username = request.data.get('username', None)
    verification_code = request.data.get('verification_code', None)
    if username and verification_code:
        try:
            user = UserModel.objects.get(username=username)
            if user.verification_code == verification_code:
                user.is_verified = True
                user.save()

                return Response({'message': 'Successfully verified'}, status=HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code.'}, status=HTTP_400_BAD_REQUEST)

        except UserModel.DoesNotExist:
            return Response({'error': 'User not found.'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You must supply a username and verification code.'}, status=HTTP_400_BAD_REQUEST)
