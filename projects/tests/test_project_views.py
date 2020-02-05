import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from projects.models import *

User = get_user_model()


class ProjectListAPIViewTestCase(APITestCase):
    url = reverse('projects:projects_list')

    def setUp(self):
        self.manager = User.objects.create(
            username="manager",
            user_type="Manager",
            email='sdfsdg@dgd.sf',
            password=make_password("1111"),
        )
        self.developer = User.objects.create(
            username="developer",
            user_type="Developer",
            password=make_password("1111"),
        )
        self.projects = []
        self.projects.append(Project.objects.create(title='abc',
                                                    description='asdasdasd',
                                                    ))
        self.projects.append(Project.objects.create(title='abcaade',
                                                    description='asdasdasd',
                                                    ))

        self.manager_token = Token.objects.create(user=self.manager)
        self.developer_token = Token.objects.create(user=self.developer)

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()
        for project in self.projects:
            project.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_view_list_without_login(self):
        response = self.client.get(self.url)
        content = json.loads(response.content).get("detail")
        self.assertTrue(content == "Authentication credentials were not provided.")

    def test_view_list_with_login_as_dev(self):
        self.api_authentication(self.developer_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get("count")
        self.assertTrue(content == len(self.projects))
        content = json.loads(response.content).get("results")[0].get("title")
        self.assertTrue(content == self.projects[0].title)

    def test_view_list_with_login_as_manager(self):
        self.api_authentication(self.manager_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get("count")
        self.assertTrue(content == len(self.projects))
        content = json.loads(response.content).get("results")[0].get("title")
        self.assertTrue(content == self.projects[0].title)


class ProjectCreateAPIViewTestCase(APITestCase):
    url = reverse('projects:create_project')

    def setUp(self):
        self.manager = User.objects.create(
            username="manager",
            user_type="Manager",
            email='sdfsdg@dgd.sf',
            password=make_password("1111"),
        )
        self.developer = User.objects.create(
            username="developer",
            user_type="Developer",
            password=make_password("1111"),
        )

        self.manager_token = Token.objects.create(user=self.manager)
        self.developer_token = Token.objects.create(user=self.developer)

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_project_as_dev_or_as_anonymous(self):
        response = self.client.post(self.url, {'title': 'test title',
                                               'description': 'test description',
                                               'members': self.developer})
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == 'Authentication credentials were not provided.')
        self.api_authentication(self.developer_token)
        response = self.client.post(self.url, {'title': 'test title',
                                               'description': 'test description',
                                               'members': self.developer})
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == 'You do not have permission to perform this action.')

    def test_create_project_as_manager(self):
        self.api_authentication(self.manager_token)
        response = self.client.post(self.url, {'title': 'test title',
                                               'description': 'test description',
                                               'members': self.developer.id})
        content = json.loads(response.content).get('title')
        self.assertTrue(content == 'test title')


class ProjectDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.manager = User.objects.create(
            username="manager",
            user_type="Manager",
            email='sdfsdg@dgd.sf',
            password=make_password("1111"),
        )
        self.another_manager = User.objects.create(
            username="another_manager",
            user_type="Manager",
            email='sdfs123dg@dgd.sf',
            password=make_password("1111"),
        )
        self.developer = User.objects.create(
            username="developer",
            user_type="Developer",
            password=make_password("1111"),
        )
        self.project = Project.objects.create(title='test project',
                                                    description='asdasdasd',
                                              )
        self.project.members.set((self.manager.id, self.developer.id))
        self.manager_token = Token.objects.create(user=self.manager)
        self.developer_token = Token.objects.create(user=self.developer)
        self.another_manager_token = Token.objects.create(user=self.another_manager)

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()
        self.another_manager.delete()
        self.another_manager_token.delete()
        self.project.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_view_or_change_project_as_not_member(self):
        url = reverse('projects:project_details', kwargs={'pk': self.project.id})
        self.api_authentication(self.another_manager_token)
        response = self.client.get(url)
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == 'You do not have permission to perform this action.')
        response = self.client.put(url, {'title': 'wrong',
                                         'description': 'test description', })
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == 'You do not have permission to perform this action.')

    def test_view_project_as_member(self):
        url = reverse('projects:project_details', kwargs={'pk': self.project.id})
        self.api_authentication(self.developer_token)
        response = self.client.get(url)
        content = json.loads(response.content).get('title')
        self.assertTrue(content == 'test project')

    def test_change_project_as_manager(self):
        url = reverse('projects:project_details', kwargs={'pk': self.project.id})
        self.api_authentication(self.manager_token)
        response = self.client.put(url, {'title': 'changed title',
                                         'description': 'wrong description',
                                         'status': 'Closed',
                                         'members': [self.manager.id, ]})
        content = json.loads(response.content).get('title')
        self.assertTrue(content == 'changed title')

    def test_change_project_as_developer(self):
        url = reverse('projects:project_details', kwargs={'pk': self.project.id})
        self.api_authentication(self.developer_token)
        response = self.client.put(url, {'title': 'changed title',
                                         'description': 'wrong description',
                                         'status': 'Closed',
                                         'members': [self.manager.id, ]})
        content = json.loads(response.content).get('detail')
        self.assertTrue(content == 'You do not have permission to perform this action.')
