from rest_framework import views, status, parsers, permissions
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from ..models import Category
from ..serializer.categorySerializer import CategorySerializer

class CategoryView(views.APIView):
    permission_classes = [permissions.AllowAny]
    # parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, *arg, **kwargs):
        categories = Category.objects.filter(is_active=True)
        
        # Serializa las categorías
        serializer = CategorySerializer(categories, many=True)
        
        # Retorna la respuesta en formato JSON
        return Response(serializer.data, status=status.HTTP_200_OK)