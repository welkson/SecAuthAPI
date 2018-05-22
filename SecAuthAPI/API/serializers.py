from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from SecAuthAPI.Core.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('name', 'description', 'content')
