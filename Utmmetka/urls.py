from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.PersonListView.as_view(), name='person_changelist'),
    path('add/pagenext', views.index2),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('add/utmupdate',views.index3)
]
