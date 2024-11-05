from django.contrib.gis.db import models
from django.utils import timezone

class UserCategory(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

