import os

from django.http import Http404
from django.db.models import Sum

from cryptocode import decrypt
from dotenv import load_dotenv

from rest_framework import status, viewsets
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAcceptable

from binanceAPI.restapi import Binance
from keysecrets.models import Secret
from userstrategies.models import UserStrategy
from userstrategies.serializers import UserStrategySerializer



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class UserStrategyView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserStrategySerializer

    def get_queryset(self, id=None):
        userId = self.request.user.id

        if id:
            if self.request.method=="POST":
                try:
                    Secret.objects.get(profile__user__id=userId,id=id)
                    return id
                except Secret.DoesNotExist:
                    raise Http404
            else:
                try:
                    return UserStrategy.objects.get(secret__profile__user__id=userId,id=id)
                except UserStrategy.DoesNotExist:
                    raise Http404
        return UserStrategy.objects.filter(secret__profile__user__id=userId)

    def list(self, request):
        userstrat = self.get_queryset()
        serializer = self.get_serializer(userstrat, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        userstrat = self.get_queryset(id=id)
        serializer = self.get_serializer(userstrat)
        return Response(serializer.data)

    def create(self, request, id):
        """
        {
    "strategy":"D Surfer (TRX)",
    "symbols":["XRPUSDT", "ETHUSDT"],
    "margin":50,
    "size":30,
    "totallSL":5,
    "risk":5,
    "baseCurrency":"USDT",
    "leverage":1,
    "marginType":"ISOLATED",
    "positionMode":"One-way",
    "timeInForce":"GTC",
    "workingType":"CONTRACT_PRICE",
    "priceProtect":"TRUE",
    "secret":1,
    "isActive":true}
    """

        data = request.data
        data['secret'] = self.get_queryset(id=id)
        serializer = self.get_serializer(data=data)
        print('\ndata----------- :', data, '---------\n')
        print('\nserializer +++++++++++:', serializer, '+++++++++++\n')
        if serializer.is_valid():
            if data['isActive']==True and \
                UserStrategy.objects.filter(secret=data['secret'], symbols=data['symbols'], isActive=True).count()>0:
                raise NotAcceptable(detail="Two strategies on same secret and symbol are not acceptable!", code=406)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, id):
        userstrat = self.get_queryset(id=id)
        secret_id = userstrat.secret.id
        symbol = userstrat.symbol
        data = request.data 
        serializer = self.get_serializer(userstrat, data=data, partial=True)
        if serializer.is_valid():
            print('\ndata:\n',data)
            if "margin" in data:
                userstrat.isActive=False
                # UserStrategy.objects.create(
                #                         secret = userstrat.secret,
                #                         margin=data['margin'],
                #                         strategy = userstrat.strategy,
                #                         symbol = userstrat.symbol,
                #                         totallSL = userstrat.totallSL,
                #                         size = userstrat.size,
                #                         baseCurrency = userstrat.baseCurrency,
                #                         leverage = userstrat.leverage,
                #                         marginType = userstrat.marginType,
                #                         positionMode = userstrat.positionMode,
                #                         timeInForce = userstrat.timeInForce,
                #                         workingType = userstrat.workingType,
                #                         priceProtect = userstrat.priceProtect,
                #                         isActive = True
                #                         )
                UserStrategy.objects.create(
                                        secret = userstrat.secret,
                                        margin=data['margin'],
                                        strategy = data['strategy'],
                                        symbol = data['symbol'],
                                        totallSL = data['totallSL'],
                                        size = data['size'],
                                        baseCurrency = data['baseCurrency'],
                                        leverage = data['leverage'],
                                        marginType = data['marginType'],
                                        positionMode = data['positionMode'],
                                        timeInForce = data['timeInForce'],
                                        workingType = data['workingType'],
                                        priceProtect = data['priceProtect'],
                                        isActive = True
                                        )
                userstrat.save()
                return Response(serializer.data)
            serializer.save()

            if "isActive" in data:
                if data['isActive']==True and \
                    UserStrategy.objects.filter(secret=secret_id, symbol=symbol, isActive=True).exclude(id=userstrat.id).count()>0:
                    raise NotAcceptable(detail="Two strategies on same secret and symbol are not acceptable!", code=406)
                posList = []
                ordList = []
                secret = Secret.objects.get(id=secret_id)
                binance = Binance(
                            decrypt(secret.apiKey, APIKEYPASS), 
                            decrypt(secret.secretKey, SECKEYPASS)
                )
                currentPos = binance.currentPositions(symbol)
                currentOrd = binance.currentOrders(symbol)
                if currentPos[0]['positionAmt'] != '0.000':
                    posList.extend(currentPos)
                ordList.extend(currentOrd)
                numpos = len(posList)
                numord = len(ordList)
                if numpos!=0 or numord!=0:
                    return Response({"detail": 
                                    f"You have {numpos} open position(s) and {numord} open order(s) on this plan."}, 
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        userstrat = self.get_queryset(id=id)
        userstrat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailableMarginView(viewsets.GenericViewSet):
    """
    get availble margin
    GET:
        /userstrategy/availmargin/<asset>/<secret_id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
            
    def retrieve(self, request, asset, id):
        userId = self.request.user.id
        secret = Secret.objects.get(id=id)
        balancein = UserStrategy.objects.filter(
                                        secret__profile__user__id=userId,
                                        isActive=True,
                                        ).aggregate(balance=Sum('margin'))['balance']
        if balancein is None:
            balancein = 0
        binance = Binance(
                    decrypt(secret.apiKey, APIKEYPASS), 
                    decrypt(secret.secretKey, SECKEYPASS)
        )
        res = binance.futuresBalance()
        for balance in res:
            if balance['asset'] == asset:
                avalmargin = (float(balance['balance'])-balancein)
                return Response(avalmargin, status=status.HTTP_200_OK)
        
        return Response({"detail": "Not a valid asset!"}, status=status.HTTP_400_BAD_REQUEST)


# class CurrentStatusView(viewsets.GenericViewSet):
#     """
#     get availble margin
#     GET:
#         /userstrategy/CurrentStatus/<secret_id>/
#     """
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         pass
            
#     def list(self, request, secret_id):
#         currentList   = []
#         userId = self.request.user.id
#         secret = Secret.objects.get(id=secret_id)
#         plans = UserStrategy.objects.filter(
#                                         secret__profile__user__id=userId,
#                                         secret=secret_id,
#                                         )
#         binance = Binance(
#                     decrypt(secret.apiKey, APIKEYPASS), 
#                     decrypt(secret.secretKey, SECKEYPASS)
#             )
#         for plan in plans:
#             currentPos = binance.currentPositions(plan.symbol)
#             currentOrd = binance.currentPositions(plan.symbol)
#             currentList.append(currentPos)
#             currentList.append(currentOrd)
      
#         return Response(currentList, status=status.HTTP_200_OK)


class CurrentStatusView(viewsets.GenericViewSet):
    """
    get availble margin
    GET:
        /userstrategy/CurrentStatus/<secret_id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
            
    def retrieve(self, request, secret_id):
        posList = []
        ordList = []
        userId = self.request.user.id
        secret = Secret.objects.get(id=secret_id)
        plans = UserStrategy.objects.filter(
                                        secret__profile__user__id=userId,
                                        secret=secret_id,
                                        )
        binance = Binance(
                    decrypt(secret.apiKey, APIKEYPASS), 
                    decrypt(secret.secretKey, SECKEYPASS)
            )
        for plan in plans:
            currentPos = binance.currentPositions(plan.symbol)
            currentOrd = binance.currentOrders(plan.symbol)
            posList.extend(currentPos)
            ordList.extend(currentOrd)
      
        return Response({"positions": posList, "orders": ordList}, status=status.HTTP_200_OK)
        


class UserStrategyPrepareView(viewsets.GenericViewSet):
    """
    strategy-panel items
    get/list-post-patch-delete
    POST:
        /userstrategy/<userstrategy_id>/prepare/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserStrategySerializer

    def get_queryset(self, id=None):
        userId = self.request.user.id
        try:
            return UserStrategy.objects.get(secret__profile__user__id=userId,id=id)
        except UserStrategy.DoesNotExist:
            raise Http404

    def create(self, request, id):
        userstrat = self.get_queryset(id=id)
        secret_id = userstrat.secret.id
        symbol = userstrat.symbol
        secret = Secret.objects.get(id=secret_id)
        binance = Binance(
                        decrypt(secret.apiKey, APIKEYPASS), 
                        decrypt(secret.secretKey, SECKEYPASS)
        )
        currentPos = binance.cancelAllOrders(symbol)
        currentOrd = binance.closeCurrentPositions(symbol)
        return Response({"detail":"Done!"}, status=status.HTTP_200_OK)