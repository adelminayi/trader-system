from rest_framework import serializers
from orders.models import Order, CanceledOrders



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CanceledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanceledOrders
        fields = "__all__"