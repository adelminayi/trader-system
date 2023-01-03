import os
from cryptocode import decrypt
from dotenv import load_dotenv

from django.db import models
from rest_framework.exceptions import NotAcceptable

from profiles.models import Profile




load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class Secret(models.Model):
    profile        = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        db_index=True ,
                                        related_name="profilesecret")
    walletName     = models.CharField(max_length=256, null=True,  blank=True)
    apiKey         = models.CharField(max_length=256, null=False, blank=False)
    secretKey      = models.CharField(max_length=256, null=False, blank=False)
    uniquesign     = models.CharField(max_length=16)
    createTime     = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from balance.models import WalletBalance
        from balance.serializers import WalletBalanceSerializer
        from binanceAPI.restapi import Binance
        super(Secret, self).save(*args, **kwargs)
        id = self.__class__.objects.get(uniquesign=self.uniquesign).id
        print('id  keysecrests model :',id)
        if not WalletBalance.objects.filter(secret=id).exists():
            try:
                binance = Binance(
                        decrypt(self.apiKey, APIKEYPASS), 
                        decrypt(self.secretKey, SECKEYPASS)
                )
                print('*********************\n' ,binance.futuresBalance(), '\n*************')
                balance = float(binance.futuresBalance()[6]['balance'])
                print('balance keysecrets model: ', balance)
                # walletbalance = WalletBalance(
                #                     profile=Profile.objects.get(id=self.profile.id),
                #                     secret=Secret.objects.get(id=id),
                #                     asset="USDT",
                #                     balance=balance        
                # )
                # walletbalance.save()
                serializer = WalletBalanceSerializer(data={
                                                        "profile":self.profile.id,
                                                        "secret":id,
                                                        "asset":"USDT",
                                                        "balance":balance
                })
                if serializer.is_valid():
                    serializer.save()
                print('serialize rdata validated and saved!')
                
            except:
                raise NotAcceptable(detail="Failed to get initial balance!", code=424)


    def __str__(self) -> str:
        return str(self.profile) + ' - ' + str(self.uniquesign)

    class Meta:
        db_table        = 'secrets'
        unique_together = ['uniquesign']
