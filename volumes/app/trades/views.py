from operator import and_
from functools import reduce

import pandas as pd 
import numpy as np

from django.http import Http404
from django.db.models import Q,F,Sum

from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from trades.models import Trade, UnplanTrade
from trades.serializers import TradeSerializer,PNLSerializer,PNLRollingSerializer, UnplanTradeSerializer



class TradeList(generics.ListAPIView, LimitOffsetPagination):
    """
    trade list
    c?strategy=GAMMA&symbol=BTCUSDT&
            from=1644483626859&to=1644490326859&
            side=BUY&
            pnllte=100&pnlgte=50&
            qtylte=1&qtygte=0.5&
            pricelte=60000&pricegte=50000&
            commissionlte=12&commissiongte=10&
            limit=5&offset=5
    """
    serializer_class    = TradeSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId          = self.request.user.id
        symbol          = self.request.query_params.get('symbol')
        fromTime        = self.request.query_params.get('from')
        toTime          = self.request.query_params.get('to')
        strategy        = self.request.query_params.get('strategy')
        side            = self.request.query_params.get('side')
        pnllte          = self.request.query_params.get('pnllte')
        pnlgte          = self.request.query_params.get('pnlgte')
        qtylte          = self.request.query_params.get('qtylte')
        qtygte          = self.request.query_params.get('qtygte')
        pricelte        = self.request.query_params.get('pricelte')
        pricegte        = self.request.query_params.get('pricegte')
        commissionlte   = self.request.query_params.get('commissionlte')
        commissiongte   = self.request.query_params.get('commissiongte')

        l1 = [fromTime,toTime]
        l2 = [pnllte,pnlgte,qtylte,qtygte,pricelte,pricegte,commissionlte,commissiongte]

        for i in range(len(l1)):
            if l1[i] is not None:
                if l1[i].isdigit():
                    l1[i] = int(l1[i])
                else:
                    raise APIException("invalid query parameters(from|to).")

        for i in range(len(l2)):
            if l2[i] is not None:
                try:
                    l2[i] = float(l2[i])
                except:
                    raise APIException("invalid query parameters(pnl|qty|price|commission).")

        Qlist=[
            Q(profile__user__id=userId),
            Q(symbol=symbol),
            Q(time__gte=l1[0]),
            Q(time__lte=l1[1]),
            Q(strategy__strategy=strategy),
            Q(side=side),
            Q(realizedPnl__lte=l2[0]),
            Q(realizedPnl__gte=l2[1]),
            Q(qty__lte=l2[2]),
            Q(qty__gte=l2[3]),
            Q(price__lte=l2[4]),
            Q(price__gte=l2[5]),
            Q(commission__lte=l2[6]),
            Q(commission__gte=l2[7]),
        ]

        return Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))

    def list(self, request):
        queryset = self.get_queryset()
        results  = self.paginate_queryset(queryset)
        serializer = TradeSerializer(results, many=True)  
        if queryset.exists():
            return self.get_paginated_response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)


# class TradeList(generics.ListAPIView, LimitOffsetPagination):
#     """
#     trade list
#     c?strategy=GAMMA&symbol=BTCUSDT&
#             from=1644483626859&to=1644490326859&
#             side=BUY&
#             pnllte=100&pnlgte=50&
#             qtylte=1&qtygte=0.5&
#             pricelte=60000&pricegte=50000&
#             commissionlte=12&commissiongte=10&
#             limit=5&offset=5
#     """
#     serializer_class    = TradeSerializer
#     permission_classes  = (IsAuthenticated,)

#     def get_queryset(self):
#         userId          = self.request.user.id
#         symbol          = self.request.query_params.get('symbol')
#         fromTime        = self.request.query_params.get('from')
#         toTime          = self.request.query_params.get('to')
#         strategy        = self.request.query_params.get('strategy')
#         side            = self.request.query_params.get('side')
#         pnllte          = self.request.query_params.get('pnllte')
#         pnlgte          = self.request.query_params.get('pnlgte')
#         qtylte          = self.request.query_params.get('qtylte')
#         qtygte          = self.request.query_params.get('qtygte')
#         pricelte        = self.request.query_params.get('pricelte')
#         pricegte        = self.request.query_params.get('pricegte')
#         commissionlte   = self.request.query_params.get('commissionlte')
#         commissiongte   = self.request.query_params.get('commissiongte')
#         limit           = self.request.query_params.get('limit')

#         l1 = [fromTime,toTime]
#         l2 = [pnllte,pnlgte,qtylte,qtygte,pricelte,pricegte,commissionlte,commissiongte]

#         for i in range(len(l1)):
#             if l1[i] is not None:
#                 if l1[i].isdigit():
#                     l1[i] = int(l1[i])
#                 else:
#                     raise APIException("invalid query parameters(from|to).")

#         for i in range(len(l2)):
#             if l2[i] is not None:
#                 try:
#                     l2[i] = float(l2[i])
#                 except:
#                     raise APIException("invalid query parameters(pnl|qty|price|commission).")
#         if limit is None:
#             limit = 30
#         else:
#             try:
#                 limit = int(limit)
#             except:
#                 raise APIException("invalid query parameters(limit).")

#         Qlist=[
#             Q(profile__user__id=userId),
#             Q(symbol=symbol),
#             Q(time__gte=l1[0]),
#             Q(time__lte=l1[1]),
#             Q(strategy__strategy=strategy),
#             Q(side=side),
#             Q(realizedPnl__lte=l2[0]),
#             Q(realizedPnl__gte=l2[1]),
#             Q(qty__lte=l2[2]),
#             Q(qty__gte=l2[3]),
#             Q(price__lte=l2[4]),
#             Q(price__gte=l2[5]),
#             Q(commission__lte=l2[6]),
#             Q(commission__gte=l2[7]),
#         ]

