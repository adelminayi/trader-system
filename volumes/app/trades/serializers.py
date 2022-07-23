from rest_framework import serializers
from trades.models import Trade, UnplanTrade
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"

class PNLSerializer(serializers.Serializer):
    pnl = serializers.FloatField()

# class PNLRollingSerializer(serializers.Serializer):
#     time = serializers.IntegerField()
#     pnl  = serializers.FloatField()

class PNLRollingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"

class UnplanTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnplanTrade
        fields = "__all__"