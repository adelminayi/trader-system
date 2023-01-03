from dataclasses import fields
from re import I
from rest_framework import serializers
import json

from .models import Person, Coin, BuyAndSell

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class BuyAndSellSerializer(serializers.ModelSerializer):
    coin = serializers.SerializerMethodField()

    class Meta:
        model = BuyAndSell
        fields = '__all__' 

    def get_coin(self, obj):
        mysjon = {}
        query = obj.coin.all()
        # qr = []
        # for item in query:
        #     qr.append(item.name)
        # mysjon['name'] = qr
        # print(str(mysjon))
        return CoinSerializer(query, many=True).data

# class BuyAndSellSerializer(serializers.ModelSerializer):
# coin = serializers.PrimaryKeyRelatedField(queryset = Coin.objects.all(), many=True)
#     class Meta:
#         ordering = ['-id']
#         model = BuyAndSell
#         fields = ("id", "name", "coin")
#         extra_kwargs = {'coin': {'required': False}}

class CoinSerializer(serializers.ModelSerializer):
    # buyandsell = BuyAndSellSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Coin
        fields = ('name',)#'__all__'#("id", "name", "buyandsell")
        # extra_kwargs = {'buyandsell': {'required': False}}
