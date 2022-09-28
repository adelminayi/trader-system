from django.urls import path
from .views import PreRegister, PersonDetailView, AllowRegister



urlpatterns = [
    path('preregister/', PreRegister.as_view(), name="pre-register"),
    path('edit/<int:pk>/', PersonDetailView.as_view(), name='timeentry_api_edit'),
    path('valid_register/', AllowRegister.as_view(), name='allow-register'),
]