from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import FloodIncident

class FloodIncidentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FloodIncident
        geo_field = 'location'
        fields = (
            'id',
            'severity',
            'status',
            'description',
            'created_at',
        )
