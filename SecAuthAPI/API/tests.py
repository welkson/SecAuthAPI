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

        # testcase
        response = self.client.post("/policy/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 1)
        self.assertEqual(Policy.objects.get().name, 'NewTicketOnlySupport')

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

        # testcase
        response = self.client.put("/policy/%s/" % policy.get_policy_name(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 1)

        # test attribute value
        policytest = XacmlUtil(content=Policy.objects.all()[0].content)
        self.assertEqual(policytest.policy.properties.get('Version').value, '2.0')

    def test_2_delete_policy(self):
        """
        Ensure we can delete a existing policy
        """

        print "\nTesting method delete_policy()..."

        # policy data
        policy_name = Policy.objects.all()[0].name

        # testcase
        response = self.client.delete("/policy/%s/" % policy_name, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 0)

    def test_3_add_attribute(self):
        """
        Ensure we can add an attribute in an existing policy
        """

        print "\nTesting method add_attribute()..."

        # new attribute properties
        new_attribute_name = "http://ifrn.edu.br/ldap/department"
        new_attribute_value = "IT"
        new_attribute_category = "urn:oasis:names:tc:xacml:1.0:subject:subject-id"

        # policy data
        policy = XacmlUtil(content=Policy.objects.all()[0].content)

        # get attribute from target
        target = policy.policy.rules[0].targets[0]
        anyof = AnyOf(parent=target)
        allof = AllOf(parent=anyof)

        # define properties to new attribute
        match = Match(parent=allof)
        match.add_property(name='MatchId', value='urn:oasis:names:tc:xacml:1.0:function:string-equal')
        match.attribute_value.value = new_attribute_value
        match.attribute_value.add_property(name='DataType', value='http://www.w3.org/2001/XMLSchema#string')

        # define type and category
        match.attribute_designator.add_property(name='AttributeId',
                                                value=new_attribute_name)
        match.attribute_designator.add_property(name='Category',
                                                value=new_attribute_category)
        match.attribute_designator.add_property(name='DataType', value='http://www.w3.org/2001/XMLSchema#string')
        match.attribute_designator.add_property(name='MustBePresent', value='true')

        # add new attribute
        allof.add_match(match=match)
        anyof.add_all_of(all_of=allof)
        target.add_any_of(any_of=anyof)

        # new policy (with new attribute)
        new_policy = policy.policy.toXML()

        # policy data
        data = {'description': 'New Ticket Only Support', 'name': 'NewTicketOnlySupport', 'content': new_policy}

        # testcase 1 (http status code return)
        response = self.client.put("/policy/%s/" % policy.get_policy_name(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # testcase 2 (retrieve policy and check new attribute)
        new_policy_test = XacmlUtil(Policy.objects.all()[0].content)
        new_attribute_test = new_policy_test.policy.get_match_by_value(new_attribute_name)
        self.assertIsNotNone(new_attribute_test)
        self.assertEqual(new_attribute_test.attribute_value.value, new_attribute_value)

    def test_4_modify_attribute(self):
        """
        Ensure we can modify an attribute in an existing policy
        """

        print "\nTesting method modify_attribute()..."

        # attribute data
        attribute_name = 'http://wso2.org/claims/role'

        # change "role" attribute (from "support" to "admin")
        policy = XacmlUtil(content=Policy.objects.all()[0].content)
        attr = policy.policy.get_match_by_value('http://wso2.org/claims/role')
        attr.attribute_value.value = 'admin'
        new_policy = policy.policy.toXML()

        # policy data
        data = {'description': 'New Ticket Only Support', 'name': 'NewTicketOnlySupport', 'content': new_policy}

        # testcase
        response = self.client.put("/policy/%s/" % policy.get_policy_name(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 1)

        # test attribute value
        policytest = XacmlUtil(content=Policy.objects.all()[0].content)
        attr = policytest.policy.get_match_by_value(attribute_name)
        self.assertEqual(attr.attribute_value.value, 'admin')

    def test_5_delete_attribute(self):
        """
        Ensure we can delete an attribute in an existing policy
        """

        print "\nTesting method delete_attribute()..."

        # attribute data
        attribute_name = 'http://wso2.org/claims/role'

        # retrieve policy
        policy = XacmlUtil(content=Policy.objects.all()[0].content)

        # remove attribute
        policy.policy.remove_any_of_by_name(attribute_name)

        # create new policy with modifications
        new_policy = policy.policy.toXML()

        # policy data
        data = {'description': 'New Ticket Only Support', 'name': 'NewTicketOnlySupport', 'content': new_policy}

        # testcase
        response = self.client.delete("/policy/%s/" % policy.get_policy_name(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 1)

        attr = new_policy.policy.get_match_by_value(attribute_name)

        # testcase
        self.assertIsNone(attr)


