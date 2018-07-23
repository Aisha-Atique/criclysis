# urls.py
from django.conf.urls import url
from .views import BowlerList
#from .views import BowlerListView
from player import views


urlpatterns = [
    url(r'^player/$', views.BowlerList.as_view(), name='BowlerList'),
]