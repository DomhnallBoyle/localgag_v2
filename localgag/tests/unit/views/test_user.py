from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APITestCase, APIRequestFactory

from localgag.views import create_user


class TestUser(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_user_200_OK(self):
        data = {
            'username': 'User123',
            'password': 'Password123',
            'number': '+441234567890'
        }
        request = self.factory.post('/users', data, format='json')
        response = create_user(request)

        self.assertEquals(response.status_code, HTTP_201_CREATED)
