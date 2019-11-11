from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
     path('', login_required(views.indexstartpage),name='start'),
     path('funnelchoose', login_required(views.choose)),
     path('funnel', login_required(views.index)),
     path('funnelsecond', login_required(views.index_for_new_funnel)),
     path('page2', login_required(views.index2)),
     path('page3', login_required(views.index2_new)),
     ]
