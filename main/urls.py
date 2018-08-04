from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # url(r'^bowlers/$', views.BowlerListView.as_view(), name='bowlers'),
    url(r'^batsmen/$', views.BatsmanListView.as_view(), name='batsmen'),
    # url(r'^bowler/(?P<pk>\d+)$', views.BowlerDetailView.as_view(), name='bowler-detail'),
    url(r'^batsman/(?P<pk>\d+)$', views.BatsmanDetailView.as_view(), name='batsman-detail'),
    url(r'^teams/', views.SelectedByUserListView.as_view(), name='teams'),
    url(r'^bowler/(?P<pk>\d+)/s/$', views.select_bowler, name='select_bowler'),
    url(r'^batsman/(?P<pk>\d+)/s/$', views.select_batsman, name='select_batsman'),
    url(r'^profile/s/$', views.select_team, name='select_team'),
    url(r'^settings/$', views.Settings.as_view(), name='settings'),
    url(r'^settings/r/$', views.reset_all, name='reset_all'),
    url(r'^settings/p/$', views.reset_pl, name='reset_pl'),
    url(r'^bowler/(?P<pk>\d+)/$', views.detail, name='bowler-detail'),

]
