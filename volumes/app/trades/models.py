from django.db import models

from profiles.models import Profile
from userstrategies.models import UserStrategy
from keysecrets.models import Secret



class Trade(models.Model):
    profile         = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE,
                                        related_name="profiletrade")
    strategy        = models.ForeignKey(UserStrategy,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="strategytrade")
    symbol          = models.CharField(db_index=True, max_length=32)
    tradeId         = models.BigIntegerField(unique=True)                              # id
    orderId         = models.BigIntegerField() 
    side            = models.CharField(db_index=True, max_length=16)
    price           = models.FloatField()
    qty             = models.FloatField()
    realizedPnl     = models.FloatField(db_index=True)
    marginAsset     = models.CharField(max_length=16)
    quoteQty        = models.FloatField()
    commission      = models.FloatField(db_index=True)
    commissionAsset = models.CharField(max_length=16)
    time            = models.BigIntegerField(db_index=True)
    positionSide    = models.CharField(db_index=True, max_length=16)
    buyer           = models.BooleanField()
    maker           = models.BooleanField()
    createTime      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trades'
        ordering = ['-time']


class UnplanTrade(models.Model):
    secret          = models.ForeignKey(Secret,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="secretunplantrade")
    symbol          = models.CharField(db_index=True, max_length=32)
    tradeId         = models.BigIntegerField(unique=True)                              # id
    orderId         = models.BigIntegerField() 
    side            = models.CharField(db_index=True, max_length=16)
    price           = models.FloatField()
    qty             = models.FloatField()
    realizedPnl     = models.FloatField(db_index=True)
    marginAsset     = models.CharField(max_length=16)
    quoteQty        = models.FloatField()
    commission      = models.FloatField(db_index=True)
    commissionAsset = models.CharField(max_length=16)
    time            = models.BigIntegerField(db_index=True)
    positionSide    = models.CharField(db_index=True, max_length=16)
    buyer           = models.BooleanField()
    maker           = models.BooleanField()
    createTime      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'unplantrades'
        ordering = ['-time']
