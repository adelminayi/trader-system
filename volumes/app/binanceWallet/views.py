import os
from tracemalloc import get_object_traceback
from dotenv import load_dotenv
from cryptocode import decrypt

from django.http import Http404
from requests import request

from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from rest_framework import viewsets


from keysecrets.models import Secret
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from binanceAPI.restapi import Binance
from binanceWallet.serializers import *
from orders.serializers import OrderSerializer, CanceledOrderSerializer
from events.serializers import EventSerializer
from userstrategies.models import UserStrategy
from userstrategies.serializers import UserStrategySerializer

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


class AccountStatus(APIView):
    """
    get status of account
    /binance/accountStatus/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.accountStatus()
        return Response(res, status=status.HTTP_200_OK)


class AccountAPIStatus(APIView):
    """
    get status of account API
    /binance/accountAPIStatus/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.accountAPIStatus()
        return Response(res, status=status.HTTP_200_OK)


class DepositHistory(APIView):
    """
    get coin deposit history
    /binance/depositHistory/<int:id>/<USDT>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, coin, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.depositHistory(coin)
        return Response(res, status=status.HTTP_200_OK)


class WithdrawHistory(APIView):
    """
    get coin deposit history
    /binance/withdrawHistory/<int:id>/<BTC>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, coin, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.withdrawHistory(coin)
        return Response(res, status=status.HTTP_200_OK)


class SpotCoins(APIView):
    """
    get Binance wallet coins
    /binance/spotCoins/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        try:
            myapikey = secret.get('apiKey')
            mysecretKey = secret.get('secretKey')
        except:
            raise Http404
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.spotCoins()
        return Response(res, status=status.HTTP_200_OK)


class FuturesBalance(APIView):
    """
    get Binance futures account balance
    /binance/futuresBalance/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.futuresBalance()
        return Response(res, status=status.HTTP_200_OK)


class MarketOrder(APIView):
    """
    send market order
    /binance/marketOrder/<int:id>/

    {'orderId': 64661052638, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'BnjxJXMBTlQ3YXUElZIJrd', 'price': '0', 'avgPrice': '0.00000',
     'origQty': '0.001', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False,
      'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False,
       'origType': 'MARKET', 'updateTime': 1658658646201}
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        userstratId = UserStrategy.objects.get(
            secret_id=secret.id, isActive=True)
        serializer = MarketOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance = Binance(apiKey, secretKey)
            res = binance.marketOrder(serializer.data["symbol"],
                                      serializer.data["side"],
                                      serializer.data["quantity"])
        saveResponse(response=res, userStrategyId=userstratId.id,
                     profileId=secret.profile_id)
        return Response(res, status=status.HTTP_200_OK)


class LimitOrder(APIView):
    """
    send limit order
    /binance/limitOrder/<int:id>/
    {"orderId":64674803757,"symbol":"BTCUSDT","status":"NEW","clientOrderId":"yYvYwoWFvKdfGtlIcqgHwk","price":10000.0,"avgPrice":0.0,"origQty":0.001,
    "executedQty":0.0,"cumQty":0.0,"cumQuote":0.0,"timeInForce":"GTC","reduceOnly":false,"closePosition":false,"side":"BUY","positionSide":"BOTH",
    "stopPrice":0.0,"workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1658665127800,"profile":4,"strategy":38,
    "orderType":"LIMIT"}
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        userstratId = UserStrategy.objects.get(
            secret_id=secret.id, isActive=True)
        serializer = LimitOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance = Binance(apiKey, secretKey)
            res = binance.limitOrder(serializer.data["symbol"],
                                     serializer.data["side"],
                                     serializer.data["quantity"],
                                     serializer.data["price"])
        saveResponse(response=res, userStrategyId=userstratId.id,
                     profileId=secret.profile_id)
        return Response(res, status=status.HTTP_200_OK)


