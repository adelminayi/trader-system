from dataclasses import fields
from re import I
from rest_framework import serializers

from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'