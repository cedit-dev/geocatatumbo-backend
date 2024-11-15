from rest_framework import views, status, parsers, permissions
from rest_framework.response import Response
from ..models import Category, GeoData
from ..serializer.geodataSerializer import GeodataSerializer

class GeoDataView(views.APIView):
    permission_classes = [permissions.AllowAny]
    # parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, category_id, *arg, **kwargs):

        # Obetener los datos
        data = GeoData.objects.filter(category_id=category_id, is_active=True)
        
        # Serializa las categorías
        serializer = GeodataSerializer(data, many=True)
        
        # Retorna la respuesta en formato JSON
        return Response(serializer.data, status=status.HTTP_200_OK)