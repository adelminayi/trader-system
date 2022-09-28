from __future__ import print_function
from operator import and_, imod
from functools import reduce
from django.shortcuts import render

from userstrategies.serializers import UserStrategySerializer
from draft.models import Person
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import views

import os
import pandas as pd

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
from rest_framework.pagination import LimitOffsetPagination


load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class AdelViewTest(generics.ListAPIView, LimitOffsetPagination):
    serializer_class = TradeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        userId = self.request.user.id
        symbol = self.request.query_params.get('symbol')

        Qlist = [
            Q(secret__profile__user__id=userId),
            Q(symbol=symbol),
        ]
        profileid = Profile.objects.get(user_id=self.request.user.id).id
        # return UnplanTrade.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        orders = Order.objects.select_related("strategy__secret").filter(
            tardeMatched=True, profile=profileid)
        # print('\n\n', len(orders),'\n\n')
        # for item in orders:
        #     print(item.orderId)
        return orders

    def list(self, request):
        profileid = Profile.objects.get(user_id=self.request.user.id).id

        orderList = []
        tardesdf = pd.DataFrame([], columns=['buyer', 'commission', 'commissionAsset', 'id', 'maker',
                                             'marginAsset', 'orderId', 'positionSide', 'price', 'qty',
                                             'quoteQty', 'realizedPnl', 'side', 'symbol', 'time', 'secret'])
        # print(tardesdf)
        # Columns: [buyer, commission, commissionAsset, id, maker, marginAsset, orderId, positionSide, price, qty, quoteQty, realizedPnl, side, symbol, time, secret]
        orders = Order.objects.select_related("strategy__secret").filter(
            tardeMatched=True, profile=profileid)
        print(orders[0])
        # order record representation
        # rezaei - 0935 560 4236, orderID:64993434619
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
        orderdf = pd.DataFrame(orderList).drop(
            ["apiKey", "secretKey", "secret", "symbol"], axis=1).sort_values(by=["orderId"])
        # print(orderdf[-10:])
        #    profile  strategy      orderId
        # 0        4        59  62721964416
        # print(orderList[-1])
        secrets = pd.DataFrame(orderList).groupby(["apiKey", "secretKey", "symbol", "secret"]).agg(['unique'])\
            .drop(["profile", "strategy", "orderId"], axis=1)\
            .to_dict('split')["index"]
        # print(secrets[-1:])
        # print(len(secrets))
        # [('rNOZt1RX+uzFS3s2A==', '+Y6bMc3o0giw==', 'BTCUSDT', 3)]

        secretList = []
        for secret in secrets:
            secretList.append((decrypt(secret[0], APIKEYPASS), decrypt(
                secret[1], SECKEYPASS), secret[2], secret[3]))
        # print(secretList[-1])
        # ('QshW2ZN4JD', 'ZOnR10u4P', 'BTCUSDT', 3)
        secrets = secretList
        # print((secretList)) ****  len: 5
        dfList = [tardesdf, ]
        for secret in secrets:
            binance = Binance(secret[0], secret[1])
            resdf = pd.DataFrame(binance.lastTrades(secret[2], "20"))
            resdf['secret'] = secret[3]
            dfList.append(resdf)
        tardesdf = pd.concat(dfList, ignore_index=True)

        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


