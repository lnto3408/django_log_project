from django.conf import settings
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.contrib import admin
from .views import upload_file

urlpatterns = [
    url(r'^upload', upload_file)
]

