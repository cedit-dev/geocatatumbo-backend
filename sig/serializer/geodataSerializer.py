from rest_framework import serializers 
from ..models import GeoData

class GeodataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoData
        fields = '__all__'
        # fields =['id', 'user_id', 'category_id', 'geometry', 'is_active', 'information']
