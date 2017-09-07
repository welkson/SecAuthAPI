# from django.urls import reverse
# from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.test import APITestCase
from SecAuthAPI.Core.models import Policy
from django.contrib.auth.models import User


class PolicyTests(APITestCase):
    def setUp(self):
        # create admin user
        username = "admin"
        password = "Test1234"
        user = User.objects.create_superuser(username, 'test@mail.com', password)

        # API Auth
        self.client.login(username=user.username, password=password)

    def test_add_policy(self):
        """
        Ensure we can create a new policy object
        """
        data = {'description': 'Policy TestCase', 'policy': 'Test XACML'}   # TODO: xacml content in field "policy"

        # testcase
        response = self.client.post("/policy/", data, format='json')
        print "\n[Response] \n%s \n[End Response]\n" % response

        # response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.coun(), 1)
        self.assertEqual(Policy.objects.get().description, 'Policy TestCase')
