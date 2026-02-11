from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FloodZone
from .serializers import FloodZoneSerializer

class FloodZoneAPIView(APIView):
    """
    Returns a read-only list of all Flood Zones.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        zones = FloodZone.objects.all()
        serializer = FloodZoneSerializer(zones, many=True)
        return Response(serializer.data)
