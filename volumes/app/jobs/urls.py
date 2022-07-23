from django.urls import path
from jobs.views import AdelViewTest, SystemTrades



urlpatterns = [
    path('', AdelViewTest.as_view(), name="adel-view-test"),
    path('systemtrades/', SystemTrades.as_view(), name="system-trades"),
    
]