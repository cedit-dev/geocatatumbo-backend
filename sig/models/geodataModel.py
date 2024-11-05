from django.contrib.gis.db import models
from django.utils import timezone

class GeoData(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    geometry = models.GeometryField()
    is_active = models.BooleanField(default=True)
    information = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Geometry: {self.geometry}"