from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from SecAuthAPI.API.serializers import PolicySerializer
from SecAuthAPI.Core.models import Policy
from SecAuthAPI.Core.xacml import Xacml
from SecAuthAPI.Adapter.adapter import Adapter
from django.http import QueryDict


class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Permisions to be viewed or edited
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


@api_view(['GET'])
def clear_cache(request):
    if request.method == 'GET':
        Adapter.clear_cache()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def policy_list(request):
    """
    List all policies (GET) or Insert (POST) a new policy
    """
    if request.method == 'GET':
        snippets = Policy.objects.all()  # all policies
        serializer = PolicySerializer(snippets, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # add policy in PAP/PDP     # TODO: refactory (name in url)
            Adapter.create_policy(serializer.data['name'],
                                  serializer.data['description'],
                                  serializer.data['content'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def policy_detail(request, policy_name):
    """
    Retrieve (GET) or delete (DELETE) a policy instance
    """
    try:
        policy = Policy.objects.get(name=policy_name)
    except Policy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PolicySerializer(policy)   # one policy
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # update policy in PAP/PDP
            Adapter.update_policy(serializer.data['name'],
                                  serializer.data['description'],
                                  serializer.data['content'])

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete policy in PAP/PDP
        Adapter.delete_policy(policy.name)

        # delete policy in database
        policy.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def policy_modify_attribute(request, policy_name, rule_name):
    """
    Modify attribute on XACML Policy rule

    :param request: additional data (category_id, attribute_value)
    :param policy_name: Policy Name on PAP
    :param rule_name: Rule name on Policy
    :return: HTTP 204 on success (no data)
    """

    try:
        policy = Policy.objects.get(name=policy_name)
    except Policy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # change policy
        new_policy = Adapter.modify_policy_attribute(policy.content, rule_name, request.data['attribute_name'],
                                                     request.data['attribute_value'])

        # define fields in request.data to serialize (querydict)
        new_request_data = QueryDict(mutable=True)
        new_request_data.appendlist('name', policy_name)
        new_request_data.appendlist('description', policy.description)
        new_request_data.appendlist('content', new_policy)
        serializer = PolicySerializer(policy, data=new_request_data)

        if serializer.is_valid():
            serializer.save()

            # update policy in PAP/PDP
            Adapter.update_policy(serializer.data['name'],
                                  serializer.data['description'],
                                  serializer.data['content'])

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: attribute_name is broken in URL parameter (special chars)
@api_view(['POST'])
def policy_add_attribute(request, policy_name, rule_name, attribute_name):
    """
    Add attribute on XACML Policy rule

    :param request: additional data (category_id, attribute_value)
    :param policy_name: Policy Name on PAP
    :param rule_name: Rule name on Policy
    :param attribute_name: Attribute name on Policy
    :return: HTTP 204 on success (no data)
    """
    pass
