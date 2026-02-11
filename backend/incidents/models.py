from django.contrib.gis.db import models
from django.contrib.auth.models import User

class FloodIncident(models.Model):
    SEVERITY_LEVELS = [
        (1, 'Low'),
        (2, 'Moderate'),
        (3, 'High'),
        (4, 'Severe'),
    ]

    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_incidents'
    )

    location = models.PointField(srid=4326)
    severity = models.IntegerField(choices=SEVERITY_LEVELS)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident {self.id} - Severity {self.severity}"
