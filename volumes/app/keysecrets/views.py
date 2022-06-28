import time
from jsonschema import validate

from django.http import Http404, HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 

from keysecrets.serializers import SecretSerializer
from keysecrets.models import Secret
from profiles.models import Profile
from binanceAPI.restapi import Binance
# from balance.models import WalletBalance
from binanceAPI.schema import apiKeyPermissionSchema


class Adel(APIView):
    permission_classes=[IsAuthenticated]

    def get (self, request, *args, **kwargs):
        query = Secret.objects.filter(profile=5)
        print(query)
        return HttpResponse({'condition': 'true'})


class UserSecret(APIView):
    """
    get all secrets or create 
    /secrets/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_id(self, userId):
        try:
            return Profile.objects.get(user__id=userId).id
        except Profile.DoesNotExist:
            raise Http404

    def get_object(self, userId):
        return Secret.objects.filter(profile__user__id=userId)

    def get(self, request, *args, **kwargs):
        secrets = self.get_object(userId=request.user.id)
        serializer = SecretSerializer(secrets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['profile'] = self.get_id(userId=request.user.id)
        data['uniquesign'] = "1234567898766379"
        # print('data views: \n', data)
        serializer = SecretSerializer(data=data)
        # print('\n\nserializer:\n ',serializer,'\n\n')
        if serializer.is_valid():
            binance = Binance(data["apiKey"],data["secretKey"])
            # print('binance 60:\n', binance,'\n')
            try:
                binanceResponse = binance.apiKeyPermission()
            except:
                return Response(binanceResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            # print('binace response :\n',binanceResponse,'\n')
            try:
                validate(binanceResponse, apiKeyPermissionSchema)
                if binanceResponse["enableFutures"]==False:
                    return Response({"detail":"Futures traiding must be enable."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif binanceResponse["enableReading"]==False:
                    return Response({"detail":"Reading must be enable."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif "tradingAuthorityExpirationTime"in binanceResponse and binanceResponse["tradingAuthorityExpirationTime"]<time.time()*1000:
                    return Response({"detail":"Expired api key."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                return Response(binanceResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
            # try:
            #     balance = float(binance.futuresBalance()[6]['balance'])
            #     walletbalance = WalletBalance(profile="",)
            # except:
            #     pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSecretReform(APIView):
    """
    get-patch-delete specific secret 
    /secrets/<secret_id>/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_id(self, userId):
        try:
            return Profile.objects.get(user__id=userId).id
        except Secret.DoesNotExist:
            raise Http404

    def get_object(self, pk, userId):
        try:
            return Secret.objects.filter(profile__user__id=userId).get(pk=pk)
        except Secret.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        secrets = self.get_object(pk=pk, userId=request.user.id)
        serializer = SecretSerializer(secrets)
        return Response(serializer.data)
    
    def patch(self, request, pk, *args, **kwargs):
        secrets = self.get_object(pk, request.user.id)
        data = request.data   
        if ("apiKey" in data and "secretKey" not in data) or \
            ("secretKey" in data and "apiKey" not in data):
            return Response(
                {"detail": "both apiKey and secretKey are required."}, 
                status=status.HTTP_406_NOT_ACCEPTABLE
                )
        data['profile'] = self.get_id(request.user.id)
        serializer = SecretSerializer(secrets, data=data, partial=True)
        if serializer.is_valid():
            try:
                binance = Binance(data["apiKey"],data["secretKey"])
            except:
                return Response(
                {"detail": "both apiKey and secretKey are required."}, 
                status=status.HTTP_406_NOT_ACCEPTABLE
                )
            # print('binance 60:\n', binance,'\n')
            try:
                binanceResponse = binance.apiKeyPermission()
            except:
                return Response(binanceResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            # print('binace response :\n',binanceResponse,'\n')
            try:
                validate(binanceResponse, apiKeyPermissionSchema)
                if binanceResponse["enableFutures"]==False:
                    return Response({"detail":"Futures traiding must be enable."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif binanceResponse["enableReading"]==False:
                    return Response({"detail":"Reading must be enable."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif "tradingAuthorityExpirationTime"in binanceResponse and binanceResponse["tradingAuthorityExpirationTime"]<time.time()*1000:
                    return Response({"detail":"Expired api key."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                return Response(binanceResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        secrets = self.get_object(pk, request.user.id)
        secrets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)