class StopOrder(APIView):
    """
    send stop order
    /binance/stopOrder/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        serializer = SLTPSerializer(data=request.data)
        if serializer.is_valid():
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance = Binance(apiKey, secretKey)
            res = binance.stopOrder(serializer.data["symbol"],
                                    serializer.data["side"],
                                    serializer.data["quantity"],
                                    serializer.data["price"],
                                    serializer.data["stopPrice"],
                                    serializer.data["workingType"],
                                    serializer.data["priceProtect"])
        saveResponse(res.json(), secret['id'], secret['profile'])
        return Response(res, status=status.HTTP_200_OK)


class TakeProfitOrder(APIView):
    """
    send takeprofit order
    /binance/takeProfitOrder/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        serializer = SLTPSerializer(data=request.data)
        if serializer.is_valid():
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance = Binance(apiKey, secretKey)
            res = binance.takeProfitOrder(serializer.data["symbol"],
                                          serializer.data["side"],
                                          serializer.data["quantity"],
                                          serializer.data["price"],
                                          serializer.data["stopPrice"],
                                          serializer.data["workingType"],
                                          serializer.data["priceProtect"])
        saveResponse(res.json(), secret['id'], secret['profile'])
        return Response(res, status=status.HTTP_200_OK)


class Adel(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaa', secret.profile_id)
        return Response({'adel': 'minayi'})


class TrailStopOrder(APIView):
    """
    send trailStop order 
    /binance/trailStopOrder/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        serializer = TrailStopOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance = Binance(apiKey, secretKey)
            res = binance.trailStopOrder(serializer.data["symbol"],
                                         serializer.data["side"],
                                         serializer.data["quantity"],
                                         serializer.data["activationPrice"],
                                         serializer.data["callbackRate"],
                                         serializer.data["workingType"])
        # saveResponse(res.json(), secret['id'], secret['profile'])
        return Response(res, status=status.HTTP_200_OK)


class CurrentOrders(APIView):
    """
    get current positions
    /binance/currentOrders/<int:id>/?symbol=ETHUSDT
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        if symbol is None:
            raise APIException("insert parameter(symbol).")
        return symbol

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.currentOrders(queryset)
        return Response(res, status=status.HTTP_200_OK)


class CancelAllOrders(APIView):
    """
    close current positions
    /binance/cancelAllOrders/<int:id>/?symbol=ETHUSDT
    {
    "code": "200", 
    "msg": "The operation of cancel all open order is done."
    }
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        if symbol is None:
            raise APIException("insert parameter(symbol).")
        return symbol

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.cancelAllOrders(queryset)
        # saveResponse(res.json(), secret.id, secret.profile_id)
        return Response(res, status=status.HTTP_200_OK)


class CancelOrder(APIView):
    """
    close current positions
    /binance/cancelOrder/<int:id>/?symbol=ETHUSDT&orderId=123456
    {"orderId":64674803757,"symbol":"BTCUSDT","status":"CANCELED","clientOrderId":"yYvYwoWFvKdfGtlIcqgHwk","price":"10000","avgPrice":"0.00000",
    "origQty":"0.001","executedQty":"0","cumQty":"0","cumQuote":"0","timeInForce":"GTC","type":"LIMIT","reduceOnly":false,"closePosition":false,"side":"BUY","positionSide":"BOTH","stopPrice":"0","workingType":"CONTRACT_PRICE","priceProtect":false,"origType":"LIMIT","updateTime":1658666944586}
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        orderId = self.request.query_params.get('orderId')
        if ("symbol" and "orderId") is None:
            raise APIException("mandatory parameters(symbol,orderId).")
        return {"symbol": symbol, "orderId": orderId}

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.cancelOrder(queryset["orderId"],
                                  queryset["symbol"])
        return Response(res, status=status.HTTP_200_OK)


class CurrentPositions(APIView):
    """
    get current positions
    /binance/currentPositions/<int:id>/?symbol=ETHUSDT
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        if symbol is None:
            raise APIException("insert parameter(symbol).")
        return symbol

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.currentPositions(queryset)
        return Response(res, status=status.HTTP_200_OK)


class CloseCurrentPositions(APIView):
    """
    close current positions
    /binance/closeCurrentPositions/<int:id>/?symbol=ETHUSDT
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        if symbol is None:
            raise APIException("insert parameter(symbol).")
        return symbol

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        userstratId = UserStrategy.objects.get(
            secret_id=secret.id, isActive=True)
        # print(secret.id, secret.profile_id)
        queryset = self.get_queryset()
        # print(queryset)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.closeCurrentPositions(queryset)
        saveResponse(response=res, userStrategyId=userstratId.id,
                     profileId=secret.profile_id)
        # res = {'name':'adel'}
        return Response(res, status=status.HTTP_200_OK)


class ChangeMarginType(APIView):
    """
    change margin type
    /binance/changeMarginType/<int:id>/?symbol=ETHUSDT&marginType=ISOLATED
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = self.request.data
        if ("symbol" and "marginType") not in data.keys():
            raise APIException("mandatory parameters(symbol,marginType).")
        return data

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def put(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.changeMarginType(queryset["symbol"],
                                       queryset["marginType"])
        return Response(res, status=status.HTTP_200_OK)


class ChangeLeverage(APIView):
    """
    change leverage
    /binance/changeLeverage/<int:id>/?symbol=ETHUSDT&leverage=1
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = self.request.data
        if ("symbol" and "leverage") not in data.keys():
            raise APIException("mandatory parameters(symbol,leverage).")
        return data

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def put(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.changeLeverage(queryset["symbol"],
                                     queryset["leverage"])
        return Response(res, status=status.HTTP_200_OK)


class IsDualSidePosition(APIView):
    """
    send market order
    /binance/isDualSidePosition/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.isDualSidePosition()
        return Response(res, status=status.HTTP_200_OK)


class DualSidePosition(APIView):
    """
    close current positions
    /binance/dualSidePosition/<int:id>/?dualSidePosition=TRUE
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = self.request.data
        if "dualSidePosition" not in data.keys():
            raise APIException("insert parameter(dualSidePosition).")
        return data

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.dualSidePosition(queryset["dualSidePosition"])
        return Response(res, status=status.HTTP_200_OK)


class LastTrades(APIView):
    """
    close current positions
    /binance/lastTrades/<int:id>/?symbol=ETHUSDT&startTime=123456&endTime=123456&limit=200
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        startTime = self.request.query_params.get('startTime')
        endTime = self.request.query_params.get('endTime')
        limit = self.request.query_params.get('limit')
        if ("symbol" and "startTime" and "endTime" and "limit") is None:
            raise APIException(
                "mandatory parameters(symbol,startTime,endTime,limit).")
        return {
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "limit": limit
        }

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.futuresTrades(
            queryset["symbol"],
            queryset["startTime"],
            queryset["endTime"],
            queryset["limit"],
        )
        return Response(res, status=status.HTTP_200_OK)


class LastOrders(APIView):
    """
    close current positions
    /binance/lastOrders/<int:id>/?symbol=ETHUSDT&startTime=123456&endTime=123456&limit=200
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        startTime = self.request.query_params.get('startTime')
        endTime = self.request.query_params.get('endTime')
        limit = self.request.query_params.get('limit')
        if ("symbol" and "startTime" and "endTime" and "limit") is None:
            raise APIException(
                "mandatory parameters(symbol,startTime,endTime,limit).")
        return {
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "limit": limit
        }

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        secret = self.get_object(userId=request.user.id, id=id)
        queryset = self.get_queryset()
        apiKey = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance = Binance(apiKey, secretKey)
        res = binance.lastOrders(
            queryset["symbol"],
            queryset["startTime"],
            queryset["endTime"],
            queryset["limit"],
        )
        return Response(res, status=status.HTTP_200_OK)


class ClosePlanTrades(views.APIView):
    """
    close all users trades and orders with special plan
    :params: strategy_name
    """
    pass

class CloseUserOrders(views.APIView):
    """
    close all user orders
    :params:
        strategy: str
        userId: int
        symbol: str
    example: http://localhost:8000/binance/cancel/?strategy=D_Surfer
    """
    permission_classes = [AllowAny]

    def get_object(self):
        strategy = self.request.query_params.get('strategy')
        # print('strategy: ',strategy)
        if "strategy" == None:
            raise APIException("mandatory parameters(strategy).")
        return strategy

    def get_queryset(self, ):
        mystrategy= self.get_object()
        try:
            return UserStrategy.objects.filter(strategy=mystrategy)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """
        just to test get_queryset
        """
        qs= self.get_queryset()
        # print('query set', qs,'\n\n')
        for item in qs:
            symbol = item.symbol
            # print('secret_id ==', item.secret.id)
            secret = Secret.objects.get(id=item.secret.id)
            # print('symbol:',symbol)
            # print('secret:',secret)
            apiKey = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            # print(secret.apiKey)
            # print(secret.secretKey)
            # print('strat id :',item.id)
            # print('profile id:', item.secret.profile_id)
            binance = Binance(apiKey, secretKey)
            cancel_orders = binance.CancelAllOrders(symbol)
            close_positions = binance.closeCurrentPositions(symbol)
            saveResponse(response=close_positions, userStrategyId=item.id,
                     profileId=secret.profile_id)




        ss=self.request.query_params.get('strategy')
        return Response([ss])