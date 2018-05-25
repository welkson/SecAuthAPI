# from django.urls import reverse
# from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.test import APITestCase
from SecAuthAPI.Core.ModelMapper import *
from SecAuthAPI.Core.models import Policy
from django.contrib.auth.models import User
from SecAuthAPI import settings
from SecAuthAPI.Core.xacml_util import XacmlUtil


class PolicyTests(APITestCase):
    def setUp(self):
        # create admin user
        username = "admin"
        password = "Test1234"
        user = User.objects.create_superuser(username, 'test@mail.com', password)

        # disable authorization server integration (test only SecAuthAPI internal storage and manipulation)
        settings.as_product = 0

        # API Auth
        self.client.login(username=user.username, password=password)

        # sample policy
        with open('extra/Policy/NewTicketOnlySupport.xml', 'r') as xacml_file:
            xacml_policy = xacml_file.read()

        # policy data
        data = {'description': 'New Ticket Only Support', 'name': 'NewTicketOnlySupport', 'content': xacml_policy}

        # testcase 1 (add policy)
        response = self.client.post("/policy/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 1)
        self.assertEqual(Policy.objects.get().name, 'NewTicketOnlySupport')

        # testcase 2 (policy existing)
        response = self.client.post("/policy/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_1_modify_policy(self):
        """
        Ensure we can modify a existing policy
        """

        print "\nTesting method modify_policy()..."

        # change "role" attribute (from "support" to "admin")
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        policy.policy.properties.get('Version').value = "2.0"
        new_policy = policy.policy.toXML()

        # policy data
        data = {'description': 'New Ticket Only Support', 'name': 'NewTicketOnlySupport', 'content': new_policy}

        # testcase 1 (modify policy)
        response = self.client.put("/policy/%s/" % policy.get_policy_name(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 1)

        # test attribute value
        policytest = XacmlUtil(content=Policy.objects.all()[0].content)
        self.assertEqual(policytest.policy.properties.get('Version').value, '2.0')

        # testcase 2 (policy inexistent)
        response = self.client.put("/policy/inexistent_policy/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_2_delete_policy(self):
        """
        Ensure we can delete a existing policy
        """

        print "\nTesting method delete_policy()..."

        # policy data
        policy_name = Policy.objects.all()[0].name

        # testcase 1 (delete policy)
        response = self.client.delete("/policy/%s/" % policy_name, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 0)

        # testcase 2 (policy inexistent)
        response = self.client.delete("/policy/inexistent_policy/", {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_3_add_attribute(self):
        """
        Ensure we can add an attribute in an existing policy
        """

        print "\nTesting method add_attribute()..."

        # policy data
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        policy_name = policy.get_policy_name()
        rule_name = policy.policy.rules[0].properties.get('RuleId').value

        # new attribute properties
        new_attribute_name1 = "http://ifrn.edu.br/ldap/department"
        new_attribute_value1 = "IT"
        new_attribute_category1 = "urn:oasis:names:tc:xacml:1.0:subject:subject-id"

        # attribute data
        data = {'category': new_attribute_category1, 'attribute_name': new_attribute_name1,
                'attribute_value': new_attribute_value1}

        # testcase 1 (http status code return)
        response = self.client.post("/policy/%s/%s/" % (policy_name, rule_name), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testcase 2 (retrieve policy and check new attribute)
        new_policy_test = XacmlUtil(Policy.objects.all()[0].content)
        new_attribute_test = new_policy_test.policy.get_match_by_value(new_attribute_name1)
        self.assertIsNotNone(new_attribute_test)
        self.assertEqual(new_attribute_test.attribute_value.value, new_attribute_value1)

        # testcase 3 (trying add an existing attribute)
        new_attribute_name2 = "urn:oasis:names:tc:xacml:1.0:action:action-id"
        new_attribute_value2 = "POST"
        new_attribute_category2 = "urn:oasis:names:tc:xacml:3.0:attribute-category:action"

        # attribute data
        data = {'category': new_attribute_category2, 'attribute_name': new_attribute_name2,
                'attribute_value': new_attribute_value2}

        response = self.client.post("/policy/%s/%s/" % (policy_name, rule_name), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_4_modify_attribute(self):
        """
        Ensure we can modify an attribute in an existing policy
        """

        print "\nTesting method modify_attribute()..."

        # policy data
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        policy_name = policy.get_policy_name()
        rule_name = policy.policy.rules[0].properties.get('RuleId').value

        # attribute data
        attribute_category1 = 'urn:oasis:names:tc:xacml:1.0:subject-category:access-subject'
        attribute_name1 = 'http://wso2.org/claims/role'
        attribute_value1 = 'admin'

        # attribute data
        data = {'category': attribute_category1, 'attribute_name': attribute_name1,
                'attribute_value': attribute_value1}

        # testcase 1 (http status code return)
        response = self.client.put("/policy/%s/%s/" % (policy_name, rule_name), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # testcase 2 (new attribute value)
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        attr = policy.policy.get_match_by_value('http://wso2.org/claims/role')
        self.assertEqual(attr.attribute_value.value, 'admin')

        # testcase 3 (attribute inexistent)
        attribute_category2 = 'urn:oasis:names:tc:xacml:1.0:subject-category:access-subject'
        attribute_name2 = 'http://ifrn.edu.br/attribute/inexistent'
        attribute_value2 = 'inexistent_attribute'

        # attribute data
        data2 = {'category': attribute_category2, 'attribute_name': attribute_name2,
                 'attribute_value': attribute_value2}

        response = self.client.put("/policy/%s/%s/" % (policy_name, rule_name), data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_5_delete_attribute(self):
        """
        Ensure we can delete an attribute in an existing policy
        """

        print "\nTesting method delete_attribute()..."

        # policy data
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        policy_name = policy.get_policy_name()
        rule_name = policy.policy.rules[0].properties.get('RuleId').value

        # attribute data
        attribute_name = 'http://wso2.org/claims/role'

        # attribute data
        data = {'attribute_name': attribute_name}

        # testcase 1 (attrbute is deleted?)
        response = self.client.delete("/policy/%s/%s/" % (policy_name, rule_name), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 1)
        policy2 = XacmlUtil(content=Policy.objects.all()[0].content)
        attr = policy2.policy.get_match_by_value(attribute_name)
        self.assertIsNone(attr)

        # testcase 2 (attribute inexistent)
        data = {'attribute_name': 'inexistent_attribute'}
        response = self.client.delete("/policy/%s/%s/" % (policy_name, rule_name), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
