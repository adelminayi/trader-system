import profile
from sqlite3 import threadsafety
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import pprint


import os
import numpy as np
import pandas as pd
import datetime

from cryptocode import decrypt
from dotenv import load_dotenv

from django.db.models import Q
from balance.models import WalletBalance

from balance.serializers import BalanceSerializer, WalletBalanceSerializer
from trades.serializers import TradeSerializer, OrderSerializer, UnplanTradeSerializer
from trades.models import Trade, UnplanTrade
from orders.models import Order
from profiles.models import Profile
from keysecrets.models import Secret
from binanceAPI.restapi import Binance
from userstrategies.models import UserStrategy


load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class AdelViewTest(generics.ListAPIView):
    serializer_class    = TradeSerializer
    permission_classes  = (AllowAny,)

    def get_queryset(self):
        userId          = self.request.user.id
        symbol          = self.request.query_params.get('symbol')

        Qlist=[
            Q(secret__profile__user__id=userId),
            Q(symbol=symbol),
        ]

        # return UnplanTrade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        orders = Order.objects.select_related("strategy__secret").filter(tardeMatched=False,profile = 31)
        # print('\n\n', len(orders),'\n\n')
        # for item in orders:
        #     print(item.orderId)

        return orders
        # for order in orders:
        #     orderList.append(
        #         {
        #             "profile":   order.profile.id,
        #             "strategy":  order.strategy.id,
        #             "symbol":    order.symbol,
        #             "orderId":   order.orderId,
        #             "apiKey":    order.strategy.secret.apiKey,
        #             "secretKey": order.strategy.secret.secretKey,
        #             "secret":    order.strategy.secret.id
        #         }
        #     )




    def list(self, request):

        orderList = []
        tardesdf  = pd.DataFrame([], columns=['buyer','commission','commissionAsset','id','maker',
                                            'marginAsset','orderId','positionSide','price','qty',
                                            'quoteQty','realizedPnl','side','symbol','time', 'secret'])
        # print(tardesdf)
        # Columns: [buyer, commission, commissionAsset, id, maker, marginAsset, orderId, positionSide, price, qty, quoteQty, realizedPnl, side, symbol, time, secret]
        orders = Order.objects.select_related("strategy__secret").filter(tardeMatched=False)
        for order in orders:
            orderList.append(
                {
                    "profile":   order.profile.id,
                    "strategy":  order.strategy.id,
                    "symbol":    order.symbol,
                    "orderId":   order.orderId,
                    "apiKey":    order.strategy.secret.apiKey,
                    "secretKey": order.strategy.secret.secretKey,
                    "secret":    order.strategy.secret.id
                }
            )
            # print(orderList[-1])
        orderdf  = pd.DataFrame(orderList).drop(["apiKey","secretKey","secret","symbol"], axis=1).sort_values(by=["orderId"])
        # print(orderdf[-10:])
        #    profile  strategy      orderId
        # 0        4        59  62721964416
        secrets  = pd.DataFrame(orderList).groupby(["apiKey","secretKey","symbol","secret"]).agg(['unique'])\
                                        .drop(["profile","strategy","orderId"], axis=1)\
                                        .to_dict('split')["index"]
        # print(secrets[-1:])
        # [('rNOZt1RX+uzFS3s2A==', '+Y6bMc3o0giw==', 'BTCUSDT', 3)]

        secretList = []
        for secret in secrets:
            secretList.append((decrypt(secret[0], APIKEYPASS), decrypt(secret[1], SECKEYPASS), secret[2], secret[3]))
        # print(secretList[-1])
        # ('QshW2ZN4JD', 'ZOnR10u4P', 'BTCUSDT', 3)
        secrets = secretList
        # print((secretList)) ****  len: 5
        dfList = [tardesdf,]
        for secret in secrets:
            binance   = Binance(secret[0], secret[1])
            resdf     = pd.DataFrame(binance.lastTrades(secret[2], "20"))
            resdf['secret'] = secret[3]
            dfList.append(resdf)
        tardesdf  = pd.concat(dfList, ignore_index=True)

        # tardesdf = tardesdf.sort_values(by=["orderId"])

        # finaldf  = pd.merge(tardesdf, orderdf, how = 'inner', on = 'orderId')
        # finaldf.rename(columns={"id": "tradeId"}, inplace=True)
        # finaldf.drop(columns=['secret'], inplace=True)

        # orderIds = finaldf["orderId"].tolist()

        # data = finaldf.to_dict("records")

        # serializer = TradeSerializer(data=data, many=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     Order.objects.filter(orderId__in=orderIds).update(tardeMatched=True)

        # unplanTradesdf = pd.merge(tardesdf, orderdf, how = 'left', on = 'orderId')
        # unplanTradesdf.rename(columns={"id": "tradeId"}, inplace=True)
        # unplanTradesdf = unplanTradesdf[unplanTradesdf['strategy'].isna()]
        # unplanTradesdf.drop(columns=['profile','strategy'], inplace=True)

        # data = unplanTradesdf.to_dict("records")

        # serializer = UnplanTradeSerializer(data=data, many=True)
        # if serializer.is_valid():
        #     serializer.save()



        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)



class SystemTrades(generics.ListAPIView):
    serializer_class    = TradeSerializer
    permission_classes  = (AllowAny,)

    def get_queryset(self):
        userId          = self.request.user.id
        symbol          = self.request.query_params.get('symbol')

        Qlist=[
            Q(secret__profile__user__id=userId),
            Q(symbol=symbol),
        ]
        # return UnplanTrade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        orders = Order.objects.select_related("strategy__secret").filter(tardeMatched=False,profile = 31)
        return orders
    
    def list(self, request):
        print(self.request.user.id)
        profile_id = Profile.objects.get(user_id=self.request.user.id)
        print(profile_id.id)
        orderList=set()
        # orders = Order.objects.select_related("strategy__secret").filter(tardeMatched=False, profile =31)
        orders = Order.objects.select_related("strategy__secret").filter(profile =profile_id)
        for order in orders:
            orderList.add(order.orderId)

        # print((orderList))
        trades = Trade.objects.select_related("strategy__secret").filter(profile=profile_id)#, strategy=49)
        # print(trades.values()[0:8])
        # print(len(trades))
        tradesList=set()
        for trade in trades:
            tradesList.add(trade.orderId)
        # print(((tradesList)))

        matched_orders = list(orderList & tradesList)
        print(len(matched_orders))
        qs = trades.filter(orderId__in=matched_orders)
        # print('\n\nqa:\n' , qs.values()[0])


        queryset = self.get_queryset() 
        
        serializer = TradeSerializer(qs, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)
