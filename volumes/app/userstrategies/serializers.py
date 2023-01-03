import os

from django.db.models import Sum
import django.utils.timezone as tz
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from cryptocode import decrypt
from dotenv import load_dotenv

# from keysecrets.models import Secret
from binanceAPI.restapi import Binance
from userstrategies.models import UserStrategy, Symbol
from keysecrets.models import Secret


load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')

class SymbolSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Symbol
        fields = '__all__'


class UserStrategySerializer(serializers.ModelSerializer):
    # symbols = serializers.PrimaryKeyRelatedField(
    #     queryset=Symbol.objects.all(), many=True)
    symbols = serializers.SerializerMethodField()

    def save(self, **kwargs):

        if "margin" in self.validated_data:

            if self.validated_data['margin'] < 50:
                raise NotAcceptable(detail="insufficient margin!", code=406)

            userId = self.context['request'].user.id
            secretid = self.validated_data["secret"].id
            secret = Secret.objects.get(id=secretid)
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
            if "baseCurrency" in self.validated_data:
                basecurrency = self.validated_data['baseCurrency']
            else:
                basecurrency = "USDT"
            for balance in res:
                if balance['asset'] == basecurrency and (float(balance['balance'])-balancein) < self.validated_data['margin']:
                    raise NotAcceptable(
                        detail=f"insufficient balance on {basecurrency}!", code=406)

        if "createTime" in self.validated_data:
            self.validated_data.pop("createTime")

        # if "isActive" in self.validated_data and self.validated_data["isActive"]==False:
        #     self.validated_data["deactivateTime"] = tz.localtime()
        return super().save(**kwargs)

    class Meta:
        ordering = ['-id']
        model = UserStrategy
        fields = '__all__'# ("id", "secret", "strategy", "symbols", "margin", "totallSL", "risk", "size", "isActive", "baseCurrency",
                #   "leverage", "marginType", "positionMode", "timeInForce", "workingType", "priceProtect", "createTime", "deactivateTime")
    
    def get_symbols(self, obj):
        query = obj.symbol.all()
        return SymbolSerializer(query, many=True).data