from operator import and_
from functools import reduce
from datetime import datetime

import pandas as pd 
import numpy as np

from django.db.models import Q

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import IsAuthenticated

from balance.models import Balance, WalletBalance
from balance.serializers import BalanceSerializer, BalanceRollingSerializer, WalletBalanceSerializer



class BalanceList(generics.ListAPIView):
    """
    balance list
    tsymbol=BTCUSDT&from=1644483626859&to=1644490326859&limit=30
    """
    serializer_class    = BalanceSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        strategy    = self.request.query_params.get('strategy')
        id          = self.request.query_params.get('id')
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
            Q(strategy__strategy=strategy),
            Q(strategy__id=id),
            Q(symbol=symbol),
            Q(createTime__gte=l[0]),
            Q(createTime__lte=l[1])
        ]

        return Balance.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None])).order_by('-createTime')[:limit]
    
    def list(self,requests):
        queryset = self.get_queryset()
        serializer = BalanceSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


class BalanceRolling(generics.ListAPIView):
    """
    balance list
    /balance/3600/?strategy=GAMMA&symbol=BTCUSDT&from=1644483626859&to=1644490326859
    """
    serializer_class    = BalanceRollingSerializer
    pagination_class    = None
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        symbol      = self.request.query_params.get('symbol')
        strategy    = self.request.query_params.get('strategy')
        fromTime    = self.request.query_params.get('from')
        toTime      = self.request.query_params.get('to')

        l = [fromTime,toTime]

        for i in range(len(l)):
            if l[i] is not None:
                try:
                    l[i] = datetime.fromtimestamp(int(l[i])/1000)
                except:
                    raise APIException("invalid query parameters(from|to).")

        Qlist=[
            Q(profile__user__id=userId),
            Q(strategy__strategy=strategy),
            Q(symbol=symbol),
            Q(createTime__gte=l[0]),
            Q(createTime__lte=l[1])
        ]

        return Balance.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))\
                                    .order_by("-createTime").values("createTime","balance")

    def list(self, request, step):
        step = str(step)
        step = step+"S"
        df = pd.DataFrame(list(self.get_queryset()))
            
        if len(df)!=0:
            df = df.set_index(['createTime'])
            df = df.resample(step).agg({"balance": "last"}).reset_index().fillna(method="ffill")
            df['time'] = df.createTime.values.astype(np.int64) // 10 ** 6
            df.drop('createTime', axis=1, inplace=True)
            df = df[['time','balance']]
            data = df.to_dict("records")
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


class WalletBalanceList(generics.ListAPIView):
    """
    wallet balance list
    /balance/wallet/?asset=BTCUSDT&from=1644483626859&to=1644490326859&limit=30
    """
    serializer_class    = WalletBalanceSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        asset       = self.request.query_params.get('symbol')
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
            Q(symbol=asset),
            Q(createTime__gte=l[0]),
            Q(createTime__lte=l[1])
        ]

        return WalletBalance.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None])).order_by('-createTime')[:limit]
    
    def list(self,requests):
        queryset = self.get_queryset()
        serializer = WalletBalanceSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)



class WalletBalanceFirst(generics.RetrieveAPIView):
    """
    wallet balance list
    /balance/wallet/first/<secret_id=int>/
    """
    serializer_class    = WalletBalanceSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self, secretId):
        userId = self.request.user.id

        try:
            return WalletBalance.objects.filter(Q(profile__user__id=userId), Q(secret__id=secretId)).first()
        except:
            Response([], status=status.HTTP_200_OK)
    
    def get(self,requests, id):
        queryset = self.get_queryset(id)
        serializer = WalletBalanceSerializer(queryset)  
        return Response(serializer.data, status=status.HTTP_200_OK)