class SystemTrades(generics.ListAPIView):
    '''
    get order list which get executed
    get trade list from db
    filter trades which not exists in orders
    '''
    serializer_class = TradeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        userId = self.request.user.id
        symbol = self.request.query_params.get('symbol')
        fromTime = self.request.query_params.get('from')
        toTime = self.request.query_params.get('to')
        strategy = self.request.query_params.get('strategy')
        side = self.request.query_params.get('side')
        pnllte = self.request.query_params.get('pnllte')
        pnlgte = self.request.query_params.get('pnlgte')
        qtylte = self.request.query_params.get('qtylte')
        qtygte = self.request.query_params.get('qtygte')
        pricelte = self.request.query_params.get('pricelte')
        pricegte = self.request.query_params.get('pricegte')
        commissionlte = self.request.query_params.get('commissionlte')
        commissiongte = self.request.query_params.get('commissiongte')
        profileid = Profile.objects.get(user_id=self.request.user.id).id

        l1 = [fromTime, toTime]
        l2 = [pnllte, pnlgte, qtylte, qtygte, pricelte,
              pricegte, commissionlte, commissiongte]

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
                    raise APIException(
                        "invalid query parameters(pnl|qty|price|commission).")
        Qlist = [
            Q(symbol=symbol),
            Q(profile_id=profileid),
            Q(updateTime__gte=l1[0]),
            Q(updateTime__lte=l1[1]),
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
            Q(tardeMatched=True)
        ]

        orders = Order.objects.filter(
            reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        return orders

    def list(self, request):
        userId = self.request.user.id
        symbol = self.request.query_params.get('symbol')
        fromTime = self.request.query_params.get('from')
        toTime = self.request.query_params.get('to')
        strategy = self.request.query_params.get('strategy')
        side = self.request.query_params.get('side')
        pnllte = self.request.query_params.get('pnllte')
        pnlgte = self.request.query_params.get('pnlgte')
        qtylte = self.request.query_params.get('qtylte')
        qtygte = self.request.query_params.get('qtygte')
        pricelte = self.request.query_params.get('pricelte')
        pricegte = self.request.query_params.get('pricegte')
        commissionlte = self.request.query_params.get('commissionlte')
        commissiongte = self.request.query_params.get('commissiongte')
        profile_id = Profile.objects.get(user_id=self.request.user.id).id

        l1 = [fromTime, toTime]
        l2 = [pnllte, pnlgte, qtylte, qtygte, pricelte,
              pricegte, commissionlte, commissiongte]

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
                    raise APIException(
                        "invalid query parameters(pnl|qty|price|commission).")
        Qlist = [
            Q(symbol=symbol),
            Q(profile_id=profile_id),
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

        trades = Trade.objects.filter(
            reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))
        # print(trades.values()[0])
        tradesdf = pd.DataFrame(list(trades.values()))
        trades_id = set(tradesdf['orderId'])
        # tradesdf.to_csv('/home/minayi/dev/users/volumes/app/jobs/tradesdf2.py',index=False)
        # print(tradesdf)

        # orderList = []
        orders = self.get_queryset()
        # print(orders.values()[0])
        ordersdf = pd.DataFrame(list(orders.values()))
        orders_id = set(ordersdf['orderId'])
        personal_trades_id = list(trades_id.difference(orders_id))
        # print(len(personal_trades_id))
        personal_trades = trades.filter(orderId__in=personal_trades_id)
        # print(personal_trades)

        results = self.paginate_queryset(personal_trades)
        serializer = TradeSerializer(data=results, many=True)

        if personal_trades.exists():
            return self.get_paginated_response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)


class TotalStopLoss(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Profile.objects.get(user_id=1)

    def list(self, request, *args, **kwargs):
        secretlist = []
        userstrat = UserStrategy.objects.select_related("secret").filter(Q(isActive=False) & \
                                                                            Q(secret__profile__isEnable=True) & \
                                                                            Q(secret__profile__isActive=True))
        # print('userstrat:', userstrat)
        for strat in userstrat:
            secretlist.append(
                {
                    "secret_id": strat.secret.id,
                    "symbol":    strat.symbol,
                    "totallSL":  strat.totallSL,
                    "margin" : strat.margin,
                    "size" : strat.size,
                    "strategy_id": strat.id,
                    "apiKey":    decrypt(strat.secret.apiKey, APIKEYPASS),
                    "secretKey": decrypt(strat.secret.secretKey, SECKEYPASS)
                }
            )
            print(strat.id)
            # orders_qs = Order.objects.filter(strategy_id=strat.id, tardeMatched=False, )
            # print(orders_qs)
        print('secretlist: ',secretlist)
        # for secret in secretlist:
        #     binance = Binance(
        #                 secret["apiKey"],
        #                 secret["secretKey"]
        #     )
            # secret["current_balances"] = float(binance.futuresBalance()[6]['balance'])
        #     # print(secret["current_balances"])
        #     secret.pop("apiKey")
        #     secret.pop("secretKey")

        #     if secret["current_balances"] * (1 - (secret["totalSL"] + secret["totalSL"] * 1.2)) < secret["margin"]:
        #         pass
        # print(secretlist)
        

    #     initial_balance = WalletBalance.objects.

    #     serializer = WalletBalanceSerializer(data=balanceList, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
        # print(self.get_queryset())
        # print('\n\n',userstrat)

        return Response([], status=status.HTTP_200_OK)


class UserInfo(views.APIView):
    permission_classes=[AllowAny, ]

    def get(self, request):
        query = Person.objects.all().order_by('id')
        data=[]
        # qs_json = serializers.serialize('json', query)
        # print(qs_json)
        for item in query:
            print('========================')
            print(item.id)
            print(item.name)
            print(item.email)
            print(str(item.phone.national_number))
            print(item.comment)
            print('------------------------')
        return Response(data)
