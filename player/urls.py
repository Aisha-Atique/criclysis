# urls.py
from django.conf.urls import url
#from .views import BowlerListView
from player import views


urlpatterns = [
    url(r'^bowlerspca/$', views.BowlerListPCA.as_view(), name='BowlerListpca'),
    url(r'^bowlersahp/$', views.BowlerList.as_view(), name='BowlerList'),
    url(r'^batsmenpca/$', views.BatsmanListPCA.as_view(), name='BatsmanPCA'),
    url(r'^batsmenahp/$', views.BatsmanListAHP.as_view(), name='BatsmanAHP'),
]
