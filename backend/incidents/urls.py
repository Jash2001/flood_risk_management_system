from django.urls import path
from .views import FloodIncidentAPIView, FloodIncidentByRiskZoneAPIView, IncidentStatusUpdateAPIView

urlpatterns = [
    path('flood_incidents/', FloodIncidentAPIView.as_view(), name='flood-incident-list-create'),
    path('flood_incidents/<int:pk>/status/', IncidentStatusUpdateAPIView.as_view(), name='flood-incident-update'),
    path('filter_by_risk_zone/', FloodIncidentByRiskZoneAPIView.as_view(),
         name='flood-incidents-by-risk-zone'),
]
