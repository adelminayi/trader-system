from rest_framework import serializers
from balance.models import Balance, WalletBalance



class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = "__all__"


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletBalance
        fields = "__all__"


class BalanceRollingSerializer(serializers.Serializer):
    time    = serializers.IntegerField()
    balance = serializers.FloatField()