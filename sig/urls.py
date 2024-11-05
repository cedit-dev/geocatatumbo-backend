from django.urls import path
from .views.uploadFileView import UploadFileView

urlpatterns = [
    path("upload-file/", UploadFileView.as_view(), name="categories")
]