from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('page2', views.index2),
]
