from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.PersonListView.as_view()), name='person_changelist'),
    path('pageurl/', login_required(views.inserturl),name='url_add'),
    path('pageurl/update', login_required(views.inserturl2)),
    path('add/pagenext', login_required(views.index2)),
    path('add/', login_required(views.PersonCreateView.as_view()), name='person_add'),
    path('ajax/load-cities/', login_required(views.load_cities), name='ajax_load_cities'),
    path('add/utmupdate',login_required(views.index3))
]


