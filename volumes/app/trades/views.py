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
        strat_id    = request.query_params.get('id')

        Qlist=[
            Q(profile__user__id=userId),
            # Q(symbol=symbol),
            # Q(time__gte=fromTime),
            # Q(time__lte=toTime),
            # Q(strategy__strategy=strategy),
            Q(strategy=strat_id),
        ]
        # queryset1 = Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        queryset1 = Trade.objects.filter( Qlist[0] & Qlist[1])
        queryset2 = queryset1.aggregate(pnl=Sum(F("realizedPnl")-F("commission")))
        print(queryset1,'\n', len(queryset1))
        return Response(queryset2, status=status.HTTP_200_OK)


# class PNLRolling(generics.ListAPIView):
#     """
#     rolling pnl
#     /trades/pnl/3600/?symbol=BTCUSDT&strategy=GAMMA&from=1644483626859&to=1644490326859
#     """
#     permission_classes  = (IsAuthenticated,)
#     pagination_class    = None
#     serializer_class    = PNLRollingSerializer

#     def get_queryset(self):
#         userId      = self.request.user.id
#         symbol      = self.request.query_params.get('symbol')
#         strategy    = self.request.query_params.get('strategy')
#         fromTime    = self.request.query_params.get('from')
#         toTime      = self.request.query_params.get('to')
#         id          = self.request.query_params.get('id')

#         l = [fromTime,toTime]

#         for i in range(len(l)):
#             if l[i] is not None:
#                 if l[i].isdigit():
#                     l[i] = int(l[i])
#                 else:
#                     raise APIException("invalid query parameters(from|to).")

#         Qlist=[
#             ~Q(realizedPnl = 0.0),
#             Q(profile__user__id=userId),
#             Q(strategy__strategy=strategy),
#             Q(strategy__id=id),
#             Q(symbol=symbol),
#             Q(time__gte=l[0]),
#             Q(time__lte=l[1]),
#         ]

#         return Trade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))\
#             .order_by("-time").values("time","realizedPnl","commission","strategy")

#     def list(self, request, step):
#         step = step+"S"
#         df = pd.DataFrame(list(self.get_queryset()))
            
#         if len(df)!=0:
#             df['time'] = pd.to_datetime(df['time'], unit='ms')
#             df = df.set_index(['time'])
#             # df = df.resample(step).sum().reset_index()
#             df = df.resample(step).mean().ffill().reset_index()
#             df['pnl'] = df['realizedPnl']-df['commission']
#             df = df.drop(columns=["realizedPnl","commission"])
#             df['time'] = df.time.values.astype(np.int64) // 10 ** 6
#             data = df.to_dict("records")
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             return Response([], status=status.HTTP_200_OK)


class PNLRolling(generics.ListAPIView):
    """
    rolling pnl
    /trades/pnl/3600/?symbol=BTCUSDT&strategy=GAMMA&from=1644483626859&to=1644490326859
    """
    permission_classes  = (IsAuthenticated,)
    pagination_class    = None
    serializer_class    = PNLRollingSerializer

    def get_queryset(self):
        queryset = Trade.objects.all()
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
                    raise APIException("invalid query parameters (from|to).")
        if int(fromTime) > int(toTime):
            raise APIException("FromTimestamp should be lower than ToTimestamp.")

        day_duration = 86400000
        l[0] = (int(fromTime) - (int(fromTime) % day_duration)) + day_duration - 1
        l[1] = (int(toTime) - (int(toTime) % day_duration)) + day_duration - 1

        Qlist=[
            # ~Q(realizedPnl = 0.0),
            Q(profile__user__id=userId),
            Q(strategy__strategy=strategy),
            Q(strategy__id=id),
            Q(symbol=symbol),
            Q(time__gte=l[0]),
            Q(time__lte=l[1]),
        ]
        print('l:', l)
        if fromTime is not None and toTime is not None:
            queryset = queryset.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None])).order_by("-time")
        return queryset
    

    def list(self, request, step):
        data=(self.get_queryset())
        fromTime = self.request.query_params.get('from')
        toTime = self.request.query_params.get('to')
        day_duration = 86400000
        result = []
        if fromTime is not None and toTime is not None:
            fromTime= int(fromTime)
            toTime=int(toTime)
            '''
            move fromTime to last second of that day, e.g.: 20:32:45 >> 23:59:59
            move toTime to last second of that day, e.g.: 00:01:02 >> 23:59:59
            '''
            if fromTime % day_duration == 0:
                fromTime = fromTime - 1
            if toTime % day_duration == 0:
                toTime = toTime - 1

            begin_day = (int(fromTime) - (int(fromTime) % day_duration)) + day_duration - 1
            end_day = (int(toTime) - (int(toTime) % day_duration)) + day_duration - 1
            steps = int((end_day - begin_day) / day_duration) + 1
            # print('begin_day :', begin_day)
            # print('end_day   :',end_day)

            # print('steps:', steps)

            for i in range(steps):
                start_step = begin_day + i * day_duration
                end_step = start_step + day_duration
                if end_step > end_day:
                    break
                # print('start : {}  - end : {}'.format(start_step, end_step))
                temp_data = data.filter(Q(time__gte= str(start_step)) & Q(time__lte = str(end_step)))
                # print('temp_data.values()  : ', temp_data.values())
                uniqe_startegy = list(set(x['strategy_id'] for x in temp_data.values('strategy_id')))
                # print('uniqe_startegy:', uniqe_startegy)
                for strat in uniqe_startegy:
                    total_pnl = 0
                    for item in temp_data.filter(strategy_id= strat).values():
                        total_pnl += item['realizedPnl']- item['commission']
                    result.append({'time': start_step+1, 'pnl': total_pnl, 'strategy':strat })
                
        if len(data) != 0:
            return Response(result, status=status.HTTP_200_OK)
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