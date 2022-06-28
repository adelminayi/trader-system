from django.urls import path
from balance.views import BalanceList, BalanceRolling, WalletBalanceList, WalletBalanceFirst



urlpatterns = [
    path('',                       BalanceList.as_view(),       name="BalanceList"),
    path('<int:step>/',            BalanceRolling.as_view(),    name="BalanceRolling"),
    path('wallet/',                WalletBalanceList.as_view(), name="WalletBalanceList"),
    path('wallet/first/<int:id>/', WalletBalanceFirst.as_view(),name="WalletBalanceFirst"),
]