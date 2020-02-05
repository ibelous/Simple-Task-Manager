import json

from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class UserRegistrationAPIViewTest(APITestCase):
    url = reverse('users:registration')

    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "user_type": "Manager",
            "password": "1111",
            "confirm_password": "1111",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_invalid_password(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "user_type": "Developer",
            "password": "1111",
            "confirm_password": "INVALID",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("users:login")

    def setUp(self):
        self.username = "testuser"
        self.password = "1111"
        self.user_type = "Developer"
        self.email = "asfsdf@sdgd.sdcs"
        self.user = User(
            username=self.username,
            user_type=self.user_type,
            email=self.email,
        )
        self.user.set_password(self.password)
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()
        self.token.delete()

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "testuser"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        user_data = {"username": self.username, "password": "INVALID"}
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in content)
        self.assertEqual(content["token"], self.token.key)


class UserListAPIViewTestCase(APITestCase):
    url = reverse('users:users_list')

    def setUp(self):
        self.manager = User.objects.create(
            username="manager",
            user_type="Manager",
            email="sfsdf@sdfds.com",
            password=make_password("1111"),
        )
        self.developer = User.objects.create(
            username="developer",
            user_type="Developer",
            email="sdfsdg@sdgsdx.xcs",
            password=make_password("1111"),
        )
        self.developer_token = Token.objects.create(user=self.developer)
        self.manager_token = Token.objects.create(user=self.manager)

    def tearDown(self):
        self.developer.delete()
        self.manager.delete()
        self.developer_token.delete()
        self.manager_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_by_developer(self):
        self.api_authentication(self.developer_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == "You do not have permission to perform this action.")

    def test_get_by_manager(self):
        self.api_authentication(self.manager_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get("count")
        self.assertTrue(content == 2)


class UserDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.manager = User.objects.create(
            username="manager",
            user_type="Manager",
            email="sfsdf@sdfds.com",
            password=make_password("1111"),
        )
        self.developer = User.objects.create(
            username="developer",
            user_type="Developer",
            email="sdfsdg@sdgsdx.xcs",
            password=make_password("1111"),
        )
        self.another_manager = User.objects.create(
            username="manager1",
            user_type="Manager",
            email="sfsd12f@sdfds.com",
            password=make_password("1111"),
        )
        self.developer_token = Token.objects.create(user=self.developer)
        self.manager_token = Token.objects.create(user=self.manager)
        self.another_manager_token = Token.objects.create(user=self.another_manager)

    def tearDown(self):
        self.developer.delete()
        self.manager.delete()
        self.another_manager.delete()
        self.another_manager_token.delete()
        self.developer_token.delete()
        self.manager_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_change_dev_by_itself(self):
        url = reverse('users:user_details', kwargs={'pk': User.objects.all()[1].id})
        self.api_authentication(self.developer_token)
        response = self.client.get(url)
        content = json.loads(response.content).get('username')
        self.assertTrue(content == "developer")
        response = self.client.put(url, {'username': 'dev1',
                                              'email': self.developer.email,
                                              'user_type': self.developer.user_type,
                                              'password': self.developer.password})
        content = json.loads(response.content).get('username')
        self.assertTrue(content == "dev1")

    def test_get_manager_by_dev(self):
        url = reverse('users:user_details', kwargs={'pk': User.objects.all()[0].id})
        self.api_authentication(self.developer_token)
        response = self.client.get(url)
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == "You do not have permission to perform this action.")

    def test_get_and_change_dev_by_manager(self):
        url = reverse('users:user_details', kwargs={'pk': User.objects.all()[1].id})
        self.api_authentication(self.manager_token)
        response = self.client.get(url)
        content = json.loads(response.content).get('username')
        self.assertTrue(content == "developer")
        response = self.client.put(url, {'username': 'dev1',
                                         'email': self.developer.email,
                                         'user_type': self.developer.user_type,
                                         'password': self.developer.password})
        content = json.loads(response.content).get('username')
        self.assertTrue(content == "dev1")
