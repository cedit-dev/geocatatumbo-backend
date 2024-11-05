from django.contrib.gis.db import models
from django.utils import timezone

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    cod = models.PositiveIntegerField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    cod_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Municipality: {self.name}'