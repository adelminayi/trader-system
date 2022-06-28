from django.urls import path
from keysecrets.views import UserSecret,UserSecretReform, Adel


urlpatterns = [
    path('', UserSecret.as_view() , name="secrets"),
    path('<int:pk>/', UserSecretReform.as_view() , name="secrets_reform"),
    path('adel', Adel.as_view() , name="secarets"),
]