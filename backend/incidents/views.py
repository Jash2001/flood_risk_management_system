from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import FloodIncident
from .serializers import FloodIncidentSerializer
from .permissions import IncidentPermission, CommandCenterPermission
from accounts.permissions import IsCommandCenter, IsAdmin
from .services import get_incidents_in_risk_zone

class FloodIncidentAPIView(APIView):
    """
    Handles listing all flood incidents and creating a new flood incident.
    GET: List all incidents (ordered by -created_at)
    POST: Create a new incident (reported_by auto-attached)
    Permissions: IsAuthenticated + IncidentPermission
    """
    permission_classes = [IsAuthenticated, IncidentPermission]

    def get(self, request, format=None):
        incidents = FloodIncident.objects.all().order_by('-created_at')
        serializer = FloodIncidentSerializer(incidents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FloodIncidentSerializer(data=request.data)
        
        # Check role-based permission manually
        permission = IncidentPermission()
        if not permission.has_permission(request, self):
            return Response({"detail": "You do not have permission to create incidents."},
                            status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save(reported_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FloodIncidentByRiskZoneAPIView(APIView):
    """
    Returns all flood incidents inside a specific risk zone.
    Query Parameter: risk_level (required)
    Permissions: Only Command Center or Admin users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Check if user is Command Center or Admin
        if not (IsCommandCenter().has_permission(request, self) or
                IsAdmin().has_permission(request, self)):
            return Response(
                {"detail": "You do not have permission to view incidents by risk zone."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get risk_level query param
        risk_level = request.query_params.get('risk_level')
        if not risk_level:
            return Response(
                {"error": "risk_level query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch incidents in that risk zone
        incidents = get_incidents_in_risk_zone(risk_level.upper())
        serializer = FloodIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    
class IncidentStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, CommandCenterPermission]

    def patch(self, request, pk, format=None):
        incident = get_object_or_404(FloodIncident, pk=pk)

        new_status = request.data.get("status")

        if new_status not in dict(FloodIncident.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        incident.status = new_status
        incident.save()

        return Response({"detail": "Status updated successfully."})
