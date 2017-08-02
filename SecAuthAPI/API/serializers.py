from rest_framework import serializers
from SecAuthAPI.Manager.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('name', 'description', 'content')
