from SecAuthAPI.Manager.models import Policy
from rest_framework import viewsets
from SecAuthAPI.API.serializers import PolicySerializer


class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Policy to be viewed or edited.
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
