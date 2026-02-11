from django.urls import path
from .views import FloodZoneAPIView

urlpatterns = [
    path('flood-zones/', FloodZoneAPIView.as_view(), name='flood-zone-list'),
]
