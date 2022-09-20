from django.urls import path
from profiles.views import UserProfile,VerifyCellphone,SendCellphoneToken



urlpatterns = [
    path('',                    UserProfile.as_view() ,        name="profile"),
    path('sendCellphoneToken/', SendCellphoneToken.as_view() , name="sendsmstoken"),
    path('verify-cellphone/',   VerifyCellphone.as_view() ,    name="verifycellphone"),
]
