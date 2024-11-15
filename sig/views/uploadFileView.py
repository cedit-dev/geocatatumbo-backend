from rest_framework import views, status, parsers, permissions
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from ..models import GeoData, User, Category
import geopandas as gpd
import tempfile
import zipfile
import os

class UploadFileView(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *arg, **kwargs):
        file = request.FILES.get('file', None)
        category_id = request.data.get('category_id')
        user_id = request.data.get('user_id')
        if not file:
            return Response({"error": "No cargado shapefile"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            category = Category.objects.get(id=category_id)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_400_BAD_REQUEST)
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = f"{tmpdirname}/uploaded_file.zip"

            with open(zip_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

             # Descomprime el archivo .zip
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
            except zipfile.BadZipFile:
                return Response({"error": "El archivo no es un zip válido"}, status=status.HTTP_400_BAD_REQUEST)

            shp_path = None
            for root, _, files in os.walk(tmpdirname):
                for f in files:
                    if f.endswith('.shp'):
                        shp_path = os.path.join(root, f)
                        break
            
            if not shp_path:
                return Response({"error": "Archivo .shp no encontrado en el zip"}, status=status.HTTP_400_BAD_REQUEST)

            # Leemos el archivo con geopandas
            try:
                gdf = gpd.read_file(shp_path)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # Convertir las geometrías 3D a 2D
            gdf['geometry'] = gdf['geometry'].apply(self.convert_to_2d)

            # Procesar el archivo (ajustar CRS si es necesario)
            gdf = self.process_file(gdf)

            gdf.fillna(value="", inplace=True)  # Reemplaza NaN y NaT con valores serializables

            for _, row in gdf.iterrows():
                geometry = row['geometry']
                properties = row.drop(labels='geometry').to_dict()  # Todas las columnas de atributos
                

                # Convierte cualquier valor no serializable en `properties`
                properties = {k: (v if isinstance(v, (str, int, float, bool)) else str(v)) for k, v in properties.items()}

                geo_data = GeoData(
                    user_id=user,
                    category_id=category,
                    geometry=GEOSGeometry(geometry.wkt),
                    is_active=True,
                    information=properties
                )
                geo_data.save()
        return Response({"info": f"Datos de la categoría '{category.name}' almacenados correctamente."}, status=status.HTTP_200_OK)
    
    def convert_to_2d(self, geom):
    # Si la geometría tiene Z, la eliminamos
        if geom.has_z:
            # Si la geometría es un tipo Point, LineString, Polygon, MultiPoint, MultiLineString o MultiPolygon
            if geom.geom_type == 'Point':
                return Point(geom.x, geom.y)
            elif geom.geom_type == 'LineString':
                return LineString([(x, y) for x, y, z in geom.coords])
            elif geom.geom_type == 'Polygon':
                return Polygon([(x, y) for x, y, z in geom.exterior.coords])
            elif geom.geom_type == 'MultiPoint':
                return MultiPoint([(x, y) for x, y, z in geom.coords])
            elif geom.geom_type == 'MultiLineString':
                # Aquí iteramos sobre las líneas dentro de un MultiLineString
                return MultiLineString([LineString([(x, y) for x, y, z in line.coords]) for line in geom.geoms])
            elif geom.geom_type == 'MultiPolygon':
                # Aquí iteramos sobre los polígonos dentro de un MultiPolygon
                return MultiPolygon([Polygon([(x, y) for x, y, z in poly.exterior.coords]) for poly in geom.geoms])
        return geom

    def process_file(self, shp_file):
        if(shp_file.crs == "EPSG:4326"):
            return shp_file
        else:
            return shp_file.to_crs(epsg=4326)

    
