from rest_framework import serializers


SymbolChoices = [
         'RAYUSDT',
         'API3USDT',
         'SUSHIUSDT',
         'CVCUSDT',
         'BTSUSDT',
         'HOTUSDT',
         'ZRXUSDT',
         'QTUMUSDT',
         'IOTAUSDT',
         'BTCBUSD',
         'WAVESUSDT',
         'ADAUSDT',
         'LITUSDT',
         'XTZUSDT',
         'BNBUSDT',
         'AKROUSDT',
         'HNTUSDT',
         'ETCUSDT',
         'XMRUSDT',
         'YFIUSDT',
         'FTTBUSD',
         'ETHUSDT',
         'ALICEUSDT',
         'ALPHAUSDT',
         'SFPUSDT',
         'REEFUSDT',
         'BATUSDT',
         'DOGEUSDT',
         'TRXUSDT',
         'RLCUSDT',
         'BTCSTUSDT',
         'STORJUSDT',
         'SNXUSDT',
         '1000XECUSDT',
         'AUDIOUSDT',
         'XLMUSDT',
         'IOTXUSDT',
         'NEOUSDT',
         'UNFIUSDT',
         'SANDUSDT',
         'DASHUSDT',
         'KAVAUSDT',
         'RUNEUSDT',
         'CTKUSDT',
         'LINKUSDT',
         'CELRUSDT',
         'RSRUSDT',
         'ADABUSD',
         'DGBUSDT',
         'SKLUSDT',
         'RENUSDT',
         'LPTUSDT',
         'TOMOUSDT',
         'MTLUSDT',
         'LTCUSDT',
         'DODOUSDT',
         'EGLDUSDT',
         'KSMUSDT',
         'BNBBUSD',
         'ONTUSDT',
         'VETUSDT',
         'IMXUSDT',
         'TRBUSDT',
         'MANAUSDT',
         'FLOWUSDT',
         'COTIUSDT',
         'CHRUSDT',
         'BAKEUSDT',
         'GRTUSDT',
         'ETHUSDT_220325',
         'FLMUSDT',
         'MASKUSDT',
         'EOSUSDT',
         'OGNUSDT',
         'SCUSDT',
         'BALUSDT',
         'STMXUSDT',
         'LUNAUSDT',
         'DENTUSDT',
         '1000BTTCUSDT',
         'KNCUSDT',
         'SRMUSDT',
         'ENJUSDT',
         'C98USDT',
         'ZENUSDT',
         'ATOMUSDT',
         'NEARUSDT',
         'SOLBUSD',
         'ENSUSDT',
         'BCHUSDT',
         'ATAUSDT',
         'IOSTUSDT',
         'HBARUSDT',
         'ZECUSDT',
         '1000SHIBUSDT',
         'TLMUSDT',
         'ANTUSDT',
         'ETHBUSD',
         'GALAUSDT',
         'AAVEUSDT',
         'GTCUSDT',
         'ALGOUSDT',
         'ICPUSDT',
         'LRCUSDT',
         'AVAXUSDT',
         'BTCUSDT_220325',
         'ARPAUSDT',
         'CELOUSDT',
         'ROSEUSDT',
         'MATICUSDT',
         '1INCHUSDT',
         'MKRUSDT',
         'PEOPLEUSDT',
         'THETAUSDT',
         'UNIUSDT',
         'LINAUSDT',
         'ARUSDT',
         'RVNUSDT',
         'FILUSDT',
         'NKNUSDT',
         'KLAYUSDT',
         'DEFIUSDT',
         'COMPUSDT',
         'BTCDOMUSDT',
         'SOLUSDT',
         'BTCUSDT',
         'OMGUSDT',
         'ICXUSDT',
         'BLZUSDT',
         'FTMUSDT',
         'YFIIUSDT',
         'BANDUSDT',
         'XRPBUSD',
         'DOGEBUSD',
         'XRPUSDT',
         'SXPUSDT',
         'CRVUSDT',
         'BELUSDT',
         'DOTUSDT',
         'XEMUSDT',
         'ONEUSDT',
         'ZILUSDT',
         'AXSUSDT',
         'DYDXUSDT',
         'OCEANUSDT',
         'CHZUSDT',
         'ANKRUSDT',
         'DUSKUSDT',
         'CTSIUSDT'
    ]

SideChoices = ['BUY', 'SELL']

WorkingTypeChoises = ['MARK_PRICE', 'CONTRACT_PRICE']

PriceProtectChoises = ['TRUE', 'FALSE']


class MarketOrderSerializer(serializers.Serializer):
    symbol   = serializers.ChoiceField(
                    required=True,
                    choices=SymbolChoices
                    )
    side     = serializers.ChoiceField(
                    required=True,
                    choices=SideChoices,
                    )
    quantity = serializers.CharField(required=True)


class LimitOrderSerializer(serializers.Serializer):
    symbol   = serializers.ChoiceField(
                    required=True,
                    choices=SymbolChoices
                    )
    side     = serializers.ChoiceField(
                    required=True,
                    choices=SideChoices,
                    )
    quantity = serializers.CharField(required=True)
    price    = serializers.CharField(required=True)


class SLTPSerializer(serializers.Serializer):
    symbol      = serializers.ChoiceField(
                    required=True,
                    choices=SymbolChoices
                    )
    side        = serializers.ChoiceField(
                    required=True,
                    choices=SideChoices,
                    )
    quantity    = serializers.CharField(required=True)
    price       = serializers.CharField(required=True)
    stopPrice   = serializers.CharField(required=True)
    workingType = serializers.ChoiceField(
                    required=True,
                    choices=WorkingTypeChoises,
                    )
    priceProtect= serializers.ChoiceField(
                    required=True,
                    choices=PriceProtectChoises,
                    )


class TrailStopOrderSerializer(serializers.Serializer):
    symbol          = serializers.ChoiceField(
                        required=True,
                        choices=SymbolChoices
                        )
    side            = serializers.ChoiceField(
                        required=True,
                        choices=SideChoices,
                        )
    quantity        = serializers.CharField(required=True)
    activationPrice = serializers.CharField(required=True)
    callbackRate    = serializers.CharField(required=True)
    workingType     = serializers.ChoiceField(
                        required=True,
                        choices=WorkingTypeChoises,
                        )