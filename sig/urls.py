from django.urls import path
from .views.uploadFileView import UploadFileView
from .views.categoryView import CategoryView
from .views.geoDataView import GeoDataView

urlpatterns = [
    path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    path("category/", CategoryView.as_view(), name="get-categories"),
    path("geodata/<int:category_id>/", GeoDataView.as_view(), name="get-geodata")
]