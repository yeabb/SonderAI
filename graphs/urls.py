from django.urls import path
from . import views

urlpatterns = [
    path("constructGraph", views.constructGraph, name="constructGraph"),
]
