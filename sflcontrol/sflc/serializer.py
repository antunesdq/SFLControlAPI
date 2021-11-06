from rest_framework import serializers


from sflc.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.fields