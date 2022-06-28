from django.urls import path
from binanceWallet.views import *



urlpatterns = [
    path('accountStatus/<int:id>/',              AccountStatus.as_view() ,        name="AccountStatus"),
    path('accountAPIStatus/<int:id>/',           AccountAPIStatus.as_view() ,     name="accountAPIStatus"),
    path('depositHistory/<int:id>/<str:coin>/',  DepositHistory.as_view() ,       name="depositHistory"),
    path('withdrawHistory/<int:id>/<str:coin>/', WithdrawHistory.as_view() ,      name="WithdrawHistory"),
    path('spotCoins/<int:id>/',                  SpotCoins.as_view() ,            name="SpotCoins"),
    path('futuresBalance/<int:id>/',             FuturesBalance.as_view() ,       name="FuturesBalance"),
    path('marketOrder/<int:id>/',                MarketOrder.as_view() ,          name="MarketOrder"),
    path('limitOrder/<int:id>/',                 LimitOrder.as_view() ,           name="LimitOrder"),
    path('stopOrder/<int:id>/',                  StopOrder.as_view() ,            name="StopOrder"),
    path('takeProfitOrder/<int:id>/',            TakeProfitOrder.as_view() ,      name="TakeProfitOrder"),
    path('trailStopOrder/<int:id>/',             TrailStopOrder.as_view() ,       name="TrailStopOrder"),
    path('currentPositions/<int:id>/',           CurrentPositions.as_view() ,     name="CurrentPositions"),
    path('currentOrders/<int:id>/',              CurrentOrders.as_view() ,        name="CurrentOrders"),
    path('cancelAllOrders/<int:id>/',            CancelAllOrders.as_view() ,      name="CancelAllOrders"),
    path('cancelOrder/<int:id>/',                CancelOrder.as_view() ,          name="CancelOrder"),
    path('closeCurrentPositions/<int:id>/',      CloseCurrentPositions.as_view(), name="CloseCurrentPositions"),
    path('changeMarginType/<int:id>/',           ChangeMarginType.as_view() ,     name="ChangeMarginType"),
    path('changeLeverage/<int:id>/',             ChangeLeverage.as_view() ,       name="ChangeLeverage"),
    path('isDualSidePosition/<int:id>/',         IsDualSidePosition.as_view() ,   name="IsDualSidePosition"),
    path('dualSidePosition/<int:id>/',           DualSidePosition.as_view() ,     name="DualSidePosition"),
    path('lastTrades/<int:id>/',                 LastTrades.as_view() ,           name="LastTrades"),
    path('lastOrders/<int:id>/',                 LastOrders.as_view() ,           name="LastOrders"),
]