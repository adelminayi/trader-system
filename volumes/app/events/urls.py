from django.urls import path
from events.views import EventList



urlpatterns = [
    path('', EventList.as_view(), name="EventList"),
]