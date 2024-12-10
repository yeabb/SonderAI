
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('graphs/', include("graphs.urls")),
    path('admin/', admin.site.urls),
]
