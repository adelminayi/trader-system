from django.db import models
import django.utils.timezone as tz

from rest_framework.exceptions import NotAcceptable
# from django.core.exceptions import ValidationError

from keysecrets.models import Secret


class Symbol(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class UserStrategy(models.Model):
    SymbolChoices = (
        ('RAYUSDT', 'RAYUSDT'),
        ('API3USDT', 'API3USDT'),
        ('SUSHIUSDT', 'SUSHIUSDT'),
        ('CVCUSDT', 'CVCUSDT'),
        ('BTSUSDT', 'BTSUSDT'),
        ('HOTUSDT', 'HOTUSDT'),
        ('ZRXUSDT', 'ZRXUSDT'),
        ('QTUMUSDT', 'QTUMUSDT'),
        ('IOTAUSDT', 'IOTAUSDT'),
        ('BTCBUSD', 'BTCBUSD'),
        ('WAVESUSDT', 'WAVESUSDT'),
        ('ADAUSDT', 'ADAUSDT'),
        ('LITUSDT', 'LITUSDT'),
        ('XTZUSDT', 'XTZUSDT'),
        ('BNBUSDT', 'BNBUSDT'),
        ('AKROUSDT', 'AKROUSDT'),
        ('HNTUSDT', 'HNTUSDT'),
        ('ETCUSDT', 'ETCUSDT'),
        ('XMRUSDT', 'XMRUSDT'),
        ('YFIUSDT', 'YFIUSDT'),
        ('FTTBUSD', 'FTTBUSD'),
        ('ETHUSDT', 'ETHUSDT'),
        ('ALICEUSDT', 'ALICEUSDT'),
        ('ALPHAUSDT', 'ALPHAUSDT'),
        ('SFPUSDT', 'SFPUSDT'),
        ('REEFUSDT', 'REEFUSDT'),
        ('BATUSDT', 'BATUSDT'),
        ('DOGEUSDT', 'DOGEUSDT'),
        ('TRXUSDT', 'TRXUSDT'),
        ('RLCUSDT', 'RLCUSDT'),
        ('BTCSTUSDT', 'BTCSTUSDT'),
        ('STORJUSDT', 'STORJUSDT'),
        ('SNXUSDT', 'SNXUSDT'),
        ('1000XECUSDT', '1000XECUSDT'),
        ('AUDIOUSDT', 'AUDIOUSDT'),
        ('XLMUSDT', 'XLMUSDT'),
        ('IOTXUSDT', 'IOTXUSDT'),
        ('NEOUSDT', 'NEOUSDT'),
        ('UNFIUSDT', 'UNFIUSDT'),
        ('SANDUSDT', 'SANDUSDT'),
        ('DASHUSDT', 'DASHUSDT'),
        ('KAVAUSDT', 'KAVAUSDT'),
        ('RUNEUSDT', 'RUNEUSDT'),
        ('CTKUSDT', 'CTKUSDT'),
        ('LINKUSDT', 'LINKUSDT'),
        ('CELRUSDT', 'CELRUSDT'),
        ('RSRUSDT', 'RSRUSDT'),
        ('ADABUSD', 'ADABUSD'),
        ('DGBUSDT', 'DGBUSDT'),
        ('SKLUSDT', 'SKLUSDT'),
        ('RENUSDT', 'RENUSDT'),
        ('LPTUSDT', 'LPTUSDT'),
        ('TOMOUSDT', 'TOMOUSDT'),
        ('MTLUSDT', 'MTLUSDT'),
        ('LTCUSDT', 'LTCUSDT'),
        ('DODOUSDT', 'DODOUSDT'),
        ('EGLDUSDT', 'EGLDUSDT'),
        ('KSMUSDT', 'KSMUSDT'),
        ('BNBBUSD', 'BNBBUSD'),
        ('ONTUSDT', 'ONTUSDT'),
        ('VETUSDT', 'VETUSDT'),
        ('IMXUSDT', 'IMXUSDT'),
        ('TRBUSDT', 'TRBUSDT'),
        ('MANAUSDT', 'MANAUSDT'),
        ('FLOWUSDT', 'FLOWUSDT'),
        ('COTIUSDT', 'COTIUSDT'),
        ('CHRUSDT', 'CHRUSDT'),
        ('BAKEUSDT', 'BAKEUSDT'),
        ('GRTUSDT', 'GRTUSDT'),
        ('ETHUSDT_220325', 'ETHUSDT_220325'),
        ('FLMUSDT', 'FLMUSDT'),
        ('MASKUSDT', 'MASKUSDT'),
        ('EOSUSDT', 'EOSUSDT'),
        ('OGNUSDT', 'OGNUSDT'),
        ('SCUSDT', 'SCUSDT'),
        ('BALUSDT', 'BALUSDT'),
        ('STMXUSDT', 'STMXUSDT'),
        ('LUNAUSDT', 'LUNAUSDT'),
        ('DENTUSDT', 'DENTUSDT'),
        ('1000BTTCUSDT', '1000BTTCUSDT'),
        ('KNCUSDT', 'KNCUSDT'),
        ('SRMUSDT', 'SRMUSDT'),
        ('ENJUSDT', 'ENJUSDT'),
        ('C98USDT', 'C98USDT'),
        ('ZENUSDT', 'ZENUSDT'),
        ('ATOMUSDT', 'ATOMUSDT'),
        ('NEARUSDT', 'NEARUSDT'),
        ('SOLBUSD', 'SOLBUSD'),
        ('ENSUSDT', 'ENSUSDT'),
        ('BCHUSDT', 'BCHUSDT'),
        ('ATAUSDT', 'ATAUSDT'),
        ('IOSTUSDT', 'IOSTUSDT'),
        ('HBARUSDT', 'HBARUSDT'),
        ('ZECUSDT', 'ZECUSDT'),
        ('1000SHIBUSDT', '1000SHIBUSDT'),
        ('TLMUSDT', 'TLMUSDT'),
        ('ANTUSDT', 'ANTUSDT'),
        ('ETHBUSD', 'ETHBUSD'),
        ('GALAUSDT', 'GALAUSDT'),
        ('AAVEUSDT', 'AAVEUSDT'),
        ('GTCUSDT', 'GTCUSDT'),
        ('ALGOUSDT', 'ALGOUSDT'),
        ('ICPUSDT', 'ICPUSDT'),
        ('LRCUSDT', 'LRCUSDT'),
        ('AVAXUSDT', 'AVAXUSDT'),
        ('BTCUSDT_220325', 'BTCUSDT_220325'),
        ('ARPAUSDT', 'ARPAUSDT'),
        ('CELOUSDT', 'CELOUSDT'),
        ('ROSEUSDT', 'ROSEUSDT'),
        ('MATICUSDT', 'MATICUSDT'),
        ('1INCHUSDT', '1INCHUSDT'),
        ('MKRUSDT', 'MKRUSDT'),
        ('PEOPLEUSDT', 'PEOPLEUSDT'),
        ('THETAUSDT', 'THETAUSDT'),
        ('UNIUSDT', 'UNIUSDT'),
        ('LINAUSDT', 'LINAUSDT'),
        ('ARUSDT', 'ARUSDT'),
        ('RVNUSDT', 'RVNUSDT'),
        ('FILUSDT', 'FILUSDT'),
        ('NKNUSDT', 'NKNUSDT'),
        ('KLAYUSDT', 'KLAYUSDT'),
        ('DEFIUSDT', 'DEFIUSDT'),
        ('COMPUSDT', 'COMPUSDT'),
        ('BTCDOMUSDT', 'BTCDOMUSDT'),
        ('SOLUSDT', 'SOLUSDT'),
        ('BTCUSDT', 'BTCUSDT'),
        ('OMGUSDT', 'OMGUSDT'),
        ('ICXUSDT', 'ICXUSDT'),
        ('BLZUSDT', 'BLZUSDT'),
        ('FTMUSDT', 'FTMUSDT'),
        ('YFIIUSDT', 'YFIIUSDT'),
        ('BANDUSDT', 'BANDUSDT'),
        ('XRPBUSD', 'XRPBUSD'),
        ('DOGEBUSD', 'DOGEBUSD'),
        ('XRPUSDT', 'XRPUSDT'),
        ('SXPUSDT', 'SXPUSDT'),
        ('CRVUSDT', 'CRVUSDT'),
        ('BELUSDT', 'BELUSDT'),
        ('DOTUSDT', 'DOTUSDT'),
        ('XEMUSDT', 'XEMUSDT'),
        ('ONEUSDT', 'ONEUSDT'),
        ('ZILUSDT', 'ZILUSDT'),
        ('AXSUSDT', 'AXSUSDT'),
        ('DYDXUSDT', 'DYDXUSDT'),
        ('OCEANUSDT', 'OCEANUSDT'),
        ('CHZUSDT', 'CHZUSDT'),
        ('ANKRUSDT', 'ANKRUSDT'),
        ('DUSKUSDT', 'DUSKUSDT'),
        ('CTSIUSDT', 'CTSIUSDT')
    )
    BaseCurrencyChoises = (
        ('USDT',    'USDT'),
        ('BUSD',    'BUSD'),
        ('BNB',     'BNB'),
    )
    MarginTypeChoises = (
        ('ISOLATED',    'ISOLATED'),
        ('CROSSED',     'CROSSED'),
    )
    PositionModeChoises = (
        ('One-way', 'One-way'),
        ('Hedge',   'Hedge'),
    )
    TimeInForceChoises = (
        ('GTC',     'GTC'),
        ('IOC',     'IOC'),
        ('FOK',     'FOK'),
    )
    WorkingTypeChoises = (
        ('MARK_PRICE',      'MARK_PRICE'),
        ('CONTRACT_PRICE',  'CONTRACT_PRICE'),
    )
    PriceProtectChoises = (
        ('TRUE',    'TRUE'),
        ('FALSE',   'FALSE'),
    )
    secret          = models.ForeignKey(Secret,
                                        on_delete=models.CASCADE, 
                                        related_name="secretuserstrategy")
    strategy        = models.CharField(max_length=32)
    # symbol          = models.CharField(max_length=14, choices=SymbolChoices, default='BTCUSDT')
    symbols         = models.ManyToManyField(Symbol ,related_name="userstrategys")
    margin          = models.FloatField()
    totallSL        = models.FloatField()
    risk            = models.FloatField()
    size            = models.FloatField(default=0)
    isActive        = models.BooleanField(default=False)
    baseCurrency    = models.CharField(max_length=4,  choices=BaseCurrencyChoises, default='USDT')
    leverage        = models.IntegerField(default=1)
    marginType      = models.CharField(max_length=10, choices=MarginTypeChoises,   default='ISOLATED')
    positionMode    = models.CharField(max_length=7,  choices=PositionModeChoises, default='One-way')
    timeInForce     = models.CharField(max_length=3,  choices=TimeInForceChoises,  default='GTC')
    workingType     = models.CharField(max_length=14, choices=WorkingTypeChoises,  default='CONTRACT_PRICE')
    priceProtect    = models.CharField(max_length=5,  choices=PriceProtectChoises, default='FALSE')
    createTime      = models.DateTimeField(auto_now_add=True)
    deactivateTime  = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # if self.isActive==True and \
        #     self.__class__.objects.filter(secret=self.secret, symbol=self.symbol, isActive=True).count()>0:
        #     raise NotAcceptable(detail="Two strategies on same secret and symbol are not acceptable!", code=406)

        if self.isActive==False:
            self.deactivateTime = tz.localtime()
        super(UserStrategy, self).save(*args, **kwargs)

    
    def __str__(self) -> str:
        return str(self.strategy)+ ' - ' + str(self.symbol)

    class Meta:
        db_table = 'user_strategy'