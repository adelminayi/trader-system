import os
from dotenv import load_dotenv
from cryptocode import decrypt

from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from keysecrets.models import Secret
from binanceAPI.restapi import Binance
from binanceWallet.serializers import *



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.accountStatus()
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.accountAPIStatus()
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.depositHistory(coin)
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.withdrawHistory(coin)
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.spotCoins()
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.futuresBalance()
        return Response(res, status=status.HTTP_200_OK)


class MarketOrder(APIView):
    """
    send market order
    /binance/marketOrder/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret    = self.get_object(userId=request.user.id, id=id)
        serializer= MarketOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey    = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance   = Binance(apiKey, secretKey)
            res       = binance.marketOrder(serializer.data["symbol"],
                                            serializer.data["side"],
                                            serializer.data["quantity"])
        return Response(res, status=status.HTTP_200_OK)


class LimitOrder(APIView):
    """
    send limit order
    /binance/limitOrder/<int:id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        secret    = self.get_object(userId=request.user.id, id=id)
        serializer= LimitOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey    = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance   = Binance(apiKey, secretKey)
            res       = binance.limitOrder(serializer.data["symbol"],
                                        serializer.data["side"],
                                        serializer.data["quantity"],
                                        serializer.data["price"])
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
        secret    = self.get_object(userId=request.user.id, id=id)
        serializer= SLTPSerializer(data=request.data)
        if serializer.is_valid():
            apiKey    = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance   = Binance(apiKey, secretKey)
            res       = binance.stopOrder(serializer.data["symbol"],
                                        serializer.data["side"],
                                        serializer.data["quantity"],
                                        serializer.data["price"],
                                        serializer.data["stopPrice"],
                                        serializer.data["workingType"],
                                        serializer.data["priceProtect"])
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
        secret    = self.get_object(userId=request.user.id, id=id)
        serializer= SLTPSerializer(data=request.data)
        if serializer.is_valid():
            apiKey    = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance   = Binance(apiKey, secretKey)
            res       = binance.takeProfitOrder(serializer.data["symbol"],
                                                serializer.data["side"],
                                                serializer.data["quantity"],
                                                serializer.data["price"],
                                                serializer.data["stopPrice"],
                                                serializer.data["workingType"],
                                                serializer.data["priceProtect"])
        return Response(res, status=status.HTTP_200_OK)


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
        secret    = self.get_object(userId=request.user.id, id=id)
        serializer= TrailStopOrderSerializer(data=request.data)
        if serializer.is_valid():
            apiKey    = decrypt(secret.apiKey, APIKEYPASS)
            secretKey = decrypt(secret.secretKey, SECKEYPASS)
            binance   = Binance(apiKey, secretKey)
            res       = binance.trailStopOrder(serializer.data["symbol"],
                                            serializer.data["side"],
                                            serializer.data["quantity"],
                                            serializer.data["activationPrice"],
                                            serializer.data["callbackRate"],
                                            serializer.data["workingType"])
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.currentOrders(queryset)
        return Response(res, status=status.HTTP_200_OK)


class CancelAllOrders(APIView):
    """
    close current positions
    /binance/cancelAllOrders/<int:id>/?symbol=ETHUSDT
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.cancelAllOrders(queryset)
        return Response(res, status=status.HTTP_200_OK)


class CancelOrder(APIView):
    """
    close current positions
    /binance/cancelOrder/<int:id>/?symbol=ETHUSDT&orderId=123456
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol  = self.request.query_params.get('symbol')
        orderId = self.request.query_params.get('orderId')
        if ("symbol" and "orderId") is None:
            raise APIException("mandatory parameters(symbol,orderId).") 
        return {"symbol":symbol,"orderId":orderId}

    def get_object(self, userId, id):
        try:
            return Secret.objects.get(profile__user__id=userId, id=id)
        except Secret.DoesNotExist:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.cancelOrder(queryset["symbol"],
                                        queryset["orderId"])
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.currentPositions(queryset)
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.closeCurrentPositions(queryset)
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.changeMarginType(queryset["symbol"],
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.changeLeverage(queryset["symbol"],
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
        secret    = self.get_object(userId=request.user.id, id=id)
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.isDualSidePosition()
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.dualSidePosition(queryset["dualSidePosition"])
        return Response(res, status=status.HTTP_200_OK)


class LastTrades(APIView):
    """
    close current positions
    /binance/lastTrades/<int:id>/?symbol=ETHUSDT&startTime=123456&endTime=123456&limit=200
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        symbol    = self.request.query_params.get('symbol')
        startTime = self.request.query_params.get('startTime')
        endTime   = self.request.query_params.get('endTime')
        limit     = self.request.query_params.get('limit')
        if ("symbol" and "startTime" and "endTime" and "limit") is None:
            raise APIException("mandatory parameters(symbol,startTime,endTime,limit).") 
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.futuresTrades(
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
        symbol    = self.request.query_params.get('symbol')
        startTime = self.request.query_params.get('startTime')
        endTime   = self.request.query_params.get('endTime')
        limit     = self.request.query_params.get('limit')
        if ("symbol" and "startTime" and "endTime" and "limit") is None:
            raise APIException("mandatory parameters(symbol,startTime,endTime,limit).") 
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
        secret    = self.get_object(userId=request.user.id, id=id)
        queryset  = self.get_queryset()
        apiKey    = decrypt(secret.apiKey, APIKEYPASS)
        secretKey = decrypt(secret.secretKey, SECKEYPASS)
        binance   = Binance(apiKey, secretKey)
        res       = binance.lastOrders(
                                queryset["symbol"],
                                queryset["startTime"],
                                queryset["endTime"],
                                queryset["limit"],
                    )
        return Response(res, status=status.HTTP_200_OK)