from django.urls import path
from orders.views import OrderList, CanceledOrderList



urlpatterns = [
    path('',            OrderList.as_view() ,           name="OrderList"),
    path('cancelled/',  CanceledOrderList.as_view() ,   name="CanceledOrderList"),
]
