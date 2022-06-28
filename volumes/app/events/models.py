from django.db import models
from profiles.models import Profile
from userstrategies.models import UserStrategy



class Events(models.Model):
    profile        = models.ForeignKey(Profile,
                                        on_delete=models.CASCADE, 
                                        db_index=True,
                                        related_name="profileEvents")
    strategy       = models.ForeignKey(UserStrategy,
                                        on_delete=models.CASCADE,
                                        db_index=True,
                                        related_name="strategyEvents")
    symbol         = models.CharField(db_index=True, max_length=32)
    detail         = models.TextField(null=False, blank=False)
    createTime     = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.profile) + ' => ' + str(self.strategy)

    class Meta:
        db_table = 'events'