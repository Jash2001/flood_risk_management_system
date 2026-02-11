from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import FloodZone

class FloodZoneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FloodZone
        geo_field = 'geometry'
        fields = ('id', 'name', 'risk_level')
