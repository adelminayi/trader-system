from django.urls import path
from trades.views import TradeList, PNL, PNLRolling, UnplanTradeList, UnplanTradeList_old



urlpatterns = [
    path('',                TradeList.as_view(),                name="TradeList"),
    path('unplan/',         UnplanTradeList_old.as_view(),          name="UnplanTradeList"),
    path('pnl/',            PNL.as_view({'get': 'retrieve'}),   name="PNL"),
    # path('pnl/<str:step>/', PNLRolling.as_view(),               name="PNLRolling"),
    path('pnl/<str:step>/', PNLRolling.as_view(),               name="PNLRolling"),
]