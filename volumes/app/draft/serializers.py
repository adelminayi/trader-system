from dataclasses import fields
from re import I
from rest_framework import serializers

from .models import Person, Coin, BuyAndSell

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'

class BuyAndSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyAndSell
        fields = '__all__'