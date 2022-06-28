from django.urls import path
from total.views import UserTotalView, NestedUserTotalView



urlpatterns = [
    # path('',      UserTotalView.as_view(),       name="usertotal"),
    path('', NestedUserTotalView.as_view(), name="nestedusertotal"),
]
