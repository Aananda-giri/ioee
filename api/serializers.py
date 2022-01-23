# serializers.py

from rest_framework import serializers
from .models import IoeNoti

class NotiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IoeNoti
        fields = ('title', 'url', 'date')
