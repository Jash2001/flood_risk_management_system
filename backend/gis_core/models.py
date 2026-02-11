from django.contrib.gis.db import models

class FloodZone(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    name = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    geometry = models.PolygonField(srid=4326)

    def __str__(self):
        return f"{self.name} ({self.risk_level})"
