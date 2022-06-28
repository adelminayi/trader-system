from django.db import models

from profiles.models import Profile
from userstrategies.models import UserStrategy



class Order(models.Model):
    profile         = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        related_name="profileorder")
    strategy        = models.ForeignKey(UserStrategy,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="strategyorder")
    activatePrice   = models.FloatField(null=True, blank=True)
    avgPrice        = models.FloatField()
    clientOrderId   = models.CharField(max_length=32)
    closePosition   = models.BooleanField()
    cumQty          = models.FloatField()
    cumQuote        = models.FloatField()
    executedQty     = models.FloatField()
    orderId         = models.BigIntegerField(unique=True)
    origQty         = models.FloatField()
    origType        = models.CharField(max_length=32)
    positionSide    = models.CharField(max_length=16)
    price           = models.FloatField()
    priceProtect    = models.BooleanField()
    priceRate       = models.FloatField(null=True, blank=True)
    reduceOnly      = models.BooleanField()
    side            = models.CharField(db_index=True, max_length=16)
    status          = models.CharField(max_length=16)
    stopPrice       = models.FloatField()
    symbol          = models.CharField(db_index=True, max_length=16)
    timeInForce     = models.CharField(max_length=16)
    orderType       = models.CharField(db_index=True, max_length=32)              # type
    updateTime      = models.BigIntegerField(db_index=True)
    workingType     = models.CharField(max_length=16)
    tardeMatched    = models.BooleanField(default=False)
    createTime      = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.profile)+', orderID:'+str(self.orderId)

    class Meta:
        db_table = 'orders'
        ordering = ['-updateTime']


class CanceledOrders(models.Model):
    profile        = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        db_index=True,
                                        related_name="profileOrderCancel")
    strategy       = models.ForeignKey(UserStrategy,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="strategyOrderCancel")
    symbol         = models.CharField(db_index=True, max_length=32)
    detail         = models.TextField(null=False, blank=False)
    createTime     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'canceledOrders'
        ordering        = ['-createTime']

