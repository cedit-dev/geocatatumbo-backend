from rest_framework import serializers 
from ..models import GeoData

class geodataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoData
        fields =['id', 'user_id', 'category_id', 'geometry', 'is_active', 'information']