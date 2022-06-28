import os

# from keysecrets.models import Secret
from .models import UserStrategy
from userstrategies.serializers import UserStrategySerializer

query = UserStrategy.objects.get(secret__profile__user__id=1,id=1)