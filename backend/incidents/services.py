from gis_core.models import FloodZone
from .models import FloodIncident

def get_incidents_in_risk_zone(risk_level):
    """
    Returns flood incidents that fall inside flood zones
    of the given risk level.
    """
    zones = FloodZone.objects.filter(risk_level=risk_level)

    incidents = FloodIncident.objects.filter(
        location__within=zones[0].geometry
    ) if zones.exists() else FloodIncident.objects.none()

    return incidents
