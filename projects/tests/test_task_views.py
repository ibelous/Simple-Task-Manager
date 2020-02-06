import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from projects.models import *

User = get_user_model()


class TasksListAPIViewTestCase(APITestCase):

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
            email="test@sdsf.com",
            password=make_password("1111"),
        )
        self.other_manager = User.objects.create(
            username="other_manager",
            user_type="Manager",
            email='othermail@bsu.by',
            password=make_password("1111"),
        )
        self.project = Project.objects.create(title='abc',
                                                    description='asdasdasd',
                                              )
        self.project.members.set((self.manager, self.developer))
        self.task = Task.objects.create(title='task',
                                        developer=self.developer,
                                        description='task descr',
                                        due_date=datetime.date.today()+datetime.timedelta(days=7),
                                        project=self.project)
        self.manager_token = Token.objects.create(user=self.manager)
        self.other_manager_token = Token.objects.create(user=self.other_manager)
        self.developer_token = Token.objects.create(user=self.developer)
        self.url = reverse('projects:tasks_list', kwargs={'project_id': self.project.id})

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()
        self.other_manager.delete()
        self.other_manager_token.delete()
        self.project.delete()
        self.task.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_view_list_without_login(self):

        response = self.client.get(self.url)
        content = json.loads(response.content).get("detail")
        self.assertTrue(content == "Authentication credentials were not provided.")

    def test_view_list_with_login_as_dev_in_project(self):
        self.api_authentication(self.developer_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get("count")
        self.assertTrue(content == 1)
        content = json.loads(response.content).get("results")[0].get("title")
        self.assertTrue(content == self.task.title)

    def test_view_list_with_login_as_manager_not_in_project(self):
        self.api_authentication(self.other_manager_token)
        response = self.client.get(self.url)
        content = json.loads(response.content).get("detail")
        self.assertTrue(content == 'You do not have permission to perform this action.')


class CreateTaskAPIViewTestCase(APITestCase):

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
            email="test@sdsf.com",
            password=make_password("1111"),
        )
        self.other_manager = User.objects.create(
            username="other_manager",
            user_type="Manager",
            email='othermail@bsu.by',
            password=make_password("1111"),
        )
        self.other_developer = User.objects.create(
            username="other_developer",
            user_type="Developer",
            email="testdev@sdsf.com",
            password=make_password("1111"),
        )
        self.project = Project.objects.create(title='abc',
                                                    description='asdasdasd',
                                              )
        self.project.members.set((self.manager, self.developer))
        self.manager_token = Token.objects.create(user=self.manager)
        self.other_manager_token = Token.objects.create(user=self.other_manager)
        self.developer_token = Token.objects.create(user=self.developer)
        self.other_developer_token = Token.objects.create(user=self.other_developer)
        self.url = reverse('projects:create_task', kwargs={'project_id': self.project.id})

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()
        self.other_manager.delete()
        self.other_manager_token.delete()
        self.project.delete()
        self.other_developer.delete()
        self.other_developer_token.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_task_as_manager_in_project(self):
        self.api_authentication(self.manager_token)
        response = self.client.post(self.url, {'title': 'task',
                                               'developer': self.developer.id,
                                               'description': 'task descr',
                                               'due_date': datetime.date.today()+datetime.timedelta(days=7),
                                               'project': self.project})
        content = json.loads(response.content).get("title")
        self.assertTrue(content == 'task')

    def test_create_task_as_manager_with_manager_as_developer(self):
        self.api_authentication(self.manager_token)
        response = self.client.post(self.url, {'title': 'task',
                                               'developer': self.manager.id,
                                               'description': 'task descr',
                                               'due_date': datetime.date.today() + datetime.timedelta(days=7),
                                               'project': self.project})
        content = json.loads(response.content).get("non_field_errors")[0]
        self.assertTrue(content == 'Assigned user must be developer.')

    def test_create_task_as_manager_with_developer_not_in_project_as_developer(self):
        self.api_authentication(self.manager_token)
        response = self.client.post(self.url, {'title': 'task',
                                               'developer': self.other_developer.id,
                                               'description': 'task descr',
                                               'due_date': datetime.date.today() + datetime.timedelta(days=7),
                                               'project': self.project})
        content = json.loads(response.content).get("non_field_errors")[0]
        self.assertTrue(content == 'Assigned user must be project member.')

    def create_task_as_manager_not_in_project(self):
        self.api_authentication(self.other_manager_token)
        response = self.client.post(self.url, {'title': 'task',
                                               'developer': self.developer.id,
                                               'description': 'task descr',
                                               'due_date': datetime.date.today()+datetime.timedelta(days=7),
                                               'project': self.project})
        content = json.loads(response.content).get("detail")
        self.assertTrue(content == 'You do not have permission to perform this action.')


class TaskDetailAPIViewTestCase(APITestCase):

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
            email="test@sdsf.com",
            password=make_password("1111"),
        )
        self.other_manager = User.objects.create(
            username="other_manager",
            user_type="Manager",
            email='othermail@bsu.by',
            password=make_password("1111"),
        )
        self.project = Project.objects.create(title='abc',
                                                    description='asdasdasd',
                                              )
        self.task = Task.objects.create(title='task',
                                        developer=self.developer,
                                        description='task descr',
                                        due_date=datetime.date.today() + datetime.timedelta(days=7),
                                        project=self.project)
        self.project.members.set((self.manager, self.developer))
        self.manager_token = Token.objects.create(user=self.manager)
        self.other_manager_token = Token.objects.create(user=self.other_manager)
        self.developer_token = Token.objects.create(user=self.developer)
        self.url = reverse('projects:task_details', kwargs={'project_id': self.project.id,
                                                            'pk': self.task.id})

    def tearDown(self):
        self.developer.delete()
        self.developer_token.delete()
        self.manager.delete()
        self.manager_token.delete()
        self.other_manager.delete()
        self.other_manager_token.delete()
        self.project.delete()
        self.task.delete()

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_change_task_as_manager_and_project_member(self):
        self.api_authentication(self.manager_token)
        response = self.client.put(self.url, {'title': 'changed title',
                                              'developer': self.developer.id,
                                              'description': 'changed task descr',
                                              'due_date': datetime.date.today() + datetime.timedelta(days=7),
                                              'project': self.project})
        content = json.loads(response.content).get("title")
        self.assertTrue(content == 'changed title')

    def test_change_task_as_manager_and_not_project_member(self):
        self.api_authentication(self.other_manager_token)
        response = self.client.put(self.url, {'title': 'changed title',
                                              'developer': self.developer.id,
                                              'description': 'changed task descr',
                                              'due_date': datetime.date.today() + datetime.timedelta(days=7),
                                              'project': self.project})
        content = json.loads(response.content).get("detail")
        self.assertTrue(content == 'You do not have permission to perform this action.')

    def test_change_task_as_assigned_developer(self):
        self.api_authentication(self.developer_token)
        response = self.client.put(self.url, {'title': 'changed title',
                                              'developer': self.developer.id,
                                              'description': 'changed task descr',
                                              'status': 'In progress',
                                              'due_date': datetime.date.today() + datetime.timedelta(days=7),
                                              'project': self.project})
        content = json.loads(response.content)[0]
        self.assertTrue(content == 'You can change only task status as developer.')
        response = self.client.put(self.url, {'title': 'task',
                                              'description': 'task descr',
                                              'status': 'In progress',
                                              })
        content = json.loads(response.content).get('status')
        self.assertTrue(content == 'In progress')
