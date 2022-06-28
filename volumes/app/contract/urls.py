from django.urls import path
from contract.views import Contract



urlpatterns = [
    path('', Contract.as_view() , name="contract"),
]
