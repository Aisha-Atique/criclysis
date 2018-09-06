from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^teams/', views.SelectedByUserListView.as_view(), name='teams'),
    url(r'^bowler/(?P<pk>\d+)/$', views.bowler_detail, name='bowler-detail'),
    url(r'^batsman/(?P<pk>\d+)/$', views.batsman_detail, name='batsman-detail'),
    url(r'^bowler/(?P<pk>\d+)/s/$', views.select_bowler, name='select_bowler'),
    url(r'^batsman/(?P<pk>\d+)/s/$', views.select_batsman, name='select_batsman'),
    url(r'^profile/s/$', views.select_team, name='select_team'),
    url(r'^settings/$', views.Settings.as_view(), name='settings'),
    url(r'^settings/r/$', views.reset_all, name='reset_all'),
    url(r'^settings/p/$', views.reset_pl, name='reset_pl'),
    url(r'^getuser/$', views.email_username, name='get-user'),
    url(r'^getuserdone/$', views.EmailUser.as_view(), name='get-user-name'),
    url(r'^getuserform/$', views.EmailUserForm.as_view(), name='get-user-form'),
    url(r'^team_analysis/(?P<pk>\d+)/$', views.team, name='team'),
]
