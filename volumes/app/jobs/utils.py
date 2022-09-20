import os
from dotenv import load_dotenv
from cryptocode import decrypt


from trades.serializers import TradeSerializer, OrderSerializer, UnplanTradeSerializer
from binanceAPI.restapi import Binance
from trades.serializers import TradeSerializer, OrderSerializer, UnplanTradeSerializer
from orders.serializers import OrderSerializer, CanceledOrderSerializer
from binanceAPI.restapi import Binance
from userstrategies.models import UserStrategy
from events.serializers import EventSerializer


load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')



def saveResponse(response, userStrategyId, profileId):
    if "orderId" in response:
        response["profile"] = profileId
        response["strategy"] = userStrategyId
        response["avgPrice"] = float(response["avgPrice"])
        response["cumQty"] = float(response["cumQty"])
        response["cumQuote"] = float(response["cumQuote"])
        response["executedQty"] = float(response["executedQty"])
        response["origQty"] = float(response["origQty"])
        response["price"] = float(response["price"])
        response["stopPrice"] = float(response["stopPrice"])
        response["orderType"] = response["type"]
        response.pop("type")
        if "activatePrice" in response:
            response["activatePrice"] = float(response["activatePrice"])
        if "priceRate" in response:
            response["priceRate"] = float(response["priceRate"])
        serializer = OrderSerializer(data=response)
        print('serializer: ', serializer)
        print(serializer.is_valid(), '\n\n\n')
        if serializer.is_valid():
            serializer.save()
    else:
        data = {}
        if "msg" in response and \
                response["msg"] != 'The operation of cancel all open order is done.':
            try:
                symbol_res = UserStrategy.objects.get(id=userStrategyId)
                symbol = symbol_res.symbol
            except:
                symbol = 'BTCUSDT'
            data["symbol"] = symbol
            data["profile"] = profileId
            data["strategy"] = userStrategyId
            data["detail"] = str(response)
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
        else:
            try:
                symbol_res = UserStrategy.objects.get(id=userStrategyId)
                symbol = symbol_res.symbol
            except:
                symbol = 'BTCUSDT'
            data["symbol"] = symbol
            data["profile"] = profileId
            data["strategy"] = userStrategyId
            data["detail"] = str(response)
            serializer = CanceledOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()



def stop_all_orders(secret):
    pass
    apiKey    = decrypt(secret.apiKey, APIKEYPASS)
    secretKey = decrypt(secret.secretKey, SECKEYPASS)
    binance = Binance(apiKey, secretKey)
    res = binance.cancelAllOrders(secret.symbol)

def close_all_positions():
    pass

def deactivate_plan():
    pass