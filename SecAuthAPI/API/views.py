from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from SecAuthAPI.API.serializers import PolicySerializer
from SecAuthAPI.Manager.models import Policy
from SecAuthAPI.PDPAdapter.adapter import Adapter


class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Permisions to be viewed or edited
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


@api_view(['GET', 'POST'])
def policy_list(request):
    """
    Insert (POST) or List all policies (GET)
    """
    if request.method == 'GET':
        snippets = Policy.objects.all()
        serializer = PolicySerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # add policy in PAP/PDP
            Adapter.add_policy(serializer.data['name'],
                               serializer.data['description'],
                               serializer.data['content'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def policy_detail(request, policy_name):
    """
    Retrieve, update or delete a policy instance
    """
    try:
        policy = Policy.objects.get(name=policy_name)
    except Policy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PolicySerializer(policy)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # update policy in PAP/PDP
            Adapter.update_policy(serializer.data['name'],
                                  serializer.data['description'],
                                  serializer.data['content'])

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete policy in PAP/PDP
        Adapter.delete_policy(policy.name)

        # delete policy in database
        policy.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def policy_publish(request, policy_name):
    """
    Deploy policy on PDP (Authorization Service)
    """
    try:
        policy = Policy.objects.get(name=policy_name)
    except Policy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        pass    # TODO: NotImplemented

    return Response(status=status.HTTP_200_OK)
