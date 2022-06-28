from operator import and_
from functools import reduce
from datetime import datetime

from django.http import Http404
from django.db.models import Q

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, CanceledOrders
from orders.serializers import OrderSerializer, CanceledOrderSerializer



class OrderList(generics.ListAPIView):
    """
    list of orders
    /orders/?strategy=GAMMA&symbol=BTCUSDT&from=1612345678911&to=1612345678911&limit=30
    """
    serializer_class    = OrderSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        strategy    = self.request.query_params.get('strategy')
        symbol      = self.request.query_params.get('symbol')
        fromTime    = self.request.query_params.get('from')
        toTime      = self.request.query_params.get('to')
        limit       = self.request.query_params.get('limit')

        l = [fromTime,toTime]     

        for i in range(len(l)):
            if l[i] is not None:
                try:
                    l[i] = datetime.fromtimestamp(int(l[i])/1000)
                except:
                    raise APIException("invalid query parameters(from|to).")

        if limit is None:
            limit = 30
        else:
            try:
                limit = int(limit)
            except:
                raise APIException("invalid query parameters(limit).")

        Qlist=[
            Q(profile__user__id=userId),
            Q(symbol=symbol),
            Q(strategy__strategy=strategy),
            Q(updateTime__gte=fromTime),
            Q(updateTime__lte=toTime)
        ]

        return Order.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))[:limit]

    def list(self,requests):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


class CanceledOrderList(generics.ListAPIView):
    """"
    list of cancelled orders
    /orders/cancelled/?strategy=GAMMA&symbol=BTCUSDT&from=1612345678911&to=1612345678911&limit=30
    """
    serializer_class    = CanceledOrderSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        strategy    = self.request.query_params.get('strategy')
        symbol      = self.request.query_params.get('symbol')
        fromTime    = self.request.query_params.get('from')
        toTime      = self.request.query_params.get('to')
        limit       = self.request.query_params.get('limit')

        l = [fromTime,toTime]     

        for i in range(len(l)):
            if l[i] is not None:
                try:
                    l[i] = datetime.fromtimestamp(int(l[i])/1000)
                except:
                    raise APIException("invalid query parameters(from|to).")

        if limit is None:
            limit = 30
        else:
            try:
                limit = int(limit)
            except:
                raise APIException("invalid query parameters(limit).")

        Qlist=[
            Q(profile__user__id=userId),
            Q(symbol=symbol),
            Q(strategy__strategy=strategy),
            Q(createTime__gte=fromTime),
            Q(createTime__lte=toTime)
        ]

        return CanceledOrders.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None])).order_by('-createTime')[:limit]
    
    def list(self,requests):
        queryset = self.get_queryset()
        serializer = CanceledOrderSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)