#         return Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))[:limit]

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = TradeSerializer(queryset, many=True)  
#         if queryset.exists():
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response([], status=status.HTTP_200_OK)


class PNL(viewsets.GenericViewSet):
    """
    pnl
    /trades/pnl/?symbol=BTCUSDT&strategy=GAMMA_H&from=1644483626859&to=1644490326859
    """
    permission_classes  = (IsAuthenticated,)
    pagination_class    = None
    serializer_class    = PNLSerializer

    def retrieve(self, request, pk=None):
        userId      = request.user.id
        symbol      = request.query_params.get('symbol')
        fromTime    = request.query_params.get('from')
        toTime      = request.query_params.get('to')
        strategy    = request.query_params.get('strategy')

        Qlist=[
            Q(profile__user__id=userId),
            Q(symbol=symbol),
            Q(time__gte=fromTime),
            Q(time__lte=toTime),
            Q(strategy__strategy=strategy),
        ]

        queryset = Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))\
                            .aggregate(pnl=Sum(F("realizedPnl")-F("commission")))
        
        return Response(queryset, status=status.HTTP_200_OK)


class PNLRolling(generics.ListAPIView):
    """
    rolling pnl
    /trades/pnl/3600/?symbol=BTCUSDT&strategy=GAMMA&from=1644483626859&to=1644490326859
    """
    permission_classes  = (IsAuthenticated,)
    pagination_class    = None
    serializer_class    = PNLRollingSerializer

    def get_queryset(self):
        userId      = self.request.user.id
        symbol      = self.request.query_params.get('symbol')
        strategy    = self.request.query_params.get('strategy')
        fromTime    = self.request.query_params.get('from')
        toTime      = self.request.query_params.get('to')
        id          = self.request.query_params.get('id')

        l = [fromTime,toTime]

        for i in range(len(l)):
            if l[i] is not None:
                if l[i].isdigit():
                    l[i] = int(l[i])
                else:
                    raise APIException("invalid query parameters(from|to).")

        Qlist=[
            ~Q(realizedPnl = 0.0),
            Q(profile__user__id=userId),
            Q(strategy__strategy=strategy),
            Q(strategy__id=id),
            Q(symbol=symbol),
            Q(time__gte=l[0]),
            Q(time__lte=l[1]),
        ]

        return Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))\
            .order_by("-time").values("time","realizedPnl","commission","strategy")

    def list(self, request, step):
        step = step+"S"
        df = pd.DataFrame(list(self.get_queryset()))
            
        if len(df)!=0:
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            df = df.set_index(['time'])
            # df = df.resample(step).sum().reset_index()
            df = df.resample(step).mean().ffill().reset_index()
            df['pnl'] = df['realizedPnl']-df['commission']
            df = df.drop(columns=["realizedPnl","commission"])
            df['time'] = df.time.values.astype(np.int64) // 10 ** 6
            data = df.to_dict("records")
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)




class UnplanTradeList(generics.ListAPIView, LimitOffsetPagination):
    """
    trade list
    c?strategy=GAMMA&symbol=BTCUSDT&
            from=1644483626859&to=1644490326859&
            side=BUY&
            pnllte=100&pnlgte=50&
            qtylte=1&qtygte=0.5&
            pricelte=60000&pricegte=50000&
            commissionlte=12&commissiongte=10&
            limit=5&offset=5
    """
    serializer_class    = UnplanTradeSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId          = self.request.user.id
        symbol          = self.request.query_params.get('symbol')
        fromTime        = self.request.query_params.get('from')
        toTime          = self.request.query_params.get('to')
        strategy        = self.request.query_params.get('strategy')
        side            = self.request.query_params.get('side')
        pnllte          = self.request.query_params.get('pnllte')
        pnlgte          = self.request.query_params.get('pnlgte')
        qtylte          = self.request.query_params.get('qtylte')
        qtygte          = self.request.query_params.get('qtygte')
        pricelte        = self.request.query_params.get('pricelte')
        pricegte        = self.request.query_params.get('pricegte')
        commissionlte   = self.request.query_params.get('commissionlte')
        commissiongte   = self.request.query_params.get('commissiongte')

        l1 = [fromTime,toTime]
        l2 = [pnllte,pnlgte,qtylte,qtygte,pricelte,pricegte,commissionlte,commissiongte]

        for i in range(len(l1)):
            if l1[i] is not None:
                if l1[i].isdigit():
                    l1[i] = int(l1[i])
                else:
                    raise APIException("invalid query parameters(from|to).")

        for i in range(len(l2)):
            if l2[i] is not None:
                try:
                    l2[i] = float(l2[i])
                except:
                    raise APIException("invalid query parameters(pnl|qty|price|commission).")

        Qlist=[
            Q(secret__profile__user__id=userId),
            Q(symbol=symbol),
            Q(time__gte=l1[0]),
            Q(time__lte=l1[1]),
            Q(strategy__strategy=strategy),
            Q(side=side),
            Q(realizedPnl__lte=l2[0]),
            Q(realizedPnl__gte=l2[1]),
            Q(qty__lte=l2[2]),
            Q(qty__gte=l2[3]),
            Q(price__lte=l2[4]),
            Q(price__gte=l2[5]),
            Q(commission__lte=l2[6]),
            Q(commission__gte=l2[7]),
        ]

        return UnplanTrade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))

    def list(self, request):
        queryset = self.get_queryset()
        results  = self.paginate_queryset(queryset)
        serializer = UnplanTradeSerializer(results, many=True)  
        if queryset.exists():
            return self.get_paginated_response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)