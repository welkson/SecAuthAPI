from django.contrib.auth.models import User, Group
from rest_framework import serializers
from SecAuthAPI.Manager.models import Policy


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
