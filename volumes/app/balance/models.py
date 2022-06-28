import profile
from django.db import models
from pyrsistent import s
from profiles.models import Profile
from userstrategies.models import UserStrategy
from keysecrets.models import Secret



class Balance(models.Model):
    profile        = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        db_index=True,
                                        related_name="profilebalance")
    strategy       = models.ForeignKey(UserStrategy,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="strategybalance")
    symbol         = models.CharField(db_index=True, max_length=32)
    balance        = models.FloatField(null=False, blank=False)
    createTime     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.profile)

    class Meta:
        db_table = 'balance'


class WalletBalance(models.Model):
    profile        = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        related_name="profilewalletbalance")
    secret         = models.ForeignKey(Secret,
                                        on_delete=models.CASCADE, 
                                        related_name="secretwalletbalance")
    asset          = models.CharField(max_length=16)
    balance        = models.FloatField(null=False, blank=False)
    createTime     = models.DateTimeField(auto_now_add=True)



    class Meta:
        db_table = 'walletbalance'