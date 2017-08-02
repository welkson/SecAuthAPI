from rest_framework import viewsets
from SecAuthAPI.API.serializers import PolicySerializer
from SecAuthAPI.Manager.models import Policy


class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Permisions to be viewed or edited.
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
