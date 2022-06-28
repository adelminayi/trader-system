import os

from dotenv import load_dotenv
from cryptocode import decrypt

from profiles.models import Profile
from userstrategies.models import UserStrategy
from total.serializers import TotalSerializer, UserProfileSerializer, SecretStrategySerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class UserTotalView(APIView):
    """
    test
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TotalSerializer

    def get(self, request):
        userprofile = {}
        secretstrat = {}
        userId = self.request.user.id
        userprofilequeryset = Profile.objects.select_related("user").filter(user__id=userId)
        for up in userprofilequeryset:
            userprofile = {
                "username"                    : up.user.username,
                "first_name"                  : up.user.first_name,
                "last_name"                   : up.user.last_name,
                "email"                       : up.user.email,
                "is_superuser"                : up.user.is_superuser,
                "is_staff"                    : up.user.is_staff,
                "is_active"                   : up.user.is_active,
                "date_joined"                 : up.user.date_joined,
                "last_login"                  : up.user.last_login,
                "image"                       : up.image,
                "dateOfBirth"                 : up.dateOfBirth,
                "address"                     : up.address,
                "addressVerified"             : up.addressVerified,
                "cellPhoneNumber"             : up.cellPhoneNumber,
                "cellPhoneNumberVerified"     : up.cellPhoneNumberVerified,
                "landingPhoneNumber"          : up.landingPhoneNumber,
                "landingPhoneNumberVerified"  : up.landingPhoneNumberVerified,
                "signedContract"              : up.signedContract,
                "payedMemmber"                : up.payedMemmber,
                "expirationTime"              : up.expirationTime,
                "isEnable"                    : up.isEnable,
                "createTime"                  : up.createTime,
                "isActive"                    : up.isActive,
            }
        secretstratqueryset = UserStrategy.objects.select_related("secret").filter(secret__profile__user__id=userId)
        for ss in secretstratqueryset:
            secretstrat = {
                "walletName"      : ss.secret.walletName,
                "apiKey"          : ss.secret.apiKey,
                "secretKey"       : ss.secret.secretKey,
                "createTime"      : ss.secret.createTime,
                "strategy"        : ss.strategy,
                "symbol"          : ss.symbol,
                "margin"          : ss.margin,
                "totallSL"        : ss.totallSL,
                "size"            : ss.size,
                "isActive"        : ss.isActive,
                "baseCurrency"    : ss.baseCurrency,
                "leverage"        : ss.leverage,
                "marginType"      : ss.marginType,
                "positionMode"    : ss.positionMode,
                "timeInForce"     : ss.timeInForce,
                "workingType"     : ss.workingType,
                "priceProtect"    : ss.priceProtect,
                "createTime"      : ss.createTime,
                "deactivateTime"  : ss.deactivateTime,
            }
        # userprofile = UserProfileSerializer(data=userprofile)
        # secretstrat = SecretStrategySerializer(data=secretstrat)
        # if userprofile.is_valid():
        #     pass
        # if secretstrat.is_valid():
        #     pass

        # queryset = [
        #     {
        #         "userprofile": userprofile.data, 
        #         "secretstrategy": secretstrat.data
        #     }
        # ]
        # serializer = TotalSerializer(data=queryset)
        # if serializer.is_valid():
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        data.update(userprofile)
        data.update(secretstrat)
        queryset = TotalSerializer(data=data)
        if queryset.is_valid(raise_exception=True):
            return Response(queryset.data)
        return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)



class NestedUserTotalView(APIView):
    """
    test
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userprofile    = []
        secretstrategy = []
        userId = self.request.user.id
        userprofilequeryset = Profile.objects.select_related("user").filter(user__id=userId)
        for obj in userprofilequeryset:
            date  = lambda obj: obj.dateOfBirth.strftime("%Y-%m-%dT%H:%M:%S.%sZ") if obj is not None else obj
            phone = lambda obj: str(obj.cellPhoneNumber) if obj is not None else obj
            userprofile.append(
                {
                    "username"                    : obj.user.username,
                    "first_name"                  : obj.user.first_name,
                    "last_name"                   : obj.user.last_name,
                    "email"                       : obj.user.email,
                    "is_superuser"                : obj.user.is_superuser,
                    "is_staff"                    : obj.user.is_staff,
                    "is_active"                   : obj.user.is_active,
                    "date_joined"                 : obj.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "last_login"                  : obj.user.last_login.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "image"                       : str(obj.image),
                    "dateOfBirth"                 : date(obj.dateOfBirth),
                    "address"                     : obj.address,
                    "addressVerified"             : obj.addressVerified,
                    "cellPhoneNumber"             : str(obj.cellPhoneNumber),
                    "cellPhoneNumberVerified"     : obj.cellPhoneNumberVerified,
                    "landingPhoneNumber"          : phone(obj.landingPhoneNumber),
                    "landingPhoneNumberVerified"  : obj.landingPhoneNumberVerified,
                    "signedContract"              : obj.signedContract,
                    "payedMemmber"                : obj.payedMemmber,
                    "expirationTime"              : obj.expirationTime.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "isEnable"                    : obj.isEnable,
                    "createTime"                  : obj.createTime.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "isActive"                    : obj.isActive
                }
            )

        secretstratqueryset = UserStrategy.objects.select_related("secret").filter(secret__profile__user__id=userId)
        for obj in secretstratqueryset:
            secretstrategy.append(
                {
                    "walletName"      : obj.secret.walletName,
                    "apiKey"          : decrypt(obj.secret.apiKey, APIKEYPASS),
                    "secretKey"       : decrypt(obj.secret.secretKey, SECKEYPASS),
                    "keyCreateTime"   : obj.secret.createTime.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "strategy"        : obj.strategy,
                    "symbol"          : obj.symbol,
                    "margin"          : obj.margin,
                    "totallSL"        : obj.totallSL,
                    "size"            : obj.size,
                    "isActive"        : obj.isActive,
                    "baseCurrency"    : obj.baseCurrency,
                    "leverage"        : obj.leverage,
                    "marginType"      : obj.marginType,
                    "positionMode"    : obj.positionMode,
                    "timeInForce"     : obj.timeInForce,
                    "workingType"     : obj.workingType,
                    "priceProtect"    : obj.priceProtect,
                    "stratCreateTime" : obj.createTime.strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
                    "deactivateTime"  : obj.deactivateTime.strftime("%Y-%m-%dT%H:%M:%S.%sZ")
                }
            )
        
        data = {"user": userprofile, "plan": secretstrategy}
        return Response(data, status=status.HTTP_200_OK)