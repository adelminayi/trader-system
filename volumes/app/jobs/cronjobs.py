import os
import numpy as np
import pandas as pd

from cryptocode import decrypt
from dotenv import load_dotenv

from django.db.models import Q
from balance.models import WalletBalance

from balance.serializers import BalanceSerializer, WalletBalanceSerializer
from trades.serializers import TradeSerializer, UnplanTradeSerializer
from trades.models import Trade, UnplanTrade
from orders.models import Order
from keysecrets.models import Secret
from binanceAPI.restapi import Binance
from userstrategies.models import UserStrategy



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


def balances():
    tradesList = []
    trades = Trade.objects.select_related("strategy__secret")
    for trade in trades:
        tradesList.append(
            {
                "profile": trade.profile.id,
                "strategy": trade.strategy.id,
                "symbol": trade.symbol,
                "margin": trade.strategy.margin,
                "pnl": trade.realizedPnl
                     - trade.commission
            }
        )
    tradesdf = pd.DataFrame(tradesList).groupby(["profile","strategy","symbol","margin"]).sum().reset_index()
    tradesdf['balance'] = tradesdf["margin"]+tradesdf["pnl"]
    data = tradesdf.drop(columns=["pnl"]).to_dict("records")

    serializer = BalanceSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()


def trades():
    orderList = []
    tardesdf  = pd.DataFrame([], columns=['buyer','commission','commissionAsset','id','maker',
                                          'marginAsset','orderId','positionSide','price','qty',
                                          'quoteQty','realizedPnl','side','symbol','time', 'secret'])
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
    orderdf  = pd.DataFrame(orderList).drop(["apiKey","secretKey","secret","symbol"], axis=1).sort_values(by=["orderId"])

    secrets  = pd.DataFrame(orderList).groupby(["apiKey","secretKey","symbol","secret"]).agg(['unique'])\
                                      .drop(["profile","strategy","orderId"], axis=1)\
                                      .to_dict('split')["index"]

    secretList = []
    for secret in secrets:
        secretList.append((decrypt(secret[0], APIKEYPASS), decrypt(secret[1], SECKEYPASS), secret[2], secret[3]))
    
    secrets = secretList

    dfList = [tardesdf,]
    for secret in secrets:
        binance   = Binance(secret[0], secret[1])
        resdf     = pd.DataFrame(binance.lastTrades(secret[2], "20"))
        resdf['secret'] = secret[3]
        dfList.append(resdf)
    tardesdf  = pd.concat(dfList, ignore_index=True)

    tardesdf = tardesdf.sort_values(by=["orderId"])

    finaldf  = pd.merge(tardesdf, orderdf, how = 'inner', on = 'orderId')
    finaldf.rename(columns={"id": "tradeId"}, inplace=True)
    finaldf.drop(columns=['secret'], inplace=True)

    orderIds = finaldf["orderId"].tolist()

    data = finaldf.to_dict("records")

    serializer = TradeSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        Order.objects.filter(orderId__in=orderIds).update(tardeMatched=True)

    unplanTradesdf = pd.merge(tardesdf, orderdf, how = 'left', on = 'orderId')
    unplanTradesdf.rename(columns={"id": "tradeId"}, inplace=True)
    unplanTradesdf = unplanTradesdf[unplanTradesdf['strategy'].isna()]
    unplanTradesdf.drop(columns=['profile','strategy'], inplace=True)

    data = unplanTradesdf.to_dict("records")

    serializer = UnplanTradeSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()

    

def totaltrades():
    from pymongo import MongoClient
    myclient    = MongoClient("mongodb://ayat:amir1374@192.168.11.66:27017/")
    db          = myclient["BinanceUsers"]
    collection  = db["trades"]
    
    secretlist = []
    tardesdf  = pd.DataFrame([], columns=['secretid','profile','walletName',
                                          'buyer','commission','commissionAsset','id','maker',
                                          'marginAsset','orderId','positionSide','price','qty',
                                          'quoteQty','realizedPnl','side','symbol','time'])
    userstrat = UserStrategy.objects.select_related("secret")
    for strat in userstrat:
        secretlist.append(
            {
                # "profile_id":   strat.secret.profile.id,
                # "walletName":   strat.secret.walletName,
                "strat_id":  strat.id,
                "secret_id": strat.secret.id,
                "symbol":    strat.symbol,
                "apiKey":    decrypt(strat.secret.apiKey, APIKEYPASS),
                "secretKey": decrypt(strat.secret.secretKey, SECKEYPASS)
            }
        )
    dfList = [tardesdf,]
    for secret in secretlist:
        binance             = Binance(secret['apiKey'], secret['secretKey'])
        resdf               = pd.DataFrame(binance.lastTrades(secret['symbol'], "20"))
        resdf['secretid']   = secret['secretid'] 
        resdf['profile']    = secret['profile'] 
        # resdf['profile']    = secret['profile'] 
        # resdf['walletName'] = secret['walletName'] 
        dfList.append(resdf)
    tardesdf  = pd.concat(dfList, ignore_index=True)
    tardesdf.rename(columns={"id": "tradeId"}, inplace=True)

    data = tardesdf.to_dict("records")
    collection.insert_many(data,ordered=False)


def walletbalances():
    balanceList = []
    secrets = Secret.objects.all()
    for secret in secrets:
        binance = Binance(
                    decrypt(secret.apiKey, APIKEYPASS), 
                    decrypt(secret.secretKey, SECKEYPASS)
        )
        res = binance.futuresBalance()
        balances = [{'asset': b['asset'], 'balance': b['balance']} for b in res if b['balance']!="0.00000000"]
        for bal in balances:
            balanceList.append(
                {
                    "profile": secret.profile.id,
                    "secret": secret.id,
                    "asset": bal["asset"],
                    "balance": bal["balance"]
                }
            )

    serializer = WalletBalanceSerializer(data=balanceList, many=True)
    if serializer.is_valid():
        serializer.save()


# def totalsl():
#     secretlist = []
#     userstrat = UserStrategy.objects.select_related("secret").filter(Q(isActive=True) & \
#                                                                     Q(secret__profile__isEnable=True) & \
#                                                                     Q(secret__profile__isActive=True))
#     for strat in userstrat:
#         secretlist.append(
#             {
#                 "secret_id": strat.secret.id,
#                 # "symbol":    strat.symbol,
#                 "totallSL":  strat.totallSL,
#                 "apiKey":    decrypt(strat.secret.apiKey, APIKEYPASS),
#                 "secretKey": decrypt(strat.secret.secretKey, SECKEYPASS)
#             }
#         )
#     for secret in secretlist:
#         binance = Binance(
#                     secret["apiKey"],
#                     secret["secretKey"]
#         )
#         secret["current_balances"] = float(binance.futuresBalance()[6]['balance'])
#         secret.pop["apiKey"]
#         secret.pop["secretKey"]

#     initial_balance = WalletBalance.objects.

#     serializer = WalletBalanceSerializer(data=balanceList, many=True)
#     if serializer.is_valid():
#         serializer.save()

    
    
                                    