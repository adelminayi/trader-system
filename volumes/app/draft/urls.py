from django.urls import path
from .views import PreRegister, PersonDetailView, AllowRegister, BuyAndSellView, CoinView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework import routers

router = DefaultRouter()
# router.register(r'buysell', BuyAndSellView, basename='buysell-view')
router.register(r'coin', CoinView, basename='coin-view')



urlpatterns = [
    path('preregister/', PreRegister.as_view(), name="pre-register"),
    path('edit/<int:pk>/', PersonDetailView.as_view(), name='timeentry_api_edit'),
    path('valid_register/', AllowRegister.as_view(), name='allow-register'),
    # path('buysell/', BuyAndSellView.as_view(), name="buy-and-sell"),
    # path(r'', include(router.urls)),
    path('buysell/', BuyAndSellView.as_view(), name="buy-and-sell"),
]