from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import FloodZone

@admin.register(FloodZone)
class FloodZoneAdmin(GISModelAdmin):
    list_display = ('name', 'risk_level')

# Register your models here.
