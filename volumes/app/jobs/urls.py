from django.urls import path
from jobs.views import AdelViewTest, SystemTrades,TotalStopLoss



urlpatterns = [
    path('', AdelViewTest.as_view(), name="adel-view-test"),
    path('systemtrades/', SystemTrades.as_view(), name="system-trades"),
    path('tsl/', TotalStopLoss.as_view(), name="total-stop-loss"),
]