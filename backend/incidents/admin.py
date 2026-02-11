from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import FloodIncident

@admin.register(FloodIncident)
class FloodIncidentAdmin(GISModelAdmin):
    list_display = ('id', 'severity', 'status', 'reported_by', 'created_at')
    list_filter = ('severity', 'status')

