from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.indexstartpage),name='start'),
    path('funnel', login_required(views.index)),
    path('page2', login_required(views.index2)),
]
