from rest_framework import serializers
from .models import Container, Files, Codes

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codes
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    codes = CodeSerializer(many=True)

    class Meta:
        model = Container
        fields = '__all__'
        ordering = ['created_on']  # Use '-' to sort in descending order based on 'created_on'