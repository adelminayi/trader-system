import os
import pandas as pd
import datetime
import gspread
import json
import datetime


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
from jobs.utils import saveResponse

from userstrategies.models import UserStrategy
from balance.models import WalletBalance
from draft.models import Person


load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')
CREDENTIALS=os.getenv('CREDENTIALS')

def onlyTestCron():
    print(datetime.datetime.now(), ' just test crontab!')


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

    print('balace saved at :', datetime.datetime.now())

def trades():
    print(datetime.datetime.now(), ' Im in trades crontab.')
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
        try:
            print('serializer data :\n',data)
        except:
            print('cant print serializer.data')
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
        print('get balance at {} for wallet name : {}'.format(datetime.datetime.now(), secret.walletName))
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
        print(datetime.datetime.now(), 'save on db success.\n\n')

def user_trades():
    print(datetime.datetime.now(), ' Im in trades crontab.')
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
        try:
            print('serializer data :\n',data)
        except:
            print('cant print serializer.data')
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
    

def total_stoploss():
    secretlist = []
    userstrat = UserStrategy.objects.select_related("secret").filter(Q(isActive=True) & \
                                                                        Q(secret__profile__isEnable=True) & \
                                                                        Q(secret__profile__isActive=True))
    # print('userstrat:', userstrat)
    for strat in userstrat:
        secretlist.append(
            {
                "profile_id": strat.secret.profile_id,
                "secret_id": strat.secret.id,
                "strategy_id": strat.id,
                "symbol":    strat.symbol,
                "totallSL":  strat.totallSL,
                "margin" : strat.margin,
                "size" : strat.size,
                "apiKey":    decrypt(strat.secret.apiKey, APIKEYPASS),
                "secretKey": decrypt(strat.secret.secretKey, SECKEYPASS)
            }
        )
        # orders_qs = Order.objects.filter(strategy_id=strat.id , tardeMatched = False)
        # print(len(orders_qs))
    # print('secretlist: ',secretlist)

    for secret in secretlist:
        binance = Binance(secret["apiKey"],secret["secretKey"])
        secret["current_balances"] = float(binance.futuresBalance()[6]['balance'])
        # print(secret["current_balances"])
        secret.pop("apiKey")
        secret.pop("secretKey")

        if secret["current_balances"] * (1 - (secret["totalSL"] + secret["totalSL"] * 1.2)/100) < secret["margin"]:
            pass
        # close all orders
        order_res = binance.cancelAllOrders(secret['symbol'])
        # close all positions
        positions_res = binance.CloseCurrentPositions(secret['symbol'])
        saveResponse(response=positions_res, userStrategyId=secret['strategy_id'],
                    profileId=secret['profile_id'])
    # return Response(secretlist, status=status.HTTP_200_OK)

def make_user_data():
    query = UserStrategy.objects.filter(isActive=True)
    result =[]
    for item in query:
        data=[item.secret.profile.user.username,
            item.secret.profile.user.first_name,
            item.secret.profile.user.last_name,
            item.secret.profile.user.date_joined,
            item.secret.profile.isActive,
            item.secret.profile.user.email,
            str(item.secret.profile.cellPhoneNumber),
            item.strategy,
            WalletBalance.objects.filter(secret=item.secret.id).latest('id').balance,
            ]
        result.append(data)

    return result

def users_status():
    credentials=json.loads(CREDENTIALS)
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key("1NhEW9CDykKkIgF3Tqj5WuTE7jGTrreWuQCijdjGjJ-k")
    worksheet = sh.worksheet("UsersInfo")
    worksheet.clear()
    try:
        print('Enter try')
        worksheet.insert_row(values= ['userName', 'firstName', 'lastName', 'dateOfJoin', 'isActive', 'email', 'phone', 'strategyName', 'Balance'])
        # worksheet.format('A1:E1', 
        #         {'textFormat': {'bold': True},
        #         })
        data = make_user_data()
        worksheet.insert_rows(row=2, values= data)
    except:
        print('faild to write')

def PreRegisterInfo():
    query = Person.objects.all()
    result =[]
    for item in query:
        data=[
            item.name,
            item.email,
            str(item.phone.national_number),
            item.comment,
        ]
        result.append(data)
        
    credentials=json.loads(CREDENTIALS)
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key("1NhEW9CDykKkIgF3Tqj5WuTE7jGTrreWuQCijdjGjJ-k")
    worksheet = sh.worksheet("PreRegistered")
    worksheet.clear()
    try:
        print('Enter Try at:', datetime.datetime.now())
        worksheet.insert_row(values=['Name', 'Phone', 'Email', 'Comment'])
        print(result)
        worksheet.insert_rows(row=2, values= result)
    except:
        print( datetime.datetime.now(),': Failed to write')
