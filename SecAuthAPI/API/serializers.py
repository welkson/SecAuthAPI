from rest_framework import serializers
from SecAuthAPI.Manager.models import Policy


class PolicySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Policy
        fields = ('name', 'content')
